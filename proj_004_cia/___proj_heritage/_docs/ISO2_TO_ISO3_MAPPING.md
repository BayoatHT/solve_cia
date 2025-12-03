# ISO2 to ISO3 Country Code Mapping

## Complete Mapping for World Heritage Sites

This document contains the complete mapping of all 170 ISO2 country codes found in the World Heritage dataset to their corresponding ISO3 codes.

---

## ISO2 → ISO3 Mapping Dictionary

```python
ISO2_TO_ISO3 = {
    'AD': 'AND',  # Andorra
    'AE': 'ARE',  # United Arab Emirates
    'AF': 'AFG',  # Afghanistan
    'AG': 'ATG',  # Antigua and Barbuda
    'AL': 'ALB',  # Albania
    'AM': 'ARM',  # Armenia
    'AO': 'AGO',  # Angola
    'AR': 'ARG',  # Argentina
    'AT': 'AUT',  # Austria
    'AU': 'AUS',  # Australia
    'AZ': 'AZE',  # Azerbaijan
    'BA': 'BIH',  # Bosnia and Herzegovina
    'BB': 'BRB',  # Barbados
    'BD': 'BGD',  # Bangladesh
    'BE': 'BEL',  # Belgium
    'BF': 'BFA',  # Burkina Faso
    'BG': 'BGR',  # Bulgaria
    'BH': 'BHR',  # Bahrain
    'BJ': 'BEN',  # Benin
    'BO': 'BOL',  # Bolivia
    'BR': 'BRA',  # Brazil
    'BW': 'BWA',  # Botswana
    'BY': 'BLR',  # Belarus
    'BZ': 'BLZ',  # Belize
    'CA': 'CAN',  # Canada
    'CD': 'COD',  # Democratic Republic of the Congo
    'CF': 'CAF',  # Central African Republic
    'CG': 'COG',  # Congo
    'CH': 'CHE',  # Switzerland
    'CI': 'CIV',  # Côte d'Ivoire
    'CL': 'CHL',  # Chile
    'CM': 'CMR',  # Cameroon
    'CN': 'CHN',  # China
    'CO': 'COL',  # Colombia
    'CR': 'CRI',  # Costa Rica
    'CU': 'CUB',  # Cuba
    'CV': 'CPV',  # Cabo Verde
    'CY': 'CYP',  # Cyprus
    'CZ': 'CZE',  # Czechia
    'DE': 'DEU',  # Germany
    'DK': 'DNK',  # Denmark
    'DM': 'DMA',  # Dominica
    'DO': 'DOM',  # Dominican Republic
    'DZ': 'DZA',  # Algeria
    'EC': 'ECU',  # Ecuador
    'EE': 'EST',  # Estonia
    'EG': 'EGY',  # Egypt
    'ER': 'ERI',  # Eritrea
    'ES': 'ESP',  # Spain
    'ET': 'ETH',  # Ethiopia
    'FI': 'FIN',  # Finland
    'FJ': 'FJI',  # Fiji
    'FM': 'FSM',  # Micronesia
    'FR': 'FRA',  # France
    'GA': 'GAB',  # Gabon
    'GB': 'GBR',  # United Kingdom
    'GE': 'GEO',  # Georgia
    'GH': 'GHA',  # Ghana
    'GM': 'GMB',  # Gambia
    'GN': 'GIN',  # Guinea
    'GR': 'GRC',  # Greece
    'GT': 'GTM',  # Guatemala
    'GW': 'GNB',  # Guinea-Bissau
    'HN': 'HND',  # Honduras
    'HR': 'HRV',  # Croatia
    'HT': 'HTI',  # Haiti
    'HU': 'HUN',  # Hungary
    'ID': 'IDN',  # Indonesia
    'IE': 'IRL',  # Ireland
    'IL': 'ISR',  # Israel
    'IN': 'IND',  # India
    'IQ': 'IRQ',  # Iraq
    'IR': 'IRN',  # Iran
    'IS': 'ISL',  # Iceland
    'IT': 'ITA',  # Italy
    'JM': 'JAM',  # Jamaica
    'JO': 'JOR',  # Jordan
    'JP': 'JPN',  # Japan
    'KE': 'KEN',  # Kenya
    'KG': 'KGZ',  # Kyrgyzstan
    'KH': 'KHM',  # Cambodia
    'KI': 'KIR',  # Kiribati
    'KN': 'KNA',  # Saint Kitts and Nevis
    'KP': 'PRK',  # North Korea
    'KR': 'KOR',  # South Korea
    'KZ': 'KAZ',  # Kazakhstan
    'LA': 'LAO',  # Laos
    'LB': 'LBN',  # Lebanon
    'LC': 'LCA',  # Saint Lucia
    'LK': 'LKA',  # Sri Lanka
    'LS': 'LSO',  # Lesotho
    'LT': 'LTU',  # Lithuania
    'LU': 'LUX',  # Luxembourg
    'LV': 'LVA',  # Latvia
    'LY': 'LBY',  # Libya
    'MA': 'MAR',  # Morocco
    'MD': 'MDA',  # Moldova
    'ME': 'MNE',  # Montenegro
    'MG': 'MDG',  # Madagascar
    'MH': 'MHL',  # Marshall Islands
    'MK': 'MKD',  # North Macedonia
    'ML': 'MLI',  # Mali
    'MM': 'MMR',  # Myanmar
    'MN': 'MNG',  # Mongolia
    'MR': 'MRT',  # Mauritania
    'MT': 'MLT',  # Malta
    'MU': 'MUS',  # Mauritius
    'MW': 'MWI',  # Malawi
    'MX': 'MEX',  # Mexico
    'MY': 'MYS',  # Malaysia
    'MZ': 'MOZ',  # Mozambique
    'NA': 'NAM',  # Namibia
    'NE': 'NER',  # Niger
    'NG': 'NGA',  # Nigeria
    'NI': 'NIC',  # Nicaragua
    'NL': 'NLD',  # Netherlands
    'NO': 'NOR',  # Norway
    'NP': 'NPL',  # Nepal
    'NZ': 'NZL',  # New Zealand
    'OM': 'OMN',  # Oman
    'PA': 'PAN',  # Panama
    'PE': 'PER',  # Peru
    'PG': 'PNG',  # Papua New Guinea
    'PH': 'PHL',  # Philippines
    'PK': 'PAK',  # Pakistan
    'PL': 'POL',  # Poland
    'PS': 'PSE',  # Palestine
    'PT': 'PRT',  # Portugal
    'PW': 'PLW',  # Palau
    'PY': 'PRY',  # Paraguay
    'QA': 'QAT',  # Qatar
    'RO': 'ROU',  # Romania
    'RS': 'SRB',  # Serbia
    'RU': 'RUS',  # Russia
    'RW': 'RWA',  # Rwanda
    'SA': 'SAU',  # Saudi Arabia
    'SB': 'SLB',  # Solomon Islands
    'SC': 'SYC',  # Seychelles
    'SD': 'SDN',  # Sudan
    'SE': 'SWE',  # Sweden
    'SG': 'SGP',  # Singapore
    'SI': 'SVN',  # Slovenia
    'SK': 'SVK',  # Slovakia
    'SL': 'SLE',  # Sierra Leone
    'SM': 'SMR',  # San Marino
    'SN': 'SEN',  # Senegal
    'SR': 'SUR',  # Suriname
    'SV': 'SLV',  # El Salvador
    'SY': 'SYR',  # Syria
    'TD': 'TCD',  # Chad
    'TG': 'TGO',  # Togo
    'TH': 'THA',  # Thailand
    'TJ': 'TJK',  # Tajikistan
    'TM': 'TKM',  # Turkmenistan
    'TN': 'TUN',  # Tunisia
    'TR': 'TUR',  # Turkey
    'TZ': 'TZA',  # Tanzania
    'UA': 'UKR',  # Ukraine
    'UG': 'UGA',  # Uganda
    'US': 'USA',  # United States
    'UY': 'URY',  # Uruguay
    'UZ': 'UZB',  # Uzbekistan
    'VA': 'VAT',  # Vatican City
    'VE': 'VEN',  # Venezuela
    'VN': 'VNM',  # Vietnam
    'VU': 'VUT',  # Vanuatu
    'YE': 'YEM',  # Yemen
    'ZA': 'ZAF',  # South Africa
    'ZM': 'ZMB',  # Zambia
    'ZW': 'ZWE',  # Zimbabwe
}
```

