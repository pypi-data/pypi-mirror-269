from typing import TypeVar, Generic, overload, Literal
from abc import ABC, abstractmethod
from haskellian import Either, Left, IsLeft, Promise, promise as P, AsyncIter
from .errors import ExistentItem, InexistentItem, DBError, InvalidData, ReadError

T = TypeVar('T')

class KV(ABC, Generic[T]):
  
  @overload
  @abstractmethod
  def insert(self, key: str, value: T, *, replace: Literal[True]) -> Promise[Either[DBError, None]]: ...
  @overload
  @abstractmethod
  def insert(self, key: str, value: T, *, replace: bool = False) -> Promise[Either[DBError | ExistentItem, None]]: ...

  # @abstractmethod
  # def update(self, key: str, value: T) -> Promise[Either[DBError | InexistentItem, None]]: ...

  @abstractmethod
  def read(self, key: str) -> Promise[Either[ReadError, T]]: ...

  @abstractmethod
  def delete(self, key: str) -> Promise[Either[DBError | InexistentItem, None]]: ...

  @abstractmethod
  def items(self, batch_size: int | None = None) -> AsyncIter[Either[DBError | InvalidData, tuple[str, T]]]: ...

  @abstractmethod
  def keys(self, batch_size: int | None = None) -> AsyncIter[Either[DBError, str]]: ...

  @abstractmethod
  def commit(self) -> Promise[Either[DBError, None]]: ...
  
  @abstractmethod
  def rollback(self) -> Promise[Either[DBError, None]]: ...

  @overload
  def copy(self, key: str, to: 'KV[T]', to_key: str, *, replace: Literal[False]) -> Promise[Either[DBError|InexistentItem|ExistentItem, None]]: ...
  @overload
  def copy(self, key: str, to: 'KV[T]', to_key: str, *, replace: bool = True) -> Promise[Either[DBError|InexistentItem, None]]: ...
  @P.lift
  async def copy(self, key: str, to: 'KV[T]', to_key: str, *, replace: bool = True):
    try:
      value = (await self.read(key)).unsafe()
      return await to.insert(to_key, value, replace=replace)
    except IsLeft as e:
      return Left(e.value)

  @overload
  def move(self, key: str, to: 'KV[T]', to_key: str, *, replace: Literal[False]) -> Promise[Either[DBError|InexistentItem|ExistentItem, None]]: ...
  @overload
  def move(self, key: str, to: 'KV[T]', to_key: str, *, replace: bool = True) -> Promise[Either[DBError|InexistentItem, None]]: ...
  @P.lift
  async def move(self, key: str, to: 'KV[T]', to_key: str, *, replace: bool = True):
    try:
      (await self.copy(key, to, to_key, replace=replace)).unsafe()
      (await self.delete(key)).unsafe()
    except IsLeft as e:
      return Left(e.value)
