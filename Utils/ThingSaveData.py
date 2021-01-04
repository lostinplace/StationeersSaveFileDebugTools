from collections import namedtuple
from Utils.StartConditionProcessing.start_condition_data_structures import InventoryData, DynamicThingData
from xml.etree import ElementTree as ET

#lander slots: 0-5 are crates, 6 & 7 are gascans

ThingSaveData = namedtuple('ThingSaveData',
                           'identity CurrentIndex ExportState LinkedDeviceReferences LastInputId CustomColorIndex '
                           'OutputSetting SleepDurationRemaining MovementControllerControlMode HairIndex Currency '
                           'PowerStored HairColourIndex Velocity PrefabName ExportCount Nutrition LastIndex Dragged '
                           'SkinCololurIndex GenderIndex AngularVelocity HealthCurrent Amount SourceCode Reagents '
                           'EyeColourIndex MothershipReferenceId CustomName CurrentInputId HasSpawnedWreckage EyeIndex '
                           'HarvestQuantity CurrentOutputHash CableNetworkId StageTime IsBurst State FacialhairIndex '
                           'Flag MasterMotherboard Setting ParentReferenceId States FilterString ReferenceId Stage '
                           'WorldPosition FabricatorJob CurrentOutput LeakRatio ClientSteamId CurrentIndexedSlot '
                           'DragOffset LogicType DeviceLables IsCustomName ImportState WorldRotation Oxygenation '
                           'ParentSlotId Quantity CurrentBuildState PipeNetworkId LastSetting Registers ImportCount '
                           'NextAddr OwnerSteamId SkinIndex OutputTemperatureSetting DraggedInteractionIndex '
                           'Indestructable DamageState parsed_element xsi_type')


def from_ET(et:ET) -> ThingSaveData:
    result_data = dict()

    for item in ThingSaveData._fields:
        value = et.find("./"+item)
        result_data[item] = value.text.strip() if value is not None and value.text is not None else None
    result_data['parsed_element'] = et
    result_data['xsi_type'] = et.get('{http://www.w3.org/2001/XMLSchema-instance}type')

    result = ThingSaveData(**result_data)
    return result



custom_colors_numbers = {
    'ColorRed': '4',
    'ColorBlack': '7',
    'ColorBrown': '8',
    'ColorGray': '1',
    'ColorOrange': '3',
    'ColorPink': '10',
    'ColorBlue': '0',
    'ColorKhaki': '9',
    'ColorPurple': '11',
    'ColorGreen': '2',
    'ColorYellow': '5',
    'ColorWhite': '6',
    None: None
}

custom_color_indexes = {v:k for k,v in custom_colors_numbers.items()}

# need to produce:
# Quantity -> StackSize done
# ParentSlotId -> SlotId done
# Figure out color numbers -> CustomColor done
# Children -> Contents
# type can be ignored
# contents needs to be generated
# ? -> Species


def to_InventoryData(item: ThingSaveData, child_dict: dict) -> InventoryData:
    result_data = dict()

    for field in InventoryData._fields:
        result_data[field] = None

    tsd_dict = item._asdict()
    result_data.update(tsd_dict)

    overrides = {
        'StackSize': item.Quantity if item.xsi_type == "StackableSaveData" else None,
        'SlotId': item.ParentSlotId,
        'CustomColor': custom_color_indexes.get(item.CustomColorIndex) if item.CustomColorIndex != '-1' else None
    }

    result_data.update(overrides)

    children = child_dict.get(item.ReferenceId)
    if children is not None:
        child_list = [to_InventoryData(_, child_dict) for _ in children]
        result_data['Contents'] = child_list

    final_result = {k: result_data[k] for k in InventoryData._fields}

    return InventoryData(**final_result)
