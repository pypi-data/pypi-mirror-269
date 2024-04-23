from typing import Generic, TypeVar
import os
from pydantic import RootModel
from haskellian import either as E, promise as P
from kv.api.append import AppendableKV
from kv.api.errors import InexistentItem, DBError, InvalidData
from ..api import FilesystemKV
from .. import ops
from . import ndjson

A = TypeVar('A')
T = TypeVar('T')

class FilesystemAppendKV(FilesystemKV[list[T]], AppendableKV[T], Generic[T]):

  @P.lift
  async def append(self, id: str, values: list[T], *, create: bool = True) -> E.Either[DBError|InexistentItem, None]:
    if not create and not os.path.exists(self._path(id)):
      return E.Left(InexistentItem(id))
    either = ops.append(self._path(id), self.dump(values))
    return either.mapl(self._parse_err) # type: ignore
    
  @classmethod
  def validated(cls, Type: type[A], base_path: str) -> 'FilesystemAppendKV[A]':
    Model = RootModel[Type]
    return FilesystemAppendKV(
      base_path=base_path, extension='.ndjson',
      parse=lambda data: ndjson.parse(data, Model).mapl(InvalidData),
      dump=lambda items: ndjson.dump(items, Model)
    )
  