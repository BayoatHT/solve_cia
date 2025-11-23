import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_exchange_rates(pass_data: dict, iso3Code: str = None) -> dict:
    """Parse exchange rates from CIA Economy section."""
    result = {}
    if not pass_data or not isinstance(pass_data, dict):
        return result
    try:
        if 'text' in pass_data:
            text = pass_data['text']
            if text and isinstance(text, str):
                result['exchange_rates'] = clean_text(text)
        if 'note' in pass_data:
            note = pass_data['note']
            if isinstance(note, str) and note.strip():
                result['exchange_rates_note'] = clean_text(note)
    except Exception as e:
        logging.error(f"Error parsing exchange_rates: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 11 >>> 'Exchange rates'
    # --------------------------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "<strong>British pounds per US dollar: </strong>0.805 (2023 est.), 0.811 (2022 est.), 0.727 (2021 est.), 0.780 (2020 est.), 0.783 (2019 est.)<br><strong>Canadian dollars per US dollar: </strong>1.35 (2023 est.), 1.302 (2022 est.), 1.254 (2021 est.), 1.341 (2020 est.), 1.327 (2019 est.)<br><strong>Chinese yuan per US dollar: </strong>7.084 (2023 est.), 6.737 (2022 est.), 6.449 (2021 est.), 6.901 (2020 est.), 6.908 (2019 est.)<br><strong>euros per US dollar: </strong>0.925 (2023 est.), 0.950 (2022 est.), 0.845 (2021 est.), 0.876 (2020 est.), 0.893 (2019 est.)<br><strong>Japanese yen per US dollar: </strong>140.49 (2023 est.), 131.50 (2022 est.), 109.75 (2021 est.), 106.78 (2020 est.), 109.01 (2019 est.)<br><br><strong>note 1: </strong>the following countries and territories use the US dollar officially as their legal tender: British Virgin Islands, Ecuador, El Salvador, Marshall Islands, Micronesia, Palau, Timor Leste, Turks and Caicos, and islands of the Caribbean Netherlands (Bonaire, Sint Eustatius, and Saba)<br><br><strong>note 2: </strong>the following countries and territories use the US dollar as official legal tender alongside local currency: Bahamas, Barbados, Belize, Costa Rica, and Panama<br><br><strong>note 3: </strong>the following countries and territories widely accept the US dollar as a dominant currency but have yet to declare it as legal tender: Bermuda, Burma, Cambodia, Cayman Islands, Honduras, Nicaragua, and Somalia"
    }
    parsed_data = parse_exchange_rates(pass_data)
    print(parsed_data)
