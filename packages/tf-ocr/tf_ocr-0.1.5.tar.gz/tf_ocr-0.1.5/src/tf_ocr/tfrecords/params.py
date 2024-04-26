from typing_extensions import NotRequired, Literal, TypedDict, Any

class DeserializeParams(TypedDict):
  keep_order: NotRequired[bool]
  compression: NotRequired[Literal['ZLIB', 'GZIP'] | None]

class EncodeParams(TypedDict):
  maxlen: NotRequired[int | None]
  char2num: NotRequired[Any | None]

class ProcessParams(EncodeParams):
  remove_checks: NotRequired[bool]

class _ReadParams(ProcessParams, DeserializeParams):
  ...

class ReadParams(_ReadParams):
  batch_size: NotRequired[int]
  shuffle_size: NotRequired[float | None]
  cache_files: NotRequired[str | None]
  prefetch: NotRequired[bool]