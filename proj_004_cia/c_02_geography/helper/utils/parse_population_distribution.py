import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_population_distribution(population_distribution_data: dict, iso3Code: str = None, return_original: bool = False)-> dict:
    """
    Parses the 'Population distribution' data for a country.

    Parameters:
        population_distribution_data (dict): The 'Population distribution' section from the data.

    Returns:
        dict: A dictionary containing parsed details of population distribution.
    """
    if return_original:
        return population_distribution_data

    result = {
        "distribution_areas": [],
        "population_distribution_note": ""
    }

    text = population_distribution_data.get("text", "")
    if not text:
        return result

    # Split the text into different chunks by semicolons
    distribution_chunks = [chunk.strip() for chunk in text.split(';')]

    # Add each chunk to the result
    result["distribution_areas"] = distribution_chunks

    # Check for the note key and clean it if present
    note = population_distribution_data.get("note", "")
    if note:
        result["population_distribution_note"] = clean_text(note)

    return result


# Example usage
if __name__ == "__main__":
    population_distribution_data = {
        "text": "large urban clusters are spread throughout the eastern half of the US (particularly the Great Lakes area, northeast, east, and southeast) and the western tier states; mountainous areas, principally the Rocky Mountains and Appalachian chain, deserts in the southwest, the dense boreal forests in the extreme north, and the central prarie states are less densely populated; Alaska's population is concentrated along its southern coast - with particular emphasis on the city of Anchorage - and Hawaii's is centered on the island of Oahu",
        "note": "some additional note about population distribution"
    }
    parsed_data = parse_population_distribution(population_distribution_data)
    print(parsed_data)
