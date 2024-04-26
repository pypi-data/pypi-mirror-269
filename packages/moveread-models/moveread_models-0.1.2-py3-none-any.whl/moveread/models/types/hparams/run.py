from pydantic import BaseModel

class RunHParams(BaseModel):
  batch_size: int
  epochs: int | None = None
