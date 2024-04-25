from typing import TypeVar, Generic, AsyncIterable
from abc import ABC, abstractmethod
from haskellian import Either, Left, IsLeft, either as E, Promise, promise as P, AsyncIter, asyn_iter as AI
from .errors import InexistentItem, DBError, InvalidData, ReadError

T = TypeVar('T')

class KV(ABC, Generic[T]):
  
  @abstractmethod
  def insert(self, key: str, value: T) -> Promise[Either[DBError, None]]: ...

  @abstractmethod
  def read(self, key: str) -> Promise[Either[ReadError, T]]: ...

  @abstractmethod
  def delete(self, key: str) -> Promise[Either[DBError | InexistentItem, None]]: ...

  @abstractmethod
  def items(self, batch_size: int | None = None) -> AsyncIter[Either[DBError | InvalidData, tuple[str, T]]]: ...

  @P.lift
  async def has(self, key: str) -> Either[DBError, bool]:
    try:
      keys = await self.keys().map(E.unsafe).sync()
      return E.Right(key in keys)
    except IsLeft as e:
      return E.Left(e.value)

  
  @AI.lift
  async def keys(self, batch_size: int | None = None) -> AsyncIterable[Either[DBError, str]]:
    async for e in self.items(batch_size):
      yield e.fmap(lambda it: it[0])
  
  @AI.lift
  async def values(self, batch_size: int | None = None) -> AsyncIterable[Either[DBError, T]]:
    async for e in self.items(batch_size):
      yield e.fmap(lambda it: it[1])

  @P.lift
  async def copy(self, key: str, to: 'KV[T]', to_key: str) -> Either[DBError|InexistentItem, None]:
    try:
      value = (await self.read(key)).unsafe()
      return await to.insert(to_key, value)
    except IsLeft as e:
      return Left(e.value)

  @P.lift
  async def move(self, key: str, to: 'KV[T]', to_key: str) -> Either[DBError|InexistentItem, None]:
    try:
      (await self.copy(key, to, to_key)).unsafe()
      (await self.delete(key)).unsafe()
    except IsLeft as e:
      return Left(e.value)
