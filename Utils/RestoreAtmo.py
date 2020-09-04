from xml.etree.ElementTree import ElementTree as ET


def load_file(path: str) -> ET:
    tree = ET()
    tree.parse(path)
    return tree


def get_restored_atmosphere_data(current_file: ET, old_file: ET) -> ET:
    from .AtmoFileLoader import atmo_file_from_root
    from .AtmosphereDataRestoration import get_restored_data

    current_atmo_file = atmo_file_from_root(current_file.getroot())
    old_atmo_file = atmo_file_from_root(old_file.getroot())

    result = get_restored_data(current_atmo_file, old_atmo_file)

    current_tree = current_file

    rooms: ET = current_tree.find('.//Rooms')
    rooms.clear()
    for room in result.Rooms:
        rooms.append(room)

    atmospheres: ET = current_tree.find('.//Atmospheres')
    atmospheres.clear()
    for asd in result.Atmospheres:
        atmospheres.append(asd)

    return current_tree


def create_restored_world_file(current_file_path: str, old_file_path: str, output_path:str):
    current_tree: ET = load_file(current_file_path)
    old_tree: ET = load_file(old_file_path)

    result = get_restored_atmosphere_data(current_tree, old_tree)

    result.write(file_or_filename=output_path, encoding="utf-8", xml_declaration=True)



