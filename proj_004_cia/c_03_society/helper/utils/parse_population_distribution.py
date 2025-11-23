import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_population_distribution(pop_distro_data: dict) -> dict:
    """

    """
    result = {}

    return result


# Example usage
if __name__ == "__main__":
    pop_distro_data = {
        "text": "large urban clusters are spread throughout the eastern half of the US (particularly the Great Lakes area, northeast, east, and southeast) and the western tier states; mountainous areas, principally the Rocky Mountains and Appalachian chain, deserts in the southwest, the dense boreal forests in the extreme north, and the central prarie states are less densely populated; Alaska's population is concentrated along its southern coast - with particular emphasis on the city of Anchorage - and Hawaii's is centered on the island of Oahu"
    }
    parsed_data = parse_population_distribution(pop_distro_data)
    print(parsed_data)
