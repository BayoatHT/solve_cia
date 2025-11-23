import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_economic_overview(pass_data: dict, iso3Code: str = None) -> dict:
    """

    """
    result = ""

    # Clean the text value and store it in the result dictionary
    result = clean_text(pass_data.get("text", ""))

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 10 >>> 'Economic overview'
    # --------------------------------------------------------------------------------------------------
    # "note" - 'economic_overview_note'
    # "text" - 'economic_overview'
    # --------------------------------------------------------------------------------------------------
    # ['economic_overview', 'economic_overview_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "Western Sahara has a small market-based economy whose main industries are fishing, phosphate mining, tourism, and pastoral nomadism. The territory's arid desert climate makes sedentary agriculture difficult, and much of its food is imported. The Moroccan Government administers Western Sahara's economy and is a key source of employment, infrastructure development, and social spending in the territory. ++ Western Sahara's unresolved legal status makes the exploitation of its natural resources a contentious issue between Morocco and the Polisario. Morocco and the EU in December 2013 finalized a four-year agreement allowing European vessels to fish off the coast of Morocco, including disputed waters off the coast of Western Sahara. As of April 2018, Moroccan and EU authorities were negotiating an amendment to renew the agreement. ++ Oil has never been found in Western Sahara in commercially significant quantities, but Morocco and the Polisario have quarreled over rights to authorize and benefit from oil exploration in the territory. Western Sahara's main long-term economic challenge is the development of a more diverse set of industries capable of providing greater employment and income to the territory. However, following King MOHAMMED VI's November 2015 visit to Western Sahara, the Government of Morocco announced a series of investments aimed at spurring economic activity in the region, while the General Confederation of Moroccan Enterprises announced a $609 million investment initiative in the region in March 2015."
    }
    parsed_data = parse_economic_overview(pass_data)
    print(parsed_data)
