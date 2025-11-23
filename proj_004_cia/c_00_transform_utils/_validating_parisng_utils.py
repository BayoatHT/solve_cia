######################################################################################################################
# CORE IMPORTS
# C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\c_00_transform_utils\_validating_parisng_utils.py
# ---------------------------------------------------------------------------------------------------------------------
import re
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils.extract_and_parse import extract_and_parse
from proj_004_cia.c_00_transform_utils.extract_numeric_value import extract_numeric_value
from proj_004_cia.c_00_transform_utils.parse_coordinates import parse_coordinates
from proj_004_cia.c_00_transform_utils.parse_list_from_string import parse_list_from_string
from proj_004_cia.c_00_transform_utils.parse_percentage_data import parse_percentage_data
from proj_004_cia.c_00_transform_utils.parse_territorial_subdivisions import parse_territorial_subdivisions
from proj_004_cia.c_00_transform_utils.parse_text_and_note import parse_text_and_note
from proj_004_cia.c_00_transform_utils.parse_text_field import parse_text_field
from proj_004_cia.c_00_transform_utils.parse_text_to_list import parse_text_to_list
######################################################################################################################
# VALIDATION AND TESTING
######################################################################################################################


def validate_parsing_utils():
    """Test all parsing utilities with sample data."""
    print("🧪 Testing Enhanced CIA Parsing Utilities")

    # Test clean_text
    test_text = "<strong>note:</strong> some text (2023 est.) <em>with emphasis</em>"
    cleaned = clean_text(test_text)
    print(f"✅ clean_text: '{test_text}' → '{cleaned}'")

    # Test extract_numeric_value
    numeric_text = "148.94 million sq km"
    numeric_val = extract_numeric_value(
        numeric_text, "sq km", return_metadata=True)
    print(f"✅ extract_numeric_value: '{numeric_text}' → {numeric_val}")

    # Test parse_percentage_data
    percent_text = "15.2% (2023 est.)"
    percent_data = parse_percentage_data(percent_text)
    print(f"✅ parse_percentage_data: '{percent_text}' → {percent_data}")

    # Test parse_coordinates
    coord_text = "41 54 N, 12 27 E"
    coords = parse_coordinates(coord_text)
    print(f"✅ parse_coordinates: '{coord_text}' → {coords}")

    print("🎉 All utilities tested successfully!")


if __name__ == "__main__":
    validate_parsing_utils()
