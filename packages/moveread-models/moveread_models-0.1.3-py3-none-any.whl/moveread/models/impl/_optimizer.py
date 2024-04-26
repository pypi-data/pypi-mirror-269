import keras
LearningRateSchedule = keras.optimizers.schedules.LearningRateSchedule
PiecewiseConstantDecay = keras.optimizers.schedules.PiecewiseConstantDecay
from ..types import hparams

def learning_rate(schedule: hparams.Schedule) -> float | LearningRateSchedule:
  match schedule.tag:
    case 'constant':
      return schedule.value
    case 'piecewise-constant':
      boundaries, values = zip(*schedule.steps.items())
      return PiecewiseConstantDecay(boundaries, values)
    
def weight_decay(schedule: hparams.Schedule) -> float:
  match schedule.tag:
    case 'constant':
      return schedule.value
    case 'piecewise-constant':
      return schedule.initial

def optimizer(params: hparams.OptimizerHParams) -> keras.Optimizer:
  match params.optimizer:
    case 'adamw':
      return keras.optimizers.AdamW(
        learning_rate(params.learning_rate), # type: ignore
        weight_decay=weight_decay(params.weight_decay),
        beta_1=params.beta_1
      )