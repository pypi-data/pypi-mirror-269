from functools import partial
import tensorflow as tf
from jaxtyping import UInt8, Float
from tf_tools import tf_function, Bytes

@partial(tf_function, reduce_retracing=True)
def b64_decode(img: Bytes[tf.Tensor, ""]) -> UInt8[tf.Tensor, "h w 1"]:
  """Decode a base64 image (any format) into a grayscale tensor"""
  decoded = tf.io.decode_base64(img)
  return tf.io.decode_png(decoded, channels=1)

@partial(tf_function, input_signature=[tf.TensorSpec(shape=(None, None, 1), dtype=tf.uint8), tf.TensorSpec(shape=(), dtype=tf.int32), tf.TensorSpec(shape=(), dtype=tf.int32)])
# @partial(tf_function, reduce_retracing=True)
def preprocess_gray(gray: UInt8[tf.Tensor, "h w 1"], width: int = 256, height: int = 64) -> Float[tf.Tensor, "width height 1"]:
  """Like `preprocess_uint8`, but skips grayscaling"""
  neg = 255 - gray
  resized = tf.image.resize_with_pad(neg, height, width) # always pads to 0. I want pad = 255 (white). So, I negate the image before and after!
  unneg = 255 - resized
  transposed = tf.transpose(unneg, perm=[1, 0, 2])
  flipped = tf.image.flip_left_right(transposed)
  normalized = tf.cast(flipped, tf.float32) / 255.
  return normalized
  
@partial(tf_function, input_signature=[tf.TensorSpec(shape=(None, None, None), dtype=tf.uint8)])
# @partial(tf_function, reduce_retracing=True)
def preprocess_uint8(img: UInt8[tf.Tensor, "h w _"], width: int = 256, height: int = 64) -> Float[tf.Tensor, "width height 1"]:
    gray = tf.image.rgb_to_grayscale(img) if tf.shape(img)[-1] == 3 else img
    return preprocess_gray(gray, width, height)
  
@partial(tf_function, input_signature=[tf.TensorSpec(shape=(), dtype=tf.string)])
# @partial(tf_function, reduce_retracing=True)
def preprocess_b64(b64img: Bytes[tf.Tensor, ""], width: int = 256, height: int = 64) -> Float[tf.Tensor, "width height 1"]:
  dec = b64_decode(b64img)
  return preprocess_gray(dec, width, height)

@partial(tf_function, reduce_retracing=True)
def preprocess(img: Bytes[tf.Tensor, ""] | UInt8[tf.Tensor, "h w _"], width: int = 256, height: int = 64) -> Float[tf.Tensor, "width height 1"]:
  """Preprocess image. The input can be:
  1. A base64-encoded `tf.string` tensor, OR
  2. A `height x width x {1|3}` `tf.uint8` tensor

  The output image is:
  1. Padded to `(width, height)` with `255` values (i.e. white)
  2. Normalized (i.e. values mapped from `[0, 255]` to `[0, 1]`)
  3. Transposed to column-major (i.e. moving in the first dimension moves across the image width)
  
  Note: more specific versions (that don't test for grayscale/rgb nor string/uint8) are found as `ocr.preprocess_b64`, `ocr.preprocess_uint8` and `ocr.preprocess_gray`
  """
  return preprocess_b64(img, width, height) if img.dtype == tf.string else preprocess_uint8(img, width, height)

def unflip(img: UInt8[tf.Tensor, "w h _"]) -> UInt8[tf.Tensor, "h w _"]:
  """Undo transposition + left-to-right flip (done for training), so that the image is nicely displayed"""
  return tf.transpose(tf.image.flip_left_right(img), [1, 0, 2])