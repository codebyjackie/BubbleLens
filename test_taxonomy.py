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

assert catalog["version"] == 20
assert catalog["sourceRowCount"] == 49844
assert catalog["tagCount"] == 49837
assert len(catalog["folders"]) == 53
assert [folder["id"] for folder in catalog["folders"]] == FOLDER_ORDER
assert len(categories) == 417
assert len(locations) == catalog["tagCount"]
assert all(category["tags"] for category in categories)
assert max(len(folder["name"]) for folder in catalog["folders"]) <= 6
assert max(len(category["name"]) for category in categories) <= 6
assert max(len(folder["categories"]) for folder in catalog["folders"] if folder["id"] not in {"copyright", "character"}) <= 13
assert catalog["fallbackCount"] == 0
assert locations["communism"] == ("themes", "social_theme")
assert locations["windshield"] == ("transport_play", "vehicle_parts")
assert locations["hilt"] == ("weapons", "weapon_parts")
assert locations["sandbox"] == ("recreation", "playground")
assert locations["cyberspace"] == ("indoor_scene", "virtual_space")
assert locations["jewelry"] == ("jewelry_accessories", "other_jewelry")
assert locations["underwear"] == ("underwear_swim", "underwear_general")
assert locations["food"] == ("food_drink", "food_general")
assert locations["indoors"] == ("indoor_scene", "indoor_general")
assert locations["pointy_ears"] == ("face", "ears")
assert locations["sleeveless"] == ("clothing_detail", "sleeve_detail")
assert locations["hair_flower"] == ("head_accessories", "themed_hair_ornament")
assert locations["nail_polish"] == ("body_detail", "nail_care")
assert locations["off_shoulder"] == ("clothing_detail", "collar_detail")
assert locations["water"] == ("nature", "water_ice")
assert locations["covered_nipples"] == ("adult_body", "adult_clothes")
assert locations["fur_trim"] == ("clothing_detail", "trim_detail")
assert locations["loli"] == ("adult_kink", "adult_taboo")
assert locations["strapless"] == ("clothing_detail", "strap_detail")
assert locations["bell"] == ("culture_objects", "music")
assert locations["capelet"] == ("outerwear_suits", "cape_cloak")
assert locations["head_tilt"] == ("pose", "head_pose")
assert locations["highleg"] == ("clothing_detail", "cutout_slit")
assert locations["on_bed"] == ("pose", "object_pose")
assert locations["petals"] == ("nature", "flower_general")
assert locations["turtleneck"] == ("clothing_detail", "collar_detail")
assert locations["zettai_ryouiki"] == ("clothing_appearance", "fashion_style")
assert locations["erection"] == ("adult", "adult_response")
assert locations["facial_mark"] == ("face", "face_mark")
assert locations["halterneck"] == ("clothing_detail", "strap_detail")
assert locations["hood_down"] == ("clothing_appearance", "wearing_state")
assert locations["ass_visible_through_thighs"] == ("body", "waist_hips")
assert locations["back"] == ("body", "torso_back")
assert locations["bed_sheet"] == ("household_objects", "storage_furniture")
assert locations["black_nails"] == ("body_detail", "nail_care")
assert locations["helmet"] == ("protective_clothes", "protective_helmet")
assert locations["military"] == ("themes", "social_theme")
assert locations["own_hands_together"] == ("pose", "hand_gesture")
assert locations["between_legs"] == ("action", "body_object")
assert locations["hakama_skirt"] == ("traditional_clothes", "traditional_japan")
assert locations["futanari"] == ("adult_body", "genital_variation")
assert locations["notice_lines"] == ("expression", "dramatic_effect")
assert locations["fins"] == ("animal_traits", "aquatic_feature")
assert locations["puffy_nipples"] == ("adult_body", "nipples")
assert locations["animal_hands"] == ("animal_traits", "claw_scale")
assert locations["one-hour_drawing_challenge"] == ("meta_info", "work_event")
assert locations["reaching"] == ("action", "body_object")
assert locations["emphasis_lines"] == ("composition", "subject_focus")
assert locations["cuffs"] == ("sensitive", "restraint")
assert locations["head_rest"] == ("pose", "object_pose")
assert locations["hat_ornament"] == ("accessories", "badges_ornaments")
assert locations[":q"] == ("face", "oral_detail")
assert locations["crossdressing_(mtf)"] == ("clothing_appearance", "fashion_style")
assert locations["pov_hands"] == ("composition", "viewpoint")
assert locations["purple_nails"] == ("body_detail", "nail_care")
assert locations["fur_collar"] == ("clothing_detail", "collar_detail")
assert locations["toenail_polish"] == ("body_detail", "nail_care")
assert locations["on_floor"] == ("pose", "object_pose")
assert locations["mini_hat"] == ("head_accessories", "themed_hair_ornament")
assert locations["on_chair"] == ("pose", "object_pose")
assert locations["glint"] == ("light_effect", "optical")
assert locations["leash"] == ("sensitive", "restraint")
assert locations["forehead_mark"] == ("face", "face_mark")
assert locations["aged_up"] == ("themes", "identity_change")
assert locations["rock"] == ("nature", "mineral")
assert locations["naughty_face"] == ("expression", "positive")
assert locations["breasts_squeezed_together"] == ("body", "breast_chest")
assert locations["object_insertion"] == ("adult_kink", "adult_insertion")
assert locations["ice"] == ("nature", "water_ice")
assert locations["large_areolae"] == ("adult_body", "nipples")
assert locations["card_(medium)"] == ("style", "medium")
assert locations["long_fingernails"] == ("body_detail", "nail_care")
assert locations["zoom_layer"] == ("composition", "layout")
assert locations["hat_flower"] == ("accessories", "badges_ornaments")
assert locations["water_drop"] == ("nature", "water_ice")
assert locations["sand"] == ("nature", "mineral")
assert locations["sharp_fingernails"] == ("body_detail", "nail_care")
assert locations["on_ground"] == ("pose", "object_pose")
assert locations["criss-cross_halter"] == ("clothing_detail", "strap_detail")
assert locations["sitting_on_person"] == ("action", "interaction")
assert locations["jacket_on_shoulders"] == ("clothing_appearance", "wearing_state")
assert locations["alternate_color"] == ("themes", "persona_variant")
assert locations["bandana"] == ("head_accessories", "headwrap_veil")
assert locations["ofuda"] == ("symbols", "religious_symbol")
assert locations["on_couch"] == ("pose", "object_pose")
assert locations["white_capelet"] == ("outerwear_suits", "cape_cloak")
assert locations["gag"] == ("sensitive", "restraint")
assert locations["gagged"] == ("sensitive", "restraint")
assert locations["licking_lips"] == ("face", "oral_detail")
assert locations["abyssal_ship"] == ("creatures", "fantasy_creature")
assert locations["angel"] == ("people", "fantasy_person")
assert locations["shota"] == ("adult_kink", "adult_taboo")
assert locations["dakimakura_(medium)"] == ("style", "medium")
assert locations["bloomers"] == ("underwear_swim", "panties_underwear")
assert locations["covering_breasts"] == ("action", "body_cover")
assert locations["tress_ribbon"] == ("head_accessories", "hairband_ribbon")
assert locations["underbust"] == ("underwear_swim", "bra_lingerie")
assert locations["w"] == ("pose", "hand_gesture")
assert locations["ahegao"] == ("adult", "adult_response")
assert locations["claw_pose"] == ("pose", "hand_gesture")
assert locations["joints"] == ("body", "internal_organs")
assert locations["+++"] == ("expression", "dramatic_effect")
assert locations["winter_clothes"] == ("clothing_appearance", "fashion_style")
assert locations["on_head"] == ("action", "interaction")
assert locations["glass"] == ("household_objects", "material")
assert locations["retro_artstyle"] == ("style", "era_style")
assert locations["armored_boots"] == ("protective_clothes", "leg_armor")
assert locations["bun_cover"] == ("head_accessories", "hairtie_ring")
assert locations["cheerleader"] == ("people", "occupation")
assert locations["open_hand"] == ("pose", "hand_gesture")
assert locations["road"] == ("outdoor_scene", "terrain_surface")
assert locations["arm_strap"] == ("accessories", "badges_ornaments")
assert locations["miko"] == ("people", "occupation")
assert locations["squiggle"] == ("expression", "dramatic_effect")
assert locations["fairy"] == ("people", "fantasy_person")
assert locations["nipple_slip"] == ("adult_body", "adult_clothes")
assert locations[">_<"] == ("expression", "fear_surprise")

