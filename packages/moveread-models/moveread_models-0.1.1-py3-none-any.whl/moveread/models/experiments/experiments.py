from typing import TypeAlias, Literal
from pydantic import BaseModel, ConfigDict
from .hparams import HParams

DatasetID: TypeAlias = str

Format = Literal['tf2', 'keras']

class Artifact(BaseModel):
  format: Format
  file: str

class Metrics(BaseModel):
  model_config = ConfigDict(extra='forbid')
  ctc_loss: float | None = None
  accuracy: float | None = None
  top5_accuracy: float | None = None
  norm_edit_distance: float | None = None

class MetricsEntry(BaseModel):
  dataset: list[DatasetID]
  metrics: Metrics

class Experiment(BaseModel):
  description: str | None = None
  notes: str | None = None
  train_ds: list[DatasetID]
  metrics: list[MetricsEntry]
  hparams: HParams
  artifact: Artifact | None
  