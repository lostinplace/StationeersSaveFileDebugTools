from xml.etree.ElementTree import ElementTree as ET, register_namespace

register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")


def load_file(path: str) -> ET:
    tree = ET()
    tree.parse(path)
    return tree