body_folder = next(item for item in catalog["folders"] if item["id"] == "body")
assert next(item for item in body_folder["categories"] if item["id"] == "internal_organs")["name"] == "骨骼内脏"
nature_folder = next(item for item in catalog["folders"] if item["id"] == "nature")
assert next(item for item in nature_folder["categories"] if item["id"] == "water_ice")["name"] == "水与冰"
animal_traits_folder = next(item for item in catalog["folders"] if item["id"] == "animal_traits")
assert next(item for item in animal_traits_folder["categories"] if item["id"] == "claw_scale")["name"] == "爪鳞触须"
assert locations["bara"] == ("style", "genre")
assert locations["bottle"] == ("household_objects", "container")
assert locations["facing_viewer"] == ("pose", "body_pose")
assert locations["looking_up"] == ("pose", "head_pose")
assert locations["plant"] == ("nature", "plant_general")
assert locations["straddling"] == ("pose", "object_pose")
assert locations["aged_down"] == ("themes", "identity_change")
assert locations["armband"] == ("accessories", "badges_ornaments")
assert locations["bdsm"] == ("adult_kink", "kink_general")
assert locations["blue_sailor_collar"] == ("clothing_detail", "collar_detail")
assert locations["clenched_hand"] == ("pose", "hand_gesture")
assert locations["crossover"] == ("themes", "character_connection")
assert locations["red_nails"] == ("body_detail", "nail_care")
assert locations["shaded_face"] == ("expression", "dramatic_effect")
assert locations["underwear_only"] == ("underwear_swim", "underwear_general")
assert locations["white_sailor_collar"] == ("clothing_detail", "collar_detail")
assert locations["..."] == ("symbols", "general_symbol")
assert locations["alternate_breast_size_(larger)"] == ("themes", "persona_variant")
assert locations["blue_nails"] == ("body_detail", "nail_care")
assert locations["cherry_blossoms"] == ("nature", "flower_species")
assert locations["ejaculation"] == ("adult", "adult_response")
assert locations["foreshortening"] == ("style", "technique")
assert locations["gold_trim"] == ("clothing_detail", "trim_detail")
assert locations["hood_up"] == ("clothing_appearance", "wearing_state")
assert locations["indie_virtual_youtuber"] == ("people", "occupation")
assert locations["lace_trim"] == ("clothing_detail", "trim_detail")
assert locations["pink_nails"] == ("body_detail", "nail_care")
assert locations["revealing_clothes"] == ("clothing_appearance", "fashion_style")
assert locations["scenery"] == ("composition", "subject_focus")
assert locations["^^^"] == ("expression", "fear_surprise")
assert locations["adapted_costume"] == ("themes", "persona_variant")
assert locations["between_breasts"] == ("action", "body_object")
assert locations["furrowed_brow"] == ("face", "eyebrows")
assert locations["hair_rings"] == ("hair", "hair_style")
assert locations["sheath"] == ("weapons", "weapon_parts")
assert locations["spikes"] == ("weapons", "weapon_parts")
assert locations["sweater_vest"] == ("clothes_main", "vest_top")
assert locations["two-tone_background"] == ("background", "background_plain")
assert locations["beads"] == ("accessories", "badges_ornaments")
assert locations["black_sailor_collar"] == ("clothing_detail", "collar_detail")
assert locations["clenched_hands"] == ("pose", "hand_gesture")
assert locations["clothes_writing"] == ("clothing_appearance", "clothing_pattern")
assert locations["covering_privates"] == ("action", "body_cover")
assert locations["jingle_bell"] == ("culture_objects", "music")
assert locations["low-tied_long_hair"] == ("hair", "hair_style")
assert locations["mary_janes"] == ("legwear_footwear", "casual_shoes")
assert locations["sleeves_rolled_up"] == ("clothing_appearance", "wearing_state")
assert locations["tachi-e"] == ("style", "art_style")
assert locations["third_eye"] == ("body", "anatomy_anomaly")
assert locations[":p"] == ("face", "oral_detail")
assert locations["ball"] == ("household_objects", "other_object")
assert locations["colored_eyelashes"] == ("face", "makeup")
assert locations["crossdressing"] == ("clothing_appearance", "fashion_style")
assert locations["fake_tail"] == ("accessories", "other_accessory")
assert locations["kemonomimi_mode"] == ("themes", "persona_variant")
assert locations["one_piece"] == ("clothes_main", "dress")
assert locations["shirt_tucked_in"] == ("clothing_appearance", "wearing_state")
assert locations["strap_slip"] == ("clothing_appearance", "wearing_state")
assert locations["tray"] == ("food_drink", "tableware")
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
    "bras_d'honneur": ("pose", "hand_gesture"),
    "blanket_veil": ("head_accessories", "headwrap_veil"),
    "headband_around_neck": ("accessories", "neckwear"),
    "onion_rings": ("food_drink", "dessert_snack"),
    "multi-lane_road": ("urban_architecture", "urban"),
    "karaginu_mo": ("traditional_clothes", "traditional_japan"),
    "wrists_extended": ("pose", "arm_pose"),
    "camel": ("creatures", "mammal"),
    "statue_of_liberty": ("urban_architecture", "tower_landmark"),
    "yari": ("weapons", "polearm"),
    "jiaoling_ruqun": ("traditional_clothes", "traditional_china"),
    "hishimochi": ("food_drink", "dessert_snack"),
    "dodecagram": ("symbols", "shape_math"),
    "automail": ("mech_scifi", "cybernetic"),
    "german_shepherd": ("creatures", "mammal"),
    "car_crash": ("sensitive", "injury_death"),
    "floorplan": ("composition", "layout"),
    "rebreather": ("protective_clothes", "civilian_helmet"),
    "wrist_blades": ("weapons", "blade"),
    "saddlebags": ("body", "waist_hips"),
    "hitchhiking": ("action", "movement"),
    "umbrella_stand": ("household_objects", "storage_furniture"),
    "dragon_horn": ("animal_traits", "horns"),
    "gyarugasaki": ("franchise_clothes", "school_variant"),
    "guqin": ("culture_objects", "music"),
    "nintendo_64": ("digital_media", "game_device"),
    "border_collie": ("creatures", "mammal"),
    "strappado": ("adult_kink", "adult_bondage"),
    "winchester_model_1897": ("weapons", "firearm"),
}
for tag_name, location in expected.items():
    assert locations[tag_name] == location, (tag_name, locations[tag_name], location)

