from typing_extensions import Callable, Literal, AsyncIterable, Sequence, TypedDict, Unpack, NotRequired
from functools import partial
import os
import time
from haskellian import kwargs as kw
import tensorflow as tf
import fs
from .examples import deserialize, serialize
from ..labels import encode
from .params import EncodeParams, _ReadParams, DeserializeParams, ProcessParams

Dataset = tf.data.Dataset

def deserialize_dataset(
  filenames: Sequence[str], *,
  keep_order: bool = False,
  compression: Literal['ZLIB', 'GZIP'] | None = 'GZIP'
) -> tf.data.Dataset:
  """Parse a series of TFRecord files into a `tf.data.TFRecordDataset`
  - Each element is of type `ocr.tfrecords.Example`
  - Note: use `read_dataset` for a ready-to-train dataset
  """
  ignore_order = tf.data.Options()
  ignore_order.experimental_deterministic = keep_order
  return (
    tf.data.TFRecordDataset(filenames, compression_type=compression, num_parallel_reads=tf.data.AUTOTUNE)
    .with_options(ignore_order)
    .map(deserialize, num_parallel_calls=tf.data.AUTOTUNE)
  )

def process_batch(batch: dict[str, tf.Tensor], remove_checks: bool = True, **p: Unpack[EncodeParams]) -> tuple[tf.Tensor, tf.SparseTensor]:
  lab = tf.strings.regex_replace(batch["label"], "[\+#]", "") if remove_checks else batch["label"]
  return batch["image"], tf.cast(encode(lab, **p), tf.int32) # type: ignore

def read_dataset(
  filenames: list[str], *, batch_size: int = 32, shuffle_size: float | None = 1e3,
  cache_file: str | None = '', prefetch: bool = True, **p: Unpack[_ReadParams]
) -> tf.data.Dataset:
  """Parse and preprocess a series of TFRecord files. Returns `(img, sparse_label)` batches
  - `shuffle_size`: if set to `None`, disables shuffling
  - `cache_file`: the default `''` caches in memory; `None` disables caching
  - `remove_checks`: whether to remove `'#'` and `'+'` symbols from the labels. Defaults to `True`
  """
  deserialize_params, process_params = kw.split(DeserializeParams, ProcessParams, p)
  ds = deserialize_dataset(filenames, **deserialize_params)
  if cache_file is not None:
    ds = ds.cache(cache_file)
  if shuffle_size is not None:
    ds = ds.shuffle(buffer_size=int(shuffle_size))
  
  ds = ds.batch(batch_size) \
    .map(partial(process_batch, **process_params), num_parallel_calls=tf.data.AUTOTUNE)
  
  if prefetch:
    ds = ds.prefetch(tf.data.AUTOTUNE)
  
  return ds


async def serialize_datasets(
  output_dir: str,
  datasets: AsyncIterable[tf.data.Dataset],
  serialize: Callable[[dict|tuple], str] = serialize, # type: ignore
  num_batches: int | None = None, max_file_size: int = 1024*1024*100,
  filename: Callable[[int], str] = lambda i: f'data_{i}.tfrecord',
  exist_ok: bool = False, compress: bool = True
):
  """Serialize a `dataset` into a series of TFRecord files
  - `dataset`: sequence of samples of type `T`
  - `num_batches`: number of batches of the dataset (for ETA estimation)
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
      serialized_example = serialize(x) # type: ignore
      example_size = len(serialized_example)
      
      if current_file_size + example_size > max_file_size:
        writer.close()
        if compress:
          fs.gzcompress(tfrecord_filename, keep=False)
        file_index += 1
        tfrecord_filename = os.path.join(output_dir, filename(file_index))
        current_file_size = 0
        writer = tf.io.TFRecordWriter(tfrecord_filename)

      writer.write(serialized_example)
      current_file_size += example_size
      i += 1
  writer.close()
  if compress:
    fs.gzcompress(tfrecord_filename, keep=False)