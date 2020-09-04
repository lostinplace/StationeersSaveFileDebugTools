import xml.etree.ElementTree as ET
from typing import Dict
from .AtmoFile import AtmoFile


def get_child_number_as_zfill_string(root: ET, child_label: str):
    raw: str = root.find(child_label).text


def number_string_to_sortable_string(text: str):
    value = int(text)
    content = abs(value)
    sign = '+' if value > 0 else '-'
    result = f'{sign}{str(content).zfill(7)}'
    return result


vector_components = ['x','y','z']


def vector_to_sortable_string(vector:ET):
    result = ''
    for v in vector_components:
        text = vector.find(v).text
        sortable_string = number_string_to_sortable_string(text)
        result += sortable_string
    return result


def get_asd_reference_tuple(asd: ET):
    thing_id: ET = asd.find("ThingReferenceId")
    network_id: ET = asd.find("NetworkReferenceId")
    thing_key = thing_id.text
    network_key = network_id.text
    position_key = None
    if thing_key == '0' and network_key == '0':
        position: ET = asd.find('Position')
        position_key = vector_to_sortable_string(position)
    return thing_key, network_key, position_key, asd


def get_atmosphere_dict(root: ET):
    ASDs = root.findall('.//AtmosphereSaveData')

    atmosphere_tuples = map(get_asd_reference_tuple, ASDs)

    by_id_dict = dict()
    by_position_dict = dict()
    by_network_dict = dict()

    for item in atmosphere_tuples:
        thing_id = item[0]
        network_id = item[1]
        position_key = item[2]
        value = item[3]

        if position_key:
            by_position_dict[position_key] = value
        elif thing_id  != '0':
            by_id_dict[thing_id] = value
        else:
            by_network_dict[network_id] = value

    return by_position_dict, by_id_dict, by_network_dict


def get_room_reference_tuple(room:ET):
    position_vector:ET = room.iter('Grid').__next__()
    vector_key = vector_to_sortable_string(position_vector)
    room_key = room.find("RoomId").text
    result = (room_key, vector_key, room)
    return result


def get_rooms_dict(root: ET):
    rooms = root.findall('.//Room')
    by_id_dict = dict()
    by_position_dict = dict()

    reference_tuples = map(get_room_reference_tuple, rooms)

    for item in reference_tuples:
        by_id_dict[item[0]] = item[2]
        by_position_dict[item[1]] = item[2]

    return by_id_dict, by_position_dict


def get_things(root: ET):
    TSDs = root.findall(".//ThingSaveData")
    result_dict = dict()

    for TSD in TSDs:
        ref_id = TSD.find('ReferenceId').text
        result_dict[ref_id] = TSD

    return result_dict


def get_things_from_id_collection(thing_dict: Dict, ids):
    result = dict()
    for i in ids:
        tmp = thing_dict.get(i)
        if tmp is not None:
            result[i] = tmp
    return result


def atmo_file_from_root(root: ET):
    atmo_by_position_dict, atmo_by_thing_id_dict, atmo_by_network_dict = get_atmosphere_dict(root)
    room_id_dict, room_position_dict = get_rooms_dict(root)
    thing_dict = get_things(root)
    result = AtmoFile(atmo_by_thing_id=atmo_by_thing_id_dict,
                      atmo_by_position=atmo_by_position_dict,
                      atmo_by_network=atmo_by_network_dict,
                      room_by_id=room_id_dict,
                      room_by_position=room_position_dict,
                      things=thing_dict
                      )
    return result