screenshot_expected = {
    "ardor_blossom_star_(e.g.o)": ("franchise_clothes", "franchise_armor"),
    "argentina": ("outdoor_scene", "country_region"),
    "chloroform": ("household_objects", "chemical_liquid"),
    "eighteen_(fate)": ("character", "letter_e"),
    "desire_driver": ("mech_scifi", "scifi_device"),
    "color-coded": ("light_effect", "palette"),
    "coiled": ("pose", "body_pose"),
    "convention_greeting": ("text_meta", "text"),
    "charisma_guard": ("pose", "body_pose"),
    "carro_veloce_cv-33": ("transport_play", "land_vehicle"),
    "after_insertion": ("adult", "adult_response"),
    "donkey": ("creatures", "mammal"),
    "anvil": ("household_objects", "tools"),
    "croupier": ("people", "occupation"),
    "dealer_(gambling)": ("people", "occupation"),
    "catcher_(baseball)": ("recreation", "sports"),
    "color_wheel_challenge": ("meta_info", "meme"),
    "crystallization": ("themes", "identity_change"),
    "doubledriver": ("mech_scifi", "scifi_device"),
    "eavesdropping": ("action", "daily_action"),
    "akg": ("digital_media", "audio_device"),
    "alstroemeria_(idolmaster)": ("relationships", "group_faction"),
    "caveman": ("people", "role_focus"),
    "elasticity": ("light_effect", "other_effect"),
    "algae": ("nature", "grass_crop"),
    "breeding_mount": ("adult_kink", "adult_toys"),
    "coaster": ("food_drink", "tableware"),
    "cosmic_heart_compact": ("jewelry_accessories", "gem_brooch"),
    "bollard": ("building_parts", "frame_structure"),
    "box_stack": ("household_objects", "container"),
    "eiserne_jungfrau": ("character", "letter_e"),
    "chrysos_heirs_(honkai:_star_rail)": ("relationships", "group_faction"),
    "extreme_dangling": ("action", "clothing_action"),
    "apocalypse": ("style", "genre"),
    "brown_hiphighs": ("legwear_footwear", "stockings"),
    "cafeteria": ("indoor_scene", "public_indoor"),
    "catheter": ("household_objects", "tools"),
    "clothes-dissolving_potion": ("clothing_appearance", "damaged_dirty"),
    "colored_veins": ("body_detail", "skin"),
    "england": ("outdoor_scene", "country_region"),
}
for tag_name, location in screenshot_expected.items():
    assert locations[tag_name] == location, (tag_name, locations[tag_name], location)

