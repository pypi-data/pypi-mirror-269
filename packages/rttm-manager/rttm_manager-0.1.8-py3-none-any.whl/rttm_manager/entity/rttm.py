from typing import Union
from pydantic import BaseModel


class RTTM(BaseModel, frozen=True):
    type: str
    file_id: str
    channel_id: int
    turn_onset: float
    turn_duration: float
    speaker_name: str
    orthography_field: Union[str, None] = None
    speaker_type: Union[str, None] = None
    confidence_score: Union[float, None] = None
    signal_lookahead_time: Union[float, None] = None
