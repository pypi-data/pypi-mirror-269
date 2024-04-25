"""
### Sqlite Kv
> Async Key-Value interface over SQLite. Supports any datatype, including JSON and BLOB

- Details
"""
from .api import SQLiteKV
from . import queries

__all__ = ['SQLiteKV', 'queries']