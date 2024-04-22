from typing import TypedDict
import tensorflow as tf
from tf_keras.layers import StringLookup
from jaxtyping import Float
import ramda as R
import tf_ctc as ctc
from tf_tools import Bytes
from ..labels import decode_sparse

class PredsProbs(TypedDict):
  preds: Bytes[tf.Tensor, "batch top_paths"]
  logprobs: Float[tf.Tensor, "batch top_paths"]

def ctc_postprocess(
  logits: Float[tf.Tensor, "batch maxlen vocabsize"],
  num2char: StringLookup | None = None, beam_width: int = 100,
  top_paths: int = 1, blank_zero: bool = True
) -> PredsProbs:
  paths, logps = ctc.beam_decode(logits, beam_width=beam_width, top_paths=top_paths, blank_zero=blank_zero)
  preds = [decode_sparse(p, num2char) for p in paths]
  samplewise_preds = tf.transpose(tf.stack(preds))
  return PredsProbs(preds=samplewise_preds, logprobs=logps)