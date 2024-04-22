from rttm_manager.entity.rttm import RTTM
from rttm_manager.service.importer import RTTMImporter
from rttm_manager.service.exporter import RTTMExporter


def import_rttm(file_path: str) -> list[RTTM]:
    return RTTMImporter.rttm_import(file_path)


def export_rttm(rttms: list[RTTM], file_path: str) -> None:
    RTTMExporter.rttm_export(rttms, file_path)