---

## Reverse Mapping (ISO3 → ISO2)

```python
ISO3_TO_ISO2 = {
    'AFG': 'AF',  # Afghanistan
    'AGO': 'AO',  # Angola
    'ALB': 'AL',  # Albania
    'AND': 'AD',  # Andorra
    'ARE': 'AE',  # United Arab Emirates
    'ARG': 'AR',  # Argentina
    'ARM': 'AM',  # Armenia
    'ATG': 'AG',  # Antigua and Barbuda
    'AUS': 'AU',  # Australia
    'AUT': 'AT',  # Austria
    'AZE': 'AZ',  # Azerbaijan
    'BDI': 'BI',  # Burundi (not in dataset, included for completeness)
    'BEL': 'BE',  # Belgium
    'BEN': 'BJ',  # Benin
    'BFA': 'BF',  # Burkina Faso
    'BGD': 'BD',  # Bangladesh
    'BGR': 'BG',  # Bulgaria
    'BHR': 'BH',  # Bahrain
    'BIH': 'BA',  # Bosnia and Herzegovina
    'BLR': 'BY',  # Belarus
    'BLZ': 'BZ',  # Belize
    'BOL': 'BO',  # Bolivia
    'BRA': 'BR',  # Brazil
    'BRB': 'BB',  # Barbados
    'BWA': 'BW',  # Botswana
    'CAF': 'CF',  # Central African Republic
    'CAN': 'CA',  # Canada
    'CHE': 'CH',  # Switzerland
    'CHL': 'CL',  # Chile
    'CHN': 'CN',  # China
    'CIV': 'CI',  # Côte d'Ivoire
    'CMR': 'CM',  # Cameroon
    'COD': 'CD',  # Democratic Republic of the Congo
    'COG': 'CG',  # Congo
    'COL': 'CO',  # Colombia
    'CPV': 'CV',  # Cabo Verde
    'CRI': 'CR',  # Costa Rica
    'CUB': 'CU',  # Cuba
    'CYP': 'CY',  # Cyprus
    'CZE': 'CZ',  # Czechia
    'DEU': 'DE',  # Germany
    'DMA': 'DM',  # Dominica
    'DNK': 'DK',  # Denmark
    'DOM': 'DO',  # Dominican Republic
    'DZA': 'DZ',  # Algeria
    'ECU': 'EC',  # Ecuador
    'EGY': 'EG',  # Egypt
    'ERI': 'ER',  # Eritrea
    'ESP': 'ES',  # Spain
    'EST': 'EE',  # Estonia
    'ETH': 'ET',  # Ethiopia
    'FIN': 'FI',  # Finland
    'FJI': 'FJ',  # Fiji
    'FRA': 'FR',  # France
    'FSM': 'FM',  # Micronesia
    'GAB': 'GA',  # Gabon
    'GBR': 'GB',  # United Kingdom
    'GEO': 'GE',  # Georgia
    'GHA': 'GH',  # Ghana
    'GIN': 'GN',  # Guinea
    'GMB': 'GM',  # Gambia
    'GNB': 'GW',  # Guinea-Bissau
    'GRC': 'GR',  # Greece
    'GTM': 'GT',  # Guatemala
    'HND': 'HN',  # Honduras
    'HRV': 'HR',  # Croatia
    'HTI': 'HT',  # Haiti
    'HUN': 'HU',  # Hungary
    'IDN': 'ID',  # Indonesia
    'IND': 'IN',  # India
    'IRL': 'IE',  # Ireland
    'IRN': 'IR',  # Iran
    'IRQ': 'IQ',  # Iraq
    'ISL': 'IS',  # Iceland
    'ISR': 'IL',  # Israel
    'ITA': 'IT',  # Italy
    'JAM': 'JM',  # Jamaica
    'JOR': 'JO',  # Jordan
    'JPN': 'JP',  # Japan
    'KAZ': 'KZ',  # Kazakhstan
    'KEN': 'KE',  # Kenya
    'KGZ': 'KG',  # Kyrgyzstan
    'KHM': 'KH',  # Cambodia
    'KIR': 'KI',  # Kiribati
    'KNA': 'KN',  # Saint Kitts and Nevis
    'KOR': 'KR',  # South Korea
    'LAO': 'LA',  # Laos
    'LBN': 'LB',  # Lebanon
    'LBY': 'LY',  # Libya
    'LCA': 'LC',  # Saint Lucia
    'LKA': 'LK',  # Sri Lanka
    'LSO': 'LS',  # Lesotho
    'LTU': 'LT',  # Lithuania
    'LUX': 'LU',  # Luxembourg
    'LVA': 'LV',  # Latvia
    'MAR': 'MA',  # Morocco
    'MDA': 'MD',  # Moldova
    'MDG': 'MG',  # Madagascar
    'MEX': 'MX',  # Mexico
    'MHL': 'MH',  # Marshall Islands
    'MKD': 'MK',  # North Macedonia
    'MLI': 'ML',  # Mali
    'MLT': 'MT',  # Malta
    'MMR': 'MM',  # Myanmar
    'MNE': 'ME',  # Montenegro
    'MNG': 'MN',  # Mongolia
    'MOZ': 'MZ',  # Mozambique
    'MRT': 'MR',  # Mauritania
    'MUS': 'MU',  # Mauritius
    'MWI': 'MW',  # Malawi
    'MYS': 'MY',  # Malaysia
    'NAM': 'NA',  # Namibia
    'NER': 'NE',  # Niger
    'NGA': 'NG',  # Nigeria
    'NIC': 'NI',  # Nicaragua
    'NLD': 'NL',  # Netherlands
    'NOR': 'NO',  # Norway
    'NPL': 'NP',  # Nepal
    'NZL': 'NZ',  # New Zealand
    'OMN': 'OM',  # Oman
    'PAK': 'PK',  # Pakistan
    'PAN': 'PA',  # Panama
    'PER': 'PE',  # Peru
    'PHL': 'PH',  # Philippines
    'PLW': 'PW',  # Palau
    'PNG': 'PG',  # Papua New Guinea
    'POL': 'PL',  # Poland
    'PRK': 'KP',  # North Korea
    'PRT': 'PT',  # Portugal
    'PRY': 'PY',  # Paraguay
    'PSE': 'PS',  # Palestine
    'QAT': 'QA',  # Qatar
    'ROU': 'RO',  # Romania
    'RUS': 'RU',  # Russia
    'RWA': 'RW',  # Rwanda
    'SAU': 'SA',  # Saudi Arabia
    'SDN': 'SD',  # Sudan
    'SEN': 'SN',  # Senegal
    'SGP': 'SG',  # Singapore
    'SLB': 'SB',  # Solomon Islands
    'SLE': 'SL',  # Sierra Leone
    'SLV': 'SV',  # El Salvador
    'SMR': 'SM',  # San Marino
    'SRB': 'RS',  # Serbia
    'SUR': 'SR',  # Suriname
    'SVK': 'SK',  # Slovakia
    'SVN': 'SI',  # Slovenia
    'SWE': 'SE',  # Sweden
    'SYC': 'SC',  # Seychelles
    'SYR': 'SY',  # Syria
    'TCD': 'TD',  # Chad
    'TGO': 'TG',  # Togo
    'THA': 'TH',  # Thailand
    'TJK': 'TJ',  # Tajikistan
    'TKM': 'TM',  # Turkmenistan
    'TUN': 'TN',  # Tunisia
    'TUR': 'TR',  # Turkey
    'TZA': 'TZ',  # Tanzania
    'UGA': 'UG',  # Uganda
    'UKR': 'UA',  # Ukraine
    'URY': 'UY',  # Uruguay
    'USA': 'US',  # United States
    'UZB': 'UZ',  # Uzbekistan
    'VAT': 'VA',  # Vatican City
    'VEN': 'VE',  # Venezuela
    'VNM': 'VN',  # Vietnam
    'VUT': 'VU',  # Vanuatu
    'YEM': 'YE',  # Yemen
    'ZAF': 'ZA',  # South Africa
    'ZMB': 'ZM',  # Zambia
    'ZWE': 'ZW',  # Zimbabwe
}
```

