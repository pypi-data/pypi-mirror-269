from dataclasses import dataclass
from kv.api import KV
from kv.fs import FilesystemKV
from .experiments import Experiment
from ..models import load_artifact

@dataclass
class ModelsAPI:
  """API to store models and experiments: artifacts, metrics, etc."""
  meta: KV[Experiment]
  artifacts: FilesystemKV[bytes]

  @classmethod
  def at(cls, path: str) -> 'ModelsAPI':
    import os
    from kv.sqlite import SQLiteKV
    return ModelsAPI(
      meta=SQLiteKV.validated(Experiment, os.path.join(path, 'meta.sqlite')),
      artifacts=FilesystemKV(os.path.join(path, 'artifacts'))
    )
  
  async def load(self, experimentId: str):
    
  