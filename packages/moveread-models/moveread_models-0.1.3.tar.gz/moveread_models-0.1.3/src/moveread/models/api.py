from dataclasses import dataclass
from kv.api import KV
from kv.fs import FilesystemKV
from .types import Experiment
from . import impl

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
    exp = (await self.meta.read(experimentId)).unsafe()
    if exp.artifact:
      return impl.load_artifact(
        format=exp.artifact.format,
        file=self.artifacts.url(exp.artifact.file)
      )
