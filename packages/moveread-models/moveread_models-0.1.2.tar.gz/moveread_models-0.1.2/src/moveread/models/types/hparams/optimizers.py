from typing import Literal
from pydantic import BaseModel

class ConstantSchedule(BaseModel):
  tag: Literal['constant'] = 'constant'
  value: float

class PiecewiseConstant(BaseModel):
  tag: Literal['piecewise-constant'] = 'piecewise-constant'
  initial: float
  steps: dict[int, float]

Schedule = PiecewiseConstant | ConstantSchedule

class AdamW(BaseModel):
  optimizer: Literal['adamw'] = 'adamw'
  learning_rate: Schedule
  weight_decay: Schedule
  beta_1: float

OptimizerHParams = AdamW