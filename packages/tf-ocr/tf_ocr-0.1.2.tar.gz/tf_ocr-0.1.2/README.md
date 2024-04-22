# TensorFlow OCR

> Tools to simplify dealing with OCR labels, predictions, models

## Pre/post processing

### Preprocessing images

- Pad and resize to a given size
- Transpose to column-major (first dimension moves across the image width)
- Normalize values to $[0, 1]$ (from $[0, 255]$)

```python
import cv2 as cv
import tensorflow as tf
import tf_ocr as ocr

paths = ['img1.jpg', 'img2.jpg', ...]
batch = tf.stack([ocr.preprocess(cv.imread(path), width=128, height=64) for path in paths])
batch.shape # [batch_size, 128, 64, 1]
```

### Encode/decode labels

```python
import tf_ocr as ocr

labs = ocr.encode(['exd4', 'O-O'], maxlen=12) # SparseTensor[int64] with dense shape [2, 12]
ocr.decode(labs) # [b'exd4', b'O-O']
```

### CTC loss/inference

Synergizes with the `tf-ctc` package

```python
import tf_ocr as ocr
import tf_ctc as ctc

labs = ocr.encode(['exd4', 'O-O'])
logits = ctc.onehot_logits(labs) # one-hot logits to simulate perfectly confident predictions
paths, _ = ctc.beam_decode(logits) # or ctc.greedy_decode(logits) 
ocr.decode(paths[0]) # [b'exd4', b'O-O']
```

Or, a higher-level abstraction:

```python
import tf_ctc as ctc

labs = ocr.encode(['exd4', 'O-O'])
logits = ctc.onehot_logits(labs)
ocr.ctc_postprocess(logits)
# {'preds': <tf.Tensor: shape=(2, 4), dtype=string, numpy=
#  array([[b'exd4', b'exd', b'Qxd4', b'exB4'],
#         [b'O-O', b'f-O', b'5-O', b'O-']], dtype=object)>,
#  'logprobs': <tf.Tensor: shape=(2, 4), dtype=float32, numpy=
#  array([[ 0.e+00, -1.e+09, -1.e+09, -1.e+09],
#         [ 0.e+00, -1.e+09, -1.e+09, -1.e+09]], dtype=float32)>}
```

## Datasets

### Serializing/Deserializing TFRecords

Single examples

```python
import tf_ocr as ocr

sample = {
  'image': <image tensor>,
  'label': <string tensor>,
  'boxid': <sample-id, string tensor>
} # usually obtained from iterating a `tf.data.Dataset`
bytes = ocr.tfrecords.serialize(sample)
x = ocr.tfrecords.deserialize(bytes)
# x is basically a copy of sample
```

Datasets

```python
import tf_ocr as ocr

raw_dataset = ocr.tfrecords.deserialize_dataset(['data1.tfrecord', 'data2.tfrecord'])
# or
preprocessed_dataset = ocr.tfrecords.read_dataset(['data1.tfrecord', 'data2.tfrecord'])

ocr.tfrecords.serialize_dataset('path/to/output', raw_dataset, serialize_sample_fn)
# uses `serialize_sample_fn = ocr.tfrecords.serialize` by default
```

## Full-pipeline serving

```python
import keras # for '*.keras' models (keras v3)
# OR
import tf_keras as keras # for SavedModel (model.save()) from keras v2 / tensorflow <2.16

import tf_ocr as ocr

ocr_model = keras.models.load_model(MODEL_PATH, compile=False)
pipeline_model = ocr.pipeline(ocr_model, top_paths=4)

b64imgs = [b'iVBORw0KGgoA....lBDQliEbY5AAA', ...] # base-64 encoded JPG/PNG/BMP/GIF images
pipeline_model(tf.constant(b6imgs))
# {'preds': <tf.Tensor: shape=(16, 4), dtype=string, numpy=
#  array([[b'e4', b'ed4', b'e5', b'de4'],
#         ...
#         [b'Cd7', b'Cd4', b'Cf7', b'Cb7']], dtype=object)>,
#  'logprobs': <tf.Tensor: shape=(16, 4), dtype=float32, numpy=
#  array([[-0.04360915, -5.172318  , -5.24123   , -5.743371  ],
#         ...
#         [-0.43625632, -3.1230826 , -3.2804542 , -3.4402318 ]],
#        dtype=float32)>}
```

The `ocr.pipeline`-generated model can be `model.export()`-ed and served with `tfserving`