import keras
from ...types import ArtifactFormat

def load_artifact(format: ArtifactFormat, file: str) -> keras.Model:
  match format:
    case 'keras':
      return keras.models.load_model(file) # type: ignore
    case 'tf2':
      import tf_keras
      return tf_keras.models.load_model(file) # type: ignore