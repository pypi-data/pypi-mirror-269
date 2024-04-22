from typing import Callable, Iterable, AsyncIterable
import os
import time
import tensorflow as tf
from keras.layers import StringLookup
from .examples import deserialize, serialize
from ..labels import encode

def deserialize_dataset(filenames: list[str], *, keep_order: bool = False) -> tf.data.TFRecordDataset:
  """Parse a series of TFRecord files into a `tf.data.TFRecordDataset`
  - Each element is of type `ocr.tfrecords.Example`
  - Note: use `read_dataset` for a ready-to-train dataset
  """
  ignore_order = tf.data.Options()
  ignore_order.experimental_deterministic = keep_order
  return (
    tf.data.TFRecordDataset(filenames, num_parallel_reads=tf.data.AUTOTUNE)
    .with_options(ignore_order)
    .map(deserialize, num_parallel_calls=tf.data.AUTOTUNE)
  )

def read_dataset(
  filenames: list[str], *, batch_size: int = 32, shuffle_size: int | None = 1e3,
  char2num: StringLookup = None, maxlen: int = None, cache_file: str | None = '',
  keep_order: bool = False, prefetch: bool = True 
) -> tf.data.TFRecordDataset:
  """Parse and preprocess a series of TFRecord files
  - `shuffle_size`: if set to `None`, disables shuffling
  - `cache_file`: the default `''` caches in memory; `None` disables caching
  """
  ds = (
    deserialize_dataset(filenames, keep_order=keep_order)
    .batch(batch_size)
    .map(lambda x: x | dict(label=encode(x['label'], maxlen, char2num)), num_parallel_calls=tf.data.AUTOTUNE)
  )
  if prefetch:
    ds = ds.prefetch(tf.data.AUTOTUNE)
  if cache_file is not None:
    ds = ds.cache(cache_file)
  if shuffle_size is not None:
    ds = ds.shuffle(buffer_size=int(shuffle_size))
  
  return ds


async def serialize_datasets(
  output_dir: str,
  datasets: AsyncIterable[tf.data.Dataset],
  serialize: Callable[[dict|tuple], bytes] = serialize,
  num_batches: int | None = None, max_file_size: int = 1024*1024*100,
  filename: Callable[[int], str] = lambda i: f'data_{i}.tfrecord',
  exist_ok: bool = False
):
  """Serialize a `dataset` into a series of TFRecord files
  - `dataset`: sequence of samples of type `T`
  - `serialize :: T -> bytes`: serializes a sample into TFRecord format, e.g. using `tf.train.Example.SerializeToString`
  - `max_file_size`: in bytes. Defaults to `100MB`
  """
  os.makedirs(output_dir, exist_ok=exist_ok)
  current_file_size = 0
  file_index = 0
  tfrecord_filename = os.path.join(output_dir, f'data_{file_index}.tfrecord')
  writer = tf.io.TFRecordWriter(tfrecord_filename)
  t0 = time.time()
  i = 0
  n = num_batches

  async for dataset in datasets:
    for x in dataset:
      t1 = time.time()
      t_mean = (t1-t0)/(i+1)
      if n is not None:
        n_left = n - i - 1
        eta = t_mean*n_left
        msg = f"\r{i+1} / {n} [{(i+1)/n*100:.2f}%] - elapsed {t1-t0:.1f} secs - eta {eta:.1f} secs = {eta/3600:.2f} hours"
      else:
        msg = f"\r{i+1} / unknown - elapsed {t1-t0:.1f} secs"
      
      print(msg, end="", flush=True)
      serialized_example = serialize(x)
      example_size = len(serialized_example)
      
      if current_file_size + example_size > max_file_size:
        writer.close()
        file_index += 1
        tfrecord_filename = os.path.join(output_dir, filename(file_index))
        current_file_size = 0
        writer = tf.io.TFRecordWriter(tfrecord_filename)

      writer.write(serialized_example)
      current_file_size += example_size
      i += 1
  writer.close()