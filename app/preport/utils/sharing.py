import requests
from typing import Any
from preport.models import DB_ShareConnection
from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
import sys

class ShareType(Enum):
    none = "none"
    deliverable = "deliverable"
    finding = "finding"

class Abstract(ABC):
    title:str
    type:ShareType = ShareType.none
    url:str
    credentials:str

    def __init__(self, connection:DB_ShareConnection) -> None:
        super().__init__()
        assert self.type.value == connection.type
        self.title = connection.title
        self.url = connection.url
        self.credentials = connection.credentials # env.get(connection.credentials)

    @abstractmethod
    def __call__(self, **kwargs) -> tuple[datetime, str]:
        pass

class Test(Abstract):
    type = ShareType.finding
    def __call__(self, **kwargs) -> tuple[datetime, str]:
        filename = kwargs.get('filename')
        res = requests.get(self.url, data="test")
        res.raise_for_status()
        return datetime.utcnow(), "done"

class PostFileTest(Abstract):
    type = ShareType.deliverable
    def __call__(self, **kwargs) -> tuple[datetime, str]:
        if 'filename' in kwargs:
            f = kwargs.get('filename', 'NoFile')
            file = {'upload_file': open(f,'rb')}
            #values = {'DB': 'photcat', 'OUT': 'csv', 'SHORT': 'short'}
            res = requests.post(self.url, files=file)#, data=values)
            res.raise_for_status()
            return datetime.utcnow(), res.text
        else:
            return datetime.utcnow(), 'Sharing Error'

class PostFile(Abstract):
    type = ShareType.deliverable
    def __call__(self, **kwargs) -> tuple[datetime, str]:
        if 'filename' in kwargs:
            f = kwargs.get('filename', 'NoFile')
            file = {'upload_file': open(f,'rb')}
            project = kwargs.get('project', '')
            return datetime.utcnow(), 'todo_get_uuid --> ' + project
        else:
            return datetime.utcnow(), 'Sharing Error'

# Export
shares_all = {k:v for k,v in globals().items() if isinstance(v, type(Abstract)) and issubclass(v,Abstract) and len(v.__mro__) > 2}
shares_finding = {k:v for k,v in shares_all.items() if v.type == ShareType.finding}
shares_deliverable = {k:v for k,v in shares_all.items() if v.type == ShareType.deliverable}