---

## Country Names by ISO3

```python
ISO3_TO_COUNTRY_NAME = {
    'AFG': 'Afghanistan',
    'AGO': 'Angola',
    'ALB': 'Albania',
    'AND': 'Andorra',
    'ARE': 'United Arab Emirates',
    'ARG': 'Argentina',
    'ARM': 'Armenia',
    'ATG': 'Antigua and Barbuda',
    'AUS': 'Australia',
    'AUT': 'Austria',
    'AZE': 'Azerbaijan',
    'BEL': 'Belgium',
    'BEN': 'Benin',
    'BFA': 'Burkina Faso',
    'BGD': 'Bangladesh',
    'BGR': 'Bulgaria',
    'BHR': 'Bahrain',
    'BIH': 'Bosnia and Herzegovina',
    'BLR': 'Belarus',
    'BLZ': 'Belize',
    'BOL': 'Bolivia',
    'BRA': 'Brazil',
    'BRB': 'Barbados',
    'BWA': 'Botswana',
    'CAF': 'Central African Republic',
    'CAN': 'Canada',
    'CHE': 'Switzerland',
    'CHL': 'Chile',
    'CHN': 'China',
    'CIV': 'Côte d\'Ivoire',
    'CMR': 'Cameroon',
    'COD': 'Democratic Republic of the Congo',
    'COG': 'Congo',
    'COL': 'Colombia',
    'CPV': 'Cabo Verde',
    'CRI': 'Costa Rica',
    'CUB': 'Cuba',
    'CYP': 'Cyprus',
    'CZE': 'Czechia',
    'DEU': 'Germany',
    'DMA': 'Dominica',
    'DNK': 'Denmark',
    'DOM': 'Dominican Republic',
    'DZA': 'Algeria',
    'ECU': 'Ecuador',
    'EGY': 'Egypt',
    'ERI': 'Eritrea',
    'ESP': 'Spain',
    'EST': 'Estonia',
    'ETH': 'Ethiopia',
    'FIN': 'Finland',
    'FJI': 'Fiji',
    'FRA': 'France',
    'FSM': 'Micronesia',
    'GAB': 'Gabon',
    'GBR': 'United Kingdom',
    'GEO': 'Georgia',
    'GHA': 'Ghana',
    'GIN': 'Guinea',
    'GMB': 'Gambia',
    'GNB': 'Guinea-Bissau',
    'GRC': 'Greece',
    'GTM': 'Guatemala',
    'HND': 'Honduras',
    'HRV': 'Croatia',
    'HTI': 'Haiti',
    'HUN': 'Hungary',
    'IDN': 'Indonesia',
    'IND': 'India',
    'IRL': 'Ireland',
    'IRN': 'Iran',
    'IRQ': 'Iraq',
    'ISL': 'Iceland',
    'ISR': 'Israel',
    'ITA': 'Italy',
    'JAM': 'Jamaica',
    'JOR': 'Jordan',
    'JPN': 'Japan',
    'KAZ': 'Kazakhstan',
    'KEN': 'Kenya',
    'KGZ': 'Kyrgyzstan',
    'KHM': 'Cambodia',
    'KIR': 'Kiribati',
    'KNA': 'Saint Kitts and Nevis',
    'KOR': 'South Korea',
    'LAO': 'Laos',
    'LBN': 'Lebanon',
    'LBY': 'Libya',
    'LCA': 'Saint Lucia',
    'LKA': 'Sri Lanka',
    'LSO': 'Lesotho',
    'LTU': 'Lithuania',
    'LUX': 'Luxembourg',
    'LVA': 'Latvia',
    'MAR': 'Morocco',
    'MDA': 'Moldova',
    'MDG': 'Madagascar',
    'MEX': 'Mexico',
    'MHL': 'Marshall Islands',
    'MKD': 'North Macedonia',
    'MLI': 'Mali',
    'MLT': 'Malta',
    'MMR': 'Myanmar',
    'MNE': 'Montenegro',
    'MNG': 'Mongolia',
    'MOZ': 'Mozambique',
    'MRT': 'Mauritania',
    'MUS': 'Mauritius',
    'MWI': 'Malawi',
    'MYS': 'Malaysia',
    'NAM': 'Namibia',
    'NER': 'Niger',
    'NGA': 'Nigeria',
    'NIC': 'Nicaragua',
    'NLD': 'Netherlands',
    'NOR': 'Norway',
    'NPL': 'Nepal',
    'NZL': 'New Zealand',
    'OMN': 'Oman',
    'PAK': 'Pakistan',
    'PAN': 'Panama',
    'PER': 'Peru',
    'PHL': 'Philippines',
    'PLW': 'Palau',
    'PNG': 'Papua New Guinea',
    'POL': 'Poland',
    'PRK': 'North Korea',
    'PRT': 'Portugal',
    'PRY': 'Paraguay',
    'PSE': 'Palestine',
    'QAT': 'Qatar',
    'ROU': 'Romania',
    'RUS': 'Russia',
    'RWA': 'Rwanda',
    'SAU': 'Saudi Arabia',
    'SDN': 'Sudan',
    'SEN': 'Senegal',
    'SGP': 'Singapore',
    'SLB': 'Solomon Islands',
    'SLE': 'Sierra Leone',
    'SLV': 'El Salvador',
    'SMR': 'San Marino',
    'SRB': 'Serbia',
    'SUR': 'Suriname',
    'SVK': 'Slovakia',
    'SVN': 'Slovenia',
    'SWE': 'Sweden',
    'SYC': 'Seychelles',
    'SYR': 'Syria',
    'TCD': 'Chad',
    'TGO': 'Togo',
    'THA': 'Thailand',
    'TJK': 'Tajikistan',
    'TKM': 'Turkmenistan',
    'TUN': 'Tunisia',
    'TUR': 'Turkey',
    'TZA': 'Tanzania',
    'UGA': 'Uganda',
    'UKR': 'Ukraine',
    'URY': 'Uruguay',
    'USA': 'United States',
    'UZB': 'Uzbekistan',
    'VAT': 'Vatican City',
    'VEN': 'Venezuela',
    'VNM': 'Vietnam',
    'VUT': 'Vanuatu',
    'YEM': 'Yemen',
    'ZAF': 'South Africa',
    'ZMB': 'Zambia',
    'ZWE': 'Zimbabwe',
}
```

