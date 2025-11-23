import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_roadways(roadways_data: dict, iso3Code: str = None) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # "Turkish Cypriot control" - 'turkish_roadways'
    # "non-urban" - 'non_urban_roadways'
    # "note" - 'roadways_note'
    # "paved" - 'paved_roadways'
    # "private and forest roads" - 'private_forest_roadways'
    # "total" - 'total_roadways'
    # "unpaved" - 'unpaved_roadways'
    # "urban" - 'urban_roadways'
    # --------------------------------------------------------------------------------------------------
    # ['turkish_roadways', 'non_urban_roadways', 'roadways_note', 'paved_roadways',
    # 'private_forest_roadways', 'total_roadways', 'unpaved_roadways', 'urban_roadways']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    roadways_data = {
        "total": {
            "text": "6,586,610 km"
        },
        "paved": {
            "text": "4,304,715 km (includes 76,334 km of expressways)"
        },
        "unpaved": {
            "text": "2,281,895 km (2012)"
        },
        "private and forest roads": {
            "text": "350,000 km (2012)"
        },
        "urban": {
            "text": "26,000 km (2012)"
        },
        "non urban": {
            "text": "26,000 km (2012)"
        },
        "Turkish Cypriot control": {
            "text": "7,000 km (2011)"
        }
    }
    parsed_data = parse_roadways(roadways_data)
    print(parsed_data)
