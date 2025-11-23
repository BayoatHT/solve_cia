import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils.parse_text_to_list import parse_text_to_list
# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_illicit_drugs(drugs_data: dict, iso3Code: str = None) -> dict:
    """
    Parses data related to illicit drugs.

    Parameters:
        drugs_data (dict): The dictionary containing illicit drug information.

    Returns:
        dict: A dictionary containing parsed illicit drug information.
    """
    result = {
        "illicit_drugs": []
    }

    drugs_text = drugs_data.get("text", "")
    if drugs_text:
        result["illicit_drugs"] = parse_text_to_list(drugs_text)

    return result


# Example usage
if __name__ == "__main__":
    # 2 >>> 'Illicit drugs'
    # >>> ['illicit_drugs']
    # ------------------------------------------------------------------------------------------------------------
    drugs_data = {
        "text": "<p>world's largest consumer of cocaine (shipped from Colombia through Mexico and the Caribbean), Colombian heroin, and Mexican heroin and marijuana; major consumer of ecstasy and Mexican methamphetamine; minor consumer of high-quality Southeast Asian heroin; illicit producer of cannabis, marijuana, depressants, stimulants, hallucinogens, and methamphetamine; money-laundering center</p>"
    }
    parsed_data = parse_illicit_drugs(drugs_data)
    print(parsed_data)
