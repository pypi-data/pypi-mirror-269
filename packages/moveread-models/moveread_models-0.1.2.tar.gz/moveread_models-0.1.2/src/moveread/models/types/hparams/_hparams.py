from pydantic import BaseModel
from .models import ModelHParams
from .optimizers import OptimizerHParams
from .run import RunHParams

class HParams(BaseModel):
  run: RunHParams
  model: ModelHParams
  optimizer: OptimizerHParams