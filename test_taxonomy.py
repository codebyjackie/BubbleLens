from server import build_catalog
from taxonomy import FOLDER_ORDER, SYMBOL_LOCATION_SETS


catalog = build_catalog()
categories = [category for folder in catalog["folders"] for category in folder["categories"]]
locations = {
    tag["name"]: (folder["id"], category["id"])
    for folder in catalog["folders"]
    for category in folder["categories"]
    for tag in category["tags"]
}
tags = {
    tag["name"]: tag
    for folder in catalog["folders"]
    for category in folder["categories"]
    for tag in category["tags"]
}

assert catalog["version"] == 14
assert catalog["sourceRowCount"] == 49844
assert catalog["tagCount"] == 49837
assert len(catalog["folders"]) == 53
assert [folder["id"] for folder in catalog["folders"]] == FOLDER_ORDER
assert len(categories) == 395
assert len(locations) == catalog["tagCount"]
assert all(category["tags"] for category in categories)
assert max(len(folder["name"]) for folder in catalog["folders"]) <= 6
assert max(len(category["name"]) for category in categories) <= 6
assert max(len(folder["categories"]) for folder in catalog["folders"] if folder["id"] not in {"copyright", "character"}) <= 12
assert catalog["fallbackCount"] == 2673
assert sum(map(len, SYMBOL_LOCATION_SETS.values())) == 414
assert len(set().union(*SYMBOL_LOCATION_SETS.values())) == 414

