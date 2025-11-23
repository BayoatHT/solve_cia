import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_climate(pass_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "Climate" - 'env_climate'
    # "note" - 'env_climate_note'
    # "ten coldest places on Earth (lowest average monthly temperature)" - 'env_climate_coldest'
    # "ten driest places on Earth (average annual precipitation)" - 'env_climate_driest'
    # "ten hottest places on Earth (highest average monthly temperature)" - 'env_climate_hottest'
    # "ten wettest places on Earth (average annual precipitation)" - 'env_climate_wettest'
    # --------------------------------------------------------------------------------------------------
    # ['env_climate', 'env_climate_note', 'env_climate_coldest',
    # 'env_climate_driest', 'env_climate_hottest', 'env_climate_wettest']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "mostly temperate, but tropical in Hawaii and Florida, arctic in Alaska, semiarid in the great plains west of the Mississippi River, and arid in the Great Basin of the southwest; low winter temperatures in the northwest are ameliorated occasionally in January and February by warm chinook winds from the eastern slopes of the Rocky Mountains",
        "note": "<strong>note:</strong> many consider Denali, the highest peak in the US, to be the world’s coldest mountain because of its combination of high elevation and its subarctic location at 63 degrees north latitude; permanent snow and ice cover over 75 percent of the mountain, and enormous glaciers, up to 45 miles long and 3,700 feet thick, spider out from its base in every direction; it is home to some of the world’s coldest and most violent weather, where winds of over 150 miles per hour and temperatures of -93˚F have been recorded.  "
    }
    parsed_data = parse_climate(pass_data)
    print(parsed_data)
