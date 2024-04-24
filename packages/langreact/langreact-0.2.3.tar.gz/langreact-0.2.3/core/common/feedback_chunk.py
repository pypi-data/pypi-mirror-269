

from dataclasses import dataclass, field

import numpy as np

from core.common.chunk import Chunk, new_none_chunk
from core.common.event import NONE_EVENT, Event


@dataclass
class FeedbackChunk(Chunk):
    feedback_chunk: Chunk = field(default_factory=new_none_chunk)
    feedback_event: Event = field(default=NONE_EVENT)
    feedback_score: float = field(default=np.nan)

    def from_json(json_chunk):
        chunk = FeedbackChunk()
        for k, v in json_chunk.items():
            if k == "feedback_chunk":
                v = Chunk.from_json(v)
            if k == "feedback_event":
                v = Event.from_json(v)
            setattr(chunk, k, v)
        return chunk
