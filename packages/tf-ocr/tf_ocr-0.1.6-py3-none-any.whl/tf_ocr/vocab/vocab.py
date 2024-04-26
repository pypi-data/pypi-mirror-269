from typing import Callable, overload
import keras
StringLookup = keras.layers.StringLookup
import tensorflow as tf
from jaxtyping import Shaped, Int, Int32
from haskellian import Thunk
import string

# VOCABULARY = list("#+-12345678=ABCDFKLNOPQRSTUabcdefghpx")
VOCABULARY = list("-12345678=ABCDFKLNOPQRSTUabcdefghpxGHW")
"""Vocabulary used in the original Moveread OCR model: `-12345678=ABCDFKLNOPQRSTUabcdefghpx`"""

NEW_VOCABULARY = list(string.ascii_letters + '12345678' + '-=')

def char2num(vocabulary: list[str] = VOCABULARY) -> Callable[[Shaped[tf.Tensor, "*n"]], Int32[tf.Tensor, "*n"]]:
  """Mapper from characters to indices. Out-of-vocabulary (OOV) characters map to 0"""
  # `mask_token` defaults to ''. If we didn't specify `None`, it would map to 1, and then the vocabulary's chars start at 2
  return StringLookup(vocabulary=vocabulary, mask_token=None)

CHAR2NUM = Thunk(char2num)

def num2char(vocabulary: list[str] = VOCABULARY) -> Callable[[Int[tf.Tensor, "*n"]], Shaped[tf.Tensor, "*n"]]:
  """Mapper from indices to characters. Out-of-vocabulary (OOV) indices (namely `0` and any `i >= len(VOCABULARY)`) map to `'[UNK]'`"""
  return StringLookup(vocabulary=vocabulary, mask_token=None, invert=True)

NUM2CHAR = Thunk(num2char)

@overload
def vectorize(chars: Shaped[tf.RaggedTensor, "*n"], char2num: StringLookup | None = None) -> Int32[tf.RaggedTensor, "*n"]: ...
@overload
def vectorize(chars: Shaped[tf.Tensor, "*n"], char2num: StringLookup | None = None) -> Int32[tf.Tensor, "*n"]: ...
def vectorize(chars, char2num = None):
  """Vectorize a string tensor using a `StringLookup`. Defaults to the original vocabulary"""
  f = char2num or CHAR2NUM.get()
  return f(chars)

@overload
def stringify(indices: Int[tf.RaggedTensor, "*n"], num2char: StringLookup | None = None) -> Shaped[tf.RaggedTensor, "*n"]: ...
@overload
def stringify(indices: Int[tf.Tensor, "*n"], num2char: StringLookup | None = None) -> Shaped[tf.Tensor, "*n"]: ...
def stringify(indices, num2char = None):
  """Stringify tensor of vocabulary indices using an inverted `StringLookup`. Defaults to the original vocabulary"""
  f = num2char or NUM2CHAR.get()
  return f(indices)