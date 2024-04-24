from typing import Type, NewType, TypeVar, List
from core.common.chunk import Chunk
from core.common.event import Event

Events = TypeVar("Events", Event, List[Event])
Chunks = TypeVar("Chunks", Chunk, List[Chunk])
