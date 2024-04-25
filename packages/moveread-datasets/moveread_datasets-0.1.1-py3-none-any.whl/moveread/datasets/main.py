from typing import Literal, Sequence, Iterable, Unpack
from dataclasses import dataclass
from pydantic import BaseModel
from haskellian import either as E, promise as P
from kv.api import KV
from kv.fs import FilesystemKV
import tf_ocr as ocr

Source = Literal['llobregat23', 'original-train', 'original-test', 'original-val']

class Dataset(BaseModel):
  file: str
  source: Source

@dataclass
class DatasetsAPI:
  meta: KV[Dataset]
  data: FilesystemKV[bytes]

  @classmethod
  def at(cls, path: str) -> 'DatasetsAPI':
    import os
    from kv.sqlite import SQLiteKV
    return DatasetsAPI(
      meta=SQLiteKV.validated(Dataset, os.path.join(path, 'meta.sqlite'), table='datasets'),
      data=FilesystemKV[bytes](os.path.join(path, 'data'))
    )
  
  @P.lift
  async def readall(self) -> Sequence[tuple[str, Dataset]]:
    return await self.meta.items().map(E.unsafe).sync()
  
  def load(self, datasetIds: Iterable[str], **params: Unpack[ocr.ReadParams]) -> ocr.Dataset:
    params['compression'] = 'GZIP'
    files = [self.data.url(id) for id in datasetIds]
    return ocr.read_dataset(files, **params)
    
