import tensorflow as tf
import keras
import tf_ctc as ctc
from .experiments import Metrics

def top5_accuracy(labs, logits):
  return ctc.accuracy(labs, logits, k=5)

def evaluate(model: keras.Model, ds: tf.data.Dataset) -> Metrics:
  metrics = dict(
    ctc_loss=ctc.loss, accuracy=ctc.accuracy,
    norm_edit_distance=ctc.edit_distance, top5_accuracy=top5_accuracy
  )
  names, funcs = zip(*metrics.items())
  model.compile(metrics=funcs)
  loss, *results = model.evaluate(ds)
  return Metrics(**dict(zip(names, results)))