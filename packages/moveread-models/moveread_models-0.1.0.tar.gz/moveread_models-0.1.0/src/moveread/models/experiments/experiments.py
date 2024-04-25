from typing import TypeAlias, Literal
from pydantic import BaseModel, ConfigDict
from .hparams import HParams

DatasetID: TypeAlias = str

Format = Literal['tf2', 'keras']

class Metrics(BaseModel):
  model_config = ConfigDict(extra='forbid')
  ctc_loss: float | None = None
  accuracy: float | None = None
  top5_accuracy: float | None = None
  norm_edit_distance: float | None = None

class Experiment(BaseModel):
  description: str | None = None
  notes: str | None = None
  train_ds: list[DatasetID]
  metrics: list[tuple[list[DatasetID], Metrics]]
  hparams: HParams
  artifact: str
  format: Format
  