from xml.etree.ElementTree import ElementTree as ET
from typing import Dict


def evaluate_expectations(tree:ET, expectations: Dict[str, str], test: str):
    for k in expectations:
        expected = expectations[k]
        result = tree.find(k)
        if test == expected or test == "both":
            assert result is not None
        else:
            assert result is None


def test_load_file():
    from Utils.AtmoFileProcessing.RestoreAtmo import get_restored_atmosphere_data, load_file

    current_data = load_file("""../Data/Lost-atmosphere/broken-world-0.xml""")
    old_data = load_file("""../Data/Lost-atmosphere/original-world.xml""")

    expectations = {
        ".//AtmosphereSaveData/NetworkReferenceId[.='577']/..": "old",
        ".//Room/RoomId[.='38']/..": "old",
        ".//AtmosphereSaveData/NetworkReferenceId[.='629']/..": "new",
        ".//Room/RoomId[.='580']/..": "new"
    }

    evaluate_expectations(current_data, expectations, "new")
    evaluate_expectations(old_data, expectations, "old")

    result = get_restored_atmosphere_data(current_data, old_data)
    evaluate_expectations(result, expectations, "both")


