from math import floor
from typing import List, Dict
import xml.etree.ElementTree as ET

from Utils.ThingSaveData import to_InventoryData, ThingSaveData
from .start_condition_data_structures import InventoryData, DynamicThingData
from ..dict_to_xml import namedtuple_to_xml

from ..tsd_processor import generate_tsd_list, generate_tsd_indices
from ..world_file_loader import load_file


import re

lander_name_re = re.compile(r"""(.+)-(.*)""")


def convert_world_file_to_startconditions(path: str) -> str:
    from importlib import resources
    world_data_tree: ET = load_file(path)

    tsd_list = generate_tsd_list(world_data_tree)
    tsd_parent_dict, tsd_prefab_dict, tsd_ref_dict = generate_tsd_indices(tsd_list)

    lander_DTDs = generate_landers(tsd_list, tsd_parent_dict, tsd_prefab_dict)
    initial_inventory_IDs = generate_initial_inventory_IDs(tsd_parent_dict, tsd_prefab_dict)

    player_inventory_contents_XML = [namedtuple_to_xml(_) for _ in initial_inventory_IDs]
    initialspawn_contents_XML = [namedtuple_to_xml(_) for _ in lander_DTDs]

    template_string = resources.read_text("Utils.StartConditionProcessing", "template_startconditions.xml")
    cleaned = template_string.replace("\n","")
    template_data = ET.fromstring(cleaned)

    player_inventory_tree = template_data.find(".//PlayerInventory")
    for item in player_inventory_contents_XML:
        player_inventory_tree.append(item)

    InitialSpawn_tree = template_data.find(".//InitialSpawn")
    for item in initialspawn_contents_XML:
        InitialSpawn_tree.append(item)

    out_string = ET.tostring(template_data, encoding='utf8', method='xml')
    from xml.dom import minidom

    out_string_formatted = minidom.parseString(out_string.decode("utf-8")).toprettyxml(indent="   ")
    return out_string_formatted


def generate_initial_inventory_IDs(tsd_parent_dict, tsd_prefab_dict):
    character_list = tsd_prefab_dict.get("Character")
    if character_list is not None and len(character_list) > 0:
        character = character_list[0]
        character_ID = to_InventoryData(character, tsd_parent_dict)
        initial_inventory_IDs = [_ for _ in character_ID.Contents if not _.PrefabName.lower().startswith('organ')]
    return initial_inventory_IDs


def generate_landers(tsd_list, tsd_parent_dict, tsd_prefab_dict):
    crate_IDs: List[InventoryData] = generate_crate_IDs(tsd_parent_dict, tsd_prefab_dict)
    gas_can_IDs = generate_gascan_IDs(tsd_list, tsd_parent_dict)
    landers_needed_for_crates = len(crate_IDs) / 6
    landers_needed_for_cans = len(gas_can_IDs) / 2
    landers_needed = int(max(landers_needed_for_cans, landers_needed_for_crates))
    lander_DTDs = list()
    for lander_index in range(landers_needed):
        crate_contents = build_contents(crate_IDs, lander_index * 6, range(0, 6))
        gas_can_contents = build_contents(gas_can_IDs, lander_index * 2, [6, 7])

        lander = DynamicThingData(None, None, crate_contents + gas_can_contents, "Lander")
        lander_DTDs.append(lander)
    return lander_DTDs


def build_contents(ID_list, offset, slots:range):

    crates = ID_list[offset:offset + len(slots)]
    slots_needed = min(len(slots), len(crates))

    lander_crates = list()
    for slot_index in range(slots_needed):
        this_slot_crate = crates[slot_index]
        crate = this_slot_crate._replace(SlotId=slot_index)
        lander_crates.append(crate)
    return lander_crates


def generate_gascan_IDs(tsd_list, tsd_parent_dict):
    gas_can_TSDs = [
        _ for _ in tsd_list
        if _.xsi_type == 'DynamicGasCanisterSaveData'
           and (_.CustomName is None or _.CustomName.lower() != "exclude")
    ]
    gas_can_IDs = [to_InventoryData(_, tsd_parent_dict) for _ in gas_can_TSDs]
    return gas_can_IDs


def generate_crate_IDs(tsd_parent_dict: Dict[str, ThingSaveData], tsd_prefab_dict: Dict[str, ThingSaveData]) -> \
        List[InventoryData]:
    crates = tsd_prefab_dict['CrateMkII'] + tsd_prefab_dict['DynamicCrate']
    crate_IDs = [
        to_InventoryData(_, tsd_parent_dict)
        for _ in crates
        if _.CustomName is None or _.CustomName.lower() != "exclude"
    ]
    return crate_IDs
