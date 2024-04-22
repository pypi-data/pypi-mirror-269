import tensorflow as tf
from jaxtyping import Float
import ramda as R
import tf_ctc as ctc
from ..labels import encode

def mock_logits(top_preds: list[list[str]], vocabsize: int = None) -> Float[tf.Tensor, "batch 2*maxlen vocabsize"]:
  """Logits that, when CTC-decoded, will roughly follow `top_preds`
  - `len(top_preds)`: batch_size
  - `top_preds[i]`: top paths considered for each sample
  
  E.g:
  ```
  z = ocr.mock_logits([['e4', 'e5'], ['Nf6', 'Nd6']])
  paths, _ = ctc.beam_decode(logits, top_paths=2)
  [ocr.decode(p) for p in paths] # [[b'e4', b'Nf6'], [b'e5', b'Nd6']]
  ```
  """
  labs = R.map(encode, R.transpose(top_preds))
  return ctc.mock_logits(labs, vocabsize=vocabsize)