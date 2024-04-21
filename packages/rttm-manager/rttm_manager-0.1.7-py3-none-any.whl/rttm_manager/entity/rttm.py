from dataclasses import dataclass


@dataclass
class RTTM:
    type: str
    file_id: str
    channel_id: int
    turn_onset: float
    turn_duration: float
    orthography_field: str
    speaker_type: str
    speaker_name: str
    confidence_score: str
    signal_lookahead_time: str
