from typing import Generic, TypeVar
import haskellian.either as E
from kv.api.append import AppendableKV
from kv.api.errors import InexistentItem
from q.api import AppendableQueue
from .api import QueueKV

A = TypeVar('A')
T = TypeVar('T')

class AppendQueueKV(QueueKV[list[T]], AppendableQueue[T], Generic[T]):

  def __init__(self, kv: AppendableKV[T]):
    super().__init__(kv)
    self._kv = kv
  
  @classmethod
  def fs(cls, Type: type[A], path: str) -> 'AppendQueueKV[A]':
    from kv.fs.append import FilesystemAppendKV
    return AppendQueueKV[A](FilesystemAppendKV.validated(Type, path))

  async def append(self, id: str, values: list[T], *, create: bool = True) -> None | bool:
    match await self._kv.append(id, values, create=create):
      case E.Left(InexistentItem()):
        return False
      case either:
        either.unsafe()
        if not create:
          return True
  