---

## Usage Examples

### Convert ISO2 to ISO3
```python
from proj_004_cia.___proj_heritage.__config.iso_mapping import ISO2_TO_ISO3

# Single conversion
iso2_code = "FR"
iso3_code = ISO2_TO_ISO3[iso2_code]  # "FRA"

# Multiple countries (transboundary)
iso2_string = "IT, FR, AT, SI, CH, DE"
iso3_codes = [ISO2_TO_ISO3[code.strip()] for code in iso2_string.split(',')]
# Result: ['ITA', 'FRA', 'AUT', 'SVN', 'CHE', 'DEU']
```

### Convert ISO3 to ISO2
```python
from proj_004_cia.___proj_heritage.__config.iso_mapping import ISO3_TO_ISO2

iso3_code = "FRA"
iso2_code = ISO3_TO_ISO2[iso3_code]  # "FR"
```

### Get Country Name
```python
from proj_004_cia.___proj_heritage.__config.iso_mapping import ISO3_TO_COUNTRY_NAME

iso3_code = "FRA"
country_name = ISO3_TO_COUNTRY_NAME[iso3_code]  # "France"
```

### Complete Conversion Function
```python
def get_country_info(iso2_code: str) -> dict:
    """Convert ISO2 to full country information."""
    iso3 = ISO2_TO_ISO3[iso2_code]
    return {
        'iso2': iso2_code,
        'iso3': iso3,
        'name': ISO3_TO_COUNTRY_NAME[iso3]
    }

# Example
info = get_country_info('FR')
# Result: {'iso2': 'FR', 'iso3': 'FRA', 'name': 'France'}
```

