from functools import partial
import tensorflow as tf
import tf_keras
from ..vocab import NUM2CHAR
from ..images import preprocess_b64
from ..utils import ctc_postprocess

class PreprocessB64(tf_keras.layers.Layer):
  """Custom `Layer` to preprocess base64-encoded images (simple wrapper around `ocr.preprocess_b64`)"""
  def __init__(self, width: int = 256, height: int = 64):
    super().__init__()
    self.width = width
    self.height = height
    
  def call(self, b64img):
    return tf.map_fn(
      partial(preprocess_b64, width=self.width, height=self.height), b64img,
      fn_output_signature=tf.TensorSpec(shape=(256, 64, 1), dtype=tf.float32)
    )
  
class PostprocessLogits(tf_keras.layers.Layer):
  """Custom `Layer` to postprocess CTC logits (simple wrapper around `ocr.ctc_postprocess`)"""
  def __init__(self, num2char: tf_keras.layers.StringLookup = None, beam_width: int = 100, top_paths: int = 16, blank_zero: bool = True):
    super().__init__()
    self.num2char = num2char or NUM2CHAR()
    self.beam_width = beam_width
    self.top_paths = top_paths
    self.blank_zero = blank_zero
  
  def call(self, logits):
    return ctc_postprocess(logits, self.num2char, self.beam_width, self.top_paths, self.blank_zero)
  
def pipeline(
    model: tf_keras.Model, width: int = 256, height: int = 64,
    num2char: tf_keras.layers.StringLookup = None, beam_width: int = 100,
    top_paths: int = 16, blank_zero: bool = True
  ) -> tf_keras.Model:
  """Full-pipeline model, with pre/post processing included in the graph
  - `model :: Uint8[tf.Tensor, "width height 1"] -> Float[tf.Tensor, "batch maxlen vocabsize"]`
  - Returns `pipeline_model :: Base64String[tf.Tensor, "batch"] -> PredsProbs`
  """
  b64img = tf_keras.layers.Input(shape=(), dtype=tf.string, name="b64_images")
  x = PreprocessB64(width, height)(b64img)
  z = model(x)
  y = PostprocessLogits(num2char, beam_width, top_paths, blank_zero)(z)
  return tf_keras.Model(inputs=b64img, outputs=y)