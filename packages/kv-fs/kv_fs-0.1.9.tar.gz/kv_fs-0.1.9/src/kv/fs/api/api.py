from typing import TypeVar, Generic, Callable, AsyncIterable
from dataclasses import dataclass
import os
from haskellian import either as E, promise as P, asyn_iter as AI
from pydantic import RootModel
from kv.api import KV
from kv.api.errors import InexistentItem, InvalidData, ExistentItem, DBError
from .. import ops

A = TypeVar('A')
T = TypeVar('T')

@dataclass
class FilesystemKV(KV[T], Generic[T]):

  @classmethod
  def validated(cls, Type: type[A], base_path: str) -> 'FilesystemKV[A]':
    Model = RootModel[Type]
    return FilesystemKV(
      base_path=base_path, extension='.json',
      parse=lambda b: E.validate_json(b, Model).fmap(lambda x: x.root).mapl(InvalidData),
      dump=lambda x: Model(x).model_dump_json(exclude_none=True)
    )

  base_path: str
  extension: str = ''
  parse: Callable[[bytes], E.Either[InvalidData, T]] = lambda x: E.Right(x) # type: ignore
  dump: Callable[[T], bytes|str] = lambda x: x # type: ignore
  
  def __post_init__(self):
    os.makedirs(self.base_path, exist_ok=True)

  def _path(self, key: str) -> str:
    return os.path.abspath(os.path.join(self.base_path, f'{key}{self.extension}'))
  
  def _parse_err(self, key: str):
    def _curried(err: OSError) -> DBError | ExistentItem | InexistentItem:
      match err:
        case FileExistsError():
          return ExistentItem(key, detail=f"File already exists: {self._path(key)}")
        case FileNotFoundError():
          return InexistentItem(key, detail=f"File not found: {self._path(key)}")
        case OSError():
          return DBError(str(err))
    return _curried
    
  @P.lift
  async def insert(self, key: str, value: T, *, replace: bool = False) -> E.Either[ExistentItem|DBError, None]:
    return ops.insert(self._path(key), self.dump(value), exists_ok=replace) \
      .mapl(self._parse_err(key=key)) # type: ignore
  
  # @P.lift
  # async def update(self, key: str, value: T) -> E.Either[DBError | InexistentItem, None]:
  #   return ops.update(self._path(key), self.dump(value)) \
  #     .mapl(self._parse_err(key=key)) # type: ignore

  @P.lift
  async def read(self, key: str) -> E.Either[DBError | InvalidData | InexistentItem, T]:
    either = ops.read(self._path(key)) \
      .mapl(self._parse_err(key=key))
    return either.bind(self.parse) # type: ignore
  
  @P.lift
  async def delete(self, key: str) -> E.Either[DBError | InexistentItem, None]:
    return ops.delete(self._path(key)) \
      .mapl(self._parse_err(key=key)) # type: ignore
  
  @AI.lift
  async def keys(self, batch_size: int | None = None) -> AsyncIterable[E.Either[DBError, str]]:
    for either in ops.filenames(self.base_path):
      yield either \
        .fmap(lambda name: os.path.splitext(name)[0]) \
        .mapl(lambda err: DBError(str(err)))
  
  @AI.lift
  async def items(self, batch_size: int | None = None) -> AsyncIterable[E.Either[DBError | InvalidData, tuple[str, T]]]:
    for either in ops.files(self.base_path):
      try:
        filename, blob = either.unsafe()
        name, _ = os.path.splitext(filename)
        value = self.parse(blob).unsafe()
        yield E.Right((name, value))
      except E.IsLeft as e:
        if isinstance(e.value, OSError):
          yield E.Left(DBError(str(e)))
        else:
          yield E.Left(e.value)

  @P.lift
  async def commit(self) -> E.Either[DBError, None]:
    return E.Right(None)
  
  @P.lift
  async def rollback(self) -> E.Either[DBError, None]:
    return E.Left(DBError('Rollback not implemented in filesystem KV'))
  
  @P.lift
  async def copy(self, key: str, to: 'KV[T]', to_key: str, *, replace: bool = True) -> E.Either[DBError|InexistentItem|ExistentItem, None]:
    if not isinstance(to, FilesystemKV):
      return await super().copy(key, to, to_key, replace=replace)
    
    if not replace and os.path.exists(to._path(to_key)):
      return E.Left(ExistentItem(to_key, detail=f'Path "{to._path(to_key)}" already exists, but replace is False'))

    match ops.copy(self._path(key), to._path(to_key)):
      case E.Right():
        return E.Right(None)
      case E.Left(FileNotFoundError()) as e:
        return E.Left(InexistentItem(key, detail=str(e.value)))
      case E.Left() as e:
        return E.Left(DBError(detail=str(e.value)))
 
  @P.lift
  async def move(self, key: str, to: 'KV[T]', to_key: str, *, replace: bool = True) -> E.Either[DBError|InexistentItem|ExistentItem, None]:
    if not isinstance(to, FilesystemKV):
      return await super().move(key, to, to_key, replace=replace)
    
    if not replace and os.path.exists(to._path(to_key)):
      return E.Left(ExistentItem(to_key, detail=f'Path "{to._path(to_key)}" already exists, but replace is False'))

    match ops.move(self._path(key), to._path(to_key)):
      case E.Right():
        return E.Right(None)
      case E.Left(FileNotFoundError()) as e:
        return E.Left(InexistentItem(key, detail=str(e.value)))
      case E.Left() as e:
        return E.Left(DBError(detail=str(e.value)))
      