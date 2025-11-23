'''
#   PURPOSE OF THIS FILE
    >>> RETURN A DICTIONARY OF GEOGRAPHY INFORMATION FROM THE CIA WORLD FACTBOOK
'''


#######################################################################################################################

######################################################################################################################
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import json
import os
# get_government ------------------------------------------------------------------------------------------------------
from proj_004_cia.c_05_government.helper.get_government import get_government
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   CORE FUNCTION
# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------


def return_government_data(
    data: dict,
    iso3Code: str
):

    # 5. GOVERNMENT
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------------------------
    # Initialize the dictionary to hold geography data
    cia_pack = {}

    # Conditional inclusion based on iso3Code
    if iso3Code != 'WLD':
        # Note: 'admin_divisions'
        cia_pack['admin_divisions'] = get_government(
            data=data, info='admin_divisions', iso3Code=iso3Code)
        # Note: 'capital'
        cia_pack['capital'] = get_government(
            data=data, info='capital', iso3Code=iso3Code)
        # Note: 'citizenship'
        cia_pack['citizenship'] = get_government(
            data=data, info='citizenship', iso3Code=iso3Code)
        # Note: 'constitution'
        cia_pack['constitution'] = get_government(
            data=data, info='constitution', iso3Code=iso3Code)
        # Note: 'country_name'
        cia_pack['country_name'] = get_government(
            data=data, info='country_name', iso3Code=iso3Code)
        # Note: 'dependency_status'
        cia_pack['dependency_status'] = get_government(
            data=data, info='dependency_status', iso3Code=iso3Code)
        # Note: 'dependency_areas'
        cia_pack['dependency_areas'] = get_government(
            data=data, info='dependency_areas', iso3Code=iso3Code)
        # Note: 'diplomatic_representation_from_us'
        cia_pack['diplomatic_representation_from_us'] = get_government(
            data=data, info='diplomatic_representation_from_us', iso3Code=iso3Code)
        # Note: 'diplomatic_representation_in_us'
        cia_pack['diplomatic_representation_in_us'] = get_government(
            data=data, info='diplomatic_representation_in_us', iso3Code=iso3Code)
        # Note: 'executive_branch'
        cia_pack['executive_branch'] = get_government(
            data=data, info='executive_branch', iso3Code=iso3Code)
        # Note: 'flag_description'
        cia_pack['flag_description'] = get_government(
            data=data, info='flag_description', iso3Code=iso3Code)
        # Note: 'government_note'
        cia_pack['government_note'] = get_government(
            data=data, info='government_note', iso3Code=iso3Code)
        # Note: 'government_type'
        cia_pack['government_type'] = get_government(
            data=data, info='government_type', iso3Code=iso3Code)
        # Note: 'independence'
        cia_pack['independence'] = get_government(
            data=data, info='independence', iso3Code=iso3Code)
        # Note: 'international_law_org_participation'
        cia_pack['international_law_org_participation'] = get_government(
            data=data, info='international_law_org_participation', iso3Code=iso3Code)
        # Note: 'international_org_participation'
        cia_pack['international_org_participation'] = get_government(
            data=data, info='international_org_participation', iso3Code=iso3Code)
        # Note: 'judicial_branch'
        cia_pack['judicial_branch'] = get_government(
            data=data, info='judicial_branch', iso3Code=iso3Code)
        # Note: 'legal_system'
        cia_pack['legal_system'] = get_government(
            data=data, info='legal_system', iso3Code=iso3Code)
        # Note: 'legislative_branch'
        cia_pack['legislative_branch'] = get_government(
            data=data, info='legislative_branch', iso3Code=iso3Code)
        # Note: 'member_states'
        cia_pack['member_states'] = get_government(
            data=data, info='member_states', iso3Code=iso3Code)
        # Note: 'national_anthem'
        cia_pack['national_anthem'] = get_government(
            data=data, info='national_anthem', iso3Code=iso3Code)
        # Note: 'national_heritage'
        cia_pack['national_heritage'] = get_government(
            data=data, info='national_heritage', iso3Code=iso3Code)
        # Note: 'national_holiday'
        cia_pack['national_holiday'] = get_government(
            data=data, info='national_holiday', iso3Code=iso3Code)
        # Note: 'national_symbols'
        cia_pack['national_symbols'] = get_government(
            data=data, info='national_symbols', iso3Code=iso3Code)
        # Note: 'political_parties'
        cia_pack['political_parties'] = get_government(
            data=data, info='political_parties', iso3Code=iso3Code)
        # Note: 'political_structure'
        cia_pack['political_structure'] = get_government(
            data=data, info='political_structure', iso3Code=iso3Code)
        # Note: 'suffrage'
        cia_pack['suffrage'] = get_government(
            data=data, info='suffrage', iso3Code=iso3Code)
        # Note: 'union_name'
        cia_pack['union_name'] = get_government(
            data=data, info='union_name', iso3Code=iso3Code)
    else:
        # Note: ''
        pass

    # Return the compiled geography data
    return cia_pack


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   TEST FUNCTION
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    country = False
    # ----------------------------------------------------------------------------------------------------------------------------------
    json_folder = f'C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia/_raw_data'
    if country:
        region_folder = f'north-america'
        cia_code = 'us'
    else:
        region_folder = f'world'
        cia_code = 'xx'
    file_path = os.path.join(json_folder, region_folder, f'{cia_code}.json')
    # --------------------------------------------------------------------------------------------------
    with open(file_path, 'r', encoding='utf-8') as country_file:
        data = json.load(country_file)
    # --------------------------------------------------------------------------------------------------
    if country:
        iso3Code = 'USA'
    else:
        iso3Code = 'WLD'
    # ------------------------------------------------------------------------------------------------------------------
    print(
        return_government_data(
            data=data,
            iso3Code=iso3Code
        )
    )
