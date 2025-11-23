import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_world_biomes(pass_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # WORLD
    # --------------------------------------------------------------------------------------------------
    # "Coniferous Forest biome" - 'env_biomes_coniferous_forest'
    # "Desert biome" - 'env_biomes_desert'
    # "Grassland biome" - 'env_biomes_grassland'
    # "Rainforest biome" - 'env_biomes_rainforest'
    # "Shrubland biome" - 'env_biomes_shrubland'
    # "Temperate Deciduous Forest biome" - 'env_biomes_temperate_deciduous_forest'
    # "Tundra biome" - 'env_biomes_tundra'
    # "Types of Biomes" - 'env_biomes_types'
    # --------------------------------------------------------------------------------------------------
    # ['env_biomes_coniferous_forest', 'env_biomes_desert', 'env_biomes_grassland', 'env_biomes_rainforest',
    # 'env_biomes_shrubland', 'env_biomes_temperate_deciduous_forest', 'env_biomes_tundra', 'env_biomes_types']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "Types of Biomes": {
            "text": "<p>A biome is a biogeographical designation describing a biological community of plants and animals that has formed in response to a physical environment and a shared regional climate. Biomes can extend over more than one continent. Different classification systems define different numbers of biomes. <em>The World Factbook</em> recognizes the following seven biomes used by NASA: tundra, coniferous forest, temperate deciduous forest, rainforest, grassland, shrubland, and desert.</p>"
        },
        "Tundra biome": {
            "text": "The tundra is the coldest of the biomes. It also receives low amounts of precipitation, making the tundra similar to a desert. Tundra comes from the Finnish word <em>tunturia</em>, meaning \"treeless plain.\" Tundra is found in the regions just below the ice caps of the Arctic, extending across North America to Europe and to Siberia in Asia. Temperatures usually range between -40°C (-40 °F) and 18°C (64°F). The temperatures are so cold that there is a layer of permanently frozen ground below the surface, called permafrost. This permafrost is a defining characteristic of the tundra biome. In the tundra summers, the top layer of soil thaws only a few inches down, providing a growing surface for the roots of vegetation. This biome sees 150 to 250 mm (6 to 10 in) of rain per year. Vegetation in the tundra has adapted to the cold and the short growing season and consists of lichens, mosses, grasses, sedges, and shrubs, but almost no trees."
        },
        "Coniferous Forest biome": {
            "text": "The coniferous forest is sandwiched between the tundra to the north and the deciduous forest to the south. Coniferous forest regions have long, cold, snowy winters; warm, humid summers; well-defined seasons; and at least four to six frost-free months. The average temperature in winter ranges from -40&deg;C (-40&deg;F) to 20&deg;C (68&deg;F). The average summer temperatures are usually around 10&deg;C (50&deg;F). 300 to 900 mm (12 to 35 in) of rain per year can be expected in this biome. Vegetation consists of trees that produce cones and needles, which are called coniferous-evergreen trees. Some needles remain on the trees all year long. Some of the more common conifers are spruces, pines, and firs."
        },
        "Temperate Deciduous Forest biome": {
            "text": "Temperate deciduous forests are located in the mid-latitude areas, which means that they are found between the polar regions and the tropics. The deciduous forest regions are exposed to warm and cold air masses, which cause this area to have four seasons. Hot summers and cold winters are typical. The average daily temperatures range between -30&deg;C (-22&deg;F) and 30&deg;C (86&deg;F), with a yearly average of 10&deg;C (50&deg;F). On average, this biome receives 750 to 1,500 mm (30 to 59 in) of rain per year. Vegetation includes broadleaf trees (oaks, maples, beeches), shrubs, perennial herbs, and mosses.&nbsp;"
        },
        "Rainforest biome": {
            "text": "The rainforest biome remains warm all year and stay frost-free. The average daily temperatures range from 20&deg;C (68&deg;F) to 25&deg;C (77&deg;F). Rainforests receive the most yearly rainfall of all of the biomes, and a typical year sees 2,000 to 10,000 mm (79 to 394 in) of rain. Vegetation typically includes vines, palm trees, orchids, and ferns. There are two types of rainforests: tropical rainforests are found closer to the equator, and temperate rainforests are found farther north near coastal areas. The majority of common houseplants come from the rainforest."
        },
        "Grassland biome": {
            "text": "Grasslands are open, continuous, and fairly flat areas of grass. Found on every continent except Antarctica, they are often located between temperate forests at high latitudes and deserts at subtropical latitudes.&nbsp; Depending on latitude, the annual temperature range can be -20&deg;C (-4&deg;F) to 30&deg;C (86&deg;F). Grasslands receive around 500 to 900 mm (20 to 35 in) of rain per year. Tropical grasslands have dry and wet seasons that remain warm all the time. Temperate grasslands have cold winters and warm summers with some rain. Vegetation is dominated by grasses but can include sedges and rushes, along with some legumes (clover) and herbs. A few trees may be found in this biome along the streams, but not many due to the lack of rainfall."
        },
        "Shrubland biome": {
            "text": "Shrublands include chaparral, woodland, and savanna, and are composed of shrubs or short trees. Many shrubs thrive on steep, rocky slopes, but there is usually not enough rain to support tall trees. Shrublands are located in west coastal regions between 30&deg; and 40&deg; North and South latitude and are usually found on the borders of deserts and grasslands. The summers are hot and dry with temperatures up to 38&deg;C (100&deg;F). Winters are cool and moist, with temperatures around -1 &deg;C (30&deg;F). Annual rainfall in the shrublands varies greatly, but 200 to 1,000 mm (8 to 40 in) of rain per year can be expected. Vegetation includes aromatic herbs (sage, rosemary, thyme, oregano), shrubs, acacia, chamise, grasses. Plants have adapted to fire caused by frequent lightning strikes in the summer."
        },
        "Desert biome": {
            "text": "The most important characteristic of a desert biome is that it receives very little rainfall, usually about 250 mm (10 in) of rain per year. During the day, desert temperatures rise to an average of 38&deg;C (100&deg;F). At night, desert temperatures fall to an average of -4&deg;C (about 25&deg;F). Vegetation is sparse, consisting of cacti, small bushes, and short grasses. Perennials survive for several years by becoming dormant and flourishing when water is available. Annuals are referred to as ephemerals because some can complete an entire life cycle in weeks. Since desert conditions are so severe, the plants that live there need to adapt to compensate. Some, such as cacti, store water in their stems and use it very slowly, while others, like bushes, conserve water by growing few leaves or by having large root systems to gather water."
        }
    }
    parsed_data = parse_world_biomes(pass_data)
    print(parsed_data)
