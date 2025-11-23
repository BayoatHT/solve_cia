import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_tele_systems(tele_systems_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # ['telecom_domestic', 'telecom_general_assessment', 'telecom_international', 'telecom_note', 'telecom_overseas_departments']
    tele_systems_data = {
        "general assessment": {
            "text": "the US telecom sector adapted well to the particular demands of the pandemic, which has led to strong growth in the number of mobile, mobile broadband, and fixed broadband subscribers since 2020; the level of growth is expected to taper off from late 2022 as the demand for working and schooling from home subsides; the pandemic also encouraged the Federal government to increase its investment in broadband infrastructure; of particular note was the Infrastructure Investment and Jobs Act of November 2021, which provided $65 billion to a range of programs aimed at delivering broadband to unserved areas, providing fiber-based broadband to upgrade existing service areas, and subsidizing the cost of services to low income households; alongside these fiscal efforts have been the several spectrum auctions undertaken during the last two years, which have greatly assisted the main licensees to improve the reach and quality of their offers based on LTE and 5G; some of this spectrum, auctioned during 2021, was only made available to licensees from February 2022; the widening availability of 5G from the main providers has resulted in a dramatic increase in mobile data traffic; in tandem with the focus on 5G, operators have closed down their GSM and CDMA networks, and have either closed down 3G networks (as AT&amp;T did in January 2022), or plan to in coming months; given the size of the US broadband market, and the growing demand for data on both fixed and mobile networks, there is continuous pressure for operators to invest in fiber networks, and to push connectivity closer to consumers; in recent years the US has seen increased activity from regional players as well as the major telcos and cablecos; although there has been considerable investment in DOCSIS4.0, some of the cablecos are looking to ditch HFC in preference for fiber broadband; the process of migrating from copper (HFC and DSL) to fiber is ongoing, but given the scale of the work involved it will take some years; some operators have investment strategies in place through to 2025, which will see the vast majority of their fixed networks being entirely on fiber; service offerings of up to 2Gb/s are becoming more widely available as the process continues (2024)"
        },
        "domestic": {
            "text": "fixed-line just over 27 per 100 and mobile-cellular is 110 per 100 (2022)"
        },
        "international": {
            "text": "country code - 1; landing points for the Quintillion Subsea Cable Network, TERRA SW, AU-Aleutian, KKFL, AKORN, Alaska United -West, &amp; -East &amp; -Southeast, North Star, Lynn Canal Fiber, KetchCar 1, PC-1, SCCN, Tat TGN-Pacific &amp; -Atlantic, Jupiter, Hawaiki, NCP, FASTER, HKA, JUS, AAG, BtoBE, Currie, Southern Cross NEXT, SxS, PLCN, Utility EAC-Pacific, SEA-US, Paniolo Cable Network, HICS, HIFN, ASH, Telstra Endeavor, Honotua, AURORA, ARCOS, AMX-1, Americas -I &amp;&nbsp;-II, Columbus IIb &amp; -III, Maya-1, MAC, GTMO-1, BICS, CFX-1, GlobeNet, Monet, SAm-1, Bahamas 2, PCCS, BRUSA, Dunant, MAREA, SAE x1,&nbsp;TAT 14,&nbsp;Apollo, Gemini Bermuda, Havfrue/AEC-2, Seabras-1,&nbsp;WALL-LI, NYNJ-1, FLAG Atalantic-1, Yellow, Atlantic Crossing-1,&nbsp;AE Connect -1, sea2shore, Challenger Bermuda-1, and&nbsp;GTT Atlantic&nbsp;submarine cable systems providing international connectivity to Europe, Africa,&nbsp;the Middle East, Asia, Southeast Asia, Australia,&nbsp;New Zealand, Pacific, &amp;&nbsp;Atlantic, and Indian Ocean&nbsp;Islands, Central and South America, Caribbean, Canada&nbsp;and US; satellite earth stations - 61 Intelsat (45 Atlantic Ocean and 16 Pacific Ocean), 5 Intersputnik (Atlantic Ocean region), and 4 Inmarsat (Pacific and Atlantic Ocean regions) (2020)"
        },
        "note": "note: the COVID-19 outbreak is negatively impacting telecommunications production and supply chains globally; consumer spending on telecom devices and services has also slowed due to the pandemic's effect on economies worldwide; overall progress towards improvements in all facets of the telecom industry - mobile, fixed-line, broadband, submarine cable and satellite - has moderated"
    }
    parsed_data = parse_tele_systems(tele_systems_data)
    print(parsed_data)
