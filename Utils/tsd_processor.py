from collections import defaultdict
from xml.etree.ElementTree import ElementTree as ET

from Utils.ThingSaveData import from_ET


def addParentInfo(et):
    for child in et:
        child.attrib['__my_parent__'] = et
        addParentInfo(child)


def generate_tsd_list(world_data_tree):
    addParentInfo(world_data_tree.getroot())
    thing_save_data_items: list[ET] = world_data_tree.findall('.//ThingSaveData')
    tsd_data_list = list(thing_save_data_items)
    tsd_list = [from_ET(_) for _ in tsd_data_list]
    return tsd_list


def generate_tsd_indices(tsd_list):
    """
    generate helpful indices from TSD entries
    :return: tuple with parent_dict (parent ref-id -> list[TSD]), prefab_dict (prefabname -> list[TSD]), and ref_dict (ref-id -> TSD)
    :returns: tuple with parent_dict (parent ref-id -> list[TSD]), prefab_dict (prefabname -> list[TSD]), and ref_dict (ref-id -> TSD)
    :rtype: object
    """
    tsd_ref_index = map(lambda _: (_.ReferenceId, _), tsd_list)
    tsd_ref_dict = dict(tsd_ref_index)
    tsd_prefab_index = map(lambda _: (_.PrefabName, _), tsd_list)
    tsd_prefab_dict = defaultdict(list)
    for item in tsd_prefab_index:
        tsd_prefab_dict[item[0]].append(item[1])
    tsd_parent_index = map(lambda _: (_.ParentReferenceId, _), tsd_list)
    tsd_parent_dict = defaultdict(list)
    for item in tsd_parent_index:
        tsd_parent_dict[item[0]].append(item[1])
    return tsd_parent_dict, tsd_prefab_dict, tsd_ref_dict