assert tags["deep_skin"]["cn"] == "抓握深陷"
assert tags["skin_fangs"]["cn"] == "双侧口缘虎牙"
assert tags["batter"]["cn"] == "面糊"
assert tags["sett"]["cn"] == "铺路石"
assert tags["yuri_(object)"]["cn"] == "百合题材物品"
assert tags["pokemon_(anime)"]["cn"] == "宝可梦（动画）"

manual_rows_1841_1920 = {
    "thighlet": ("jewelry_accessories", "other_jewelry"),
    "inverted_nipples": ("adult_body", "nipples"),
    "green_nails": ("body_detail", "nail_care"),
}
for tag_name, location in manual_rows_1841_1920.items():
    assert locations[tag_name] == location, (tag_name, locations[tag_name], location)

manual_rows_1921_2000 = {
    "anchor_symbol": ("symbols", "emblem"),
    "clothes_around_waist": ("clothing_appearance", "wearing_state"),
    "gohei": ("culture_objects", "ritual_object"),
    "paw_print": ("symbols", "general_symbol"),
    "frilled_thigh_strap": ("accessories", "other_accessory"),
    "bound_arms": ("sensitive", "restraint"),
    "own_hands_clasped": ("pose", "hand_gesture"),
    "naked_shirt": ("clothing_appearance", "wearing_state"),
    "head_wreath": ("head_accessories", "headpiece"),
    "text_focus": ("composition", "subject_focus"),
    "aqua_nails": ("body_detail", "nail_care"),
}
for tag_name, location in manual_rows_1921_2000.items():
    assert locations[tag_name] == location, (tag_name, locations[tag_name], location)