expected = {
    "hair_ribbon": ("head_accessories", "hairband_ribbon"),
    "hairclip": ("head_accessories", "hairclip_pin"),
    "wig": ("head_accessories", "wig_hairpiece"),
    "star_hair_ornament": ("head_accessories", "themed_hair_ornament"),
    "tracen_school_uniform": ("franchise_clothes", "school_variant"),
    "happy_party_train": ("franchise_clothes", "idol_outfit"),
    "normal_suit_(gundam)": ("franchise_clothes", "franchise_outfit"),
    "obi": ("traditional_clothes", "traditional_japan"),
    "hanfu": ("traditional_clothes", "traditional_china"),
    "hanbok": ("traditional_clothes", "traditional_korea"),
    "sari": ("traditional_clothes", "traditional_other"),
    "keffiyeh": ("traditional_clothes", "traditional_other"),
    "african_clothes": ("traditional_clothes", "traditional_other"),
    "armor": ("protective_clothes", "full_armor"),
    "red_armor": ("protective_clothes", "full_armor"),
    "living_armor": ("people", "fantasy_person"),
    "breastplate": ("protective_clothes", "torso_armor"),
    "chest_guard": ("protective_clothes", "torso_armor"),
    "chest_protector": ("protective_clothes", "torso_armor"),
    "shoulder_pads": ("protective_clothes", "shoulder_armor"),
    "arm_guards": ("protective_clothes", "arm_armor"),
    "single_arm_guard": ("protective_clothes", "arm_armor"),
    "elbow_pads": ("protective_clothes", "arm_armor"),
    "single_elbow_pad": ("protective_clothes", "arm_armor"),
    "wrist_guards": ("protective_clothes", "arm_armor"),
    "knee_pads": ("protective_clothes", "leg_armor"),
    "single_knee_pad": ("protective_clothes", "leg_armor"),
    "knee_guards": ("protective_clothes", "leg_armor"),
    "knee_brace": ("protective_clothes", "leg_armor"),
    "shin_guards": ("protective_clothes", "leg_armor"),
    "cast": ("body_detail", "bandage_patch"),
    "arm_sling": ("body_detail", "bandage_patch"),
    "leg_cast": ("body_detail", "bandage_patch"),
    "flak_jacket": ("protective_clothes", "protective_suit"),
    "bulletproof_vest": ("protective_clothes", "protective_suit"),
    "body_armor": ("protective_clothes", "protective_suit"),
    "power_suit": ("protective_clothes", "protective_suit"),
    "power_armor": ("protective_clothes", "protective_suit"),
    "springsuit": ("protective_clothes", "protective_suit"),
    "highleg_springsuit": ("protective_clothes", "protective_suit"),
    "battlesuit": ("protective_clothes", "protective_suit"),
    "armored_bodysuit": ("protective_clothes", "protective_suit"),
    "armored_leotard": ("protective_clothes", "protective_suit"),
    "respirator": ("protective_clothes", "civilian_helmet"),
    "ear_protection": ("protective_clothes", "civilian_helmet"),
    "chainmail": ("protective_clothes", "flexible_armor"),
    "leather_armor": ("protective_clothes", "flexible_armor"),
    "scale_armor": ("protective_clothes", "flexible_armor"),
    "gambeson": ("protective_clothes", "flexible_armor"),
    "lamellar_armor": ("protective_clothes", "flexible_armor"),
    "broken_armor": ("clothing_appearance", "damaged_dirty"),
    "load_bearing_equipment": ("accessories", "bags_belts"),
    "sneaking_suit": ("franchise_clothes", "franchise_outfit"),
    "shoulder_spikes": ("protective_clothes", "shoulder_armor"),
    "kabuto_(helmet)": ("protective_clothes", "combat_helmet"),
    "school_swimsuit": ("underwear_swim", "school_swim"),
    "trinity_general_school_swimsuit": ("franchise_clothes", "franchise_swim"),
    "high_heels": ("legwear_footwear", "heels"),
    "combat_boots": ("legwear_footwear", "work_special_shoes"),
    "thigh_boots": ("legwear_footwear", "short_boots"),
    "knee_boots": ("legwear_footwear", "short_boots"),
    "single_thigh_boot": ("legwear_footwear", "short_boots"),
    "single_knee_boot": ("legwear_footwear", "short_boots"),
    "thighhighs_under_boots": ("legwear_footwear", "stockings"),
    "bootjob": ("adult", "adult_sex"),
    "rose": ("nature", "flower_species"),
    "lily_(flower)": ("nature", "flower_species"),
    "qingxin_flower": ("nature", "unusual_plant"),
    "thatched_roof": ("building_parts", "roof_exterior"),
    "lighthouse": ("urban_architecture", "tower_landmark"),
    "architecture": ("urban_architecture", "architecture_style"),
    "penis": ("adult_body", "penis"),
    "testicles": ("adult_body", "testicles"),
    "clitoris": ("adult_body", "clitoris"),
    "pubic_hair": ("adult_body", "pubic_hair"),
    "fake_animal_ears": ("head_accessories", "headpiece"),
    "raccoon_tails_(hairstyle)": ("hair", "hair_style"),
    "eyebrows": ("face", "eyebrows"),
    "nose": ("face", "nose"),
    "teabag": ("food_drink", "drink"),
    "human_head": ("creatures", "fantasy_creature"),
    "hirschgeweih_antennas": ("mech_scifi", "machine"),
    "halo": ("light_effect", "halo_effect"),
    "aura": ("light_effect", "glow_aura"),
    "magic": ("light_effect", "magic_energy"),
    "note": ("culture_objects", "books_paper"),
    "notes": ("symbols", "music_symbol"),
    "aquarius_(zodiac)": ("outdoor_scene", "sky_space"),
    "aquarius_(symbol)": ("symbols", "zodiac_symbol"),
    "bridge_piercing": ("jewelry_accessories", "piercing"),
    "multiple_tattoos": ("body_detail", "tattoo_mark"),
    "mole_on_breast": ("body_detail", "mole_freckle"),
    "scarab": ("creatures", "insect"),
    "spasm": ("text_meta", "comic"),
    "battle_damage": ("mech_scifi", "mecha"),
    "barefoot": ("body", "feet_toes"),
    "cannibalism": ("sensitive", "vore"),
    "blood_on_clothes": ("sensitive", "blood"),
    "bandaids_on_nipples": ("adult_body", "adult_clothes"),
    "tongue": ("face", "oral_detail"),
    "nose_ring": ("jewelry_accessories", "piercing"),
    "mismatched_animal_ear_colors": ("animal_traits", "animal_ears"),
    "mechanical_halo": ("light_effect", "halo_effect"),
    "red_bow": ("accessories", "bows_ribbons"),
    "casual": ("clothing_appearance", "fashion_style"),
    "gothic_lolita": ("clothing_appearance", "fashion_style"),
    "metal_wrist_cuffs": ("sensitive", "restraint"),
    "nipple_piercing": ("adult_kink", "adult_piercing"),
    "vaginal_object_insertion": ("adult_kink", "adult_insertion"),
    "femdom": ("adult_kink", "adult_power"),
    "scat": ("adult_kink", "adult_excretion"),
    "orgasm": ("adult", "adult_response"),
    "rape": ("sensitive", "sexual_violence"),
    "death": ("sensitive", "injury_death"),
    "multiple_insertions": ("adult_kink", "adult_insertion"),
    "hime_lolita": ("clothing_appearance", "fashion_style"),
    "deep_skin": ("body_detail", "body_state"),
    "skin_fangs": ("face", "oral_detail"),
    "tan_tattoo": ("body_detail", "tattoo_mark"),
    "sunburn": ("body_detail", "skin"),
    "yuri_(object)": ("culture_objects", "books_paper"),
    "batter": ("food_drink", "bakery"),
    "tiles": ("building_parts", "surface"),
    "ruins": ("urban_architecture", "public_building"),
}
for tag_name, location in expected.items():
    assert locations[tag_name] == location, (tag_name, locations[tag_name], location)

