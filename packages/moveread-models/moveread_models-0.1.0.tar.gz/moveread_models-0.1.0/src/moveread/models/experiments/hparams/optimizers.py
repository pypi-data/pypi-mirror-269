from typing import Literal
from pydantic import BaseModel

class ConstantSchedule(BaseModel):
  tag: Literal['constant'] = 'constant'
  value: float

class CustomSchedule(BaseModel):
  tag: Literal['custom'] = 'custom'
  initial: float
  epochs: dict[int, float]

Schedule = CustomSchedule | ConstantSchedule

class AdamW(BaseModel):
  optimizer: Literal['adamw'] = 'adamw'
  learning_rate: Schedule
  weight_decay: Schedule
  beta_1: Schedule

OptimizerHParams = AdamW