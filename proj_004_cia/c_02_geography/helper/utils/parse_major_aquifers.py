import logging
import re

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_major_aquifers(aquifers_data: dict, iso3Code: str = None, return_original: bool = False)-> dict:
    """
    Parses the 'Major aquifers' data for a country.

    Parameters:
        aquifers_data (dict): The 'Major aquifers' section from the data.

    Returns:
        dict: A dictionary containing a list of major aquifers.
    """
    if return_original:
        return aquifers_data

    result = []

    # Extract the text from aquifers_data
    text = aquifers_data.get("text", "")
    if text:
        # Split by commas and strip whitespace
        aquifers_list = [aquifer.strip() for aquifer in text.split(",")]
        result = aquifers_list
    else:
        result = []

    return result


def parse_wld_major_aquifers(aquifers_data: dict, iso3Code: str = None, return_original: bool = False)-> dict:
    """
    Parses the 'Major aquifers' data for the world ('WLD') specifically.

    Parameters:
        aquifers_data (dict): The 'Major aquifers' section from the data.

    Returns:
        dict: A dictionary containing parsed details of major aquifers.
    """
    if return_original:
        return aquifers_data

    result = {
        "description": "",
        "major_aquifers_info": {
            "listed_count": 0,
            "countries_covered": 0,
            "distribution_by_continent": {}
        },
        "importance": {
            "freshwater_percentage": "",
            "uses": {}
        }
    }

    text = aquifers_data.get("text", "")
    if not text:
        return result

    # Extract the description part before "The World Factbook" section
    description_match = re.search(
        r'(.*?)(?=<em>The World Factbook)', text, re.DOTALL)
    if description_match:
        result["description"] = description_match.group(1).strip()

    # Extract the major aquifers information
    listed_count_match = re.search(
        r'lists (\d+) major aquifers across (\d+) countries', text)
    if listed_count_match:
        result["major_aquifers_info"]["listed_count"] = int(
            listed_count_match.group(1))
        result["major_aquifers_info"]["countries_covered"] = int(
            listed_count_match.group(2))

    # Extract distribution by continent information
    distribution_matches = re.findall(r'(\w+) - (\d+)', text)
    for continent, count in distribution_matches:
        result["major_aquifers_info"]["distribution_by_continent"][continent] = int(
            count)

    # Extract importance details
    freshwater_match = re.search(
        r'the major aquifers .*? represent more than (\d+%) of the world\'s fresh water', text)
    if freshwater_match:
        result["importance"]["freshwater_percentage"] = freshwater_match.group(
            1)

    # Extract uses information
    uses_match = re.search(
        r'globally, (\d+%) of groundwater withdrawn is used for agriculture', text)
    if uses_match:
        result["importance"]["uses"][
            "global_agriculture"] = f"{uses_match.group(1)} of groundwater is used for agriculture"

    drinking_water_match = re.search(
        r'groundwater also supplies almost half of all drinking water worldwide', text)
    if drinking_water_match:
        result["importance"]["uses"]["drinking_water_supply"] = "Almost half of all drinking water worldwide"

    irrigation_match = re.search(
        r'groundwater is primarily used for irrigation', text)
    if irrigation_match:
        result["importance"]["uses"]["irrigation"] = "Primary use in the US is for irrigation"

    return result


# Example usage
if __name__ == "__main__":
    aquifers_data = {
        "text": "Northern Great Plains Aquifer, Cambrian-Ordovician Aquifer System, Californian Central Valley Aquifer System, Ogallala Aquifer (High Plains), Atlantic and Gulf Coastal Plains Aquifer"
    }
    parsed_data = parse_major_aquifers(aquifers_data)
    print(parsed_data)