manual_rows_2001_2080 = {
    "black_capelet": ("outerwear_suits", "cape_cloak"),
    "tied_shirt": ("clothing_appearance", "wearing_state"),
    "lowleg": ("clothing_detail", "cutout_slit"),
    "alternate_eye_color": ("themes", "persona_variant"),
    "red_pupils": ("face", "eye_color"),
    "areolae": ("adult_body", "nipples"),
    "whisker_markings": ("face", "face_mark"),
    "against_wall": ("pose", "object_pose"),
    "vampire": ("people", "fantasy_person"),
    "hat_feather": ("accessories", "badges_ornaments"),
}
for tag_name, location in manual_rows_2001_2080.items():
    assert locations[tag_name] == location, (tag_name, locations[tag_name], location)

ritual_folder = next(item for item in catalog["folders"] if item["id"] == "culture_objects")
assert next(category for category in ritual_folder["categories"] if category["id"] == "ritual_object")["name"] == "礼仪用品"

assert tags["load_bearing_equipment"]["cn"] == "携行装备"

for folder_id in {
    "head_accessories", "uniform_costume", "franchise_clothes", "traditional_clothes",
    "protective_clothes", "underwear_swim", "legwear_footwear", "nature",
    "building_parts", "urban_architecture",
}:
    folder = next(item for item in catalog["folders"] if item["id"] == folder_id)
    assert len(folder["categories"]) <= 10, (folder_id, len(folder["categories"]))

adult_body = next(item for item in catalog["folders"] if item["id"] == "adult_body")
assert len(adult_body["categories"]) <= 11

category_keys = {(folder["id"], category["id"]) for folder in catalog["folders"] for category in folder["categories"]}
folder_ids = {folder["id"] for folder in catalog["folders"]}
protective = next(folder for folder in catalog["folders"] if folder["id"] == "protective_clothes")
assert [category["id"] for category in protective["categories"]] == [
    "full_armor", "torso_armor", "shoulder_armor", "arm_armor", "leg_armor",
    "flexible_armor", "protective_helmet", "combat_helmet", "civilian_helmet", "protective_suit",
]
assert [category["name"] for category in protective["categories"]] == [
    "铠甲", "胸甲", "肩甲", "手臂护具", "下肢护具",
    "柔性护甲", "防护头盔", "战斗头盔", "头戴装备", "防护服",
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
assert next(category for category in footwear["categories"] if category["id"] == "short_boots")["tagCount"] == 40
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

print("taxonomy v20: ok")
