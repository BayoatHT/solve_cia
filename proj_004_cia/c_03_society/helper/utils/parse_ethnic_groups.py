import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_ethnic_groups(ethnic_data: dict) -> dict:
    """

    """
    result = {}

    return result


# Example usage
if __name__ == "__main__":
    ethnic_data = {
        "text": "White 61.6%, Black or African American 12.4%, Asian 6%, Indigenous and Alaska native 1.1%, Native Hawaiian and Other Pacific Islander 0.2%, other 8.4%, two or more races 10.2% (2020 est.)",
        "note": "<strong>note:</strong> a separate listing for Hispanic is not included because the US Census Bureau considers Hispanic to mean persons of Spanish/Hispanic/Latino origin including those of Mexican, Cuban, Puerto Rican, Dominican Republic, Spanish, and Central or South American origin living in the US who may be of any race or ethnic group (White, Black, Asian, etc.); an estimated 18.7% of the total US population is Hispanic as of 2020"
    }
    parsed_data = parse_ethnic_groups(ethnic_data)
    print(parsed_data)