assert tags["deep_skin"]["cn"] == "抓握深陷"
assert tags["skin_fangs"]["cn"] == "双侧口缘虎牙"
assert tags["batter"]["cn"] == "面糊"
assert tags["sett"]["cn"] == "铺路石"
assert tags["yuri_(object)"]["cn"] == "百合题材物品"

assert tags["load_bearing_equipment"]["cn"] == "携行装备"

for folder_id in {
    "head_accessories", "uniform_costume", "franchise_clothes", "traditional_clothes",
    "protective_clothes", "underwear_swim", "legwear_footwear", "nature",
    "building_parts", "urban_architecture", "adult_body",
}:
    folder = next(item for item in catalog["folders"] if item["id"] == folder_id)
    assert len(folder["categories"]) <= 10, (folder_id, len(folder["categories"]))

category_keys = {(folder["id"], category["id"]) for folder in catalog["folders"] for category in folder["categories"]}
folder_ids = {folder["id"] for folder in catalog["folders"]}
protective = next(folder for folder in catalog["folders"] if folder["id"] == "protective_clothes")
assert [category["id"] for category in protective["categories"]] == [
    "full_armor", "torso_armor", "shoulder_armor", "arm_armor", "leg_armor",
    "flexible_armor", "combat_helmet", "civilian_helmet", "protective_suit",
]
assert [category["name"] for category in protective["categories"]] == [
    "铠甲", "胸甲", "肩甲", "手臂护具", "下肢护具",
    "柔性护甲", "战斗头盔", "头戴装备", "防护服",
]
traditional = next(folder for folder in catalog["folders"] if folder["id"] == "traditional_clothes")
assert [category["id"] for category in traditional["categories"]] == [
    "traditional_japan", "traditional_china", "traditional_korea",
    "traditional_se_asia", "traditional_europe", "traditional_americas",
    "traditional_other",
]
footwear = next(folder for folder in catalog["folders"] if folder["id"] == "legwear_footwear")
assert [category["id"] for category in footwear["categories"]] == [
    "socks", "stockings", "heels", "casual_shoes", "sandals_slippers",
    "traditional_shoes", "sports_shoes", "short_boots", "work_special_shoes",
]
assert next(category for category in footwear["categories"] if category["id"] == "short_boots")["name"] == "靴子"
assert next(category for category in footwear["categories"] if category["id"] == "short_boots")["tagCount"] == 39
assert "clothing_state" not in folder_ids
for removed_key in {
    ("franchise_clothes", "character_costume"),
    ("nature", "aquatic_flower"), ("nature", "fungus_fantasy"),
    ("nature", "rose"),
    ("urban_architecture", "ruin_structure"),
    ("urban_architecture", "surface"),
    ("body_detail", "surface_decor"),
    ("traditional_clothes", "traditional_india"),
    ("traditional_clothes", "traditional_central_west"),
    ("traditional_clothes", "traditional_africa"),
    ("protective_clothes", "powered_armor"),
    ("protective_clothes", "pads_support"),
    ("legwear_footwear", "tall_boots"),
}:
    assert removed_key not in category_keys

print("taxonomy v14: ok")
