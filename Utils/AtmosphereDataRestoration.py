from .AtmoFile import AtmoFile, RestoredAtmoData
from typing import Dict


def restore_missing_entries_to_dict(current_dict, old_dict):
    result = {**old_dict, **current_dict}
    return result


def restore_atmospheres_from_backup(current_file: AtmoFile, old_file: AtmoFile):
    thing_atmos = restore_missing_entries_to_dict(current_file.atmo_by_thing_id, old_file.atmo_by_thing_id)
    network_atmos = restore_missing_entries_to_dict(current_file.atmo_by_network, old_file.atmo_by_network)
    position_atmos = restore_missing_entries_to_dict(current_file.atmo_by_position, old_file.atmo_by_position)
    restored_atmospheres = [*thing_atmos.values(), *network_atmos.values(), *position_atmos.values()]
    return restored_atmospheres


def restore_rooms_from_backup(current_file: AtmoFile, old_file: AtmoFile):
    restored_rooms_dict = restore_missing_entries_to_dict(current_file.room_by_id, old_file.room_by_id)
    restored_rooms = restored_rooms_dict.values()
    return restored_rooms


def get_restored_data(current_file: AtmoFile, old_file: AtmoFile) -> RestoredAtmoData:
    rooms = restore_rooms_from_backup(current_file, old_file)
    atmos = restore_atmospheres_from_backup(current_file, old_file)
    result = RestoredAtmoData(atmos, rooms)
    return result