from typing import Literal
from pydantic import BaseModel
from .optimizers import OptimizerHParams

class OriginalModel(BaseModel):
  model: Literal['original'] = 'original'
  num_classes: int = 37
  conv_kernel_initializer: Literal['lecun_uniform']
  lstm_dropout: float

ModelHParams = OriginalModel

class HParams(BaseModel):
  tag: Literal['v1'] = 'v1'
  batch_size: int
  model: ModelHParams
  optimizer: OptimizerHParams