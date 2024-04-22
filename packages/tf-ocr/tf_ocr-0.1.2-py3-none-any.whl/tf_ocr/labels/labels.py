from typing import overload, Literal
import tensorflow as tf
from keras.layers import StringLookup
from jaxtyping import Shaped, Int
from tf_tools import tf_function

from ..vocab import vectorize, stringify

@tf_function 
def encode(label: str | list[str], maxlen: int | None = None, char2num: StringLookup = None) -> Shaped[tf.SparseTensor, "maxlen"]:
  """Convert a label (or labels) into a valid OCR input (a batch of `SparseTensor`s)"""
  labels = [label] if isinstance(label, str) else label
  chars: tf.RaggedTensor = tf.strings.unicode_split(labels, 'UTF-8')
  inds = vectorize(chars, char2num)
  if maxlen is None:
    return inds.to_sparse()
  else:
    padded = inds.to_tensor(shape=(len(labels), maxlen))
    return tf.sparse.from_dense(padded)
  
@tf_function
def remove_blanks(path: tf.Tensor, blank: int = 0) -> tf.Tensor | tf.RaggedTensor:
  """Remove zeros from `path` across the last dimension"""
  mask = tf.not_equal(path, blank)
  return tf.ragged.boolean_mask(path, mask)
  
@tf_function
def decode_dense(inds: Int[tf.Tensor, "batch maxlen"], num2char: StringLookup = None) -> Shaped[tf.Tensor, "batch"]:
  """Converts an encoded label/prediction back into a string tensor"""
  chars = stringify(remove_blanks(inds), num2char)
  return tf.strings.reduce_join(chars, axis=-1)
  
@tf_function
def decode_sparse(inds: Int[tf.SparseTensor, "batch maxlen"], num2char: StringLookup = None) -> Shaped[tf.Tensor, "batch"]:
  """Converts an encoded label/prediction back into a string tensor"""
  dense = tf.sparse.to_dense(inds)
  chars = stringify(remove_blanks(dense), num2char)
  return tf.strings.reduce_join(chars, axis=-1)

@overload
def decode(inds: Int[tf.SparseTensor | tf.Tensor, "batch maxlen"], num2char: StringLookup = None, *, output: Literal['str']) -> list[str]: ...
@overload
def decode(inds: Int[tf.SparseTensor | tf.Tensor, "batch maxlen"], num2char: StringLookup = None, *, output: Literal['bytes'] = None) -> list[bytes]: ...

def decode(inds: Int[tf.Tensor, "batch maxlen"], num2char: StringLookup = None, *, output: Literal['bytes'] = None) -> list[bytes]:
  """Inverse of `encode`. Converts an encoded label/prediction back into `bytes/str`"""  
  f = decode_sparse if isinstance(inds, tf.SparseTensor) else decode_dense
  arr = f(inds, num2char).numpy()
  return list(map(bytes.decode, arr)) if output == 'str' else list(arr)
  