---

## Special Cases

### Kosovo
Note: Kosovo is not in the current UNESCO dataset but may be added in the future:
```python
'XK': 'UNK',  # Kosovo (temporary code, not official ISO)
```

### Historical Countries
Some sites may reference historical countries (e.g., Yugoslavia). Handle these with mapping notes:
```python
# Not in current dataset but may appear in historical data
'YU': 'YUG',  # Yugoslavia (dissolved)
'SU': 'SUN',  # Soviet Union (dissolved)
```

### Disputed Territories
Palestine is included:
```python
'PS': 'PSE',  # Palestine
```

---

## Validation

All 170 ISO2 codes from the World Heritage dataset are accounted for in this mapping.

### Verification Script
```python
# Verify all codes in dataset are mapped
import json

# Load heritage data
with open('all_world_heritage.json') as f:
    data = json.load(f)

# Collect all ISO2 codes
dataset_codes = set()
for site in data:
    iso = site.get('iso_codes', '')
    if iso:
        for code in iso.split(','):
            dataset_codes.add(code.strip())

# Verify all are in mapping
missing = dataset_codes - set(ISO2_TO_ISO3.keys())
if missing:
    print(f"Missing codes: {missing}")
else:
    print(f"✓ All {len(dataset_codes)} ISO2 codes mapped successfully")
```

