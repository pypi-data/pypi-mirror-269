"""
### Key-Value Api
> API spec for an async Key-Value DB

- Details
"""
from .kv import KV
from .impl import SimpleKV
from .errors import DBError, InexistentItem, InvalidData, ReadError
from .append import AppendableKV, SimpleAppendKV