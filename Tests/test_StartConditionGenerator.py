from Utils.StartConditionProcessing.startcondition_analyzers import analyze_start_condition_file, generate_schemas_for_worldfile_TSD, \
    diff_schemas, print_color_names_from_worldfile
from Utils.StartConditionProcessing.StartConditionGenerator import convert_world_file_to_startconditions
from Utils.world_file_loader import load_file


def test_load_world_file():
    current_data = convert_world_file_to_startconditions("""../Data/ConditionGenerator/world.xml""")


def test_analyze_start_condition_file():
    current_data = load_file("""../Data/ConditionGenerator/old_startconditions.xml""")
    analyze_start_condition_file(current_data)


def test_analyze_world_file_thing_save_data():
    current_data = load_file("""../Data/ConditionGenerator/world.xml""")

    generate_schemas_for_worldfile_TSD(current_data)


def test_analyze_and_compare_ID_to_TSD():
    current_data = load_file("""../Data/ConditionGenerator/world.xml""")
    current_ID_data = load_file("""../Data/ConditionGenerator/old_startconditions.xml""")

    diff_schemas(current_ID_data, current_data)


def test_get_custom_color_names():
    current_data = load_file("""../Data/ConditionGenerator/world.xml""")

    print_color_names_from_worldfile(current_data)


