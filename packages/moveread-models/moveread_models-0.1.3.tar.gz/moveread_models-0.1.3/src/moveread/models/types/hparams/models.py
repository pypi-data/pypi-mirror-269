from typing import Literal
from pydantic import BaseModel

class OriginalModel(BaseModel):
  model: Literal['original'] = 'original'
  num_classes: int = 37
  conv_kernel_initializer: Literal['lecun_uniform']
  lstm_dropout: float

ModelHParams = OriginalModel
