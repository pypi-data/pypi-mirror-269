from typing import TypedDict
import tensorflow as tf
from jaxtyping import Float
from tf_tools import Bytes

OutputFeatures = dict[str, tf.io.FixedLenFeature | tf.io.VarLenFeature]

def input_features(width: int = 256, height: int = 64):
  """Features describing data stored in a TFRecord. Can be used with `ocr.tfrecords.deserialize` (a wrapper for `tf.io.parse_single_example`)"""
  return {
    'boxid': tf.io.FixedLenFeature([], tf.string),
    'image': tf.io.FixedLenFeature([width, height, 1], tf.float32),
    'label': tf.io.FixedLenFeature([], tf.string)
  }
  
class Example(TypedDict):
  boxid: Bytes[tf.Tensor, '']
  label: Bytes[tf.Tensor, '']
  image: Float[tf.Tensor, "width height 1"]

def deserialize(example: Bytes[tf.Tensor, ''], *, width: int = 256, height: int = 64, features: OutputFeatures = None) -> Example:
  """Parse a TFRecord-encoded tensor (as obtained via `tf.data.TFRecordDataset`)"""
  return tf.io.parse_single_example(example, features or input_features(width, height))

def serialize(example: Example) -> bytes:
  """Serialize an `Example` into a TFRecord-compatible bytes object (can be used with `tf.io.TFRecordWriter` to export)"""
  feature = {
    'boxid': tf.train.Feature(bytes_list=tf.train.BytesList(value=[example['boxid'].numpy()])), 
    'image': tf.train.Feature(float_list=tf.train.FloatList(value=example['image'].numpy().flatten())),
    'label': tf.train.Feature(bytes_list=tf.train.BytesList(value=[example['label'].numpy()]))
  }
  example_proto = tf.train.Example(features=tf.train.Features(feature=feature))
  return example_proto.SerializeToString()