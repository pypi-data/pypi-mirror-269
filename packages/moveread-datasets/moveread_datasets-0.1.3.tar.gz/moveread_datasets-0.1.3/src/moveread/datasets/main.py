from typing import Literal, Sequence, Iterable
from typing_extensions import Unpack
from dataclasses import dataclass
from pydantic import BaseModel
from haskellian import either as E, promise as P
from kv.api import KV
from kv.fs import FilesystemKV
import tf_ocr as ocr

Source = Literal['llobregat23', 'original-train', 'original-test', 'original-val'] | str

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
  
  async def load(self, datasetIds: Iterable[str], **params: Unpack[ocr.ReadParams]):
    datasets = await P.all([self.meta.read(id).then(E.unsafe) for id in datasetIds])
    params['compression'] = 'GZIP'
    files = [self.data.url(d.file) for d in datasets]
    return ocr.read_dataset(files, **params)
    
