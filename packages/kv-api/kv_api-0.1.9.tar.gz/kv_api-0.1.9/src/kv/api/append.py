from typing import Generic, TypeVar, overload, Literal
from abc import ABC, abstractmethod
from haskellian import Either, Left, Right, Promise, promise as P
from .kv import KV
from .impl import SimpleKV
from .errors import DBError, InexistentItem

T = TypeVar('T')

class Appendable(ABC, Generic[T]):
  @overload
  @abstractmethod
  def append(self, id: str, values: list[T], *, create: Literal[False]) -> Promise[Either[DBError|InexistentItem, None]]:
    """Appends `values` if it already existed. Otherwise doesn't append, and returns `Left[ExistentItem]`"""
  @overload
  @abstractmethod
  def append(self, id: str, values: list[T], *, create: bool = True) -> Promise[Either[DBError, None]]:
    """Appends `values` to `id`, creating the item if needed"""

class AppendableKV(KV[list[T]], Appendable, Generic[T]):
  ...
  
class SimpleAppendKV(AppendableKV[T], SimpleKV[list[T]], Generic[T]):

  @P.lift
  async def append(self, key: str, values: list[T], *, create: bool = True) -> Either[DBError|InexistentItem, None]:
    if not key in self.xs:
      if create:
        self.xs[key] = values
      else:
        return Left(InexistentItem(key))
    else:
      self.xs[key].extend(values)
    return Right(None)