---

## Regional Distribution

| Region | ISO3 Codes |
|--------|-----------|
| **Europe & North America** | AND, AUT, BEL, BGR, BLR, CAN, CHE, CYP, CZE, DEU, DNK, ESP, EST, FIN, FRA, GBR, GEO, GRC, HRV, HUN, IRL, ISL, ITA, LTU, LUX, LVA, MDA, MKD, MNE, NLD, NOR, POL, PRT, ROU, RUS, SMR, SRB, SVK, SVN, SWE, TUR, UKR, USA, VAT |
| **Asia & Pacific** | AFG, AUS, AZE, BGD, CHN, FJI, FSM, IDN, IND, IRN, JPN, KAZ, KGZ, KHM, KIR, KOR, LAO, LKA, MHL, MMR, MNG, MYS, NPL, NZL, PAK, PHL, PLW, PNG, PRK, SGP, THA, TJK, TKM, UZB, VNM, VUT |
| **Latin America & Caribbean** | ARG, ATG, BLZ, BOL, BRA, BRB, CHL, COL, CRI, CUB, DMA, DOM, ECU, GTM, HND, HTI, JAM, KNA, LCA, MEX, NIC, PAN, PER, PRY, SLV, SUR, URY, VEN |
| **Africa** | AGO, BEN, BFA, BWA, CAF, CIV, CMR, COD, COG, CPV, DZA, EGY, ERI, ETH, GAB, GHA, GIN, GMB, GNB, KEN, LSO, LBY, MAR, MDG, MLI, MOZ, MRT, MUS, MWI, NAM, NER, NGA, RWA, SDN, SEN, SLE, SYC, TCD, TGO, TZA, UGA, ZAF, ZMB, ZWE |
| **Arab States** | ARE, BHR, DZA, EGY, IRQ, JOR, LBN, LBY, MAR, OMN, PSE, QAT, SAU, SDN, SYR, TN, YEM |

Note: Some countries appear in multiple regions (e.g., Egypt in both Africa and Arab States).
