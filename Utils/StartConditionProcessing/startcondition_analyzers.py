from xml.etree.ElementTree import ElementTree as ET
from Utils.ThingSaveData import from_ET


def analyze_start_condition_file(current_data):
    DTD_schema = get_schema_for_element_type(current_data, "DynamicThingData")
    ID_schema = get_schema_for_element_type(current_data, "InventoryData")
    print(generate_namedtuple_entry(DTD_schema))
    print(generate_namedtuple_entry(ID_schema))


def generate_schemas_for_worldfile_TSD(current_data):
    TSD_schema = get_schema_for_element_type(current_data, "ThingSaveData")
    print(generate_namedtuple_entry(TSD_schema))


def diff_schemas(current_ID_data, current_data):
    TSD_schema = get_schema_for_element_type(current_data, "ThingSaveData")
    ID_schema = get_schema_for_element_type(current_ID_data, "InventoryData")
    out = ID_schema[1].difference(TSD_schema[1])
    pass


def print_color_names_from_worldfile(current_data):
    custom_names_and_colors = current_data.findall(""".//CustomName/../CustomColorIndex/..""")
    out = map(from_ET, custom_names_and_colors)
    out_list = list(out)
    result_items = [(_.CustomName, _.CustomColorIndex)
                    for _ in out_list
                    if _.CustomName is not None and _.CustomName.startswith("Color")]
    result = dict(result_items)
    print(result)
    pass


def get_schema_for_element_type(tree: ET, tag:str):
    from string import Template
    template = Template('.//$tag')
    query = template.substitute(tag=tag)

    elements = tree.findall(query)
    element_list = list(elements)

    prop_set = set()

    for item in element_list:
        props = item.findall("*")
        prop_names = set([_.tag for _ in props])
        prop_set = prop_set.union(prop_names)

    return (tag, prop_set)


def generate_namedtuple_entry(schema_result):
    from string import Template
    template_string = "$tag = namedtuple('$tag', '$props')"
    template = Template(template_string)

    result = template.substitute(tag=schema_result[0], props = ' '.join(schema_result[1]))
    return result