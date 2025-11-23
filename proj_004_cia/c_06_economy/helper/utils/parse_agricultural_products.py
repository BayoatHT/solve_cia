import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_agricultural_products(pass_data: dict, iso3Code: str = None) -> dict:
    """
    Parses agricultural products information, extracting date, products, and note (if available).

    Parameters:
        pass_data (dict): The dictionary containing agricultural products data.

    Returns:
        dict: Parsed agricultural products with keys `date`, `agricultural_products`, and `agricultural_products_note`.
    """
    result = {
        "agricultural_products": [],
        "date": "",
        "agricultural_products_note": ""
    }

    # Extract text for products and note, if available
    text = pass_data.get("text", "")
    note = pass_data.get("note", "")

    # Check if the text ends with a date in parentheses and extract it
    date_match = re.search(r"\((\d{4})\)$", text)
    if date_match:
        result["date"] = date_match.group(1)
        # Remove the date portion from the text
        text = text[:date_match.start()].strip()

    # Split the text by commas for agricultural products
    result["agricultural_products"] = [item.strip()
                                       for item in text.split(",")]

    # Clean the note text if present
    if note:
        result["agricultural_products_note"] = clean_text(note)

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 1 >>> 'Agricultural products'
    # --------------------------------------------------------------------------------------------------
    # "note" - 'agricultural_products_note'
    # "text" - 'agricultural_products'
    # --------------------------------------------------------------------------------------------------
    # ['agricultural_products', 'agricultural_products_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "maize, soybeans, milk, wheat, sugarcane, sugar beets, chicken, potatoes, beef, pork (2022)",
        "note": "<b>note:</b> top ten agricultural products based on tonnage"
    }
    parsed_data = parse_agricultural_products(pass_data)
    print(parsed_data)
