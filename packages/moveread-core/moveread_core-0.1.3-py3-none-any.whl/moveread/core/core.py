from typing import TypeVar
from dataclasses import dataclass
import haskellian.either as E
from kv.api import KV
from .models import Game

T = TypeVar('T')

@dataclass
class CoreAPI:

  games: KV[Game]
  blobs: KV[bytes]

  @classmethod
  def at(cls, path: str, blobs_extension: str = '.jpg') -> 'CoreAPI':
    from .local import LocalAPI
    return LocalAPI(path, blobs_extension)
  
  @classmethod
  def debug(cls, path: str, blobs_extension: str = '.jpg') -> 'CoreAPI':
    from .local import DebugAPI
    return DebugAPI(path, blobs_extension)
