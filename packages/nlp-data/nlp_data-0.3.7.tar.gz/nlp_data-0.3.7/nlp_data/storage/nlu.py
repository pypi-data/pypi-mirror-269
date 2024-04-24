from typing import Iterator
from ..document import NLUDocList, NLUDoc
from .base import BaseDocStore
from docarray import DocList
import random


class NLUDocStore(BaseDocStore):
    
    bucket_name = 'nlu'
    
    @classmethod
    def pull(cls, name: str, show_progress: bool = True) -> NLUDocList:
        name = name.strip()
        docs = DocList[NLUDoc].pull(url=f's3://{cls.bucket_name}/{name}', show_progress=show_progress)
        return NLUDocList(docs)
    
    @classmethod
    def push(cls, docs: NLUDocList, name: str, show_progress: bool = True, shuffle: bool = True) -> None:
        name = name.strip()
        if shuffle:
            random.shuffle(docs)
        _ = DocList[NLUDoc].push_stream(docs, url=f's3://{cls.bucket_name}/{name}', show_progress=show_progress)
        return

    @classmethod
    def pull_stream(cls, name: str, show_progress: bool = True) -> Iterator[NLUDoc]:
        name = name.strip()
        for doc in DocList[NLUDoc].pull_stream(url=f's3://{cls.bucket_name}/{name}', show_progress=show_progress):
            yield doc
            
class NLUDocStoreZH(NLUDocStore):
    
    bucket_name = 'nlu'
    
    
class NLUDocStoreEN(NLUDocStore):
    
    bucket_name = 'nlu-en'