import os
from typing import Any,Dict, List, Optional

from langchain_core.embeddings import Embeddings
from langchain_core.pydantic_v1 import BaseModel, root_validator


class AscendEmbeddings(Embeddings, BaseModel):
    """
    Ascend NPU accelerate Embedding model

    Please ensure that you haved installed CANN and torch_npu.

    Example:

    from langchain_community.embeddings import AscendEmbeddings
    model = AscendEmbeddings(model_path=<path_to_model>,
        device_id=0,
        query_instruction="Represend this sentence for searching relevant passages: "
    )
    """

    """model path"""
    model_path: str
    """Ascend NPU device id."""
    device_id: int = 0
    """Unstruntion to used for embedding query."""
    query_instruction: str = ""
    """Unstruntion to used for embedding document."""
    document_instruction: str = ""
    use_fp16: bool = True
    pooling_method: Optional[str] = 'cls'
    model: Any
    tokenizer: Any
    is_npu_avaiable: bool = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            from transformers import AutoTokenizer, AutoModel
        except ImportError as e:
            raise ImportError(
                "Unable to import transformers, please install with "
                "`pip install -U transformers`."
            ) from e
        try:
            if self.is_npu_avaiable:
                self.model = AutoModel.from_pretrained(self.model_path).npu().eval()
            else:
                self.model = AutoModel.from_pretrained(self.model_path).eval()
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        except Exception as e:
            raise Exception(f"Failed to load model [self.model_path], due to following error:{e}")

        if self.use_fp16:
            self.model.half()
        self.encode([f"warmup {i} times" for i in range(10)])

    @root_validator
    def validate_environment(cls, values: Dict) -> Dict:
        if not os.access(values['model_path'], os.F_OK):
            raise FileNotFoundError(f"Unabled to find valid model path in [{values['model_path']}]")
        try:
            import torch_npu
        except ImportError:
            values['is_npu_avaiable'] = False
            return values
        except Exception as e:
            raise e
        try:
            torch_npu.npu.set_device(values['device_id'])
        except Exception as e:
            raise Exception(f"set device failed due to {e}")
        return values

    def encode(self, sentences):
        inputs = self.tokenizer(sentences,
            padding=True,
            truncation=True,
            return_tensors='pt',
            max_length=512)
        try:
            import torch
        except ImportError as e:
            raise ImportError("Unable to import torch, please install with "
                "`pip install -U torch`."
            ) from e
        if self.is_npu_avaiable:
            last_hidden_state = self.model(inputs.input_ids.npu(), return_dict=True).last_hidden_state
            tmp = self.pooling(last_hidden_state, inputs['attention_mask'].npu())
        else:
            last_hidden_state = self.model(inputs.input_ids, return_dict=True).last_hidden_state
            tmp = self.pooling(last_hidden_state, inputs['attention_mask'])
        embeddings = torch.nn.functional.normalize(tmp, dim=-1)
        return embeddings.cpu().detach().numpy()


    def pooling(self,
            last_hidden_state: Any,
            attention_mask: Any = None):
        if self.pooling_method == 'cls':
            return last_hidden_state[:, 0]
        elif self.pooling_method == 'mean':
            s = torch.sum(last_hidden_state * attention_mask.unsqueeze(-1).float(), dim=-1)
            d = attention_mask.sum(dim=1, keepdim=True).float()
            return s / d
        else:
            raise NotImplementedError(f"Pooling method [{self.pooling_method}] not implemented")


    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.encode([self.document_instruction + text for text in texts])

    def embed_query(self, text:str) -> List[float]:
        return self.encode([self.query_instruction + text])[0]
