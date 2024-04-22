from typing import Generic, TypeVar, AsyncIterable
from haskellian import Left, Right, Either, either as E, promise as P, asyn_iter as AI
from .api import KV
from .errors import ExistentItem, InexistentItem, DBError, InvalidData, ReadError

T = TypeVar('T')

class SimpleKV(KV[T], Generic[T]):
  """Simple `KV` using a `dict`"""

  def __init__(self, items: dict[str, T] = {}):
    self.xs = items

  @P.lift
  async def insert(self, key: str, value: T, *, replace: bool = False) -> Either[ExistentItem, None]:
    if not replace and key in self.xs:
      return Left(ExistentItem(key))
    else:
      self.xs[key] = value
      return Right(None)

  @P.lift
  async def read(self, key: str) -> Either[ReadError, T]:
    return E.maybe(self.xs.get(key)).mapl(lambda _: InexistentItem(key))

  @P.lift
  async def delete(self, key: str) -> Either[DBError | InexistentItem, None]:
    if not key in self.xs:
      return Left(InexistentItem(key))
    else:
      del self.xs[key]
      return Right(None)

  @AI.lift
  async def items(self, batch_size: int | None = None) -> AsyncIterable[Either[DBError | InvalidData, tuple[str, T]]]:
    for item in self.xs.items():
      yield Right(item)

  @AI.lift
  async def keys(self, batch_size: int | None = None) -> AsyncIterable[Either[DBError, str]]:
    for key in self.xs.keys():
      yield Right(key)

  @P.lift
  async def commit(self) -> Either[DBError, None]:
    ...
  
  @P.lift
  async def rollback(self) -> Either[DBError, None]:
    raise NotImplementedError('Rollback not implemented in `SimpleKV`')