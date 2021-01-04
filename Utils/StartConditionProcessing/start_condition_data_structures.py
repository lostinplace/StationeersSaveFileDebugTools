from collections import namedtuple

DynamicThingData = namedtuple('DynamicThingData', 'CustomColor CustomName Contents PrefabName')
InventoryData = namedtuple('InventoryData',
                           'Type Species UseMasterColor CustomColor StackSize Contents CustomName SlotId PrefabName')
