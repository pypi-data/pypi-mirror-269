from typing import Generic, TypeVar
from haskellian.either import Left, Right, Either
import haskellian.asyn.promises as P
from ..simple import SimpleKV
from ..errors import InexistentItem, DBError
from .append import AppendableKV

T = TypeVar('T')

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
    