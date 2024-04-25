from ..experiments import Format

def load_artifact(format: Format, file: str):
  match format:
    case 'keras':
      import keras
      return keras.models.load_model(file)
    case 'tf2':
      import tf_keras
      return tf_keras.models.load_model(file)