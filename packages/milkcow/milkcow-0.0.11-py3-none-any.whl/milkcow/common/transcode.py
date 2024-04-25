import json
from typing import Any, Optional

from milkcow.common.basestore import BaseStore


class BaseModelStore(BaseStore):
    def __init__(self, classmodel):
        '''Take class at initialization for transcoding'''
        super().__init__()
        self.classmodel: type = classmodel


class JqStore(BaseStore):
    '''Take json list of objects and save as list of strings'''

    def __init__(self, key_on: Optional[Any] = None,
                 classmodel: Optional[Any] = None) -> None:
        super().__init__()
        self.key_on = key_on
        self.classmodel = classmodel
        if self.key_on is None and self.classmodel is None:
            raise AttributeError

    def _transcode(self, value: str) -> Any:
        '''Turn list of strings into python of list objects'''
        if self.classmodel is not None:
            return self.classmodel(**json.loads(value))
        else:
            return value


class BlobStore(BaseStore):
    def _transcode(self, value: str):
        '''Encode string into bytes'''
        assert type(value) is str, value
        return value.encode()


class StrObjectStore(BaseModelStore):
    def _transcode(self, value: str):
        '''Encode string into pydantic model'''
        assert type(value) is str
        return self.classmodel(**json.loads(value))


class ByObjectStore(BaseModelStore):
