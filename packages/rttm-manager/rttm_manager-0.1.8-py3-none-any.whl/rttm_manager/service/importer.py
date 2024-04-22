from rttm_manager.entity.rttm import RTTM
from pathlib import Path


class RTTMImporter:

    @staticmethod
    def _get_rttm_from_line(line: str) -> RTTM:
        line = line.rstrip()  # 改行やスペース削除
        values = line.split(" ")
        assert len(values) == 10

        return RTTM(
            type=values[0],
            file_id=values[1],
            channel_id=int(values[2]),
            turn_onset=float(values[3]),
            turn_duration=float(values[4]),
            orthography_field=None if values[5] == "<NA>" else values[5],
            speaker_type=None if values[6] == "<NA>" else values[6],
            speaker_name=values[7],
            confidence_score=None if values[8] == "<NA>" else float(values[8]),
            signal_lookahead_time=None if values[9] == "<NA>" else float(values[9]),
        )

    @staticmethod
    def rttm_import(file_name: str) -> list[RTTM]:
        file_path = Path(file_name)
        with open(str(file_path)) as f:
            lines = f.readlines()
        return [RTTMImporter._get_rttm_from_line(line) for line in lines]
