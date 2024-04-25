import keras
from ..experiments import ModelHParams
from ._original import original

def create(params: ModelHParams, batch_size: int | None = None) -> keras.Model:
  match params.model:
    case 'original':
      return original(
        num_classes=params.num_classes, batch_size=batch_size,
        conv_kernel_initializer=params.conv_kernel_initializer,
        lstm_dropout=params.lstm_dropout
      )