from rttm_manager.entity.rttm import RTTM
from pathlib import Path


class RTTMExporter:

    @staticmethod
    def _generate_rttm_line(rttm: RTTM):
        line = [
            rttm.type,
            rttm.file_id,
            f"{rttm.channel_id}",
            f"{rttm.turn_onset:.2f}",
            f"{rttm.turn_duration:.2f}",
            rttm.orthography_field if rttm.orthography_field is not None else "<NA>",
            rttm.speaker_type if rttm.speaker_type is not None else "<NA>",
            rttm.speaker_name,
            (
                f"{rttm.confidence_score:.2f}"
                if rttm.confidence_score is not None
                else "<NA>"
            ),
            (
                f"{rttm.signal_lookahead_time:.2f}"
                if rttm.signal_lookahead_time is not None
                else "<NA>"
            ),
        ]
        return " ".join(line) + "\n"

    @staticmethod
    def rttm_export(rttms: list[RTTM], file_name: str) -> None:
        file_path = Path(file_name)
        assert isinstance(rttms, list)

        lines = [RTTMExporter._generate_rttm_line(rttm) for rttm in rttms]

        with open(str(file_path), "w") as f:
            f.writelines(lines)
