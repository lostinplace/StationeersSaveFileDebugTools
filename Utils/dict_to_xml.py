from collections import namedtuple
from xml.etree.ElementTree import Element,tostring


def namedtuple_to_xml(item: namedtuple):
    elem = Element(type(item).__name__)
    asdict = item._asdict().items()
    for key, val in asdict:
        if val is None:
            continue

        if type(val) is namedtuple:
            child = namedtuple_to_xml(val)
        elif type(val) is list:
            child = Element(key)
            for item in val:
                child.append(namedtuple_to_xml(item))
        else:
            child = Element(key)
            child.text = str(val)
        elem.append(child)

    return elem
