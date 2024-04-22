from typing import Generic, Literal, TypeVar, overload
import asyncio
from datetime import timedelta
from haskellian import either as E, AsyncIter
from kv.api import KV
from q.api import Queue

A = TypeVar('A')
B = TypeVar('B')

class QueueKV(Queue[A], Generic[A]):

  def __init__(
    self, kv: KV[A],
    poll_interval: timedelta = timedelta(seconds=5),
  ):
    self._kv = kv
    self.poll_interval = poll_interval

  @classmethod
  def fs(cls, Type: type[B], path: str) -> 'QueueKV[B]':
    try:
      from kv.fs import FilesystemKV
    except ImportError:
      raise ImportError('Install `kv-fs` to run in filesystem')
    return QueueKV(FilesystemKV.validated(Type, path))
  
  @classmethod
  def sqlite(cls, Type: type[B], path: str, table: str = 'queue') -> 'QueueKV[B]':
    try:
      from kv.sqlite import SQLiteKV
    except ImportError:
      raise ImportError('Install `kv-sqlite-sync` to run in local SQLite')
    if len(path.split('.')) == 1:
      path += '.sqlite'
    return QueueKV(SQLiteKV.validated(Type, path, table))
  
  @classmethod
  @overload
  def at(cls, Type: type[B], path: str, protocol: Literal['fs']) -> 'QueueKV[B]': ...
  @classmethod
  @overload
  def at(cls, Type: type[B], path: str, protocol: Literal['sqlite'], table: str = 'queue') -> 'QueueKV[B]': ...
  
  @classmethod
  def at(cls, Type: type[B], path: str, protocol: Literal['fs', 'sqlite'], table: str = 'queue') -> 'QueueKV[B]':
    return QueueKV.fs(Type, path) if protocol == 'fs' else QueueKV.sqlite(Type, path, table)


  async def push(self, key: str, value: A):
    return (await self._kv.insert(key, value, replace=True)).unsafe()
  
  async def _read(self, id: str | None = None, remove: bool = False) -> None | tuple[str, A]:
    if id is None:
      head = await self._kv.keys().head()
      if head is None:
        await asyncio.sleep(self.poll_interval.total_seconds())
        return await self._read(id, remove)
      else:
        key = head.unsafe()
    else:
      key = id

    value = (await self._kv.read(key)).unsafe()
    if remove:
      (await self._kv.delete(key)).unsafe()
    return key, value
    
  def _items(self) -> AsyncIter[tuple[str, A]]:
    return self._kv.items().map(E.unsafe)
  