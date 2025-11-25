import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils.parse_text_to_list import parse_text_to_list
# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_argicultural_products_2(pass_data: dict, iso3Code: str = None, return_original: bool = False)-> dict:
    """
    Parses agricultural products data into a list.

    Parameters:
        pass_data (dict): The dictionary containing agricultural products data.

    Returns:
        dict: A dictionary with a key `agriculture_products` containing a list of parsed agricultural products.
    """
    if return_original:
        return pass_data

    result = {
        "agriculture_products": []
    }

    # Extract text and convert to a list of agricultural products
    text = pass_data.get("text", "")
    result["agriculture_products"] = parse_text_to_list(text)

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 2 >>> 'Agriculture - products'
    # --------------------------------------------------------------------------------------------------
    # text - 'agriculture_products'
    # --------------------------------------------------------------------------------------------------
    # ['agriculture_products']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "fruits and vegetables (grown in the few oases); camels, sheep, goats (kept by nomads); fish"
    }
    parsed_data = parse_argicultural_products_2(pass_data)
    print(parsed_data)
