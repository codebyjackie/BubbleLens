"""Deterministic taxonomy for the local Danbooru tag library.

The classifier deliberately prefers high-confidence name patterns.  Every tag is
assigned exactly once.  Copyright and character tags use Danbooru's source type;
general tags that cannot be classified safely go to an explicit alphabetical
"other" bucket instead of being forced into a misleading semantic category.
"""

from __future__ import annotations

import re
import string


def category(category_id: str, name: str):
    return {"id": category_id, "name": name}


def folder(folder_id: str, name: str, icon: str, accent: str, description: str, categories: list[dict]):
    return {
        "id": folder_id,
        "name": name,
        "icon": icon,
        "accent": accent,
        "description": description,
        "categories": categories,
    }


ALPHA_CATEGORIES = [category(f"letter_{letter.lower()}", letter) for letter in string.ascii_uppercase]
ALPHA_CATEGORIES.append(category("letter_other", "数字与其他"))

OTHER_CATEGORIES = [
    category("other_a_e", "A–E"),
    category("other_f_j", "F–J"),
    category("other_k_o", "K–O"),
    category("other_p_t", "P–T"),
    category("other_u_z", "U–Z"),
    category("other_symbol", "数字符号"),
]


TAXONOMY = [
    folder("people", "人物设定", "◉", "#9587ff", "人数、性别、年龄、职业与人物类型", [
        category("count_gender", "人数性别"), category("age", "年龄阶段"),
        category("occupation", "职业身份"), category("role_focus", "角色类型"),
        category("fantasy_person", "幻想种族"),
    ]),
    folder("relationships", "人物关系", "∞", "#aa82eb", "配对、亲属、朋友、对手与人物组合", [
        category("romance_orientation", "恋爱配对"), category("family_relation", "亲属关系"),
        category("social_relation", "社交关系"), category("comparison", "人物对照"),
        category("group_faction", "团体组织"),
    ]),
    folder("themes", "剧情设定", "◆", "#b17ee8", "身份变化、角色变体、人物关联、剧情情境与社会主题", [
        category("identity_change", "身份变化"), category("persona_variant", "角色变体"),
        category("narrative_situation", "剧情情境"), category("character_connection", "角色关联"),
        category("social_theme", "社会主题"),
    ]),
    folder("body", "体型部位", "◒", "#e789b3", "体型、胸腹、四肢、器官与身体结构", [
        category("build", "体型身高"), category("breast_chest", "胸部"),
        category("torso_back", "躯干背腹"), category("waist_hips", "腰臀胯部"),
        category("legs_knees", "腿部膝盖"), category("arms_hands", "手臂手部"),
        category("feet_toes", "足部脚趾"), category("internal_organs", "内部器官"),
        category("limb_variation", "肢体差异"), category("anatomy_anomaly", "异形身体"),
    ]),
    folder("body_detail", "身体特征", "◓", "#df83ad", "皮肤、体毛、印记、伤痕与身体状态", [
        category("skin", "皮肤特征"), category("tattoo_mark", "纹身印记"),
        category("mole_freckle", "痣与雀斑"), category("scar_wound", "伤口疤痕"),
        category("bandage_patch", "绷带贴布"), category("surface_stain", "体表附着"),
        category("body_hair", "体毛"),
        category("body_function", "生理反应"), category("body_state", "身体状态"),
    ]),
    folder("face", "面部五官", "◌", "#43c2df", "眼睛、眉毛、鼻子、脸型、口耳与妆容", [
        category("eye_color", "眼睛颜色"), category("eye_shape", "眼形瞳孔"),
        category("eyebrows", "眉毛"), category("nose", "鼻子"), category("face_shape", "脸部轮廓"),
        category("mouth", "嘴型嘴唇"), category("oral_detail", "舌头牙齿"),
        category("ears", "耳朵"), category("facial_hair", "面部毛发"), category("makeup", "妆容装饰"),
    ]),
    folder("hair", "发型发色", "≈", "#ee78b2", "发色、长度、造型、刘海与头发状态", [
        category("hair_color", "头发颜色"), category("hair_length", "头发长度"),
        category("hair_style", "造型编发"), category("bangs", "刘海发际"),
        category("hair_action", "头发状态"),
    ]),
    folder("expression", "表情情绪", "☺", "#ffad55", "情绪、神态和面部表情", [
        category("positive", "开心笑容"), category("sad_cry", "悲伤哭泣"),
        category("anger", "愤怒不满"), category("fear_surprise", "紧张惊讶"),
        category("shy_blush", "害羞脸红"), category("neutral_expression", "中性表情"),
    ]),
    folder("pose", "姿势视线", "↗", "#51d0ab", "视线、手势、静态姿态与身体姿势", [
        category("gaze", "视线朝向"), category("stationary_pose", "站坐跪躺"),
        category("body_pose", "身体姿势"), category("leg_pose", "腿脚姿势"),
        category("arm_pose", "手臂姿势"), category("hand_gesture", "手势符号"),
    ]),
    folder("action", "动作互动", "⇢", "#39c59b", "手持、运动、战斗、人物互动与日常行为", [
        category("holding", "拿持携带"), category("movement", "移动运动"),
        category("combat_action", "战斗动作"), category("interaction", "人物互动"),
        category("daily_action", "日常活动"), category("clothing_action", "穿脱整理"),
    ]),
    folder("clothes_main", "日常服装", "◇", "#9bd454", "上衣、下装、裙装、睡衣与日常穿着", [
        category("shirt_top", "衬衫上衣"), category("sweater_hoodie", "毛衣卫衣"),
        category("vest_top", "背心短衣"), category("bottoms", "裤装"),
        category("skirt", "半身裙"), category("dress", "连衣裙"),
        category("apron_cover", "围裙罩衣"), category("sleepwear", "睡衣"),
        category("robe", "长袍"),
    ]),
    folder("outerwear_suits", "外套套装", "◊", "#94cf58", "夹克、大衣、斗篷、披肩、礼服与连体服", [
        category("jacket_coat", "夹克大衣"), category("cape_cloak", "斗篷披肩"),
        category("cardigan_shawl", "开衫披巾"), category("formal_suit", "西装礼服"),
        category("jumpsuit", "连体工装"),
    ]),
    folder("uniform_costume", "制服装扮", "♢", "#86c958", "通用校服、职业制服、军警制服、运动服与主题装扮", [
        category("school_uniform", "校服款式"),
        category("sailor_uniform", "水手服"),
        category("service_uniform", "服务制服"), category("occupation_uniform", "职业制服"),
        category("military_uniform", "军警制服"), category("sports_uniform", "运动服"),
        category("themed_costume", "主题装扮"),
    ]),
    folder("franchise_clothes", "作品服装", "☆", "#80c95f", "动漫、游戏等作品中的专属校服、制服、舞台服与套装", [
        category("school_variant", "作品校服"), category("franchise_uniform", "作品制服"),
        category("idol_outfit", "偶像舞台服"), category("franchise_outfit", "作品套装"),
        category("franchise_swim", "作品泳装"), category("franchise_armor", "作品盔甲"),
    ]),
    folder("traditional_clothes", "传统服饰", "⌘", "#7ec568", "按国家和地区整理的传统、民族与历史服饰", [
        category("traditional_japan", "日本服饰"), category("traditional_china", "中国服饰"),
        category("traditional_korea", "韩国服饰"), category("traditional_se_asia", "东南亚服饰"),
        category("traditional_europe", "欧洲服饰"), category("traditional_americas", "美洲服饰"),
        category("traditional_other", "其他传统服饰"),
    ]),
    folder("protective_clothes", "盔甲护具", "⬡", "#78bd72", "盔甲、头盔与功能防护装备", [
        category("full_armor", "铠甲"), category("torso_armor", "胸甲"),
        category("shoulder_armor", "肩甲"), category("arm_armor", "手臂护具"),
        category("leg_armor", "下肢护具"), category("flexible_armor", "柔性护甲"),
        category("combat_helmet", "战斗头盔"), category("civilian_helmet", "头戴装备"),
        category("protective_suit", "防护服"),
    ]),
    folder("underwear_swim", "内衣泳装", "◈", "#ef8f9f", "胸衣、内裤、泳装与紧身衣", [
        category("bra_lingerie", "胸衣内衣"), category("panties_underwear", "内裤"),
        category("bodysuit_leotard", "紧身连体衣"), category("bikini", "比基尼"),
        category("onepiece_swim", "连体泳衣"), category("school_swim", "校园泳装"),
        category("male_swim", "男式泳装"), category("highleg_swim", "高叉泳装"),
        category("other_swim", "其他泳装"),
    ]),
    folder("legwear_footwear", "鞋袜", "◫", "#72c779", "袜类、腿部穿戴、鞋与靴", [
        category("socks", "短袜"), category("stockings", "长袜裤袜"),
        category("heels", "高跟鞋"), category("casual_shoes", "普通鞋履"),
        category("sandals_slippers", "凉鞋拖鞋"), category("traditional_shoes", "传统鞋履"),
        category("sports_shoes", "运动鞋履"), category("short_boots", "靴子"),
        category("work_special_shoes", "特殊鞋履"),
    ]),
    folder("clothing_appearance", "服装属性", "⌁", "#b8d06a", "服装的颜色、图案、材质、风格与穿着状态", [
        category("clothing_color", "服装颜色"), category("clothing_pattern", "图案印花"),
        category("clothing_material", "面料材质"), category("fashion_style", "穿衣风格"),
        category("damaged_dirty", "破损脏污"), category("unworn_missing", "未穿缺失"),
        category("open_wear", "开合状态"),
    ]),
    folder("clothing_detail", "服装剪裁", "⌁", "#b4ce68", "服装的版型、袖领、肩带、开衩、扣件与装饰结构", [
        category("silhouette_fit", "版型轮廓"),
        category("sleeve_detail", "袖型"), category("collar_detail", "领口"), category("strap_detail", "绑带肩带"),
        category("cutout_slit", "镂空开衩"), category("fastener", "扣链结构"),
        category("trim_detail", "花边饰边"), category("pocket_detail", "口袋细节"),
        category("other_structure", "其他款式"),
    ]),
    folder("head_accessories", "头部配饰", "✦", "#e3c459", "发饰、帽子、头巾、冠饰、眼镜与面罩", [
        category("hairband_ribbon", "发带蝴蝶结"), category("hairclip_pin", "发夹与发簪"),
        category("hairtie_ring", "束发饰品"), category("wig_hairpiece", "假发与发套"),
        category("themed_hair_ornament", "造型发饰"),
        category("hats_caps", "帽子"),
        category("headwrap_veil", "头巾面纱"), category("headpiece", "冠饰头饰"),
        category("eyewear", "眼镜"), category("face_mask", "面罩"),
    ]),
    folder("jewelry_accessories", "首饰珠宝", "◇", "#dfbd59", "耳饰、项链、戒指、手足饰、穿孔与宝石饰品", [
        category("earrings", "耳饰"), category("necklace_choker", "项链颈饰"),
        category("rings", "戒指"), category("bracelet_anklet", "手足饰"),
        category("piercing", "身体穿孔"), category("gem_brooch", "宝石胸针"),
    ]),
    folder("accessories", "穿戴配饰", "✧", "#d8bd5c", "领饰、手套、包袋、腰带、徽章与其他随身装饰", [
        category("neckwear", "领巾领带"),
        category("handwear", "手套腕带"), category("bags_belts", "包袋腰带"),
        category("bows_ribbons", "蝴蝶结丝带"), category("badges_ornaments", "徽章饰物"),
        category("other_accessory", "其他配饰"),
    ]),
    folder("weapons", "武器", "⚔", "#ef765f", "冷兵器、枪械、弓箭、爆炸物、盾牌与武器部件", [
        category("blade", "刀剑"), category("firearm", "枪械"),
        category("bow", "弓弩"), category("polearm", "长柄"), category("blunt_chain", "钝器链鞭"),
        category("magic_weapon", "幻想武器"), category("explosive", "爆炸重武"),
        category("shield", "盾牌"), category("weapon_parts", "武器部件"),
        category("other_weapon", "其他武器"),
    ]),
    folder("food_drink", "食品饮料", "◍", "#e7a75b", "食材、料理、甜点、水果、饮料与餐具", [
        category("staple_food", "主食料理"), category("bakery", "面包面点"),
        category("meat_seafood", "肉类海鲜"), category("dairy_ingredient", "蛋奶食材"),
        category("seasoning", "调味食材"),
        category("dessert_snack", "甜点零食"), category("fruit_vegetable", "果蔬"),
        category("drink", "饮料酒水"), category("tableware", "餐饮器具"),
    ]),
    folder("digital_media", "电子设备", "▦", "#d29a60", "手机、电脑、相机、游戏与影音设备", [
        category("phone_device", "手机电话"), category("game_device", "游戏设备"),
        category("computer_device", "电脑设备"), category("audio_device", "音频设备"),
        category("camera_video", "摄影影像"),
    ]),
    folder("culture_objects", "文化用品", "▤", "#c99562", "书报纸张、文具画具与乐器设备", [
        category("books_paper", "书报纸张"), category("stationery", "文具画具"),
        category("music", "音乐乐器"),
    ]),
    folder("household_objects", "生活用品", "▣", "#c49d73", "家具、灯具、家电、工具、容器与药剂液体", [
        category("seating_table", "桌椅床具"), category("storage_furniture", "家居陈设"),
        category("lighting_clock", "灯具"), category("clock", "时钟"), category("appliance", "家电炉具"),
        category("umbrella_fan", "伞具扇子"), category("rope_lock", "绳链锁具"),
        category("care_cleaning", "清洁护理"), category("tools", "工具器材"),
        category("container", "容器包装"), category("chemical_liquid", "药剂液体"),
        category("other_object", "其他用品"),
    ]),
    folder("transport_play", "交通工具", "◎", "#c88d63", "陆地、空中、水上交通工具与载具部件", [
        category("land_vehicle", "陆地载具"), category("air_vehicle", "飞行器"),
        category("water_vehicle", "水上载具"), category("vehicle_parts", "载具部件"),
    ]),
    folder("recreation", "运动娱乐", "◉", "#c57f68", "体育、游戏、玩具、收藏品与游乐设施", [
        category("sports", "体育用品"), category("games", "游戏牌类"), category("toys", "玩具人偶"),
        category("playground", "游乐设施"),
    ]),
    folder("animal_traits", "动物特征", "♧", "#63ce86", "兽耳、角、尾巴、毛皮、翅膀与鳞爪等特征", [
        category("animal_ears", "兽耳"), category("horns", "角鹿角"), category("tails", "尾巴"),
        category("fur_feature", "毛皮兽征"), category("wing_feather", "翅膀羽毛"),
        category("claw_scale", "爪鳞触手"),
    ]),
    folder("creatures", "动物种类", "♤", "#59c982", "现实动物、幻想生物与其他生物种类", [
        category("mammal", "哺乳动物"),
        category("bird", "鸟类"), category("aquatic", "水生生物"),
        category("insect", "昆虫节肢"), category("reptile", "爬行两栖"),
        category("fantasy_creature", "幻想生物"), category("other_creature", "其他生物"),
    ]),
    folder("nature", "植物矿物", "♣", "#60c97f", "花卉、树木、草本、菌类、奇幻植物与矿物", [
        category("flower_general", "通用花卉"),
        category("flower_species", "花卉品种"),
        category("tree", "树木"), category("foliage_vine", "枝叶藤蔓"),
        category("grass_crop", "草本与菌藻"), category("potted_shrub", "盆栽与灌木"),
        category("unusual_plant", "奇异植物"), category("mineral", "矿物晶体"),
    ]),
    folder("mech_scifi", "机械科幻", "⚙", "#64a9c8", "机器人、机甲、义体、机械与科幻装置", [
        category("robot_android", "机器人"), category("mecha", "机甲"),
        category("cybernetic", "义体改造"), category("machine", "机器零件"),
        category("scifi_device", "科幻装置"),
    ]),
    folder("indoor_scene", "室内场所", "▥", "#61bf91", "住宅房间、公共与商业场所，以及虚拟空间", [
        category("home_room", "住宅房间"), category("public_indoor", "公共室内"),
        category("commercial", "商业场所"), category("virtual_space", "虚拟空间"),
    ]),
    folder("building_parts", "建筑构件", "▥", "#61b7a1", "门窗、楼梯、围栏、通道、梁柱与建筑表面", [
        category("door_window", "门窗出入口"), category("stairs_railing", "楼梯栏杆"),
        category("fence_gate", "围栏大门"), category("bridge_walkway", "桥梁通道"),
        category("roof_exterior", "屋顶外构"), category("frame_structure", "梁柱构架"),
        category("surface", "建筑表面"),
    ]),
    folder("urban_architecture", "城市建筑", "▨", "#5dbb98", "城市街道、住宅、公共建筑、地标与建筑风格", [
        category("urban", "城市街道"),
        category("residential", "住宅建筑"), category("public_building", "各类建筑"),
        category("religious_building", "宗教建筑"), category("tower_landmark", "塔楼与地标"),
        category("architecture_style", "建筑风格"),
    ]),
    folder("outdoor_scene", "自然场景", "▧", "#55cc82", "森林、地貌、水域、天空与户外地点", [
        category("forest_field", "森林田野"), category("mountain_desert", "山地荒漠"),
        category("water_scene", "水域水边"), category("sky_space", "天空宇宙"),
        category("terrain_surface", "地面道路"),
        category("country_region", "国家地区"),
        category("other_scene", "户外地点"),
    ]),
    folder("background", "背景样式", "▦", "#58c68d", "纯色、渐变、图案与抽象画面背景", [
        category("background_plain", "纯色背景"), category("background_pattern", "图案背景"),
    ]),
    folder("time_weather", "时间天气", "☂", "#67b5e8", "昼夜、天气、季节、节庆与时间状态", [
        category("time_day", "昼夜时刻"), category("weather", "天气气象"),
        category("season", "季节"), category("holiday", "节日庆典"), category("calendar", "年代日期"),
    ]),
    folder("composition", "镜头构图", "⌗", "#73a4ff", "景别、视角、布局、焦点与裁切", [
        category("shot", "景别"), category("camera_angle", "镜头角度"),
        category("layout", "画面布局"), category("subject_focus", "主体焦点"), category("focus", "景深模糊"),
        category("border", "边框"), category("framing", "裁切遮挡"), category("viewpoint", "特殊视角"),
    ]),
    folder("light_effect", "光影特效", "☼", "#ff806b", "光照、配色、粒子、烟火与视觉效果", [
        category("lighting", "光照"), category("palette", "配色色调"),
        category("fire_smoke", "火焰烟雾"), category("particles", "粒子漂浮物"),
        category("optical", "光学效果"), category("halo_effect", "光环"),
        category("glow_aura", "发光气场"), category("magic_energy", "魔法能量"),
        category("other_effect", "其他特效"),
    ]),
    folder("style", "画风媒介", "✎", "#bd83f1", "媒介、技法、艺术风格、年代与质量", [
        category("medium", "制作媒介"), category("technique", "绘画技法"),
        category("art_style", "艺术风格"), category("genre", "题材风格"),
        category("era_style", "年代风格"), category("quality", "画面质量"),
        category("photo_3d", "摄影与3D"),
    ]),
    folder("text_meta", "文字界面", "#", "#9aa4b8", "文字、漫画语法、品牌文字与屏幕界面", [
        category("text", "文字语言"),
        category("comic", "漫画拟声"), category("screen_ui", "屏幕界面"), category("brand", "品牌标识"),
    ]),
    folder("symbols", "符号标识", "✣", "#929db2", "几何、乐谱、宗教、星相、旗帜与科学符号", [
        category("general_symbol", "通用符号"),
        category("shape_math", "数学几何"), category("music_symbol", "乐谱符号"),
        category("religious_symbol", "宗教符号"), category("zodiac_symbol", "星相符号"),
        category("flag", "旗帜"), category("emblem", "纹章徽记"),
        category("science_sign", "科学标识"),
    ]),
    folder("meta_info", "创作信息", "※", "#8e9caf", "梗、角色扮演、作品活动、审查与创作数据", [
        category("meme", "梗与戏仿"), category("cosplay", "角色扮演"),
        category("work_event", "作品活动"), category("censorship", "审查遮挡"), category("meta", "创作数据"),
    ]),
    folder("adult_body", "成人身体", "◆", "#e65f78", "身体裸露、衣着走光与按部位整理的成人身体标签", [
        category("adult_nudity", "身体裸露"), category("adult_clothes", "衣着走光"),
        category("penis", "阴茎"), category("testicles", "睾丸"),
        category("vulva", "外阴阴道"), category("clitoris", "阴蒂"),
        category("anus", "肛门"), category("pubic_hair", "阴毛"),
        category("reproductive", "生殖结构"), category("genital_variation", "生殖差异"),
    ]),
    folder("adult", "成人行为", "◇", "#df5b75", "性交、口部、自慰、手部行为与性体液", [
        category("adult_sex", "性交行为"), category("adult_oral", "口交行为"),
        category("adult_self", "自慰"), category("adult_hand", "手部性行为"),
        category("adult_fluid", "性体液"), category("adult_response", "性反应状态"),
        category("adult_suggestive", "性暗示互动"), category("adult_theme", "成人题材"),
    ]),
    folder("adult_kink", "成人偏好", "◈", "#d85770", "束缚、情趣用品、支配关系、穿孔、插入与其他成人偏好", [
        category("adult_bondage", "束缚调教"),
        category("adult_toys", "情趣用品"), category("adult_power", "支配服从"),
        category("adult_piercing", "私密穿孔"), category("adult_insertion", "异物插入"),
        category("adult_excretion", "排泄偏好"), category("adult_fetish", "恋物偏好"),
        category("adult_taboo", "禁忌内容"),
    ]),
    folder("sensitive", "暴力敏感", "!", "#c94f62", "血液、伤亡、肢解、非性拘束与吞噬内容", [
        category("blood", "血液"), category("injury_death", "伤亡自伤"),
        category("gore", "肢解内脏"), category("sexual_violence", "性化暴力"),
        category("restraint", "拘束限制"), category("vore", "吞噬"),
    ]),
    folder("copyright", "作品系列", "©", "#55b8d5", "Danbooru 原始版权/作品标签，按首字母完整归档", ALPHA_CATEGORIES),
    folder("character", "角色名称", "★", "#f0b85a", "Danbooru 原始角色标签，按首字母完整归档", ALPHA_CATEGORIES),
    folder("other", "其他标签", "…", "#8d96a8", "没有足够语义证据时保留在此，避免错误归类", OTHER_CATEGORIES),
]


# Display order follows the way a prompt is normally assembled: establish the
# subject and source first, then appearance/action, clothing, props, setting,
# visual treatment, and finally restricted or fallback content.
FOLDER_ORDER = [
    "people", "copyright", "character", "relationships", "themes",
    "body", "body_detail", "face", "hair", "expression", "pose", "action",
    "clothes_main", "outerwear_suits", "uniform_costume", "franchise_clothes", "traditional_clothes",
    "protective_clothes", "underwear_swim", "legwear_footwear", "clothing_appearance",
    "clothing_detail", "head_accessories", "jewelry_accessories", "accessories",
    "weapons", "food_drink", "digital_media", "culture_objects", "household_objects",
    "transport_play", "recreation", "animal_traits", "creatures", "nature", "mech_scifi",
    "indoor_scene", "building_parts", "urban_architecture", "outdoor_scene", "background", "time_weather",
    "composition", "light_effect", "style", "text_meta", "symbols", "meta_info",
    "adult_body", "adult", "adult_kink", "sensitive", "other",
]
_folder_order_index = {folder_id: index for index, folder_id in enumerate(FOLDER_ORDER)}
assert len(_folder_order_index) == len(TAXONOMY), "FOLDER_ORDER must list every folder exactly once"
TAXONOMY.sort(key=lambda item: _folder_order_index[item["id"]])


FOLDER_BY_ID = {item["id"]: item for item in TAXONOMY}
CATEGORY_IDS = {item["id"]: {cat["id"] for cat in item["categories"]} for item in TAXONOMY}


# Complete v7 audit of the former 414-item symbol bucket.  Exact membership is
# intentional: ``note`` is a paper note while ``notes`` is musical notation,
# and ``*_zodiac`` depicts a constellation rather than a zodiac glyph.
SYMBOL_LOCATION_SETS = {
    ("text_meta", "shape_math"): {
        "diamond_(shape)", "triangle", "pentagram", "circle", "cube", "hexagram", "x_(symbol)",
        "dotted_line", "hexagon", "infinity_symbol", "square", "spiral", "plus_sign",
        "pyramid_(geometry)", "small_stellated_dodecahedron", "rectangle", "stellated_octahedron",
        "octagram", "length_markings", "omega_symbol", "lambda_symbol", "minus_sign",
    },
    ("text_meta", "music_symbol"): {
        "musical_note", "eighth_note", "beamed_eighth_notes", "treble_clef", "musical_staff",
        "quarter_note", "beamed_sixteenth_notes", "bass_clef", "sixteenth_note", "half_note",
        "sharp_sign", "notes", "flat_sign", "quarter_rest", "eighth_rest", "whole_note",
        "dotted_quarter_note", "natural_sign", "forte_(symbol)",
    },
    ("text_meta", "religious_symbol"): {
        "cross", "yin_yang", "latin_cross", "inverted_cross", "ankh", "star_of_david", "swastika",
        "trigram", "triquetra", "greek_cross", "celtic_cross", "ouroboros", "good_fortune_symbol",
        "inverted_pentagram", "bagua", "mandala", "star_and_crescent", "large_cross",
        "flamel_symbol", "wheel_of_dharma", "endless_knot",
    },
    ("text_meta", "zodiac_symbol"): {
        "chinese_zodiac", "mars_symbol", "venus_symbol", "zodiac", "gemini_(symbol)", "zodiac_wheel",
        "cancer_(symbol)", "scorpio_(symbol)", "aquarius_(symbol)", "leo_(symbol)", "libra_(symbol)",
        "pisces_(symbol)", "taurus_(symbol)", "virgo_(symbol)", "aries_(symbol)",
        "capricorn_(symbol)", "sagittarius_(symbol)", "jupiter_symbol", "mercury_symbol",
        "saturn_symbol", "neptune_symbol", "uranus_symbol",
    },
    ("text_meta", "science_sign"): {
        "red_cross", "chemical_structure", "radiation_symbol", "star_of_life", "recycling_symbol",
        "dna", "atom", "biohazard_symbol", "rod_of_asclepius",
    },
    ("text_meta", "flag"): {
        "flag", "american_flag", "banner", "string_of_flags", "union_jack", "japanese_flag",
        "pennant", "italian_flag", "checkered_flag", "german_flag", "brazilian_flag",
        "rising_sun_flag", "french_flag", "white_flag", "russian_flag", "ukrainian_flag",
        "mini_flag", "red_flag", "transgender_flag", "z_flag", "battle_standard", "rainbow_flag",
        "south_korean_flag", "canadian_flag", "swedish_flag", "race_flag", "lesbian_flag",
        "people's_republic_of_china_flag", "soviet_flag", "signal_flag", "swiss_flag",
        "flag_on_vehicle", "indonesian_flag", "finnish_flag", "republic_of_china_flag", "war_flag",
        "mexican_flag", "argentinian_flag", "australian_flag", "torn_flag", "numbered_flag",
        "spanish_flag", "bisexual_flag", "polish_flag", "dutch_flag", "english_flag",
        "white_ensign", "green_flag", "norwegian_flag", "belgian_flag",
    },
    ("text_meta", "emblem"): {
        "emblem", "millennium_science_school_logo", "iron_cross", "school_emblem", "japari_symbol",
        "triforce", "poke_ball_symbol", "konohagakure_symbol", "crest", "hammer_and_sickle",
        "sakuramon", "chaldea_logo", "roundel", "family_crest", "oda_uri",
        "rhodes_island_logo_(arknights)", "kikumon", "survey_corps_(emblem)",
        "trinity_general_school_logo", "jolly_roger", "st._gloriana's_(emblem)", "red_star",
        "kamisato_clan_(emblem)", "fleur-de-lis", "batman_symbol", "cross_of_prontera",
        "training_corps_(emblem)", "ooarai_(emblem)", "bc_freedom_(emblem)", "nerv_logo",
        "sakura_empire_(emblem)", "gehenna_academy_logo", "reichsadler", "iron_blood_(emblem)",
        "pravda_(emblem)", "eagle_union_(emblem)", "kuromorimine_(emblem)", "superman_logo",
        "coat_of_arms", "abydos_high_school_logo", "roto's_emblem",
        "japanese_tankery_league_(emblem)", "nasa_logo", "character_logo",
        "royal_navy_emblem_(azur_lane)", "delta_rune_(symbol)", "anzio_(emblem)",
        "saunders_(emblem)", "sanada_clan_(emblem)", "keizoku_(emblem)",
        "selection_university_(emblem)", "straw_hats_jolly_roger", "mega_evolution_symbol",
        "404_logo_(girls'_frontline)", "red_winter_federal_academy_logo", "balkenkreuz",
        "uchiha_symbol", "imperial_aquila", "digital_hazard", "omnitrix_symbol", "arrow_cross",
        "kazimierz_logo", "reunion_logo_(arknights)", "black_bulls_(emblem)", "aquila_(symbol)",
        "kjerag_logo", "sunagakure_symbol", "heart_pirates_jolly_roger",
        "naranja_academy_(emblem)", "skull_and_crossed_swords", "ursus_logo", "fatui_logo",
        "kill_markings", "z_(russian_symbol)", "kirigakure_symbol", "chi-hatan_(emblem)",
        "cross_patty", "uva_academy_(emblem)", "sardegna_empire_(emblem)",
        "northern_parliament_(emblem)", "uzumaki_symbol", "vichya_dominion_(emblem)",
        "bismarck_(coat_of_arms)", "siegrunen", "fairy_tail_logo",
        "whitebeard_pirates_jolly_roger", "iwagakure_symbol", "ultra_instinct_sign",
        "digimon_crest", "iris_libre_(emblem)", "mark_of_the_doom_slayer",
        "wild_hunt_academy_of_arts_logo", "mitsu_uroko", "signet_of_ego",
        "military_police_brigade_(emblem)",
    },
    ("text_meta", "general_symbol"): {
        "heart", "star_(symbol)", "?", "crescent", "!", "arrow_(symbol)", "heart_of_string",
        "barcode", "lightning_bolt_symbol", "tomoe_(symbol)", "mitsudomoe_(shape)", "spade_(shape)",
        "sun_symbol", "flower_symbol", "emoji", "skull_and_crossbones", "qr_code", "broken_heart",
        "club_(shape)", "arrow_through_heart", "androgyne_symbol", "warning_sign", "winged_heart",
        "circled_9", "handprint", "gem_(symbol)", "peace_symbol", "anemo_symbol_(genshin_impact)",
        "hashtag", "seal_impression", "emoticon", "dollar_sign", "pixel_heart", "eye_symbol",
        "stamp_mark", "no_symbol", "yen_sign", "electro_symbol_(genshin_impact)",
        "four-pointed_star", "hydro_symbol_(genshin_impact)", "drawn_heart", "male-female_symbol",
        "cut-here_line", "symbol", "shoshinsha_mark", "celtic_knot", "no_smoking",
        "interlocked_mars_and_venus_symbols", "pyro_symbol_(genshin_impact)", "falling_star",
        "cryo_symbol_(genshin_impact)", "geo_symbol_(genshin_impact)", "japanese_postal_mark",
        "chevron_(symbol)", "crown_(symbol)", "onsen_symbol", "checkmark",
        "dendro_symbol_(genshin_impact)", "drawn_crown", "shooting_star_(symbol)", "compass_rose",
        "@_(symbol)", "rabbit_symbol", "interlocked_venus_symbols", "postmark", "matsu_symbol",
        "o_x", "cat_symbol", "hanamaru",
    },
}

SYMBOL_LOCATION_SETS.update({
    ("text_meta", "brand"): {
        "logo", "patreon_logo", "twitter_logo", "instagram_logo", "twitter_x_logo", "pixiv_logo",
        "facebook_logo", "deviantart_logo", "rhine_lab_logo", "company_logo", "bluesky_logo",
        "youtube_logo", "subscribestar_logo", "dvd_logo", "fanbox_logo", "penguin_logistics_logo",
        "tiktok_logo", "gumroad_logo", "griffin_&_kryuger_logo", "mihuashi_logo", "tumblr_logo",
        "twitch_logo", "playstation_logo", "artstation_logo", "bilibili_logo", "ko-fi_logo",
        "kessoku_band_logo", "discord_logo", "super_smash_bros._logo", "blu-ray_logo",
        "overwatch_(logo)", "lofter_logo", "windows_logo", "endfield_industries_logo",
        "xiaohongshu_logo", "itch.io_logo",
    },
    ("meta_info", "meta"): {
        "watermark", "weibo_watermark", "artist_logo", "sample_watermark", "copyright_logo",
        "watermark_grid", "miyoushe_watermark", "character_watermark", "xiaohongshu_watermark",
    },
    ("text_meta", "screen_ui"): {
        "power_symbol", "icon_(computing)", "loading_icon", "wi-fi_symbol", "playstation_symbols",
        "volume_symbol",
    },
    ("text_meta", "comic"): {"squiggle", "squeans"},
    ("text_meta", "text"): {"runes"},
    ("clothing_detail", "clothing_pattern"): {
        "anchor_symbol", "flag_print", "american_flag_print", "brazilian_flag_print", "no_emblem",
        "italian_flag_print", "argentinian_flag_print", "german_flag_print", "japanese_flag_print",
    },
    ("outdoor_scene", "sky_space"): {
        "aquarius_(zodiac)", "capricorn_(zodiac)", "gemini_(zodiac)", "aries_(zodiac)",
        "cancer_(zodiac)", "libra_(zodiac)", "leo_(zodiac)", "pisces_(zodiac)",
        "sagittarius_(zodiac)", "scorpio_(zodiac)", "taurus_(zodiac)", "virgo_(zodiac)",
    },
    ("indoor_scene", "urban"): {
        "road_sign", "stop_sign", "no_entry_sign", "no_parking_sign", "bus_stop_sign",
        "speed_limit_sign", "crossbuck", "one_way_sign",
    },
    ("indoor_scene", "commercial"): {"chalkboard_sign", "neon_sign", "hanging_sign", "open_sign"},
    ("indoor_scene", "public_indoor"): {
        "exit_sign", "restroom_symbol", "men's_toilet_symbol", "emergency_exit", "women's_toilet_symbol",
    },
    ("household_objects", "other_object"): {"sign", "sticker"},
    ("culture_objects", "books_paper"): {"note", "eye_chart"},
    ("transport_play", "land_vehicle"): {"license_plate"},
    ("recreation", "games"): {"the_magician_(tarot)"},
    ("accessories", "badges_ornaments"): {"military_rank_insignia", "ss_insignia", "navy_cross"},
    ("adult", "adult_fetish"): {"race_fetishism_symbol", "queen_of_spades_symbol"},
    ("adult", "adult_suggestive"): {"phallic_symbol", "yonic_symbol", "omanko_mark"},
    ("face", "eye_shape"): {"+_-"},
})

# Small v10 corrections found by the second-pass semantic audit.  These are
# intentionally exact: each term is a known homonym or a tag that the broad
# legacy classifier could not place safely from fragments alone.
V10_EXACT_LOCATIONS = {
    "barioth_(armor)": ("franchise_clothes", "franchise_armor"),
    "nargacuga_(armor)": ("franchise_clothes", "franchise_armor"),
    "kamura_(armor)": ("franchise_clothes", "franchise_armor"),
    "lagombi_(armor)": ("franchise_clothes", "franchise_armor"),
    "rathalos_(armor)": ("franchise_clothes", "franchise_armor"),
    "zinogre_(armor)": ("franchise_clothes", "franchise_armor"),
    "infinity_gauntlet": ("franchise_clothes", "franchise_armor"),
    "armored_corset": ("protective_clothes", "torso_armor"),
    "armored_trooper": ("people", "role_focus"),
    "asari_(mass_effect)": ("people", "fantasy_person"),
    "lily_servant": ("people", "role_focus"),
    "single_gauntlet": ("protective_clothes", "arm_armor"),
    "armored_gloves": ("protective_clothes", "arm_armor"),
    "clawed_gauntlets": ("protective_clothes", "arm_armor"),
    "spiked_gauntlets": ("protective_clothes", "arm_armor"),
    "black_gauntlets": ("protective_clothes", "arm_armor"),
    "gold_gauntlets": ("protective_clothes", "arm_armor"),
    "elbow_gauntlets": ("protective_clothes", "arm_armor"),
    "barred_window": ("building_parts", "door_window"),
    "elevator_door": ("building_parts", "door_window"),
    "picket_fence": ("building_parts", "fence_gate"),
    "post_and_rail_fence": ("building_parts", "fence_gate"),
    "trap_door": ("building_parts", "door_window"),
    "breaking_through_window": ("action", "combat_action"),
    "on_fence": ("pose", "stationary_pose"),
    "on_windowsill": ("pose", "stationary_pose"),
    "tokyo_skytree": ("urban_architecture", "tower_landmark"),
    "churchill_(tank)": ("transport_play", "land_vehicle"),
    "cornflower": ("nature", "flower_species"),
    "dead_plants": ("nature", "flower_general"),
    "erdtree_(elden_ring)": ("nature", "unusual_plant"),
    "leaf_on_liquid": ("nature", "foliage_vine"),
    "leaf_pile": ("nature", "foliage_vine"),
    "sunflower_seed": ("nature", "grass_crop"),
    "plant_on_head": ("head_accessories", "themed_hair_ornament"),
    "flower_pin": ("head_accessories", "hairclip_pin"),
    "bamboo_slips": ("culture_objects", "books_paper"),
    "tree-topper": ("household_objects", "other_object"),
    "flower_underskirt": ("clothing_detail", "trim_detail"),
    "flower_wrapper": ("household_objects", "container"),
    "flower_tact": ("weapons", "magic_weapon"),
    "roseate_desire_(e.g.o)": ("weapons", "magic_weapon"),
    "flower_swing": ("recreation", "toys"),
    "planted_arrow": ("weapons", "bow"),
    "kusarigama": ("weapons", "blunt_chain"),
    "planted_shovel": ("household_objects", "tools"),
    "lily_white_(love_live!)": ("relationships", "group_faction"),
    "roselia_(bang_dream!)": ("relationships", "group_faction"),
    "cooperative_pussyjob": ("adult", "adult_sex"),
    "non-pubic_inmon": ("body_detail", "tattoo_mark"),
    "used_artificial_vagina": ("adult_kink", "adult_toys"),
    "bikini_in_mouth": ("action", "holding"),
    "guilty_gear_strive_x_tower_records": ("franchise_clothes", "franchise_outfit"),
    "character_costume": ("uniform_costume", "themed_costume"),
    "unofficial_precure_costume": ("franchise_clothes", "franchise_outfit"),
    "tracen_ondo_outfit_(umamusume)": ("franchise_clothes", "franchise_outfit"),
    "bokura_wa_ima_no_naka_de": ("franchise_clothes", "idol_outfit"),
    "dream_believers": ("franchise_clothes", "idol_outfit"),
    "starry_sky_bright_(idolmaster)": ("franchise_clothes", "idol_outfit"),
    "takaramonozu": ("franchise_clothes", "idol_outfit"),
    "rough_time_school_(idolmaster)": ("franchise_clothes", "idol_outfit"),
    "companion/af": ("franchise_clothes", "franchise_outfit"),
    "kuuhaku_to_catharsis": ("franchise_clothes", "franchise_outfit"),
    "no_thank_you!_(k-on!)": ("franchise_clothes", "franchise_outfit"),
    "anna_miller": ("uniform_costume", "service_uniform"),
    "medical_scrubs": ("uniform_costume", "occupation_uniform"),
    "outfit_connection": ("themes", "character_connection"),
    "ironmouse_outfit_art_contest": ("meta_info", "meta"),
    "elden_ring_(object)": ("symbols", "religious_symbol"),
    "ring_(identity)_(project_moon)": ("themes", "persona_variant"),
    "ring_(sonic)": ("recreation", "games"),
    "maria_the_ripper": ("character", "letter_m"),
    "meslamtaea_(fate)": ("character", "letter_m"),
    "mood_(umamusume)": ("character", "letter_m"),
    "hasu_no_shousankaku": ("copyright", "letter_h"),
    "four_of_a_kind_(touhou)": ("themes", "persona_variant"),
    "bankai": ("themes", "persona_variant"),
    "legendary_super_saiyan": ("themes", "persona_variant"),
    "terastallization": ("themes", "persona_variant"),
    "substitute_(pokemon)": ("themes", "persona_variant"),
    "gattai": ("themes", "identity_change"),
    "nt-d": ("themes", "persona_variant"),
    "life_fiber": ("clothing_appearance", "clothing_material"),
    "orange_shrug": ("outerwear_suits", "cardigan_shawl"),
    "black_tabard": ("outerwear_suits", "cape_cloak"),
    "peplos": ("traditional_clothes", "traditional_europe"),
    "menpoo": ("protective_clothes", "combat_helmet"),
    "air_jordan_1": ("legwear_footwear", "sports_shoes"),
    "christian_louboutin_(brand)": ("text_meta", "brand"),
    "slides": ("legwear_footwear", "sandals_slippers"),
    "la_chancla": ("legwear_footwear", "sandals_slippers"),
    "on_mushroom": ("pose", "body_pose"),
    "super_leaf_(transformation)": ("themes", "persona_variant"),
    "spirit_blossom_(league_of_legends)": ("themes", "persona_variant"),
    "aurora_flower_(love_live!)": ("franchise_clothes", "idol_outfit"),
    "vital_sunflower_(idolmaster)": ("franchise_clothes", "idol_outfit"),
    "fire_flower": ("recreation", "games"),
    "1-up_mushroom": ("recreation", "games"),
    "shroud_of_magdalene": ("weapons", "magic_weapon"),
    "invisible_air_(fate)": ("weapons", "magic_weapon"),
    "bolverk": ("weapons", "firearm"),
    "kagune_(tokyo_ghoul)": ("weapons", "magic_weapon"),
    "fin_funnels": ("mech_scifi", "scifi_device"),
    "walther_ppk": ("weapons", "firearm"),
    "ak-74": ("weapons", "firearm"),
    "l85": ("weapons", "firearm"),
    "famas": ("weapons", "firearm"),
    "arrow_in_head": ("sensitive", "injury_death"),
    "sword_in_head": ("sensitive", "injury_death"),
    "sword_to_throat": ("action", "combat_action"),
    "amos'_bow_(genshin_impact)": ("weapons", "bow"),
    "palutena_bow_(kid_icarus)": ("weapons", "bow"),
    "arrow_(jojo)": ("weapons", "magic_weapon"),
    "heart_arrow": ("weapons", "bow"),
    "flaming_arrow": ("weapons", "bow"),
    "sword_hilt": ("weapons", "blade"),
    "spear_of_cassius": ("weapons", "polearm"),
    "cloud_hair": ("hair", "hair_style"),
    "claw_hair_clip": ("head_accessories", "hairclip_pin"),
    "bouncing_hair": ("hair", "hair_action"),
    "hair_wagging": ("hair", "hair_action"),
    "hair_visible_through_wig": ("hair", "hair_action"),
    "hair_half_over_shoulder": ("hair", "hair_style"),
    "hair_around_horn": ("hair", "hair_style"),
    "hair_sprinkles": ("head_accessories", "themed_hair_ornament"),
    "stray_hair": ("hair", "hair_style"),
    "paint_in_hair": ("hair", "hair_action"),
    "kinky_hair": ("hair", "hair_style"),
    "lion_hair": ("hair", "hair_style"),
    "metal_hair": ("hair", "hair_style"),
    "slime_hair": ("hair", "hair_style"),
    "iridescent_hair": ("hair", "hair_color"),
    "polka_dot_hair": ("hair", "hair_color"),
    "three-tone_hair": ("hair", "hair_color"),
    "knuckle_hair": ("body_detail", "body_hair"),
    "single_empty_eye": ("face", "eye_shape"),
    "single_blank_eye": ("face", "eye_shape"),
    "butterfly_over_eye": ("face", "eye_shape"),
    "butterfly_in_eye": ("face", "eye_shape"),
    "condom_in_hair": ("adult_kink", "adult_fetish"),
    "hair_over_crotch": ("adult_body", "adult_nudity"),
    "jack_daniel's": ("text_meta", "brand"),
    "subaru_(brand)": ("text_meta", "brand"),
    "juubako": ("household_objects", "container"),
    "blister_pack": ("household_objects", "container"),
    "furoshiki_around_neck": ("accessories", "bags_belts"),
    "rin's_pendant_(fate)": ("jewelry_accessories", "necklace_choker"),
    "incoming_call": ("digital_media", "phone_device"),
    "playstation_4": ("digital_media", "game_device"),
    "wii": ("digital_media", "game_device"),
    "lcl": ("mech_scifi", "scifi_device"),
    "vernier_thrusters": ("mech_scifi", "machine"),
    "minecraft_pickaxe": ("household_objects", "tools"),
    "stepladder": ("household_objects", "tools"),
    "pestle": ("household_objects", "tools"),
    "gavel": ("household_objects", "tools"),
    "set_square": ("culture_objects", "stationery"),
    "bachi": ("culture_objects", "music"),
    "french_horn": ("culture_objects", "music"),
    "accordion": ("culture_objects", "music"),
    "bunbunmaru": ("culture_objects", "books_paper"),
    "hurricane_glass": ("food_drink", "tableware"),
    "model": ("recreation", "toys"),
    "fuwapuchi": ("recreation", "toys"),
    "shogi_piece": ("recreation", "games"),
    "tenbou": ("recreation", "games"),
    "gnosis_(genshin_impact)": ("recreation", "games"),
    "print_innertube": ("recreation", "sports"),
    "nobori": ("symbols", "flag"),
    "double_helix": ("symbols", "science_sign"),
    "totenkopf": ("symbols", "emblem"),
    "gold_bar": ("nature", "mineral"),
    "lunar_tear": ("nature", "unusual_plant"),
    "orange_tulip": ("nature", "flower_species"),
    "herb": ("nature", "grass_crop"),
    "chikuwa": ("food_drink", "meat_seafood"),
    "wafer": ("food_drink", "dessert_snack"),
    "peanut": ("food_drink", "fruit_vegetable"),
    "shiruko_(food)": ("food_drink", "staple_food"),
    "oreo": ("food_drink", "dessert_snack"),
    "scone": ("food_drink", "bakery"),
    "kyoto": ("urban_architecture", "urban"),
    "construction_site": ("urban_architecture", "urban"),
    "yakiniku": ("indoor_scene", "commercial"),
    "gensokyo": ("outdoor_scene", "other_scene"),
    "astral_express_(honkai:_star_rail)": ("transport_play", "land_vehicle"),
    "bluebird": ("creatures", "bird"),
    "crab_on_head": ("creatures", "aquatic"),
    "molcar": ("creatures", "fantasy_creature"),
    "hrothgar": ("people", "fantasy_person"),
    "ena_(species)": ("people", "fantasy_person"),
    "cupid": ("people", "fantasy_person"),
    "pact_holder": ("people", "role_focus"),
    "barbarian": ("people", "role_focus"),
    "neet": ("people", "occupation"),
    "farmer": ("people", "occupation"),
    "sith": ("relationships", "group_faction"),
    "united_states_navy": ("relationships", "group_faction"),
    "straylight_(idolmaster)": ("relationships", "group_faction"),
    "nepolabo": ("relationships", "group_faction"),
    "holopromise": ("relationships", "group_faction"),
    "humming": ("action", "daily_action"),
    "oshikatsu": ("action", "daily_action"),
    "pokemon_on_back": ("action", "interaction"),
    "apple_on_head": ("pose", "body_pose"),
    "through_painting": ("themes", "narrative_situation"),
    "punishment": ("themes", "narrative_situation"),
    "height_conscious": ("themes", "narrative_situation"),
    "tsukimi": ("time_weather", "holiday"),
    "oktoberfest": ("time_weather", "holiday"),
    "reiwa": ("time_weather", "calendar"),
    "alchemy": ("light_effect", "magic_energy"),
    "firecrackers": ("weapons", "explosive"),
    "key_in_head": ("body", "anatomy_anomaly"),
    "uwu": ("expression", "positive"),
    "sulking": ("expression", "anger"),
    "disdain": ("expression", "anger"),
    "take_it_home": ("expression", "positive"),
    "eargasm": ("adult", "adult_response"),
    "downpants": ("clothing_appearance", "open_wear"),
    "pee_puddle": ("adult", "adult_fluid"),
    "soapland": ("adult", "adult_theme"),
    "nyotaimori": ("adult", "adult_theme"),
    "ruined_for_marriage": ("adult", "adult_theme"),
    "sexual_exercising": ("adult", "adult_sex"),
    "neglect_play": ("adult_kink", "adult_bondage"),
    "all_the_way_through": ("adult_kink", "adult_insertion"),
    "tube_chastity_cage": ("adult_kink", "adult_toys"),
    "wrapped_up": ("sensitive", "restraint"),
    "omake": ("meta_info", "meta"),
    "reflected_worlds": ("meta_info", "meta"),
    "you_work_you_lose": ("meta_info", "meme"),
    "pet_shaming": ("meta_info", "meme"),
    "sponsor": ("meta_info", "meme"),
    "equipment_layout": ("composition", "layout"),
    "rogues'_gallery": ("composition", "layout"),
    "anatomy": ("style", "technique"),
    "idea": ("text_meta", "comic"),
    "ara_ara": ("text_meta", "comic"),
    "pan-pa-ka-paaan!": ("text_meta", "comic"),
}


# v13: explicit semantic moves that must survive chained normalization.  Some
# of these tags enter through the old broad ``helmet_protective`` bucket; an
# exact final location prevents a second normalization pass from collapsing
# them back into generic full-body armor.
V13_EXACT_LOCATIONS = {
    "knee_pads": ("protective_clothes", "leg_armor"),
    "single_knee_pad": ("protective_clothes", "leg_armor"),
    "knee_guards": ("protective_clothes", "leg_armor"),
    "knee_brace": ("protective_clothes", "leg_armor"),
    "shin_guards": ("protective_clothes", "leg_armor"),
    "arm_guards": ("protective_clothes", "arm_armor"),
    "single_arm_guard": ("protective_clothes", "arm_armor"),
    "elbow_pads": ("protective_clothes", "arm_armor"),
    "single_elbow_pad": ("protective_clothes", "arm_armor"),
    "wrist_guards": ("protective_clothes", "arm_armor"),
    "shoulder_pads": ("protective_clothes", "shoulder_armor"),
    "chest_guard": ("protective_clothes", "torso_armor"),
    "chest_protector": ("protective_clothes", "torso_armor"),
    "cast": ("body_detail", "bandage_patch"),
    "arm_sling": ("body_detail", "bandage_patch"),
    "leg_cast": ("body_detail", "bandage_patch"),
    "respirator": ("protective_clothes", "civilian_helmet"),
    "ear_protection": ("protective_clothes", "civilian_helmet"),
    "flak_jacket": ("protective_clothes", "protective_suit"),
    "bulletproof_vest": ("protective_clothes", "protective_suit"),
    "power_suit": ("protective_clothes", "protective_suit"),
    "power_armor": ("protective_clothes", "protective_suit"),
    "powered_armor": ("protective_clothes", "protective_suit"),
    "mechanical_armor": ("protective_clothes", "protective_suit"),
    "springsuit": ("protective_clothes", "protective_suit"),
    "highleg_springsuit": ("protective_clothes", "protective_suit"),
    "battlesuit": ("protective_clothes", "protective_suit"),
    "armored_bodysuit": ("protective_clothes", "protective_suit"),
    "armored_leotard": ("protective_clothes", "protective_suit"),
    # "living armor" describes a sentient armor species rather than equipment
    # being worn by a character.
    "living_armor": ("people", "fantasy_person"),
    "broken_armor": ("clothing_appearance", "damaged_dirty"),
    "load_bearing_equipment": ("accessories", "bags_belts"),
    "sneaking_suit": ("franchise_clothes", "franchise_outfit"),
}

V14_EXACT_LOCATIONS = {
    # This tag describes thigh-high socks being worn underneath boots, not a
    # boot shaft length.
    "thighhighs_under_boots": ("legwear_footwear", "stockings"),
    "bootjob": ("adult", "adult_sex"),
}


def _normalize_location_once(location: tuple[str, str], tag_name: str = "") -> tuple[str, str]:
    """Map legacy classifier targets into the refined display taxonomy."""
    folder_id, category_id = location
    name = tag_name.lower()
    base_name = re.sub(r"_\([^)]*\)$", "", name)
    tokens = {item for item in re.split(r"[_()\-/' ]+", base_name) if item}

    if name in V13_EXACT_LOCATIONS:
        return V13_EXACT_LOCATIONS[name]
    if name in V14_EXACT_LOCATIONS:
        return V14_EXACT_LOCATIONS[name]

    if folder_id == "clothing_state" and category_id in {"damaged_dirty", "unworn_missing", "open_wear"}:
        return "clothing_appearance", category_id
    if folder_id == "nature" and category_id == "rose":
        return "nature", "flower_species"
    if folder_id in {"indoor_scene", "urban_architecture"} and category_id == "surface":
        return "building_parts", "surface"
    if folder_id == "building_parts" and category_id == "surface":
        return "building_parts", "surface"

    # v12: stains, paint and small stickers are all temporary material attached
    # to the body.  The former seven-item decoration bucket duplicated the
    # adjacent stain bucket without offering a useful selection boundary.
    if category_id == "surface_decor" and folder_id in {"body", "body_detail"}:
        return "body_detail", "surface_stain"

    if name in V10_EXACT_LOCATIONS:
        return V10_EXACT_LOCATIONS[name]

    # v10: user-facing splits.  Each family is routed before the stable-folder
    # guard so builtin tags, exact overrides and older saved locations all use
    # the same semantic rules.
    if category_id in {"hair_accessory", "hairband_ribbon", "hairclip_pin", "hairtie_ring", "flower_hairpiece", "wig_hairpiece", "themed_hair_ornament"} and folder_id in {
        "accessories", "head_accessories",
    }:
        if any(part in base_name for part in ("wrist_scrunchie", "arm_scrunchie")):
            return "accessories", "handwear"
        if any(part in base_name for part in ("ankle_scrunchie", "thigh_scrunchie", "ear_scrunchie")):
            return "accessories", "other_accessory"
        if any(part in base_name for part in ("unworn_hair", "no_hair_ornament", "no_hairband", "no_hair_bow", "removed_hair")):
            return "clothing_state", "unworn_missing"
        if any(part in base_name for part in ("torn_hair_ribbon", "broken_hair")):
            return "clothing_state", "damaged_dirty"
        if any(part in base_name for part in (
            "hairclip", "hair_clip", "hairpin", "bobby_pin", "kanzashi", "hair_stick",
            "hairpin", "hirabitai", "motoyui", "hair_flower", "flower_in_hair", "flower_in_braid", "flower_braid",
        )) or re.search(r"(^|_)pin($|_)", base_name):
            return "head_accessories", "hairclip_pin"
        if any(part in base_name for part in (
            "hair_tie", "hairtie", "scrunchie", "hair_ring", "hair_bobble", "hair_bead",
            "hair_tube", "ponytail_holder",
        )):
            return "head_accessories", "hairtie_ring"
        if any(part in base_name for part in (
            "hairpiece", "wig", "hair_extension", "bun_cover", "hair_net", "fake_hair_bun",
        )):
            return "head_accessories", "wig_hairpiece"
        if any(part in base_name for part in ("hairband", "headband", "hair_ribbon", "hair_bow", "head_bow", "ribbon_in_braid", "ribbon_braid")):
            return "head_accessories", "hairband_ribbon"
        return "head_accessories", "themed_hair_ornament"

    if category_id in {"school_variant", "franchise_uniform"} and folder_id in {
        "clothes_special", "uniform_costume", "franchise_clothes",
    }:
        generic_school_variants = {
            "tactical_school_uniform", "indonesian_high_school_uniform", "thai_school_uniform", "soviet_school_uniform",
        }
        if category_id == "school_variant" and base_name in generic_school_variants:
            return "uniform_costume", "school_uniform"
        generic_uniforms = {
            "adapted_uniform", "band_uniform", "fast_food_uniform", "white_uniform", "alternate_uniform",
            "expedition_uniform", "scout_uniform",
        }
        if category_id == "franchise_uniform" and base_name in generic_uniforms:
            if base_name == "fast_food_uniform":
                return "uniform_costume", "service_uniform"
            return "uniform_costume", "occupation_uniform"
        return "franchise_clothes", category_id

    if category_id in {"idol_outfit", "franchise_outfit", "franchise_swim", "franchise_armor"}:
        return "franchise_clothes", category_id

    if category_id == "character_costume" and folder_id == "franchise_clothes":
        if "precure" in base_name:
            return "franchise_clothes", "franchise_outfit"
        return "uniform_costume", "themed_costume"

    if category_id == "themed_costume" and folder_id in {"clothes_special", "uniform_costume"}:
        idol_words = ("love_live", "hololive", "umamusume", "idolmaster", "idol_heart_incom", "happy_party_train")
        if base_name == "unofficial_precure_costume":
            return "franchise_clothes", "franchise_outfit"
        if any(word in name for word in idol_words):
            return "franchise_clothes", "idol_outfit"
        if base_name in {"workout_clothes", "ballet_class_clothes", "riding_outfit"}:
            return "uniform_costume", "sports_uniform"
        named_franchise_outfits = {
            "kourindou_tengu_costume", "gerudo_set", "archaic_set", "danganronpa_10th_anniversary_costume",
            "order_suit", "pearl_clan_outfit", "anglerfish_costume", "sanbaka_anniversary_outfit",
            "elmo_dormitory_outfit", "keisanchuu_new_costume", "princess_rosa_costume",
            "yd_dancer_outfit", "desert_voe_set", "sage_outfit",
        }
        if re.search(r"_\([^)]*\)$", name) or base_name in named_franchise_outfits:
            return "franchise_clothes", "franchise_outfit"

    traditional_categories = {
        "traditional_east", "traditional_world", "traditional_japan", "traditional_china",
        "traditional_korea", "traditional_india", "traditional_se_asia", "traditional_central_west",
        "traditional_europe", "traditional_americas", "traditional_africa", "traditional_other",
    }
    if category_id in traditional_categories and folder_id in {"clothes_special", "traditional_clothes"}:
        if any(word in base_name for word in (
            "kimono", "yukata", "hakama", "haori", "miko", "shinto", "japanese", "japan_",
            "ainu", "uchikake", "furisode", "junihitoe", "kariginu", "sokutai", "jinbei",
            "obi", "hagoromo", "kappougi", "juban", "happi", "kesa", "hanten", "chihaya",
            "kosode", "shiromuku", "kataginu", "jinbaori", "chanchanko", "dotera", "karaginu_mo", "fundoshi", "shiroshouzoku",
        )):
            return "traditional_clothes", "traditional_japan"
        if any(word in base_name for word in (
            "hanfu", "china_dress", "chinese", "tangzhuang", "changpao", "qipao", "cheongsam",
            "ruqun", "aoqun", "mamian", "dudou", "miao_clothes", "tibetan_clothes",
            "yuanlingpao", "qi_lolita", "zhijupao", "yunjian", "mian_guan", "daxiushan",
        )):
            return "traditional_clothes", "traditional_china"
        if any(word in base_name for word in ("hanbok", "korean", "jeogori", "chima")):
            return "traditional_clothes", "traditional_korea"
        if any(word in base_name for word in ("sari", "saree", "indian", "lehenga", "salwar", "dhoti")):
            return "traditional_clothes", "traditional_other"
        if any(word in base_name for word in (
            "ao_dai", "vietnam", "thai_", "thailand", "indonesian", "malay", "filipino", "baro't_saya", "sarong",
        )):
            return "traditional_clothes", "traditional_se_asia"
        if any(word in base_name for word in (
            "mongol", "kazakh", "uzbek", "arab", "persian", "turkish", "kaftan", "keffiyeh", "middle_eastern", "central_asian",
        )):
            return "traditional_clothes", "traditional_other"
        if any(word in base_name for word in (
            "dirndl", "kilt", "toga", "roman", "greek", "german", "slavic", "russian", "ukrainian",
            "renaissance", "victorian", "european", "medieval", "folk_dress", "chiton", "himation",
        )):
            return "traditional_clothes", "traditional_europe"
        if any(word in base_name for word in (
            "native_american", "aztec", "mayan", "mexican", "colombian", "andean", "inca", "american_indian",
        )):
            return "traditional_clothes", "traditional_americas"
        if any(word in base_name for word in ("african", "egyptian", "masai", "maasai", "zulu")):
            return "traditional_clothes", "traditional_other"
        return "traditional_clothes", "traditional_other"

    armor_categories = {
        "armor", "helmet", "helmet_protective", "torso_armor", "shoulder_armor", "arm_armor",
        "leg_armor", "full_armor", "flexible_armor", "powered_armor", "combat_helmet", "civilian_helmet",
        "pads_support", "protective_suit",
    }
    if category_id in armor_categories and folder_id in {"legwear_footwear", "clothes_special", "protective_clothes"}:
        franchise_armor_names = {
            "saiyan_armor", "kirin", "kavacha", "gold_saint", "integrity_knight_armor",
            "berserker_armor", "christmas_nightmare", "twilight", "terminator_armor", "azure",
            "4th_match_flame", "power_armor_(fallout)", "high-cut_armor_(persona)",
        }
        if name in franchise_armor_names or base_name in franchise_armor_names or (
            re.search(r"_\([^)]*\)$", name) and any(word in base_name for word in ("armor", "armour", "combat_suit"))
        ):
            return "franchise_clothes", "franchise_armor"
        franchise_suits = {
            "normal_suit", "deva_battle_suit", "fortified_suit", "gantz_suit", "praetor_suit",
            "planet_diving_suit", "hev_suit", "gravity_suit",
        }
        if category_id in {"helmet_protective", "protective_suit"} and (
            base_name in franchise_suits or (
                re.search(r"_\([^)]*\)$", name) and any(word in base_name for word in ("suit", "clothes", "armor", "armour"))
            )
        ):
            return "franchise_clothes", "franchise_outfit"
        if base_name in {"respirator", "rebreather", "ear_protection"}:
            return "protective_clothes", "civilian_helmet"
        helmet_names = {"helm", "armet", "pickelhaube", "assault_visor", "face_shield"}
        if category_id in {"helmet", "combat_helmet", "civilian_helmet"} or "helmet" in base_name or "kabuto" in base_name or base_name in helmet_names:
            civilian_words = (
                "baseball", "football", "bicycle", "bike_helmet", "motorcycle", "racing", "sports",
                "mining", "construction", "firefighter", "fire_helmet", "hard_hat", "pith_helmet",
                "space_helmet", "diving_helmet", "fishbowl_helmet", "pilot_helmet", "assault_visor", "face_shield",
            )
            if any(word in base_name for word in civilian_words):
                return "protective_clothes", "civilian_helmet"
            return "protective_clothes", "combat_helmet"
        if category_id in {"helmet_protective", "pads_support", "protective_suit"}:
            if base_name in {"cast", "arm_sling", "leg_cast"} or any(word in base_name for word in ("medical_sling", "splint")):
                return "body_detail", "bandage_patch"
            if "shoulder" in base_name:
                return "protective_clothes", "shoulder_armor"
            if any(word in base_name for word in ("arm_", "elbow", "wrist", "forearm")):
                return "protective_clothes", "arm_armor"
            if any(word in base_name for word in ("knee", "shin", "leg_", "thigh", "ankle")):
                return "protective_clothes", "leg_armor"
            if any(word in base_name for word in ("chest_", "torso_")):
                return "protective_clothes", "torso_armor"
            if base_name == "rash_guard":
                return "protective_clothes", "protective_suit"
            return "protective_clothes", "protective_suit"
        if any(word in base_name for word in (
            "pauldron", "shoulder_armor", "shoulder_guard", "shoulder_spike", "shoulder_pad",
            "shoulder_plate", "spauld", "besagew", "sode",
        )):
            return "protective_clothes", "shoulder_armor"
        if any(word in base_name for word in (
            "gauntlet", "vambrace", "bracer", "arm_armor", "arm_guard", "couter", "rerebrace", "kote",
        )):
            return "protective_clothes", "arm_armor"
        if any(word in base_name for word in (
            "greave", "sabaton", "poleyn", "cuisses", "suneate", "leg_armor", "leg_guard", "foot_armor",
            "knee_armor", "thigh_armor", "hip_armor", "faulds", "kusazuri",
        )) or base_name in {"codpiece", "tassets"}:
            return "protective_clothes", "leg_armor"
        if base_name == "rondel":
            return "protective_clothes", "arm_armor"
        if any(word in base_name for word in ("chainmail", "chain_mail", "scale_armor", "lamellar", "gambeson", "leather_armor")):
            return "protective_clothes", "flexible_armor"
        if base_name in {"body_armor", "flak_jacket", "bulletproof_vest", "power_suit"} or any(
            word in base_name for word in ("power_armor", "powered_armor", "mechanical_armor", "living_armor")
        ):
            return "protective_clothes", "protective_suit"
        if any(word in base_name for word in ("visor", "happuri")):
            return "protective_clothes", "combat_helmet"
        if base_name in {
            "breastplate", "muneate", "gorget", "boobplate", "cuirass", "plackart", "dou", "armored_corset",
        }:
            return "protective_clothes", "torso_armor"
        return "protective_clothes", "full_armor"

    swim_categories = {
        "swimsuit", "bikini", "onepiece_swim", "school_swim", "male_swim", "highleg_swim", "other_swim",
    }
    if category_id in swim_categories and folder_id in {"underwear_swim", "clothes_special"}:
        if any(word in base_name for word in ("wetsuit", "rash_guard", "diving_suit", "scuba_suit")):
            return "protective_clothes", "protective_suit"
        if re.search(r"_\([^)]*\)$", name) or any(word in base_name for word in (
            "hololive_summer", "angel's_swimsuit", "idolmaster_swimsuit", "fire_emblem_swimsuit",
            "dragon_quest_swimsuit", "franchise_swimsuit", "tracen_swimsuit", "gris_swimsuit", "ashford_academy_swimsuit",
        )):
            return "franchise_clothes", "franchise_swim"
        if any(word in base_name for word in ("swimsuit_tug", "swimsuit_pull", "adjusting_swimsuit")):
            return "action", "clothing_action"
        if any(word in base_name for word in (
            "hand_under_swimsuit", "hand_in_swimsuit", "hand_in_bikini", "object_in_swimsuit",
            "vibrator_in_swimsuit", "vibrator_under_swimsuit",
        )):
            return "adult", "adult_suggestive"
        generic_school_swim = {
            "school_swimsuit", "old_school_swimsuit", "new_school_swimsuit", "competition_school_swimsuit",
            "school_swimsuit_flap", "nontraditional_school_swimsuit",
        }
        if ("school_swimsuit" in base_name or "school_swimwear" in base_name) and base_name not in generic_school_swim:
            return "franchise_clothes", "franchise_swim"
        if "school_swimsuit" in base_name or "school_swimwear" in base_name:
            return "underwear_swim", "school_swim"
        if any(word in base_name for word in ("swim_trunks", "swim_briefs", "male_swim", "board_shorts", "speedo", "legskin", "jammers")):
            return "underwear_swim", "male_swim"
        if any(word in base_name for word in ("highleg", "high-leg", "slingshot_swimsuit", "sling_bikini")):
            return "underwear_swim", "highleg_swim"
        if "bikini" in base_name:
            return "underwear_swim", "bikini"
        if any(word in base_name for word in ("one-piece_swimsuit", "one_piece_swimsuit", "competition_swimsuit", "racing_swimsuit")):
            return "underwear_swim", "onepiece_swim"
        return "underwear_swim", "other_swim"

    shoe_categories = {
        "shoes", "boots", "heels", "casual_shoes", "sandals_slippers", "traditional_shoes",
        "sports_shoes", "short_boots", "tall_boots", "work_special_shoes",
    }
    if category_id in shoe_categories and folder_id == "legwear_footwear":
        if any(word in base_name for word in (
            "unworn", "no_shoes", "missing_shoe", "shoe_loss", "single_shoe", "mismatched", "untied", "torn_shoes", "dirty_shoes",
            "torn_footwear", "dirty_footwear", "single_sandal", "single_slipper", "single_boot",
        )):
            if "untied" in base_name:
                return "clothing_state", "open_wear"
            return "clothing_state", "unworn_missing" if any(word in base_name for word in ("unworn", "no_shoes", "missing", "loss", "single")) else "damaged_dirty"
        if any(word in base_name for word in ("geta", "zouri", "zori", "waraji", "okobo", "mojari", "gomusin", "clogs", "traditional_footwear")):
            return "legwear_footwear", "traditional_shoes"
        if any(word in base_name for word in ("sandals", "sandal", "flip-flops", "flip_flops", "slippers", "slipper", "crocs")):
            return "legwear_footwear", "sandals_slippers"
        if any(word in base_name for word in ("sneakers", "trainers", "running_shoes", "tennis_shoes", "cleats", "skates", "high_tops")):
            return "legwear_footwear", "sports_shoes"
        if any(word in base_name for word in (
            "high_heels", "high-heel", "high_heel", "pumps", "stiletto", "platform_heels", "mary_janes",
            "strappy_heels", "wedge_heels", "block_heels", "heel-less_heels", "d'orsay_heels",
        )):
            return "legwear_footwear", "heels"
        if "boot" in base_name or base_name in {"waders", "sweatboots"}:
            if any(word in base_name for word in ("thighhigh", "thigh_high", "thigh_boot", "knee_boot", "knee-high", "over-the-knee", "tall_boot")):
                return "legwear_footwear", "short_boots"
            if any(word in base_name for word in (
                "combat_boot", "cowboy_boot", "riding_boot", "rubber_boot", "snow_boot", "steel-toe",
                "wrestling_boot", "mechanical_boot", "rocket_boot", "jet_boot", "armored_boot", "clawed_boot", "winged_boot",
            )):
                return "legwear_footwear", "work_special_shoes"
            return "legwear_footwear", "short_boots"
        if any(word in base_name for word in ("loafers", "oxfords", "flats", "school_shoes", "dress_shoes", "lace-up_shoes")):
            return "legwear_footwear", "casual_shoes"
        if any(word in base_name for word in (
            "armored_shoes", "mechanical_shoes", "winged_shoes", "hoof_shoes", "rocket_shoes",
            "jet_shoes", "clawed_shoes", "rudder_footwear", "paw_shoes", "glass_footwear", "spiked_shoes",
        )):
            return "legwear_footwear", "work_special_shoes"
        if category_id == "heels":
            return "legwear_footwear", "heels"
        return "legwear_footwear", "casual_shoes"

    plant_categories = {
        "plant", "flower_general", "rose", "flower_species", "aquatic_flower", "tree",
        "foliage_vine", "grass_crop", "potted_shrub", "fungus_fantasy", "unusual_plant",
    }
    if category_id in plant_categories and folder_id == "nature":
        if base_name in {"mandrake", "mandragora"}:
            return "nature", "unusual_plant"
        if base_name == "sapling":
            return "nature", "tree"
        if any(word in base_name for word in ("mushroom", "fungus", "toadstool", "mycelium", "agaric")):
            return "nature", "grass_crop"
        if name.endswith("_(flower)"):
            return "nature", "flower_species"
        if name.endswith("_(plant)"):
            if any(word in base_name for word in ("rice", "cotton", "myouga")):
                return "nature", "grass_crop"
            return "nature", "flower_species"
        if any(word in base_name for word in (
            "magic_flower", "fantasy_flower", "crystal_flower", "ice_flower", "fire_flower",
            "glowing_flower", "giant_flower", "oversized_flower", "alien_plant", "monster_plant",
            "qingxin_flower", "silent_princess", "elpis_flower", "padisarah_flower", "carnivorous_plant", "oversized_plant",
        )) or re.search(r"_\((?!flower\)|plant\))[^)]*\)$", name):
            return "nature", "unusual_plant"
        if "rose" in base_name:
            return "nature", "flower_species"
        if any(word in base_name for word in ("seaweed", "algae", "aquatic_plant")):
            return "nature", "grass_crop"
        if any(word in base_name for word in ("lotus", "water_lily", "lily_pad")):
            return "nature", "flower_species"
        if any(word in base_name for word in (
            "leaf", "leaves", "branch", "vine", "ivy", "thorn", "tendril", "twig", "root", "foliage", "clover",
            "trefoil", "shamrock", "holly", "mistletoe",
        )):
            return "nature", "foliage_vine"
        if any(word in base_name for word in (
            "tree", "sakura", "cherry_blossom_tree", "palm", "willow", "pine", "maple_tree", "birch", "oak", "acorn",
        )):
            return "nature", "tree"
        if any(word in base_name for word in (
            "grass", "wheat", "rice", "crop", "hay", "reed", "bamboo", "corn", "barley", "moss", "herb",
            "fern", "mint", "weed", "marijuana", "seed", "sprout", "strawberry_plant",
        )):
            return "nature", "grass_crop"
        if any(word in base_name for word in (
            "potted", "pot_plant", "hanging_plant", "bush", "shrub", "hedge", "cactus", "succulent", "bonsai", "topiary", "kadomatsu",
        )):
            return "nature", "potted_shrub"
        named_flowers = (
            "lily", "tulip", "sunflower", "daisy", "orchid", "hydrangea", "camellia", "chrysanthemum",
            "carnation", "chamomile", "dandelion", "lavender", "hibiscus", "peony", "poppy", "iris", "violet",
            "anemone", "narcissus", "cosmos_flower", "morning_glory", "forget-me-not", "wisteria",
            "plumeria", "bellflower", "pansy", "gerbera", "daffodil", "osmanthus", "baby's-breath",
            "poinsettia", "epiphyllum", "dahlia", "magnolia", "gladiolus", "rapeseed_blossom",
            "peach_blossom", "orange_blossom", "strawberry_blossom", "trumpet_creeper", "bird_of_paradise_flower",
        )
        if any(word in base_name for word in named_flowers):
            return "nature", "flower_species"
        return "nature", "flower_general"

    architecture_categories = {
        "architecture", "door_window", "stairs_railing", "fence_gate", "bridge_walkway", "residential",
        "public_building", "religious_building", "tower_landmark", "ruin_structure", "architecture_style",
        "roof_exterior", "frame_structure", "surface",
    }
    if category_id in architecture_categories and folder_id in {"indoor_scene", "urban_architecture", "building_parts"}:
        if any(word in base_name for word in ("torii", "shrine", "temple", "church", "cathedral", "mosque", "pagoda", "jizou", "synagogue", "onbashira")):
            return "urban_architecture", "religious_building"
        if any(word in base_name for word in (
            "shouji", "fusuma", "noren", "stained_glass", "lattice", "sliding_doors", "windowsill", "muntins", "boarded_windows",
        )) or re.search(r"(^|_)(door|doors|window|windows|doorway|entrance|exit|hatch|shutter)($|_)", base_name):
            return "building_parts", "door_window"
        if any(word in base_name for word in ("padded_walls",)):
            return "building_parts", "surface"
        if any(word in base_name for word in ("stairs", "staircase", "steps", "railing", "banister", "handrail", "balustrade", "baluster")):
            return "building_parts", "stairs_railing"
        if any(word in base_name for word in ("fence", "gate", "gateway", "turnstile", "palisade", "barbed_wire", "iron_bars", "grate", "trellis")):
            return "building_parts", "fence_gate"
        if any(word in base_name for word in ("bridge", "walkway", "overpass", "boardwalk", "footbridge", "tunnel", "viaduct", "elevator", "escalator")):
            return "building_parts", "bridge_walkway"
        if any(word in base_name for word in (
            "roof", "chimney", "smokestack", "awning", "balcony", "dome", "spire", "steeple", "skylight", "drainpipe", "vent",
        )):
            return "building_parts", "roof_exterior"
        if "broken" in base_name and any(word in base_name for word in ("pillar", "column")):
            return "building_parts", "frame_structure"
        if base_name in {"arch", "archway", "arches"} or any(word in base_name for word in (
            "pillar", "column", "bollard", "truss", "steel_beam", "scaffolding", "colonnade",
        )):
            return "building_parts", "frame_structure"
        if any(word in base_name for word in (
            "tower", "lighthouse", "windmill", "skyscraper", "monument", "landmark", "eiffel", "tokyo_tower", "ferris_wheel", "statue_of_liberty", "moai",
        )):
            return "urban_architecture", "tower_landmark"
        if any(word in base_name for word in (
            "house", "home", "mansion", "villa", "cottage", "apartment", "barn", "farmhouse", "treehouse",
            "greenhouse", "porch", "veranda", "residence",
        )):
            return "urban_architecture", "residential"
        if any(word in base_name for word in (
            "ruin", "abandoned", "broken_building", "ancient_structure", "aqueduct",
        )):
            return "urban_architecture", "public_building"
        if any(word in base_name for word in (
            "architecture", "gothic", "baroque", "modernist", "brutalist", "european_style", "east_asian_style",
            "greco-roman", "middle_eastern_style", "mesoamerican",
        )):
            return "urban_architecture", "architecture_style"
        return "urban_architecture", "public_building"

    if (folder_id, category_id) == ("urban_architecture", "surface") and any(word in base_name for word in ("window", "door")):
        return "building_parts", "door_window"

    private_categories = {
        "adult_anatomy", "penis", "testicles", "vulva", "clitoris", "anus", "pubic_hair",
        "reproductive", "genital_variation",
    }
    if category_id in private_categories and folder_id in {"adult", "adult_body"}:
        if any(word in base_name for word in ("prince_albert", "clitoris_ring", "genital_piercing", "penis_piercing")):
            return "adult_kink", "adult_piercing"
        if any(word in base_name for word in ("insertion", "sounding")):
            return "adult_kink", "adult_insertion"
        if any(word in base_name for word in (
            "nipple_stimulation", "nipple_tweak", "nipple_rub", "nipple_pull", "nipple_press",
            "nipples_pressed", "tickling_nipples", "nipple_flick", "body_exploration", "womb_massage",
            "large_bulge", "nipple_guessing", "nipple_injection", "areola_measuring",
        )):
            return "adult", "adult_suggestive"
        hand_action_words = (
            "grab", "caress", "squeez", "hands_on", "touching", "tickling", "tweak", "rubbing",
            "pulling", "massage", "measuring", "milking",
        )
        if any(word in base_name for word in hand_action_words):
            return "adult", "adult_hand"
        if any(word in base_name for word in (
            "penis_on", "testicles_on", "penis_to", "penis_over", "hug", "poking", "slapping",
            "touching", "sandwich", "press", "slip", "focus", "awe",
        )):
            return "adult", "adult_suggestive"
        if any(word in base_name for word in ("food_on", "chocolate_on", "lipstick_mark", "sock_on", "panties_on", "saliva_on")):
            return "adult_kink", "adult_fetish"
        if any(word in base_name for word in (
            "no_genitals", "misplaced_genitals", "extra_genitals", "artificial_genital", "mechanical_genital",
            "animal_genital", "disembodied_genital", "futanari", "gynomorph", "andromorph",
            "no_penis", "extra_penis", "mechanical_penis", "animal_penis", "disembodied_penis",
            "no_testicles", "futa_without_balls", "no_pussy", "artificial_vagina", "futa_without_pussy",
            "no_anus", "deformed_anus", "tail_anus",
        )):
            return "adult_body", "genital_variation"
        if "pubic_hair" in base_name or base_name in {"bush", "hairy_pussy", "hairy_genitals", "pubic_stubble"}:
            return "adult_body", "pubic_hair"
        if any(word in base_name for word in ("testicle", "testicles", "scrotum", "balls", "ball_sack")):
            return "adult_body", "testicles"
        if any(word in base_name for word in ("clitoris", "clitoral", "clit")):
            return "adult_body", "clitoris"
        if any(word in base_name for word in ("anus", "anal", "butthole")):
            return "adult_body", "anus"
        if any(word in base_name for word in ("vulva", "vagina", "vaginal", "pussy", "labia", "mons_pubis", "hymen", "cleft_of_venus", "fat_mons")):
            return "adult_body", "vulva"
        if any(word in base_name for word in ("penis", "penile", "cock", "phallus", "foreskin", "glans", "frenulum", "erection", "flaccid", "half-erect", "phimosis", "smegma")):
            return "adult_body", "penis"
        if any(word in base_name for word in ("sperm", "fertilization", "urethra", "reproductive", "cervix", "ovary", "uterus", "perineum", "fetus")):
            return "adult_body", "reproductive"
        return "adult_body", "genital_variation"

    if (folder_id, category_id) == ("adult_body", "adult_suggestive"):
        return "adult", "adult_suggestive"

    # v8: split broad, visually crowded categories by the meaning a user sees
    # in the tag.  These rules run before the stable-folder guard because old
    # user data and exact overrides can already point at the v8 parent folder.
    if folder_id in {"clothes_special", "uniform_costume"} and category_id in {
        "school_uniform", "occupation_uniform", "sports_uniform", "themed_costume",
    }:
        sports_uniform_names = {
            "buruma", "gym_uniform", "cheerleader", "dougi", "sportswear", "tutu", "bikesuit",
            "riding_outfit", "wrestling_outfit", "race_queen", "racing_colors",
        }
        if (
            base_name in sports_uniform_names
            or any(word in base_name for word in (
                "buruma", "gym_uniform", "training_uniform", "track_uniform", "sports_uniform",
                "soccer_uniform", "baseball_uniform", "basketball_uniform", "tennis_uniform",
                "volleyball_uniform", "rugby_uniform", "cycling_uniform", "football_uniform",
                "cheerleader_uniform", "sportswear", "track_suit", "tracksuit",
            ))
        ):
            return "uniform_costume", "sports_uniform"

        if category_id == "school_uniform":
            if "serafuku" in base_name or "sailor" in tokens or "sailor_uniform" in base_name:
                return "uniform_costume", "sailor_uniform"
            generic_school_uniforms = {
                "school_uniform", "winter_uniform", "summer_uniform", "gakuran", "kindergarten_uniform",
                "elementary_school_uniform", "middle_school_uniform", "high_school_uniform",
                "tactical_school_uniform", "indonesian_high_school_uniform", "thai_school_uniform", "soviet_school_uniform",
            }
            if base_name not in generic_school_uniforms and (
                "school_uniform" in base_name or "academy_uniform" in base_name or "high_school_uniform" in base_name
            ):
                return "uniform_costume", "school_variant"
            return "uniform_costume", "school_uniform"

        if category_id == "occupation_uniform":
            service_words = {
                "maid", "waitress", "waiter", "barista", "butler", "housekeeper", "stewardess",
                "concierge", "bellhop", "server", "vendor", "croupier", "usher", "apron",
            }
            military_words = {
                "military", "army", "navy", "naval", "marine", "soldier", "officer", "police",
                "sheriff", "guard", "trooper", "combat", "tactical", "corps", "force", "fleet",
                "gendarmerie", "wehrmacht", "luftwaffe", "imperial", "admiral", "general",
            }
            if "apron" in tokens or "apron" in base_name:
                return "clothes_main", "apron_cover"
            if tokens & service_words or any(word in base_name for word in ("maid_", "_maid", "enmaid", "waitress", "cafe_uniform")):
                return "uniform_costume", "service_uniform"
            if tokens & military_words or any(word in base_name for word in (
                "military_uniform", "police_uniform", "naval_uniform", "army_uniform",
                "combat_uniform", "guard_uniform", "corps_uniform", "force_uniform",
            )):
                return "uniform_costume", "military_uniform"
            generic_occupation_uniforms = {
                "uniform", "lab_coat", "nurse", "nurse_uniform", "chef", "chef_uniform", "pilot",
                "pilot_uniform", "doctor", "medical_uniform", "employee_uniform", "work_uniform",
                "office_lady", "clerical_uniform", "prison_uniform", "prisoner_uniform",
                "adapted_uniform", "band_uniform", "white_uniform", "alternate_uniform", "expedition_uniform", "scout_uniform",
            }
            if base_name not in generic_occupation_uniforms and (
                base_name.endswith("_uniform") or "_uniform_" in base_name
            ):
                return "uniform_costume", "franchise_uniform"
            return "uniform_costume", "occupation_uniform"

        if category_id == "themed_costume":
            fashion_names = {
                "lolita_fashion", "jirai_kei", "ouji_fashion", "biker_clothes", "sweet_lolita",
                "accurate_lolita_coord", "wa_lolita", "aristocratic_clothes", "emo_fashion", "decora",
                "classic_lolita", "amesuku_gyaru", "yabi_fashion", "techwear", "hawaiian_clothes",
                "contemporary_traditional_clothes",
            }
            if base_name in fashion_names:
                return "clothing_appearance", "fashion_style"
            if base_name in {
                "plugsuit", "zero_suit", "taimanin_suit", "parasite_suit", "kittysuit",
                "vault_suit", "mobile_trace_suit", "palette_suit", "varia_suit",
            }:
                return "underwear_swim", "bodysuit_leotard"
            if base_name in {"tactical_clothes", "sneaking_suit"}:
                return "protective_clothes", "helmet_protective"
            if base_name in {"traditional_clothes", "contemporary_traditional_clothes"}:
                return "traditional_clothes", "traditional_world"
            if base_name == "prison_clothes":
                return "uniform_costume", "occupation_uniform"

        return "uniform_costume", category_id

    if (folder_id, category_id) == ("style", "genre") and base_name in {
        "gothic_lolita", "lolita_fashion", "jirai_kei", "ouji_fashion", "sweet_lolita",
        "wa_lolita", "emo_fashion", "decora", "classic_lolita", "techwear", "streetwear",
    }:
        return "clothing_appearance", "fashion_style"

    if folder_id == "adult_kink" and category_id == "adult_fetish":
        nonsexual_restraints = {
            "chained", "chained_wrists", "immobilization", "pillory", "stocks", "cuffed",
            "metal_wrist_cuffs", "rope_around_neck", "hobble", "restraints", "belly_riding",
            "tied_up", "jinki-style_restrained", "forced",
        }
        if base_name in nonsexual_restraints or base_name.endswith("_restrained"):
            return "sensitive", "restraint"
        if base_name == "condom_in_mouth":
            return "adult", "adult_oral"
        if base_name == "slime":
            return "light_effect", "other_effect"
        if base_name == "muzzle":
            return "head_accessories", "face_mask"
        if base_name == "chikan":
            return "sensitive", "sexual_violence"
        if base_name == "pokephilia":
            return "adult_kink", "adult_taboo"
        if base_name == "egg_implantation":
            return "adult_kink", "adult_insertion"
        if base_name in {"unusual_insertion", "assisted_object_insertion"}:
            return "adult_kink", "adult_insertion"
        if base_name in {"spider_gag"}:
            return "adult_kink", "adult_bondage"
        if base_name in {"drinking_from_condom", "licking_dildo"}:
            return "adult", "adult_oral"
        private_body_words = {
            "nipple", "nipples", "areola", "clitoral", "clitoris", "pussy", "vulva", "labia",
            "penis", "penile", "cock", "scrotum", "genital", "urethral", "frenulum",
        }
        if tokens & private_body_words and tokens & {"piercing", "piercings", "ring", "rings", "bar", "jewelry", "bells", "tag", "tassels"}:
            return "adult_kink", "adult_piercing"
        if any(fragment in base_name for fragment in (
            "object_insertion", "ball_insertion", "food_insertion", "shared_object_insertion",
            "sounding", "glory_hole", "glory_wall", "human_toilet", "human_stacking",
        )):
            return "adult_kink", "adult_insertion"
        power_names = {
            "femdom", "assertive_female", "spanked", "humiliation", "pet_play", "spanking",
            "dominatrix", "masochism", "sadism", "public_use", "futasub", "cbt", "ball_busting",
            "small_penis_humiliation", "feminization", "submission", "perverted_utility",
        }
        if base_name in power_names:
            return "adult_kink", "adult_power"
        if tokens & {"scat", "pee", "excrement", "toilet"} or base_name in {"drinking_pee", "personality_excrement"}:
            return "adult_kink", "adult_excretion"
        if base_name == "stripper_pole":
            return "adult_kink", "adult_toys"
        return "adult_kink", "adult_fetish"

    if folder_id == "adult_kink" and category_id == "adult_other":
        response_names = {
            "orgasm", "female_orgasm", "mutual_orgasm", "imminent_orgasm", "implied_orgasm",
            "aroused", "fucked_silly", "morning_after", "mind_break", "orgasm_denial", "rape_face",
        }
        if base_name in response_names:
            return "adult", "adult_response"
        if base_name == "navel_insertion":
            return "adult_kink", "adult_insertion"
        return "adult", "adult_theme"

    if (folder_id, category_id) == ("face", "mouth"):
        if base_name == "condom_in_mouth":
            return "adult", "adult_oral"
        if base_name in {"dildo_in_mouth", "gag_in_mouth"}:
            return "adult_kink", "adult_toys"
        if base_name == "mouth_veil":
            return "head_accessories", "face_mask"
        if base_name == "food_in_mouth":
            return "action", "daily_action"
        if base_name in {"clothes_in_mouth", "card_in_mouth", "flower_in_mouth", "weapon_in_mouth"}:
            return "action", "holding"
        oral_words = {
            "tongue", "teeth", "tooth", "fang", "fangs", "tusk", "tusks", "saliva", "drool",
            "uvula", "palate", "gum", "gums", "dental", "braces",
        }
        if tokens & oral_words or any(word in base_name for word in ("tongue", "tooth", "teeth", "fang", "saliva", "drool")):
            return "face", "oral_detail"

    if (folder_id, category_id) == ("face", "nose"):
        nose_exceptions = {
            "nose_ring": ("jewelry_accessories", "piercing"),
            "nose_piercing": ("jewelry_accessories", "piercing"),
            "nose_hook": ("adult_kink", "adult_fetish"),
            "butterfly_on_nose": ("creatures", "insect"),
            "nose_bubble": ("body_detail", "body_state"),
            "runny_nose": ("body_detail", "body_state"),
            "snot": ("body_detail", "body_state"),
            "nose_picking": ("action", "daily_action"),
            "wiping_nose": ("action", "daily_action"),
            "blowing_nose": ("action", "daily_action"),
            "rubbing_nose": ("pose", "arm_pose"),
            "nose_pinch": ("action", "interaction"),
            "poking_nose": ("action", "interaction"),
            "red_nose": ("head_accessories", "face_mask"),
            "clown_nose": ("head_accessories", "face_mask"),
            "fake_nose": ("head_accessories", "face_mask"),
            "nose_tape": ("head_accessories", "face_mask"),
        }
        if base_name in nose_exceptions:
            return nose_exceptions[base_name]

    if (folder_id, category_id) == ("face", "ears"):
        if base_name in {"rabbit_ear_headphones", "headphones_for_animal_ears", "earphones_on_animal_ears"}:
            return "digital_media", "audio_device"
        if base_name in {"ear_ribbon", "ear_covers", "single_ear_cover", "animal_ear_headwear", "animal_ear_hood", "ear_bell", "heart_ear_ornament"}:
            return "head_accessories", "headpiece"
        if base_name in {"ear_chain", "ear_tag"}:
            return "jewelry_accessories", "earrings"
        if base_name == "hair_behind_ear" or base_name == "hair_around_ear":
            return "hair", "hair_action"
        if base_name == "bunny_ears_prank":
            return "action", "interaction"
        if base_name == "ear_cuffs":
            return "jewelry_accessories", "earrings"
        if base_name == "tentacle_in_ear":
            return "adult_kink", "adult_insertion"
        if "animal_ear" in base_name or base_name in {"ears_down", "one_ear_down", "notched_ear", "ear_wiggle"}:
            return "animal_traits", "animal_ears"

    if (folder_id, category_id) == ("pose", "body_pose"):
        if tokens & {"arm", "arms", "hand", "hands", "elbow", "elbows", "wrist", "wrists"}:
            return "pose", "arm_pose"
        leg_words = {
            "leg", "legs", "foot", "feet", "toe", "toes", "knee", "knees", "thigh", "thighs",
            "ankle", "ankles", "split", "splits", "straddle", "squatting", "tiptoe", "tiptoes",
        }
        if tokens & leg_words or any(word in base_name for word in ("crossed_legs", "raised_leg", "legs_", "knees_", "feet_")):
            return "pose", "leg_pose"

    if (folder_id, category_id) == ("pose", "hand_gesture"):
        if base_name in {"bras_d'honneur", "palm-fist_greeting", "reverse_prayer"}: return "pose", "hand_gesture"
        if "another's" in base_name or "another_s" in base_name or base_name in {
            "hand_on_another", "finger_in_another's_mouth", "hand_on_another's_head",
        }:
            return "action", "interaction"
        symbolic_gestures = {
            "v", "peace", "victory", "thumbs", "thumbsup", "pointing", "salute", "saluting",
            "wave", "waving", "finger", "fingers", "gesture", "sign", "heart", "ok", "shushing",
            "middle", "index", "pinky", "counting", "snap", "snapping", "clap", "clapping",
        }
        if tokens & symbolic_gestures or any(word in base_name for word in (
            "finger_gun", "hand_heart", "heart_hands", "v_over_eye", "w_over_eye", "pointing_",
            "thumbs_up", "thumbs_down", "peace_sign", "middle_finger", "ok_sign",
        )):
            return "pose", "hand_gesture"
        return "pose", "arm_pose"

    if folder_id == "accessories" and category_id == "hair_accessory":
        return "head_accessories", "hair_accessory"
    if folder_id == "accessories" and category_id in {"headwear", "eyewear"}:
        mask_words = {"mask", "masque", "respirator", "blindfold", "eyepatch", "visor"}
        veil_words = {"veil", "veiled", "headscarf", "kerchief", "hijab", "niqab", "wimple", "hood", "balaclava"}
        headpiece_words = {
            "crown", "tiara", "circlet", "diadem", "headdress", "headpiece", "headband", "halo",
            "forehead", "antlers", "horns", "ears", "ear", "antennae", "headgear",
        }
        if base_name == "mechanical_halo":
            return "light_effect", "halo_effect"
        if base_name == "visor_cap":
            return "head_accessories", "hats_caps"
        if tokens & mask_words or any(word in base_name for word in ("face_mask", "mouth_mask", "eye_mask", "gas_mask")):
            return "head_accessories", "face_mask"
        if tokens & veil_words or any(word in base_name for word in ("headscarf", "head_wrap")):
            return "head_accessories", "headwrap_veil"
        if category_id == "eyewear":
            return "head_accessories", "eyewear"
        if tokens & headpiece_words:
            return "head_accessories", "headpiece"
        return "head_accessories", "hats_caps"

    if (folder_id, category_id) == ("accessories", "jewelry"):
        if base_name == "jewel_butt_plug":
            return "adult_kink", "adult_toys"
        adult_jewelry_words = {"nipple", "nipples", "clitoral", "clitoris", "penis", "penile", "cock", "genital", "urethral", "labia", "vulva"}
        if tokens & adult_jewelry_words:
            return "adult_kink", "adult_piercing"
        if "piercing" in tokens or "piercings" in tokens or "pierced" in tokens or name.endswith("_(piercing)"):
            return "jewelry_accessories", "piercing"
        if tokens & {"earring", "earrings", "earclip", "earclips"} or "earring" in base_name:
            return "jewelry_accessories", "earrings"
        if tokens & {"necklace", "choker", "torc", "locket"} or any(word in base_name for word in ("necklace", "choker")):
            return "jewelry_accessories", "necklace_choker"
        if tokens & {"ring", "rings"} or base_name.endswith("_ring"):
            return "jewelry_accessories", "rings"
        if tokens & {"bracelet", "bracelets", "anklet", "anklets", "armlet", "armlets", "bangle", "bangles"}:
            return "jewelry_accessories", "bracelet_anklet"
        return "jewelry_accessories", "gem_brooch"

    if (folder_id, category_id) == ("accessories", "badges_ornaments"):
        if tokens & {"bow", "bows", "ribbon", "ribbons"} or any(word in base_name for word in ("bow_", "_bow", "ribbon_", "_ribbon")):
            return "accessories", "bows_ribbons"
        return "accessories", "badges_ornaments"

    if (folder_id, category_id) == ("household_objects", "tools"):
        if tokens & {"crotch", "chastity"}:
            return "adult_kink", "adult_bondage"
        if tokens & {"handcuff", "handcuffs", "shackle", "shackles", "restraint", "restraints"}:
            return "sensitive", "restraint"
        electric_fans = {"electric_fan", "ceiling_fan", "handheld_electric_fan", "bladeless_fan"}
        if base_name in electric_fans:
            return "household_objects", "appliance"
        if tokens & {"umbrella", "parasol", "fan", "uchiwa", "sensu"} or base_name in {"tuanshan", "harisen"}:
            return "household_objects", "umbrella_fan"
        if tokens & {"rope", "chain", "lock", "key", "padlock", "cable", "cord", "shackle", "carabiner"}:
            return "household_objects", "rope_lock"
        if tokens & {
            "cleaning", "cleaner", "cleanser", "soap", "shampoo", "detergent", "sponge", "brush",
            "broom", "mop", "towel", "toothbrush", "razor", "comb", "dryer", "cosmetic", "makeup",
            "lotion", "syringe", "needle", "pill", "stethoscope", "thermometer", "medicine", "medical",
            "sunscreen", "toothpaste", "pump", "cotton", "clipper", "clippers", "roller", "rollers",
            "curling", "straightener", "pregnancy", "first", "aid", "intravenous", "scalpel", "surgical",
        }:
            return "household_objects", "care_cleaning"
        if base_name == "clothes_gag":
            return "adult_kink", "adult_bondage"
        if base_name == "rock_paper_scissors":
            return "pose", "hand_gesture"
        return "household_objects", "tools"

    if folder_id in {
        "body_detail", "outerwear_suits", "uniform_costume", "traditional_clothes",
        "protective_clothes", "clothing_state", "animal_traits", "urban_architecture",
        "background", "symbols", "adult_body", "adult_kink", "head_accessories",
        "clothing_appearance",
        "jewelry_accessories",
    }:
        return folder_id, category_id

    # Stable v7 categories that only changed parent folder in v8.  Handle them
    # before older name-based compatibility rules so an already-audited target
    # cannot be pulled back into its removed parent on the next normalization
    # pass.
    if folder_id == "body" and category_id in {
        "skin", "tattoo_mark", "mole_freckle", "scar_wound", "bandage_patch",
        "surface_stain", "surface_decor", "body_hair", "body_function",
    }:
        return "body_detail", category_id
    if folder_id == "clothes_main" and category_id in {
        "jacket_coat", "cape_cloak", "cardigan_shawl", "formal_suit", "jumpsuit",
    }:
        return "outerwear_suits", category_id
    if folder_id == "clothes_special" and category_id in {
        "school_uniform", "occupation_uniform", "sports_uniform", "themed_costume",
    }:
        return "uniform_costume", category_id
    if folder_id == "clothes_special" and category_id in {"traditional_east", "traditional_world"}:
        return "traditional_clothes", category_id
    if folder_id == "clothes_special" and category_id == "casualwear":
        return "clothing_appearance", "fashion_style"
    if folder_id == "clothes_special" and category_id in {"sleepwear", "robe"}:
        return "clothes_main", category_id
    if folder_id == "clothes_special" and category_id in {"armor", "helmet"}:
        return "protective_clothes", category_id
    if folder_id == "clothing_detail" and category_id in {"damaged_dirty", "unworn_missing", "open_wear"}:
        return "clothing_state", category_id
    if folder_id == "clothing_detail" and category_id in {"clothing_color", "clothing_pattern", "clothing_material"}:
        return "clothing_appearance", category_id
    if folder_id == "creatures" and category_id in {
        "animal_ears", "horns", "tails", "fur_feature", "wing_feather", "claw_scale",
    }:
        return "animal_traits", category_id
    if folder_id == "indoor_scene" and category_id in {"urban", "architecture", "surface"}:
        return "urban_architecture", category_id
    if folder_id == "outdoor_scene" and category_id in {"background_plain", "background_pattern"}:
        return "background", category_id
    if folder_id == "text_meta" and category_id in {
        "general_symbol", "shape_math", "music_symbol", "religious_symbol", "zodiac_symbol",
        "flag", "emblem", "science_sign",
    }:
        return "symbols", category_id

    if (folder_id, category_id) == ("text_meta", "symbol"):
        for target, symbol_names in SYMBOL_LOCATION_SETS.items():
            if name in symbol_names:
                return target
        return "text_meta", "general_symbol"

    # v7: the former "tattoos/scars" bucket also contained moles, temporary
    # bandages, surface stains and body decoration.  These rules cover all 283
    # audited members, with wiki-confirmed homonyms handled before fragments.
    if (folder_id, category_id) == ("body", "body_marks"):
        body_mark_exceptions = {
            "blood_stain": ("sensitive", "blood"),
            "blood_on_breasts": ("sensitive", "blood"),
            "blood_on_neck": ("sensitive", "blood"),
            "blood_on_stomach": ("sensitive", "blood"),
            "self-harm_scar": ("sensitive", "injury_death"),
            "deep_wound": ("sensitive", "injury_death"),
            "gunshot_wound": ("sensitive", "injury_death"),
            "glasgow_smile": ("sensitive", "gore"),
            "oripathy_lesion_(arknights)": ("body", "body_state"),
            "bindi": ("face", "makeup"),
            "w_over_eye": ("pose", "hand_gesture"),
            "armpit_hair_peek": ("body", "body_hair"),
            "tan_tattoo": ("body", "skin"),
            "bandaids_on_nipples": ("adult", "adult_clothes"),
            "bandaid_on_clothes": ("clothing_detail", "other_structure"),
            "bandage_on_hair": ("accessories", "hair_accessory"),
            "taped_hands": ("accessories", "handwear"),
            "taped_arms": ("sensitive", "restraint"),
            "bandage_in_mouth": ("action", "holding"),
            "ofuda_on_leg": ("accessories", "other_accessory"),
        }
        if name in body_mark_exceptions:
            return body_mark_exceptions[name]
        tattoo_marks = {
            "facial_mark", "forehead_mark", "whisker_markings", "body_markings",
            "tacet_mark_(wuthering_waves)", "command_spell", "mark_under_eye", "marking_on_cheek",
            "archon_mark", "brand_of_the_exalt", "glowing_markings", "markings", "cutie_mark",
            "arm_markings", "thigh_marking", "chest_markings", "sparkle_facial_mark", "irezumi",
            "tramp_stamp",
        }
        if "tattoo" in name or name in tattoo_marks:
            return "body", "tattoo_mark"
        if any(fragment in name for fragment in ("mole", "freckle", "birthmark")):
            return "body", "mole_freckle"
        if any(fragment in name for fragment in (
            "scar", "bruise", "wound", "cuts", "scratches", "hickey", "bite", "bitten",
            "stitch", "scrape", "whip_marks", "rope_marks", "branded", "slap_mark",
        )):
            return "body", "scar_wound"
        if any(fragment in name for fragment in ("bandaid", "bandage", "gauze")):
            return "body", "bandage_patch"
        if name in {"food_on_face", "paint_splatter_on_face", "cream_on_face", "rice_on_face", "paint_stains"}:
            return "body", "surface_stain"
        if name in {
            "bodypaint", "paint_on_body", "ink_on_face", "sticker_on_face", "sticker_on_arm",
            "sticker_on_leg", "heart_on_cheek",
        }:
            return "body", "surface_decor"
        return "body", "tattoo_mark"

    # v7: actual transient body conditions remain in body_state.  Anatomy,
    # bodily functions, stains, violence, actions and composition phenomena
    # were individually removed from the former 185-item mixed bucket.
    if (folder_id, category_id) == ("body", "body_state"):
        body_state_targets = {
            ("body", "arms_hands"): {
                "fingernails", "long_fingernails", "sharp_fingernails", "very_long_fingernails", "left-handed",
            },
            ("body", "legs_knees"): {"kneepits", "digitigrade", "reverse-jointed_legs"},
            ("body", "skin"): {"skindentation", "veins"},
            ("body", "torso_back"): {"dimples_of_venus"},
            ("body", "internal_organs"): {"bone", "twitching_womb"},
            ("body", "breast_chest"): {
                "bursting_breasts", "breast_expansion", "bursting_pectorals", "floating_breasts",
                "extra_breasts", "breast_reduction",
            },
            ("body", "body_hair"): {"hairy", "very_hairy", "white_armpit_hair"},
            ("body", "limb_variation"): {
                "disembodied_hand", "extra_arms", "amputee", "fewer_digits", "no_feet", "multiple_legs",
                "double_amputee", "quadruple_amputee", "asymmetrical_arms", "skeletal_arm",
                "skeletal_hand", "extra_legs", "armless_amputee", "extra_hands", "extra_digits",
                "rayman_limbs", "ghost_hands", "triple_amputee", "no_hands", "legless_amputee",
                "detached_legs", "too_many_hands", "no_fingers", "transparent_hand", "missing_finger",
                "no_toes",
            },
            ("body", "anatomy_anomaly"): {
                "material_growth", "disembodied_head", "multiple_heads", "headless", "extra_faces",
                "conjoined", "hollow_body", "hand_eye", "void_face",
            },
            ("body", "bandage_patch"): {
                "bandages", "bandage_over_one_eye", "bandaged_head", "bandaged_neck", "gauze",
            },
            ("body", "surface_stain"): {
                "dirty", "dirty_face", "chocolate_on_body", "chocolate_on_breasts", "messy",
                "wet_face", "snow_on_head", "chocolate_on_face", "cream_on_body", "oiled", "snow_on_body",
            },
            ("body", "body_function"): {
                "sweat", "lactation", "pee", "very_sweaty", "snot", "have_to_pee", "holding_breath",
                "stomach_growling", "vomiting", "vomit", "poop", "fart", "male_lactation",
                "alternate_body_fluid", "sparkling_sweat", "bedwetting", "hiccup", "dripping_sweat",
            },
            ("sensitive", "blood"): {
                "blood", "blood_on_face", "blood_on_hands", "nosebleed", "blood_splatter", "bleeding",
                "pink_blood", "blood_on_arm", "blood_drip", "blood_on_leg", "blood_on_bandages",
                "blood_on_chest", "blood_from_forehead", "blue_blood", "blood_on_body",
                "excessive_nosebleed", "blood_on_feet", "blood_on_hand",
            },
            ("sensitive", "injury_death"): {
                "injury", "asphyxiation", "burnt", "arrow_in_body", "beaten", "broken_arm", "broken_leg",
            },
            ("sensitive", "gore"): {
                "hole_on_body", "exposed_muscle", "broken_skin", "torn_skin", "growing_out_of_body",
            },
            ("adult", "adult_suggestive"): {"cameltoe", "bulge", "in_heat", "aroused_nosebleed"},
            ("adult", "adult_other"): {"egg_laying"},
            ("adult", "adult_taboo"): {"egg_implantation"},
            ("themes", "narrative_situation"): {
                "stuck", "trapped", "entangled", "buried", "giving_birth", "merfolk_out_of_environment",
            },
            ("mech_scifi", "cybernetic"): {"doll_joints", "artificial_eye", "false_limb"},
            ("mech_scifi", "mecha"): {"battle_damage"},
            ("meta_info", "censorship"): {"convenient_leg", "convenient_arm", "convenient_hand"},
            ("meta_info", "meta"): {"anatomical_nonsense"},
            ("style", "quality"): {"bad_leg"},
            ("text_meta", "comic"): {"spasm"},
            ("pose", "body_pose"): {"attitude_derriere"},
            ("pose", "hand_gesture"): {"w_over_eye"},
            ("composition", "framing"): {"covered_face"},
            ("composition", "layout"): {"floating_head", "giant_hand", "cramped"},
            ("action", "holding"): {"heavy"},
            ("action", "daily_action"): {"recharging"},
            ("action", "interaction"): {"cheek_squash", "squishing"},
            ("action", "movement"): {"fainting"},
            ("sensitive", "restraint"): {"separated_arms"},
            ("clothing_detail", "damaged_dirty"): {"pee_stain", "sweat_stain"},
            ("clothing_detail", "other_clothes"): {"swaddled"},
            ("light_effect", "fire_smoke"): {"steaming_body"},
        }
        for target, state_names in body_state_targets.items():
            if name in state_names:
                return target
        return "body_detail", "body_state"

    # v7: hair ornaments are wearable accessories, not hair morphology.  A
    # complete wiki-level audit found seven items whose actual meaning differs
    # from their translated label; keep those explicit instead of moving the
    # old bucket blindly.
    if (folder_id, category_id) == ("hair", "hair_accessory"):
        hair_accessory_exceptions = {
            "feather_hair": ("creatures", "wing_feather"),
            "hair_rollers": ("household_objects", "tools"),
            "wrist_scrunchie": ("accessories", "handwear"),
            "arm_scrunchie": ("accessories", "handwear"),
            "ear_scrunchie": ("accessories", "other_accessory"),
            "ankle_scrunchie": ("accessories", "other_accessory"),
            "thigh_scrunchie": ("accessories", "other_accessory"),
        }
        return hair_accessory_exceptions.get(base_name, ("accessories", "hair_accessory"))

    # v7: the former brows/nose bucket mixed facial anatomy with props, body
    # states and actions.  Route every audited member by its documented meaning.
    if (folder_id, category_id) == ("face", "brows_nose"):
        brows_nose_exceptions = {
            "aegyo_sal": ("face", "eye_shape"),
            "forehead": ("face", "face_shape"),
            "cheekbones": ("face", "face_shape"),
            "large_forehead": ("face", "face_shape"),
            "shiny_forehead": ("face", "face_shape"),
            "sunken_cheeks": ("face", "face_shape"),
            "snot": ("body", "body_state"),
            "nose_bubble": ("body", "body_state"),
            "runny_nose": ("body", "body_state"),
            "nose_ring": ("accessories", "jewelry"),
            "red_nose": ("accessories", "other_accessory"),
            "clown_nose": ("accessories", "other_accessory"),
            "fake_nose": ("accessories", "other_accessory"),
            "nose_tape": ("accessories", "other_accessory"),
            "nose_hook": ("adult", "adult_fetish"),
            "butterfly_on_nose": ("creatures", "insect"),
            "nose_picking": ("action", "daily_action"),
            "wiping_nose": ("action", "daily_action"),
            "blowing_nose": ("action", "daily_action"),
            "rubbing_nose": ("pose", "hand_gesture"),
            "nose_pinch": ("action", "interaction"),
            "poking_nose": ("action", "interaction"),
        }
        if base_name in brows_nose_exceptions:
            return brows_nose_exceptions[base_name]
        if "eyebrow" in tokens or "eyebrows" in tokens:
            return "face", "eyebrows"
        return "face", "nose"

    # v7: split the former mixed sleep/casual bucket by actual garment type.
    if (folder_id, category_id) == ("clothes_special", "sleep_casual"):
        if "sarong" in tokens:
            return "clothes_special", "traditional_world"
        if base_name in {"business_casual", "casual", "streetwear"}:
            return "clothing_appearance", "fashion_style"
        if "robe" in tokens or base_name == "bathrobe":
            return "clothes_special", "robe"
        return "clothes_special", "sleepwear"

    # The removed five-item design bucket duplicated better-defined categories:
    # crinoline is a structural skirt support; the rest are swimsuit cuts.
    if (folder_id, category_id) == ("underwear_swim", "underwear_design"):
        if base_name == "crinoline":
            return "clothing_detail", "other_structure"
        return "underwear_swim", "swimsuit"

    # v7: ears, horns and tails are independent creature traits.  The old name
    # "ears/horns/tails" was a literal overlap rather than a useful category.
    if (folder_id, category_id) == ("creatures", "animal_feature"):
        animal_feature_exceptions = {
            "fake_animal_ears": ("accessories", "headwear"),
            "mickey_mouse_ears": ("accessories", "headwear"),
            "minnie_mouse_ears": ("accessories", "headwear"),
            "fake_horns": ("accessories", "headwear"),
            "fake_antlers": ("accessories", "headwear"),
            "hair_ears": ("hair", "hair_style"),
            "raccoon_tails_(hairstyle)": ("hair", "hair_style"),
            "headphones_for_animal_ears": ("digital_media", "audio_device"),
            "earphones_on_animal_ears": ("digital_media", "audio_device"),
            "playing_with_another's_ears": ("action", "interaction"),
            "flapping_ears": ("action", "movement"),
            "flapping": ("action", "movement"),
            "innertube_with_ears": ("recreation", "sports"),
            "tail_insertion": ("adult", "adult_sex"),
            "implied_tail_plug": ("adult", "adult_toys"),
            "tail_bell": ("accessories", "badges_ornaments"),
            "bandaged_tail": ("body", "body_marks"),
            "foxtail": ("creatures", "tails"),
            "dock_(tail)": ("creatures", "tails"),
            "talons": ("creatures", "claw_scale"),
            "suction_cups": ("creatures", "claw_scale"),
            "hirschgeweih_antennas": ("mech_scifi", "machine"),
        }
        if name in animal_feature_exceptions:
            return animal_feature_exceptions[name]
        if tokens & {"wing", "wings", "feather", "feathers", "plumage"}:
            return "creatures", "wing_feather"
        if tokens & {"claw", "claws", "scale", "scales", "tentacle", "tentacles", "fin", "fins", "paw", "paws", "antenna", "antennae"}:
            return "creatures", "claw_scale"
        if tokens & {"ear", "ears"} or base_name.endswith(("_ear", "_ears")):
            return "creatures", "animal_ears"
        if tokens & {"horn", "horns", "antler", "antlers"}:
            return "creatures", "horns"
        if tokens & {"tail", "tails"}:
            return "creatures", "tails"
        return "creatures", "fur_feature"

    # v7: a halo is a geometric light marker, an aura/glow is emitted light,
    # while spells, beams and elemental powers are actual magical energy.  The
    # old bucket's 144 members were checked individually before this split.
    if (folder_id, category_id) == ("light_effect", "magic_effect"):
        halo_names = {
            "halo", "blue_halo", "pink_halo", "yellow_halo", "red_halo", "black_halo",
            "green_halo", "grey_halo", "traditional_halo", "purple_halo", "white_halo",
            "star_halo", "halo_behind_head", "rectangular_halo", "missing_halo",
            "multicolored_halo", "no_halo", "broken_halo", "aqua_halo", "spiked_halo",
            "orange_halo", "dark_halo", "brown_halo", "cross_halo", "two-tone_halo",
            "winged_halo", "melting_halo", "gradient_halo", "liquid_halo", "blood_halo",
            "heart_halo", "double_halo", "tilted_halo", "distorted_halo", "glowing_halo",
            "crescent_halo", "triangle_halo", "flaming_halo", "gold_halo", "side_halo",
            "intentionally_missing_halo", "multiple_halos", "no_halo_on_purpose",
            "flower_halo", "pregnancy_halo", "drawn_halo", "blurry_halo", "snowflake_halo",
        }
        glow_names = {
            "glowing", "glowing_eyes", "aura", "glowing_eye", "glowing_weapon", "dark_aura",
            "sparkling_aura", "glowing_butterfly", "glowing_hair", "loving_aura",
            "glowing_wings", "glowing_horns", "happy_aura", "glowing_flower", "glowing_hand",
            "glowing_mouth", "outer_glow", "glowing_lines", "glowing_gem", "glowing_clothes",
            "glowing_hands", "glowing_pupils", "glowing_skin", "glowing_arm", "red_aura",
            "glowing_feather", "blue_aura", "glowing_tail", "glowing_hot", "glowing_headgear",
            "glowing_heart", "glowing_fist", "glowing_crystal", "glowing_veins",
            "fiery_aura", "purple_aura", "glowing_arrow", "glowing_muzzle", "glowing_liquid",
            "aura_sphere_(pokemon)", "glowing_jewelry", "glowing_mushroom", "glowing_chest",
            "glowing_windows", "glowing_ears",
        }
        if name in halo_names:
            return "light_effect", "halo_effect"
        if name in glow_names:
            return "light_effect", "glow_aura"
        return "light_effect", "magic_energy"

    # v7: the old clothing-state bucket mixed actions with three distinct
    # garment states.  This ordered split was checked against all 386 members.
    if (folder_id, category_id) == ("clothing_detail", "clothing_state"):
        clothing_action_names = {
            "clothes_lift", "clothes_pull", "dressing", "dressing_another", "undressing",
            "undressing_another", "untying", "tying", "unbuttoning", "clothes_on_and_off",
            "imminent_forced_dressing", "skirt_flip", "clothes_tug", "removing_bra_under_shirt",
        }
        if (
            base_name.startswith(("adjusting_", "removing_", "putting_on_", "lifting_", "pulling_"))
            or any(fragment in base_name for fragment in ("_lift", "_pull", "_aside"))
            or base_name in clothing_action_names
        ):
            return "action", "clothing_action"
        if base_name == "lactation_through_clothes":
            return "clothing_detail", "damaged_dirty"
        if base_name in {"torn", "rags", "burning_clothes"} or base_name.startswith(("torn_", "wet_", "blood_on_")):
            return "clothing_detail", "damaged_dirty"
        if (
            base_name == "clothes_on_floor"
            or base_name.startswith(("unworn_", "no_", "missing_"))
            or "_unworn_" in base_name
        ):
            return "clothing_detail", "unworn_missing"
        return "clothing_detail", "open_wear"

    # v7: split structural garment details into non-overlapping construction
    # types, after removing actions, props and accessories found in the old mix.
    if (folder_id, category_id) == ("clothing_detail", "clothing_structure"):
        structure_exceptions = {
            "zipping": ("action", "clothing_action"),
            "unzipping": ("action", "clothing_action"),
            "pressing_button": ("action", "daily_action"),
            "hands_in_pocket": ("pose", "hand_gesture"),
            "thumb_in_pocket": ("pose", "hand_gesture"),
            "hand_in_another's_pocket": ("action", "interaction"),
            "in_pocket": ("pose", "body_pose"),
            "frilled_pillow": ("household_objects", "storage_furniture"),
            "frilled_umbrella": ("household_objects", "tools"),
            "safety_pin": ("household_objects", "tools"),
            "frilled_innertube": ("recreation", "sports"),
            "cardboard_cutout": ("culture_objects", "books_paper"),
            "frilled_headwear": ("accessories", "headwear"),
            "frilled_bonnet": ("accessories", "headwear"),
            "wide_brim": ("accessories", "headwear"),
            "eyewear_strap": ("accessories", "eyewear"),
            "frilled_ascot": ("accessories", "neckwear"),
            "frilled_necktie": ("accessories", "neckwear"),
            "frilled_bowtie": ("accessories", "neckwear"),
            "frilled_armband": ("accessories", "handwear"),
            "frilled_wristband": ("accessories", "handwear"),
            "glove_cuffs": ("accessories", "handwear"),
            "frilled_armlet": ("accessories", "jewelry"),
            "cellphone_strap": ("accessories", "other_accessory"),
            "shoulder_sash": ("accessories", "bags_belts"),
            "dress_flower": ("accessories", "badges_ornaments"),
            "pom_pom": ("accessories", "badges_ornaments"),
            "single_epaulette": ("accessories", "badges_ornaments"),
            "weapon_strap": ("weapons", "other_weapon"),
            "shoe_strap": ("legwear_footwear", "shoes"),
            "shirt_tucked_in": ("clothing_detail", "open_wear"),
            "hem_peeking_out": ("clothing_detail", "open_wear"),
        }
        if base_name in structure_exceptions:
            return structure_exceptions[base_name]
        if base_name in {
            "pocket", "breast_pocket", "exposed_pocket", "object_in_pocket", "pen_in_pocket",
            "pocket_square", "phone_in_pocket", "carrot_in_pocket",
        }:
            return "clothing_detail", "pocket_detail"
        if tokens & {"sleeve", "sleeves", "cuff", "cuffs"}:
            return "clothing_detail", "sleeve_detail"
        if tokens & {"collar", "neckline", "lapel"}:
            return "clothing_detail", "collar_detail"
        if tokens & {"strap", "straps", "suspender", "suspenders"}:
            return "clothing_detail", "strap_detail"
        if tokens & {"cutout", "cutouts", "slit", "slits"}:
            return "clothing_detail", "cutout_slit"
        if (
            tokens & {"button", "buttons", "zipper", "zippers", "buckle", "buckles"}
            or any(fragment in base_name for fragment in ("lace-up", "cross-laced", "o-ring"))
            or base_name in {"drawstring", "pankou", "toggles", "pull_cord"}
        ):
            return "clothing_detail", "fastener"
        if tokens & {"frill", "frills", "frilled", "trim", "trimmed", "feather", "fringe"}:
            return "clothing_detail", "trim_detail"
        return "clothing_detail", "other_structure"

    # v7: split the oversized generic top and outerwear buckets by garment form.
    if (folder_id, category_id) == ("clothes_main", "tops"):
        top_exceptions = {
            "shirt_tug": ("action", "clothing_action"),
            "sweater_tug": ("action", "clothing_action"),
            "hand_under_shirt": ("pose", "hand_gesture"),
            "gym_shirt": ("clothes_special", "sports_uniform"),
            "basketball_jersey": ("clothes_special", "sports_uniform"),
            "baseball_jersey": ("clothes_special", "sports_uniform"),
            "bike_jersey": ("clothes_special", "sports_uniform"),
            "compression_shirt": ("clothes_special", "sports_uniform"),
            "tuxedo_shirt": ("clothes_main", "formal_suit"),
            "jeogori": ("clothes_special", "traditional_east"),
            "chanchanko": ("clothes_special", "traditional_east"),
            "orange_tabard": ("clothes_main", "cape_cloak"),
            "sleeveless_shrug": ("clothes_main", "cardigan_shawl"),
            "playboy_bunny_vest": ("clothes_special", "themed_costume"),
            "fuck-me_shirt": ("adult", "adult_clothes"),
            "muffin_top": ("body", "build"),
            "shirt_tan": ("body", "skin"),
            "racerback": ("clothing_detail", "strap_detail"),
        }
        if base_name in top_exceptions:
            return top_exceptions[base_name]
        top_states = {
            "unbuttoned_shirt", "tied_shirt", "untucked_shirt", "sweater_around_waist", "upshirt",
            "shirt_partially_tucked_in", "shirt_around_waist", "sweater_around_neck", "shirt_on_shoulders",
            "shirt_behind_neck", "tied_sweater", "shirt_over_head", "jacket_over_hoodie", "shirt_under_shirt",
            "sweater_tucked_in", "shirt_under_sweater", "dress_over_shirt", "bikini_top_under_shirt",
            "camisole_over_clothes", "sweater_under_shirt", "tied_hoodie_strings",
        }
        if base_name in top_states:
            return "clothing_detail", "open_wear"
        if tokens & {"shirt", "blouse", "tunic", "jersey", "chemise", "guimpe"}:
            return "clothes_main", "shirt_top"
        if tokens & {"sweater", "hoodie"} or base_name in {"turtleneck", "sleeveless_turtleneck"}:
            return "clothes_main", "sweater_hoodie"
        return "clothes_main", "vest_top"

    if (folder_id, category_id) == ("clothes_main", "outerwear"):
        outer_exceptions = {
            "jacket_tug": ("action", "clothing_action"),
            "shared_coat": ("action", "interaction"),
            "shared_jacket": ("action", "interaction"),
            "shared_cape": ("action", "interaction"),
            "jacket_over_head": ("pose", "body_pose"),
            "track_jacket": ("clothes_special", "sports_uniform"),
            "hooded_track_jacket": ("clothes_special", "sports_uniform"),
            "nijigasaki_track_jacket": ("clothes_special", "sports_uniform"),
            "suit_jacket": ("clothes_main", "formal_suit"),
            "tailcoat": ("clothes_main", "formal_suit"),
            "flak_jacket": ("clothes_special", "armor"),
            "tracen_winter_coat": ("clothes_special", "school_uniform"),
            "fatui_coat": ("clothes_special", "occupation_uniform"),
            "closed_lab_coat": ("clothes_special", "occupation_uniform"),
            "barber_cape": ("clothes_special", "occupation_uniform"),
        }
        if base_name in outer_exceptions:
            return outer_exceptions[base_name]
        if base_name in {
            "jacket_on_shoulders", "coat_on_shoulders", "jacket_around_waist", "cardigan_around_waist",
            "tied_jacket", "jacket_over_shoulder", "cardigan_on_shoulders", "jacket_around_neck",
            "unworn_blazer", "coat_stash",
        }:
            return "clothing_detail", "open_wear"
        if tokens & {"jacket", "coat", "blazer", "raincoat", "parka", "windbreaker", "duster", "smock"} or base_name == "sukajan":
            return "clothes_main", "jacket_coat"
        if tokens & {"cape", "cloak", "poncho", "tabard", "surcoat"}:
            return "clothes_main", "cape_cloak"
        return "clothes_main", "cardigan_shawl"

    # v7: separate phones, game hardware, computers, audio gear and imaging
    # devices.  The former two mixed digital buckets hid these distinct uses.
    if (folder_id, category_id) == ("digital_media", "phone_computer"):
        digital_exceptions = {
            "talking_on_phone": ("action", "interaction"),
            "showing_phone": ("action", "interaction"),
            "cradling_phone": ("action", "holding"),
            "hacking": ("action", "daily_action"),
            "gacha_(game_mechanic)": ("recreation", "games"),
            "cellphone_photo": ("digital_media", "camera_video"),
            "phone_over_face": ("composition", "framing"),
            "cellphone_charm": ("accessories", "other_accessory"),
            "smartphone_case": ("accessories", "other_accessory"),
            "rabbit_ear_smartphone_case": ("accessories", "other_accessory"),
            "remote_control": ("household_objects", "tools"),
            "radio_controller": ("household_objects", "tools"),
            "phone_stand": ("household_objects", "other_object"),
            "odaibako": ("meta_info", "meta"),
            "infection_monitor_(arknights)": ("mech_scifi", "scifi_device"),
        }
        if name in digital_exceptions:
            return digital_exceptions[name]
        phone_devices = {
            "phone", "cellphone", "smartphone", "flip_phone", "corded_phone", "antique_phone", "iphone",
            "rotary_phone", "payphone", "feature_phone", "bar_phone", "string_phone", "camera_phone",
            "phone_with_ears", "cordless_phone", "phone_on_wall", "slide_phone", "cracked_phone", "x-ray_phone",
        }
        if name in phone_devices:
            return "digital_media", "phone_device"
        game_devices = {
            "controller", "game_controller", "handheld_game_console", "nintendo_switch", "game_console", "d-pad",
            "playstation_controller", "playstation_portable", "nintendo_ds", "game_boy", "joy-con", "nintendo_3ds",
            "dualshock", "game_boy_(original)", "game_boy_advance", "famicom", "playstation_vita", "playstation_5",
            "nintendo_switch_2", "super_famicom_controller", "gamecube_controller", "nintendo_64_controller",
            "xbox_controller", "famicom_controller", "nintendo_switch_pro_controller", "flight_stick",
        }
        if name in game_devices:
            return "digital_media", "game_device"
        return "digital_media", "computer_device"

    if (folder_id, category_id) == ("digital_media", "camera_media"):
        media_exceptions = {
            "recording_audio": ("action", "daily_action"),
            "adjusting_headphones": ("action", "daily_action"),
            "adjusting_headset": ("action", "daily_action"),
            "shared_earphones": ("action", "interaction"),
            "game_show": ("style", "genre"),
            "binoculars": ("household_objects", "tools"),
        }
        if name in media_exceptions:
            return media_exceptions[name]
        audio_devices = {
            "headphones", "microphone", "headset", "headphones_around_neck", "animal_ear_headphones",
            "earphones", "cat_ear_headphones", "radio_antenna", "microphone_stand", "earpiece", "megaphone",
            "speaker", "mp3_player", "earbuds", "walkie-talkie", "radio", "cd", "ipod",
            "behind-the-head_headphones", "audio_jack", "throat_microphone", "wireless_earphones",
            "headphones_removed", "boombox", "earphones_removed", "ipod_nano", "cassette_player",
            "cassette_tape", "digital_walkman", "speaking_tube_headset", "studio_microphone",
            "single_earphone_removed", "walkman", "walkman_nw-s203f", "stereo", "binaural_microphone",
            "axent_wear", "akg_k-series_headphones", "humagear_headphones", "field_radio", "bunny_headphones",
            "boom_microphone", "wireless_microphone", "horn_speaker", "tape_recorder", "beats_by_dr._dre",
            "microphone_cord", "sony_mdr-series_headphones", "in-ear_earphones",
        }
        if name in audio_devices:
            return "digital_media", "audio_device"
        return "digital_media", "camera_video"

    # v7: remove overlapping body-part buckets.  Cross-domain actions, props and
    # garments are supplied as exact semantic overrides below; these rules cover
    # the remaining physical attributes only.
    if (folder_id, category_id) == ("body", "chest"):
        if name in {"heart_(organ)", "stomach_(organ)"} or base_name == "brain":
            return "body", "internal_organs"
        if base_name in {
            "extra_breasts", "breast_expansion", "breast_reduction", "floating_breasts",
            "bursting_breasts", "bursting_pectorals", "stomach_ache", "full_stomach", "stomach_growling",
        }:
            return "body", "body_state"
        breast_words = {
            "breast", "breasts", "pectoral", "pectorals", "cleavage", "chest", "boob", "boobs",
            "bust", "sidepec", "underpec", "underbust",
        }
        if tokens & breast_words or "cup_size" in base_name:
            return "body", "breast_chest"
        return "body", "torso_back"

    if (folder_id, category_id) == ("body", "waist_legs"):
        if tokens & {"leg", "legs", "thigh", "thighs", "knee", "knees", "calf", "calves"}:
            return "body", "legs_knees"
        if tokens & {"waist", "hip", "hips", "ass", "butt", "buttocks", "groin", "crotch", "lap", "lower", "body"}:
            return "body", "waist_hips"
        return "body", "body_state"

    if (folder_id, category_id) == ("body", "arms_hands_feet"):
        if base_name in {
            "red_hands", "black_hands", "blue_hands", "purple_hands", "green_hands", "yellow_hands",
            "red_feet", "golden_arms", "light-skinned_palms", "green_arm",
        }:
            return "body", "skin"
        if tokens & {"foot", "feet", "toe", "toes", "sole", "soles", "heel", "heels", "toenail", "toenails"}:
            return "body", "feet_toes"
        if tokens & {"arm", "arms", "hand", "hands", "finger", "fingers", "nail", "nails", "elbow", "elbows", "armpit", "armpits", "palm", "palms", "triceps", "joint", "joints"}:
            return "body", "arms_hands"
        return "body", "body_state"

    # v7: violence is sensitive content, but it is not inherently adult sexual
    # content.  The former gore bucket was checked item by item against its wiki.
    if (folder_id, category_id) == ("adult", "adult_gore"):
        if base_name == "human_head":
            return "creatures", "fantasy_creature"
        if base_name == "detached_legs":
            return "body", "body_state"
        if base_name in {"blood_on_ground", "pool_of_blood", "blood_on_wall", "blood_spray", "blood_trail"}:
            return "sensitive", "blood"
        if base_name in {
            "corpse", "impaled", "stab", "self-harm", "torture", "wrist_cutting", "suicide",
            "crucifixion", "cannibalism", "hanged", "implied_murder", "imminent_suicide",
            "execution", "knife_in_head", "pile_of_corpses",
        }:
            return "sensitive", "injury_death"
        if base_name in {"ryona", "ero_guro", "reverse_ryona"}:
            return "sensitive", "sexual_violence"
        return "sensitive", "gore"

    # Body fluids and similarly named visual effects were previously mixed with
    # sexual fluids.  Keep only the genuinely sexual entries in the adult group.
    if (folder_id, category_id) == ("adult", "adult_fluid"):
        if base_name in {"vomit", "poop", "lactation", "male_lactation", "alternate_body_fluid", "pee", "pee_stain"}:
            return "body", "body_state"
        if base_name == "lactation_through_clothes":
            return "clothing_detail", "damaged_dirty"
        if base_name == "saliva_pool":
            return "face", "mouth"
        if base_name in {"ambiguous_red_liquid", "squirting_liquid"}:
            return "light_effect", "other_effect"
        if base_name in {"yellow_blood", "black_blood", "blood_drop"}:
            return "sensitive", "blood"
        if base_name == "sperm_cell":
            return "adult", "adult_anatomy"
        if base_name in {"gokkun", "licking_cum", "cum_swap", "own_cum_in_mouth"}:
            return "adult", "adult_oral"
        if base_name in {"no_nut_november", "nonstop_nut_november"}:
            return "adult", "adult_other"
        if base_name == "requesting_internal_cumshot":
            return "adult", "adult_suggestive"

    if (folder_id, category_id) == ("adult", "adult_suggestive"):
        if base_name == "foodgasm":
            return "expression", "positive"
        if base_name in {"presenting_tanlines", "presenting_foot"}:
            return "pose", "body_pose"
        if base_name == "body_exploration":
            return "adult", "adult_anatomy"

    # Restraint without documented sexual context and vore belong to the
    # independent violence/sensitivity library, not the adult fetish bucket.
    if (folder_id, category_id) == ("adult", "adult_fetish"):
        if base_name in {"vore", "imminent_vore"}:
            return "sensitive", "vore"
        if base_name in {
            "chained", "chained_wrists", "immobilization", "pillory", "stocks", "cuffed",
            "metal_wrist_cuffs", "rope_around_neck", "hobble", "restraints", "belly_riding",
            "tied_up", "jinki-style_restrained", "forced",
        }:
            return "sensitive", "restraint"
        if base_name.endswith("_restrained"):
            return "sensitive", "restraint"
        adult_toys = {
            "anal_beads", "anal_hook", "animal_dildo", "artificial_vagina_with_body", "butt_plug",
            "colored_condom", "condom", "condom_packet_strip", "condom_thigh_strap", "condom_wrapper",
            "dildo", "dildo_gag", "dildo_harness", "dildo_reveal", "double_dildo", "dragon_dildo",
            "egg_vibrator", "enema", "food_dildo", "hitachi_magic_wand", "holding_sex_toy",
            "horse_dildo", "huge_dildo", "implied_vibrator", "living_fleshlight", "lube",
            "multiple_condoms", "okamoto_condoms", "pointless_condom", "public_vibrator",
            "rabbit_vibrator", "remote_control_vibrator", "sex_doll", "sex_machine", "sex_toy",
            "sex_toy_pull", "spiked_dildo", "strap-on", "suction_cup_dildo", "too_many_sex_toys",
            "vibrator", "vibrator_bulge", "vibrator_cord", "vibrator_in_anus", "vibrator_in_thigh_strap",
            "vibrator_on_clitoris", "vibrator_on_nipple", "vibrator_on_penis", "wireless_sex_toy_controller",
            "anal_ball_wear", "anal_tail",
        }
        if base_name in adult_toys:
            return "adult", "adult_toys"
        adult_bondage = {
            "applying_gag", "armbinder", "ball_and_chain_restraint", "ball_gag", "bdsm", "bit_gag",
            "bondage", "bondage_mittens", "bondage_outfit", "box_tie", "breast_bondage",
            "chastity_cage", "chastity_cage_strap", "cleave_gag", "clitoris_chain", "clitoris_torture",
            "cloth_gag", "dental_gag", "dilation_belt", "flat_chastity_cage", "frogtie", "gag",
            "gag_chinstrap", "gag_harness", "gagged", "gimp_suit", "hair_bondage", "hogtie",
            "implied_bondage", "improvised_gag", "knot_gag", "linked_gag", "nipple_chain",
            "nipple_clamps", "nipple_torture", "o-ring_harness", "over_the_nose_gag",
            "predicament_bondage", "public_bondage", "ribbon_bondage", "ring_gag", "self_bondage",
            "shibari", "shibari_over_clothes", "shibari_under_clothes", "shock_collar",
            "single_handcuff", "small_chastity_cage", "snake_bondage", "spreader_bar",
            "standing_restraints", "stationary_restraints", "stealth_bondage", "stuffed_gag",
            "suspension", "tape_bondage", "tape_gag", "tickle_torture", "ungagged",
            "upright_restraints", "wiffle_gag", "x-cross",
        }
        if base_name in adult_bondage:
            return "adult", "adult_bondage"

    # v7: self-stimulation and partner hand actions were previously conflated.
    if (folder_id, category_id) == ("adult", "adult_self"):
        if (
            "masturbat" in base_name
            or "_own_" in base_name
            or base_name.startswith(("grabbing_own_", "spreading_own_", "tweaking_own_", "auto"))
            or base_name in {"crotch_rub", "tail_masturbation", "water_masturbation"}
        ):
            return "adult", "adult_self"
        return "adult", "adult_hand"

    # Anatomy entries whose documented subject is an action are routed to the
    # matching adult action class instead of being kept as body morphology.
    if (folder_id, category_id) == ("adult", "adult_anatomy"):
        if base_name in {
            "nipple_stimulation", "nipple_tweak", "penis_grab", "clitoral_stimulation",
            "caressing_testicles", "nipple_rub", "nipple_pull", "glansjob", "testicle_grab",
            "nipple_tweak_through_clothes", "penis_milking", "nipple_press", "squeezing_testicles",
            "womb_massage", "clitoris_tweak", "tickling_pussy", "tickling_nipples", "nipple_flick",
            "penis_in_glove", "poking_penis", "pussy_squeeze",
        }:
            return "adult", "adult_hand"
        if base_name in {
            "penis_on_face", "penises_touching", "penis_on_ass", "tentacle_on_penis",
            "nipples_pressed_together", "pussy_sandwich", "penis_and_testicles_touching",
            "slapping_with_penis", "testicles_touching", "penis_hug", "poking_with_penis",
        }:
            return "adult", "adult_sex"
        if base_name in {"penis_awe", "spread_pussy_under_clothes", "foot_pussy"}:
            return "adult", "adult_suggestive"
        if base_name in {"small_penis_humiliation", "nipple_injection", "food_on_penis"}:
            return "adult_kink", "adult_fetish"
        if base_name in {"penis_measuring", "nipple_guessing_game", "areola_measuring", "penis_chart"}:
            return "adult", "adult_other"

    if (folder_id, category_id) == ("adult", "adult_sex"):
        if base_name in {"anal_hair", "vaginal_prolapse", "anal_prolapse", "anal_cross-section", "fertilization"}:
            return "adult", "adult_anatomy"
        if base_name == "anal_fluid":
            return "adult", "adult_fluid"
        if base_name == "after_anilingus":
            return "adult", "adult_oral"
        if base_name in {"anal_ball_wear", "anal_tail"}:
            return "adult", "adult_toys"
        if base_name in {"sex_ed", "paizuri_day"}:
            return "adult", "adult_other"

    if (folder_id, category_id) == ("adult", "adult_other"):
        if base_name in {"peeing", "peeing_self", "peeing_together", "peeing_in_cup", "peeing_in_bottle", "assisted_peeing"}:
            return "action", "daily_action"
        if base_name == "fart":
            return "body", "body_state"
        if base_name == "forced":
            return "sensitive", "restraint"
        if base_name == "drinking_pee":
            return "adult", "adult_fetish"
        if base_name in {
            "after_rape", "assisted_rape", "bestiality", "forced_orgasm", "group_incest",
            "imminent_bestiality", "imminent_rape", "implied_bestiality", "implied_incest",
            "implied_rape", "incest", "kodomo_doushi", "lolidom", "molestation", "rape",
            "sexual_harassment", "shotadom", "sleep_molestation", "toddlercon", "twincest",
        }:
            return "adult", "adult_taboo"

    # Predicate-first compounds describe an action even when their object is a
    # body part, animal, garment, or prop.  Apply this as a final semantic pass
    # so noun rules cannot steal tags such as ``kissing_hand`` or
    # ``viewer_holding_phone``.  Explicit adult locations keep their stricter
    # classification.
    if base_name == "twisted_torso":
        return "pose", "body_pose"
    if base_name.startswith("kissing_") and folder_id != "adult":
        return "action", "interaction"
    if base_name.startswith("licking_") and folder_id != "adult":
        if base_name == "licking_food":
            return "action", "daily_action"
        return "action", "interaction"
    if base_name.startswith("looking_at_") and folder_id != "adult":
        return "pose", "gaze"
    if base_name.startswith("viewer_holding_"):
        return "action", "holding"
    if base_name.startswith("playing_with_"):
        return "action", "interaction"
    if base_name.startswith("playing_") and not base_name.startswith("playing_card"):
        return "action", "daily_action"
    if base_name.startswith("washing_") and base_name != "washing_machine":
        return "action", "daily_action"
    if base_name == "watching" or base_name.startswith("watching_"):
        return "action", "daily_action"
    if base_name in {
        "assisted_carrying", "carry_me", "lifting_animal", "cleaning_eyewear",
        "looking_for_glasses",
    }:
        return "action", "holding" if base_name in {"assisted_carrying", "carry_me", "lifting_animal"} else "daily_action"
    if base_name in {
        "hugging_another's_leg", "arm_on_another's_shoulder", "arms_on_another's_shoulder",
        "imminent_hand_holding", "noses_touching", "touching",
    }:
        return "action", "interaction"

    # Calendar themes and permanent skin details take precedence over the
    # animal/body-part tokens embedded in their names.
    if base_name.startswith("year_of_the_"):
        return "time_weather", "holiday"
    if base_name == "freckles" or base_name == "no_freckles" or base_name.endswith("_freckles") or base_name.startswith("mole_on_"):
        if folder_id != "adult":
            return "body", "mole_freckle"

    # Piercing tags describe jewellery/body modification, not the pierced face
    # part.  Genital variants remain in the adult fetish group.
    piercing_tag = base_name == "piercing" or base_name.endswith(("_piercing", "_piercings"))
    if piercing_tag:
        if tokens & {"areola", "clitoral", "clitoris", "frenulum", "labia", "nipple", "penis", "pussy", "scrotum"}:
            return "adult_kink", "adult_piercing"
        return "accessories", "jewelry"

    east_traditional = {"ainu_clothes", "miao_clothes"}
    world_traditional = {
        "african_clothes", "arabian_clothes", "ancient_egyptian_clothes", "ancient_greek_clothes",
        "greco-roman_clothes", "asian_indian_clothes", "indian_clothes", "indonesian_clothes",
        "kazakh_clothes", "mayan_clothes", "mexican_clothes", "mexican_dress", "mongolian_clothes",
        "native_american_clothes", "renaissance_clothes", "roman_clothes", "russian_clothes",
        "slavic_clothes", "thai_clothes", "tibetan_clothes", "ukrainian_clothes", "vietnamese_clothes",
        "german_clothes", "colombian_clothes", "sari", "dirndl", "toga", "kilt", "sarong",
    }
    sports_uniforms = {
        "american_football_uniform", "baseball_uniform", "basketball_uniform", "cycling_uniform",
        "rugby_uniform", "soccer_uniform", "tennis_uniform", "track_uniform", "volleyball_uniform",
        "cheerleader", "dougi", "gym_uniform", "sportswear", "tutu", "bikesuit",
        "riding_outfit", "wrestling_outfit", "millennium_cheerleader_outfit",
    }
    if base_name in east_traditional:
        return "clothes_special", "traditional_east"
    if base_name in world_traditional:
        return "clothes_special", "traditional_world"
    if base_name in sports_uniforms or base_name.endswith((
        "_gym_uniform", "_training_uniform", "_cheerleader_uniform", "_cheerleader_outfit", "_sportswear",
    )):
        return "clothes_special", "sports_uniform"
    if (base_name == "babydoll" or base_name.endswith("_babydoll")) and folder_id not in {"action", "clothing_detail"}:
        return "underwear_swim", "bra_lingerie"

    # Split the old mixed "suit" bucket into garment form and actual use.
    if (folder_id, category_id) == ("clothes_main", "suit"):
        protective_suits = {
            "deva_battle_suit", "fortified_suit", "gantz_suit", "gravity_suit", "hev_suit",
            "planet_diving_suit", "praetor_suit",
        }
        themed_suits = {
            "mobile_trace_suit", "order_suit", "palette_suit", "parasite_suit", "sneaking_suit",
            "taimanin_suit", "varia_suit", "vault_suit", "zero_suit",
        }
        if base_name == "mecha_pilot_suit":
            return "clothes_special", "occupation_uniform"
        if base_name == "track_suit" or base_name.endswith("_track_suit"):
            return "clothes_special", "sports_uniform"
        if base_name in protective_suits or any(base_name.startswith(item + "_") for item in protective_suits):
            return "clothes_special", "helmet_protective"
        if base_name in themed_suits:
            return "clothes_special", "themed_costume"
        if base_name in {"skin_suit", "leather_suit"}:
            return "underwear_swim", "bodysuit_leotard"
        if base_name == "overalls" or base_name.endswith(("_overalls", "_jumpsuit", "_romper")) or base_name in {"jumpsuit", "romper"}:
            return "clothes_main", "jumpsuit"
        return "clothes_main", "formal_suit"

    # Relationship tags used to share a catch-all bucket inside 人物构成.
    # Route them into explicit pair/family/interaction/organisation groups.
    family_words = {
        "family", "parent", "parents", "child", "children", "mother", "father", "daughter", "son",
        "sibling", "siblings", "sister", "sisters", "brother", "brothers", "twin", "twins", "cousin", "cousins",
    }
    group_words = {
        "team", "club", "clan", "army", "alliance", "force", "forces", "faction", "organization",
        "organisation", "corps", "squad", "gang", "guild", "unit", "group", "heroines",
    }
    known_groups = {
        "ho-kago_tea_time", "tea_party", "tea_party_(blue_archive)", "holy_quintet", "sailor_senshi",
        "imperium_of_man", "ultramarines", "sternritter", "wandenreich", "thirteen_flame-chasers",
        "chaos_(warhammer)", "inquisition_(warhammer)", "red_ribbon_army", "type-moon_heroines",
        "chaos", "inquisition", "cleaning_&_clearing", "hololive_fantasy", "pink_check_school",
        "re;iris", "afterglow", "golden_deer", "sunset_nostalgie", "pastel_palettes",
        "japan_national_police", "idol_heroes", "sangvis_ferri", "zeon", "shinsengumi",
        "emperor's_children", "the_children", "earth_federation", "kessoku_band", "dollchestra",
    }
    if folder_id == "people" and category_id == "relationship":
        folder_id = "relationships"
        if tokens & group_words or name.endswith("_(group)") or base_name in known_groups:
            category_id = "group_faction"
        elif tokens & family_words:
            category_id = "family_relation"
        elif "couple" in tokens:
            category_id = "romance_orientation"
        else:
            category_id = "social_relation"
    elif folder_id == "themes" and category_id in {"romance_orientation", "family_relation", "social_relation"}:
        folder_id = "relationships"
    if folder_id == "relationships" and category_id == "social_relation":
        if tokens & group_words or name.endswith("_(group)") or base_name in known_groups:
            return "relationships", "group_faction"
        comparison_names = {
            "age_difference", "height_difference", "look-alike", "matching_outfits", "size_comparison",
            "size_difference",
        }
        if base_name in comparison_names:
            return "relationships", "comparison"

    if name.endswith("_(eve_online)") and re.search(r"(ship|cruiser|battlecruiser|frigate|droneboat)$", base_name):
        return "transport_play", "air_vehicle"

    if folder_id == "other":
        group_exceptions = {"condenser_unit", "post_guild_war_celebration", "kurokumo_clan"}
        if (tokens & group_words or base_name in known_groups) and base_name not in group_exceptions:
            return "relationships", "group_faction"
        if tokens & {"husband", "wife", "wives", "parent"}:
            return "relationships", "family_relation"
        if "harem" in tokens:
            return "relationships", "romance_orientation"
        if name.endswith("_(company)"):
            return "text_meta", "brand"

    if folder_id == "legwear_footwear" and category_id == "armor":
        if base_name in {"no_armor", "unworn_armor", "blood_on_armor"}:
            return ("clothing_detail", "damaged_dirty") if base_name == "blood_on_armor" else ("clothing_detail", "unworn_missing")
        if base_name == "metal_wrist_cuffs":
            return "sensitive", "restraint"
        if base_name == "wrist_cuffs" or base_name.endswith("_wrist_cuffs"):
            return "accessories", "handwear"
        if base_name == "chaps":
            return "clothes_main", "bottoms"
        if base_name == "gaiters" or base_name.endswith("_gaiters"):
            return "legwear_footwear", "stockings"
        if base_name in {"bulletproof_vest", "life_vest", "load_bearing_vest", "shoulder_pads", "wrist_guards"}:
            return "clothes_special", "helmet_protective"
        return "clothes_special", "armor"
    if folder_id in {"legwear_footwear", "clothes_special"} and category_id == "helmet_protective":
        if base_name == "flight_suit":
            return "clothes_special", "occupation_uniform"
        if base_name == "racing_suit":
            return "clothes_special", "sports_uniform"
        if base_name == "snorkel":
            return "recreation", "sports"
        if base_name == "helm" or "helmet" in tokens or base_name in {
            "armet", "assault_visor", "face_shield", "kabuto", "pickelhaube",
        }:
            return "clothes_special", "helmet"
        return "protective_clothes", "helmet_protective"
    if folder_id == "culture_objects" and category_id in {"phone_computer", "camera_media"}:
        return normalize_location(("digital_media", category_id), tag_name)
    if folder_id == "transport_play" and category_id in {"sports", "games", "toys"}:
        return "recreation", category_id
    if folder_id == "creatures" and category_id in {"plant", "mineral"}:
        return "nature", category_id
    if folder_id == "text_meta" and category_id in {"meme", "cosplay", "censorship", "meta"}:
        return "meta_info", category_id

    if (folder_id, category_id) == ("composition", "focus") and (base_name == "back" or (base_name.endswith("_focus") and base_name not in {"soft_focus", "sharp_focus"})):
        return "composition", "subject_focus"
    if (folder_id, category_id) == ("composition", "framing"):
        border_names = {"border", "framed", "frame", "letterboxed", "pillarboxed", "round_image", "partially_bordered"}
        if "border" in tokens or base_name in border_names or base_name.endswith(("_border", "_bordered")):
            return "composition", "border"

    if (folder_id, category_id) == ("household_objects", "lighting_clock"):
        if tokens & {"clock", "watch", "timer", "hourglass", "sundial"}:
            return "household_objects", "clock"
        electric_fans = {"electric_fan", "ceiling_fan", "handheld_electric_fan", "bladeless_fan"}
        if base_name in electric_fans or tokens & {"appliance", "refrigerator", "oven", "heater", "conditioner", "cooker", "boiler", "cooler", "machine", "television", "blender", "mixer", "toaster", "dishwasher", "dryer", "vacuum"}:
            return "household_objects", "appliance"
        if base_name == "fan" or base_name.endswith("_fan"):
            return "household_objects", "tools"

    if (folder_id, category_id) == ("weapons", "polearm") and (tokens & {"hammer", "mallet", "mace", "club", "flail", "whip", "chain", "bat", "tonfa"} or base_name.endswith("hammer")):
        return "weapons", "blunt_chain"

    if folder_id == "food_drink":
        if tokens & {"egg", "eggs", "cheese", "butter", "yogurt", "dairy"} and category_id in {"staple_food", "meat_seafood", "drink"}:
            return "food_drink", "dairy_ingredient"
        if category_id == "staple_food" and tokens & {"bread", "bun", "buns", "baguette", "croissant", "pastry", "dough", "toast", "roll", "flatbread"}:
            return "food_drink", "bakery"

    if (folder_id, category_id) == ("creatures", "animal_feature"):
        if tokens & {"wing", "wings", "feather", "feathers", "plumage"}:
            return "creatures", "wing_feather"
        if tokens & {"claw", "claws", "scale", "scales", "tentacle", "tentacles", "fin", "fins", "paw", "paws", "antenna", "antennae"}:
            return "creatures", "claw_scale"

    if base_name == "crossdressing" or base_name.startswith("crossdressing_"):
        return "themes", "identity_change"
    if base_name == "metal_wrist_cuffs":
        return "sensitive", "restraint"
    if base_name == "wrist_cuffs" or base_name.endswith("_wrist_cuffs"):
        return "accessories", "handwear"

    # v8 display hierarchy.  Keep the mature v7 semantic classifier above and
    # move only stable semantic groups into smaller, plain-language folders.
    # normalize_location() applies this after any legacy target has settled.
    if folder_id == "body" and category_id in {
        "skin", "tattoo_mark", "mole_freckle", "scar_wound", "bandage_patch",
        "surface_stain", "surface_decor", "body_hair", "body_function", "body_state",
    }:
        return "body_detail", category_id

    if folder_id == "clothes_main" and category_id in {
        "jacket_coat", "cape_cloak", "cardigan_shawl", "formal_suit", "jumpsuit",
    }:
        return "outerwear_suits", category_id
    if folder_id == "clothes_special":
        if category_id in {"school_uniform", "occupation_uniform", "sports_uniform", "themed_costume"}:
            return "uniform_costume", category_id
        if category_id in {"traditional_east", "traditional_world"}:
            return "traditional_clothes", category_id
        if category_id == "casualwear":
            return "clothing_appearance", "fashion_style"
        if category_id in {"sleepwear", "robe"}:
            return "clothes_main", category_id
        if category_id in {"armor", "helmet", "helmet_protective"}:
            return "protective_clothes", category_id

    if folder_id == "clothing_detail" and category_id in {"damaged_dirty", "unworn_missing", "open_wear"}:
        return "clothing_state", category_id
    if (folder_id, category_id) == ("clothing_detail", "other_clothes"):
        adult_clothing_fragments = {
            "erection", "vibrator", "dildo", "condom", "clitoral", "buttjob", "breast_sucking",
            "fuck-me", "nippleless", "object_in_clothes", "tentacles_under", "hand_under_clothes",
        }
        if any(fragment in base_name for fragment in adult_clothing_fragments):
            return "adult_body", "adult_suggestive"
        if any(fragment in base_name for fragment in (
            "dirty", "sweaty", "burnt", "stained", "dissolving", "exploding", "paint_on",
            "food_on", "chocolate_on", "frayed", "steaming", "wet_clothes",
        )):
            return "clothing_state", "damaged_dirty"
        if any(fragment in base_name for fragment in (
            "backless", "sideless", "frontless", "through_clothes", "tail_through", "wings_through",
        )):
            return "clothing_detail", "cutout_slit"
        if any(fragment in base_name for fragment in (
            "argyle", "patterned", "patchwork", "food-themed", "gingham", "diamond", "split-color",
        )):
            return "clothing_detail", "clothing_pattern"
        if any(fragment in base_name for fragment in (
            "shiny", "fluffy", "iridescent", "reflective", "quilted", "liquid", "skeletal", "fiery",
        )):
            return "clothing_detail", "clothing_material"
        if any(fragment in base_name for fragment in (
            "idol_clothes", "harem_outfit", "tactical_clothes", "biker_clothes", "prison_clothes",
            "aristocratic_clothes", "workout_clothes", "ballet_class_clothes", "dancer_outfit",
            "dormitory_outfit", "clan_outfit", "traditional_clothes", "hawaiian_clothes",
            "living_clothes", "expressive_clothes", "transforming_clothes", "plant_clothing",
        )):
            return "uniform_costume", "themed_costume"
        return "clothing_detail", "silhouette_fit"

    if folder_id == "creatures" and category_id in {
        "animal_ears", "horns", "tails", "fur_feature", "wing_feather", "claw_scale",
    }:
        return "animal_traits", category_id
    if folder_id == "indoor_scene" and category_id in {"urban", "architecture", "surface"}:
        return "urban_architecture", category_id
    if folder_id == "outdoor_scene" and category_id in {"background_plain", "background_pattern"}:
        return "background", category_id
    if folder_id == "text_meta" and category_id in {
        "general_symbol", "shape_math", "music_symbol", "religious_symbol", "zodiac_symbol",
        "flag", "emblem", "science_sign",
    }:
        return "symbols", category_id

    if folder_id == "adult" and category_id in {
        "adult_nudity", "adult_anatomy", "adult_clothes",
    }:
        return "adult_body", category_id
    if folder_id == "adult" and category_id in {
        "adult_bondage", "adult_toys", "adult_fetish", "adult_taboo", "adult_other",
    }:
        if category_id == "adult_taboo" and any(fragment in base_name for fragment in (
            "rape", "molestation", "sexual_harassment", "forced_orgasm", "assisted_rape",
        )):
            return "sensitive", "sexual_violence"
        return "adult_kink", category_id

    if (folder_id, category_id) == ("action", "interaction") and (
        base_name in {"bound", "restrained", "bound_wrists", "bound_ankles", "tied_up_(nonsexual)", "bound_together"}
        or base_name.startswith(("bound_", "restrained_"))
    ):
        return "sensitive", "restraint"
    if (folder_id, category_id) == ("action", "holding"):
        if any(fragment in base_name for fragment in (
            "grabbing_another", "holding_another", "carrying_person", "lifting_person", "princess_carry",
            "shoulder_carry", "carrying_over_shoulder", "lifting_animal", "carry_me", "assisted_carrying",
        )):
            return "action", "interaction"
        if any(fragment in base_name for fragment in ("clothes_grab", "skirt_hold", "dress_lift", "sheet_grab")):
            return "action", "clothing_action"

    if (folder_id, category_id) == ("accessories", "jewelry") and tokens & {
        "nipple", "nipples", "penis", "clitoris", "clitoral", "labia", "pussy", "scrotum", "genital",
    }:
        return "adult_kink", "adult_fetish"

    return folder_id, category_id


def normalize_location(location: tuple[str, str], tag_name: str = "") -> tuple[str, str]:
    """Resolve chained legacy moves to a stable current taxonomy location."""
    current = (str(location[0]), str(location[1]))
    seen = set()
    for _ in range(8):
        if current in seen:
            return current
        seen.add(current)
        next_location = _normalize_location_once(current, tag_name)
        if next_location == current:
            return current
        current = next_location
    return current


COLORS = {
    "black", "brown", "blonde", "blond", "red", "orange", "yellow", "green", "blue", "aqua",
    "cyan", "purple", "pink", "white", "grey", "gray", "silver", "gold", "multicolored", "rainbow",
    "two-tone", "gradient", "streaked", "dark", "light",
}


# High-visibility tags whose meaning is established but whose short or symbolic
# names do not expose enough tokens for generic rules.  Keeping these explicit
# also makes taxonomy changes auditable.
EXACT_OVERRIDES = {
    "holding": ("action", "holding"), "carrying": ("action", "holding"),
    "reaching": ("action", "daily_action"), "floating": ("action", "movement"),
    "wading": ("action", "movement"), "trembling": ("pose", "body_pose"),
    "dual_wielding": ("action", "combat_action"), "kiss": ("action", "interaction"),
    "on_back": ("pose", "stationary_pose"), "on_side": ("pose", "stationary_pose"),
    "wariza": ("pose", "stationary_pose"), "all_fours": ("pose", "body_pose"),
    "v": ("pose", "hand_gesture"), "double_v": ("pose", "hand_gesture"),
    "profile": ("composition", "camera_angle"), "straight-on": ("composition", "camera_angle"),
    "back": ("composition", "viewpoint"), "foreshortening": ("composition", "camera_angle"),
    "bare_shoulders": ("body", "chest"), "collarbone": ("body", "chest"),
    "abs": ("body", "chest"), "large_pectorals": ("body", "chest"),
    "fingernails": ("body", "arms_hands_feet"), "toenails": ("body", "arms_hands_feet"),
    "long_fingernails": ("body", "arms_hands_feet"), "skindentation": ("body", "body_state"),
    "veins": ("body", "body_state"), "bandages": ("body", "body_state"),
    "toned": ("body", "build"), "tanlines": ("body", "skin"),
    "dark-skinned_female": ("body", "skin"), "dark-skinned_male": ("body", "skin"),
    "nail_polish": ("face", "makeup"), "toenail_polish": ("face", "makeup"),
    "colored_sclera": ("face", "eye_shape"), "wide-eyed": ("face", "eye_shape"),
    "fangs": ("face", "mouth"), "drooling": ("face", "mouth"),
    "beard": ("face", "facial_hair"), "stubble": ("face", "facial_hair"),
    "mustache": ("face", "facial_hair"), "sideburns": ("face", "facial_hair"),
    "ahoge": ("hair", "hair_style"), "two_side_up": ("hair", "hair_style"),
    "one_side_up": ("hair", "hair_style"), "double_bun": ("hair", "hair_style"),
    "twin_drills": ("hair", "hair_style"), "half_updo": ("hair", "hair_style"),
    "blunt_ends": ("hair", "hair_style"),
    ":d": ("expression", "positive"), ";d": ("expression", "positive"),
    "^_^": ("expression", "positive"), "^^^": ("expression", "positive"),
    ":o": ("expression", "fear_surprise"), ":3": ("expression", "positive"),
    ">_<": ("expression", "neutral_expression"), ":p": ("expression", "neutral_expression"),
    ":q": ("expression", "neutral_expression"), ":<": ("expression", "anger"),
    "@_@": ("expression", "fear_surprise"), "furrowed_brow": ("expression", "anger"),
    "tail": ("creatures", "animal_feature"), "horns": ("creatures", "animal_feature"),
    "wings": ("creatures", "animal_feature"), "halo": ("creatures", "animal_feature"),
    "feathers": ("creatures", "animal_feature"), "claws": ("creatures", "animal_feature"),
    "fins": ("creatures", "animal_feature"), "multiple_tails": ("creatures", "animal_feature"),
    "single_horn": ("creatures", "animal_feature"), "animal": ("creatures", "other_creature"),
    "pokemon_(creature)": ("creatures", "fantasy_creature"), "oni": ("creatures", "fantasy_creature"),
    "furry": ("people", "fantasy_person"), "furry_female": ("people", "fantasy_person"),
    "furry_male": ("people", "fantasy_person"), "virtual_youtuber": ("people", "occupation"),
    "magical_girl": ("people", "role_focus"), "trap": ("people", "role_focus"),
    "genderswap": ("people", "role_focus"), "dual_persona": ("people", "role_focus"),
    "aged_down": ("people", "age"), "aged_up": ("people", "age"),
    "no_humans": ("people", "count_gender"), "1other": ("people", "count_gender"),
    "age_difference": ("people", "relationship"), "height_difference": ("people", "relationship"),
    "chibi": ("style", "art_style"), "chibi_only": ("style", "art_style"),
    "tachi-e": ("style", "genre"), "spot_color": ("light_effect", "palette"),
    "motion_lines": ("light_effect", "optical"), "reflection": ("light_effect", "optical"),
    "letterboxed": ("composition", "framing"), "glint": ("light_effect", "particles"),
    "outdoors": ("outdoor_scene", "other_scene"), "scenery": ("outdoor_scene", "other_scene"),
    "nature": ("outdoor_scene", "other_scene"), "rock": ("outdoor_scene", "mountain_desert"),
    "window": ("indoor_scene", "architecture"), "stairs": ("indoor_scene", "architecture"),
    "curtains": ("household_objects", "storage_furniture"), "pillow": ("household_objects", "storage_furniture"),
    "gift": ("household_objects", "other_object"), "cigarette": ("household_objects", "other_object"),
    "handgun": ("weapons", "firearm"), "sheath": ("weapons", "blade"),
    "heart": ("text_meta", "symbol"), "?": ("text_meta", "symbol"), "!": ("text_meta", "symbol"),
    "...": ("text_meta", "text"), "cross": ("text_meta", "symbol"), "crescent": ("text_meta", "symbol"),
    "musical_note": ("text_meta", "symbol"), "spoken_heart": ("text_meta", "comic"),
    "spoken_ellipsis": ("text_meta", "comic"), "emphasis_lines": ("text_meta", "comic"),
    "notice_lines": ("text_meta", "comic"), "2koma": ("text_meta", "comic"),
    "signature": ("text_meta", "meta"), "twitter_username": ("text_meta", "meta"),
    "patreon_username": ("text_meta", "meta"), "dated": ("text_meta", "meta"),
    "web_address": ("text_meta", "text"), "copyright_notice": ("text_meta", "meta"),
    "cover": ("text_meta", "meta"), "cover_page": ("text_meta", "meta"),
}

EXACT_OVERRIDES.update({
    "sleeveless": ("clothing_detail", "clothing_structure"),
    "off_shoulder": ("clothing_detail", "clothing_structure"),
    "vest": ("clothes_main", "tops"), "apron": ("clothes_special", "occupation_uniform"),
    "turtleneck": ("clothes_main", "tops"), "capelet": ("clothes_main", "outerwear"),
    "highleg": ("underwear_swim", "underwear_design"), "halterneck": ("clothing_detail", "clothing_structure"),
    "hood": ("accessories", "headwear"), "hood_down": ("clothing_detail", "clothing_state"),
    "hood_up": ("clothing_detail", "clothing_state"), "white_apron": ("clothes_special", "occupation_uniform"),
    "suspenders": ("clothing_detail", "clothing_structure"), "pelvic_curtain": ("clothes_special", "themed_costume"),
    "corset": ("underwear_swim", "bodysuit_leotard"), "robe": ("clothes_special", "sleep_casual"),
    "pajamas": ("clothes_special", "sleep_casual"), "side_slit": ("clothing_detail", "clothing_structure"),
    "denim": ("clothing_detail", "clothing_material"), "lace": ("clothing_detail", "clothing_material"),
    "pom_pom_(clothes)": ("clothing_detail", "clothing_structure"),
    "collar": ("accessories", "neckwear"), "neckerchief": ("accessories", "neckwear"),
    "ascot": ("accessories", "neckwear"), "red_neckerchief": ("accessories", "neckwear"),
    "wrist_cuffs": ("accessories", "handwear"), "single_glove": ("accessories", "handwear"),
    "armlet": ("accessories", "handwear"), "beret": ("accessories", "headwear"),
    "headband": ("accessories", "headwear"), "headgear": ("accessories", "headwear"),
    "veil": ("accessories", "headwear"), "sunglasses": ("accessories", "eyewear"),
    "ring": ("accessories", "jewelry"), "single_earring": ("accessories", "jewelry"),
    "pendant": ("accessories", "jewelry"), "watch": ("accessories", "handwear"),
    "gem": ("accessories", "jewelry"), "beads": ("accessories", "jewelry"),
    "bell": ("accessories", "badges_ornaments"), "jingle_bell": ("accessories", "badges_ornaments"),
    "neck_bell": ("accessories", "neckwear"), "tassel": ("accessories", "badges_ornaments"),
    "o-ring": ("accessories", "jewelry"), "buckle": ("accessories", "bags_belts"),
    "epaulettes": ("accessories", "badges_ornaments"),
    "breath": ("light_effect", "other_effect"), "heavy_breathing": ("action", "daily_action"),
    "bouquet": ("creatures", "plant"), "bubble": ("light_effect", "particles"),
})

# Popular short/ambiguous tags audited against the bundled Chinese names and
# wiki descriptions.  These explicit assignments take priority over broad
# token rules, which keeps the most frequently used choices predictable.
EXACT_OVERRIDES.update({
    # Pairings, identity changes and narrative concepts.
    "hetero": ("themes", "romance_orientation"), "yuri": ("themes", "romance_orientation"),
    "yaoi": ("themes", "romance_orientation"), "bara": ("themes", "romance_orientation"),
    "interracial": ("themes", "romance_orientation"), "interspecies": ("themes", "romance_orientation"),
    "brother_and_sister": ("themes", "family_relation"), "husband_and_wife": ("themes", "family_relation"),
    "age_difference": ("themes", "social_relation"), "height_difference": ("themes", "social_relation"),
    "size_difference": ("themes", "social_relation"), "side-by-side": ("themes", "social_relation"),
    "sandwiched": ("themes", "social_relation"), "face-to-face": ("themes", "social_relation"),
    "genderswap": ("themes", "identity_change"), "genderswap_(mtf)": ("themes", "identity_change"),
    "genderswap_(ftm)": ("themes", "identity_change"), "humanization": ("themes", "identity_change"),
    "animalization": ("themes", "identity_change"), "animification": ("themes", "identity_change"),
    "enmaided": ("themes", "identity_change"), "dark_persona": ("themes", "persona_variant"),
    "multiple_persona": ("themes", "persona_variant"), "dual_persona": ("themes", "persona_variant"),
    "borrowed_character": ("themes", "persona_variant"), "everyone": ("themes", "narrative_situation"),
    "slice_of_life": ("themes", "narrative_situation"), "battle": ("themes", "narrative_situation"),
    "defeat": ("themes", "narrative_situation"), "voice_actor_connection": ("themes", "character_connection"),
    "name_connection": ("themes", "character_connection"), "trait_connection": ("themes", "character_connection"),

    # Censorship and publishing metadata.
    "censored": ("text_meta", "censorship"), "uncensored": ("text_meta", "censorship"),
    "mosaic_censoring": ("text_meta", "censorship"), "bar_censor": ("text_meta", "censorship"),
    "heart_censor": ("text_meta", "censorship"), "convenient_censoring": ("text_meta", "censorship"),
    "pointless_censoring": ("text_meta", "censorship"), "content_rating": ("text_meta", "censorship"),
    "doujin_cover": ("text_meta", "meta"), "company_name": ("text_meta", "meta"),
    "page_number": ("text_meta", "text"), "sign": ("text_meta", "symbol"),
    "diamond_(shape)": ("text_meta", "symbol"), "yin_yang": ("text_meta", "symbol"),
    "eighth_note": ("text_meta", "symbol"), "beamed_eighth_notes": ("text_meta", "symbol"),
    "3koma": ("text_meta", "comic"), "zzz": ("text_meta", "comic"),
    "speed_lines": ("light_effect", "optical"), "chibi_inset": ("style", "art_style"),
    "bad_anatomy": ("style", "quality"), "recording": ("text_meta", "screen_ui"),

    # Symbolic facial expressions.
    "+_+": ("expression", "positive"), ":t": ("expression", "anger"),
    "!?": ("expression", "fear_surprise"), "=_=": ("expression", "neutral_expression"),
    ";)": ("expression", "positive"), "o_o": ("expression", "fear_surprise"),
    "|_|": ("expression", "neutral_expression"), ":>": ("expression", "positive"),
    ":/": ("expression", "fear_surprise"), ">: )": ("expression", "positive"),
    ">:)": ("expression", "positive"), "!!": ("expression", "fear_surprise"),
    ":|": ("expression", "neutral_expression"), ";o": ("expression", "fear_surprise"),
    "0_0": ("expression", "fear_surprise"), "xd": ("expression", "positive"),
    "tearing_up": ("expression", "sad_cry"), "smirk": ("expression", "positive"),
    "wince": ("expression", "fear_surprise"), "torogao": ("expression", "neutral_expression"),
    "glaring": ("expression", "anger"), "multiple_expressions": ("expression", "neutral_expression"),

    # Body, appearance and people.
    "midriff": ("body", "chest"), "midriff_peek": ("body", "chest"),
    "groin": ("body", "waist_legs"), "sideboob": ("body", "chest"),
    "underboob": ("body", "chest"), "underbust": ("body", "chest"),
    "soles": ("body", "arms_hands_feet"), "cameltoe": ("body", "waist_legs"),
    "bulge": ("body", "waist_legs"), "butt_crack": ("body", "waist_legs"),
    "kneepits": ("body", "waist_legs"), "belly": ("body", "chest"),
    "bare_back": ("body", "chest"), "shoulder_blades": ("body", "chest"),
    "median_furrow": ("body", "chest"), "linea_alba": ("body", "chest"),
    "biceps": ("body", "build"), "toned_male": ("body", "build"),
    "toned_female": ("body", "build"), "joints": ("body", "body_state"),
    "injury": ("body", "body_state"), "blood": ("body", "body_state"),
    "blood_splatter": ("body", "body_state"), "nosebleed": ("body", "body_state"),
    "wet": ("body", "body_state"), "dirty": ("body", "body_state"),
    "prosthesis": ("mech_scifi", "cybernetic"), "material_growth": ("body", "body_state"),
    "multiple_moles": ("body", "body_marks"), "colored_extremities": ("body", "skin"),
    "sharp_fingernails": ("body", "arms_hands_feet"), "covered_collarbone": ("body", "chest"),
    "mini_person": ("people", "role_focus"), "minigirl": ("people", "role_focus"),
    "giantess": ("people", "role_focus"), "bishounen": ("people", "age"),
    "gyaru": ("people", "role_focus"), "tomboy": ("people", "role_focus"),
    "bride": ("people", "role_focus"), "ninja": ("people", "occupation"),
    "multiple_others": ("people", "count_gender"), "merfolk": ("people", "fantasy_person"),
    "miqo'te": ("people", "fantasy_person"), "draph": ("people", "fantasy_person"),
    "arthropod_girl": ("people", "fantasy_person"),

    # Eyes, face and hair.
    "sideways_glance": ("pose", "gaze"), "turning_head": ("pose", "gaze"),
    "eyeball": ("face", "eye_shape"), "one-eyed": ("face", "eye_shape"),
    "third_eye": ("face", "eye_shape"), "heart_in_eye": ("face", "eye_shape"),
    "star_in_eye": ("face", "eye_shape"), "goatee": ("face", "facial_hair"),
    "beard_stubble": ("face", "facial_hair"), "long_sideburns": ("face", "facial_hair"),
    "colored_tips": ("hair", "hair_color"), "red_streaks": ("hair", "hair_color"),
    "white_streaks": ("hair", "hair_color"), "blue_streaks": ("hair", "hair_color"),
    "single_sidelock": ("hair", "bangs"), "bald": ("hair", "hair_style"),
    "undercut": ("hair", "hair_style"), "topknot": ("hair", "hair_style"),
    "heart_ahoge": ("hair", "hair_style"), "bun_cover": ("hair", "hair_accessory"),

    # Pose and actions.
    "restrained": ("action", "interaction"), "partially_submerged": ("action", "movement"),
    "licking": ("action", "interaction"), "headpat": ("action", "interaction"),
    "talking": ("action", "daily_action"), "smoking": ("action", "daily_action"),
    "biting": ("action", "interaction"), "feeding": ("action", "daily_action"),
    "taking_picture": ("action", "daily_action"), "shouting": ("action", "daily_action"),
    "moaning": ("action", "daily_action"), "shushing": ("pose", "hand_gesture"),
    "tiptoes": ("pose", "body_pose"), "split": ("pose", "body_pose"),
    "folded": ("pose", "body_pose"), "pose": ("pose", "body_pose"),
    "top-down_bottom-up": ("pose", "body_pose"), "yokozuwari": ("pose", "stationary_pose"),
    "under_covers": ("pose", "stationary_pose"), "on_head": ("pose", "body_pose"),
    "heads_together": ("action", "interaction"), "tail_wagging": ("action", "movement"),
    "clothes_grab": ("action", "holding"), "sheet_grab": ("action", "holding"),
    "trigger_discipline": ("action", "combat_action"), "sheathed": ("action", "combat_action"),

    # Garments, footwear and accessories.
    "strapless": ("clothing_detail", "clothing_structure"), "double-breasted": ("clothing_detail", "clothing_structure"),
    "drawstring": ("clothing_detail", "clothing_structure"), "criss-cross_halter": ("clothing_detail", "clothing_structure"),
    "single_bare_shoulder": ("clothing_detail", "clothing_structure"), "two-sided_fabric": ("clothing_detail", "clothing_material"),
    "open_fly": ("clothing_detail", "clothing_state"), "center_opening": ("clothing_detail", "clothing_state"),
    "unbuttoned": ("clothing_detail", "clothing_state"), "unzipped": ("clothing_detail", "clothing_state"),
    "partially_unzipped": ("clothing_detail", "clothing_state"), "crop_top_overhang": ("clothing_detail", "clothing_state"),
    "v-neck": ("clothing_detail", "clothing_structure"), "fringe_trim": ("clothing_detail", "clothing_structure"),
    "sleeveless_turtleneck": ("clothes_main", "tops"), "undershirt": ("clothes_main", "tops"),
    "tunic": ("clothes_main", "tops"), "tailcoat": ("clothes_main", "outerwear"),
    "shrug_(clothing)": ("clothes_main", "outerwear"), "shawl": ("clothes_main", "outerwear"),
    "tabard": ("clothes_main", "outerwear"), "white_capelet": ("clothes_main", "outerwear"),
    "black_capelet": ("clothes_main", "outerwear"), "red_capelet": ("clothes_main", "outerwear"),
    "blue_capelet": ("clothes_main", "outerwear"), "microskirt": ("clothes_main", "skirt"),
    "cutoffs": ("clothes_main", "bottoms"), "buruma": ("clothes_special", "school_uniform"),
    "gakuran": ("clothes_special", "school_uniform"), "sportswear": ("clothes_special", "themed_costume"),
    "dougi": ("clothes_special", "occupation_uniform"), "race_queen": ("clothes_special", "occupation_uniform"),
    "kariginu": ("clothes_special", "traditional_east"), "tate_eboshi": ("accessories", "headwear"),
    "sarong": ("clothes_special", "traditional_world"), "babydoll": ("underwear_swim", "bra_lingerie"),
    "bodystocking": ("underwear_swim", "bodysuit_leotard"), "fundoshi": ("underwear_swim", "panties_underwear"),
    "maebari": ("underwear_swim", "panties_underwear"), "lowleg": ("underwear_swim", "underwear_design"),
    "fishnets": ("legwear_footwear", "stockings"), "single_thighhigh": ("legwear_footwear", "stockings"),
    "single_sock": ("legwear_footwear", "socks"), "tabi": ("legwear_footwear", "socks"),
    "mary_janes": ("legwear_footwear", "shoes"), "geta": ("legwear_footwear", "shoes"),
    "zouri": ("legwear_footwear", "shoes"), "shoe_soles": ("legwear_footwear", "shoes"),
    "greaves": ("legwear_footwear", "armor"), "muneate": ("legwear_footwear", "armor"),
    "kote": ("legwear_footwear", "armor"), "shoulder_pads": ("legwear_footwear", "armor"),
    "circlet": ("accessories", "headwear"), "beanie": ("accessories", "headwear"),
    "bandana": ("accessories", "headwear"), "headpiece": ("accessories", "headwear"),
    "headdress": ("accessories", "headwear"), "headscarf": ("accessories", "headwear"),
    "bonnet": ("accessories", "headwear"), "earmuffs": ("accessories", "headwear"),
    "bridal_veil": ("accessories", "headwear"), "triangular_headpiece": ("accessories", "headwear"),
    "bespectacled": ("accessories", "eyewear"), "handbag": ("accessories", "bags_belts"),
    "randoseru": ("accessories", "bags_belts"), "multiple_belts": ("accessories", "bags_belts"),
    "harness": ("accessories", "bags_belts"), "name_tag": ("accessories", "badges_ornaments"),
    "wristwatch": ("accessories", "handwear"), "cuffs": ("accessories", "handwear"),
    "bangle": ("accessories", "jewelry"), "thighlet": ("accessories", "jewelry"),
    "earclip": ("accessories", "jewelry"), "magatama": ("accessories", "jewelry"),
    "multiple_rings": ("accessories", "jewelry"), "blue_gem": ("accessories", "jewelry"),
    "red_gem": ("accessories", "jewelry"), "green_gem": ("accessories", "jewelry"),
    "lanyard": ("accessories", "other_accessory"), "tasuki": ("accessories", "other_accessory"),

    # Nature, creatures, scenes, equipment and everyday objects.
    "spikes": ("household_objects", "other_object"), "tentacles": ("creatures", "animal_feature"),
    "antlers": ("creatures", "animal_feature"), "antennae": ("creatures", "animal_feature"),
    "scales": ("creatures", "animal_feature"), "whiskers": ("creatures", "animal_feature"),
    "single_wing": ("creatures", "animal_feature"), "tail_raised": ("creatures", "animal_feature"),
    "creature": ("creatures", "other_creature"), "kitsune": ("creatures", "fantasy_creature"),
    "skull": ("creatures", "fantasy_creature"), "skeleton": ("creatures", "fantasy_creature"),
    "hitodama": ("creatures", "fantasy_creature"), "digimon_(creature)": ("creatures", "fantasy_creature"),
    "shell": ("creatures", "other_creature"), "bush": ("creatures", "plant"),
    "vines": ("creatures", "plant"), "hibiscus": ("creatures", "plant"),
    "pumpkin": ("food_drink", "fruit_vegetable"), "popsicle": ("food_drink", "dessert_snack"),
    "ice_cream": ("food_drink", "dessert_snack"), "ice_cream_cone": ("food_drink", "dessert_snack"),
    "pocky": ("food_drink", "dessert_snack"), "burger": ("food_drink", "staple_food"),
    "teapot": ("food_drink", "tableware"), "saucer": ("food_drink", "tableware"),
    "earphones": ("culture_objects", "camera_media"), "whistle": ("culture_objects", "music"),
    "dakimakura_(medium)": ("household_objects", "storage_furniture"), "bookshelf": ("household_objects", "storage_furniture"),
    "futon": ("household_objects", "seating_table"), "cushion": ("household_objects", "seating_table"),
    "candle": ("household_objects", "lighting_clock"), "vase": ("household_objects", "container"),
    "sack": ("household_objects", "container"), "coin": ("household_objects", "other_object"),
    "balloon": ("household_objects", "other_object"), "sticker": ("household_objects", "other_object"),
    "tape": ("household_objects", "tools"), "syringe": ("household_objects", "tools"),
    "string": ("household_objects", "tools"), "chain": ("household_objects", "tools"),
    "innertube": ("transport_play", "sports"), "pom_pom_(cheerleading)": ("transport_play", "sports"),
    "watercraft": ("transport_play", "water_vehicle"), "anchor": ("transport_play", "water_vehicle"),
    "cable": ("mech_scifi", "machine"), "rigging": ("mech_scifi", "machine"),
    "orb": ("mech_scifi", "scifi_device"), "ofuda": ("weapons", "magic_weapon"),
    "gohei": ("weapons", "magic_weapon"), "scythe": ("weapons", "polearm"),
    "scabbard": ("weapons", "blade"), "planted": ("action", "combat_action"),

    # Places, backgrounds and visual effects.
    "ice": ("outdoor_scene", "water_scene"), "sand": ("outdoor_scene", "mountain_desert"),
    "horizon": ("outdoor_scene", "other_scene"), "onsen": ("outdoor_scene", "water_scene"),
    "road": ("indoor_scene", "urban"), "railing": ("indoor_scene", "architecture"),
    "fence": ("indoor_scene", "architecture"), "door": ("indoor_scene", "architecture"),
    "pillar": ("indoor_scene", "architecture"), "torii": ("indoor_scene", "architecture"),
    "sliding_doors": ("indoor_scene", "architecture"), "utility_pole": ("indoor_scene", "urban"),
    "tatami": ("indoor_scene", "surface"), "bath": ("indoor_scene", "home_room"),
    "bathtub": ("indoor_scene", "home_room"), "light": ("light_effect", "lighting"),
    "shade": ("light_effect", "lighting"), "dark": ("light_effect", "lighting"),
    "rainbow": ("light_effect", "palette"), "alternate_color": ("light_effect", "palette"),
    "air_bubble": ("light_effect", "particles"), "puff_of_air": ("light_effect", "other_effect"),
    "ripples": ("light_effect", "other_effect"), "dripping": ("light_effect", "other_effect"),
    "magic": ("light_effect", "magic_effect"), "gap_(touhou)": ("light_effect", "magic_effect"),
    "silhouette": ("style", "technique"), "partially_colored": ("style", "technique"),
    "halftone": ("style", "technique"), "jaggy_lines": ("style", "technique"),
    "deformed": ("style", "art_style"), "contemporary": ("style", "era_style"),
    "upside-down": ("composition", "camera_angle"), "x-ray": ("composition", "viewpoint"),
    "cross-section": ("composition", "viewpoint"),

    # Explicit content whose short name needs a precise adult destination.
    "erection": ("adult", "adult_anatomy"), "cleft_of_venus": ("adult", "adult_anatomy"),
    "dildo": ("adult", "adult_fetish"), "condom": ("adult", "adult_fetish"),
    "condom_wrapper": ("adult", "adult_fetish"), "used_condom": ("adult", "adult_fluid"),
    "bound": ("adult", "adult_fetish"), "bound_wrists": ("adult", "adult_fetish"),
    "handcuffs": ("adult", "adult_fetish"), "shackles": ("adult", "adult_fetish"),
    "pantyshot": ("adult", "adult_clothes"), "panty_pull": ("adult", "adult_clothes"),
    "clothing_aside": ("adult", "adult_clothes"), "presenting": ("adult", "adult_suggestive"),
    "female_orgasm": ("adult", "adult_other"), "lactation": ("adult", "adult_fluid"),
    "pee": ("adult", "adult_fluid"), "public_indecency": ("adult", "adult_nudity"),
    "assertive_female": ("adult", "adult_fetish"), "futa_with_female": ("adult", "adult_sex"),
})

EXACT_OVERRIDES.update({
    "facial": ("adult", "adult_fluid"), "futanari": ("themes", "identity_change"),
    "vibrator": ("adult", "adult_fetish"), "gagged": ("adult", "adult_fetish"),
    "teamwork_(sexual)": ("adult", "adult_sex"), "netorare": ("adult", "adult_fetish"),
    "exhibitionism": ("adult", "adult_fetish"), "fucked_silly": ("adult", "adult_other"),
    "pervert": ("adult", "adult_other"), "female_pervert": ("adult", "adult_other"),
    "take_your_pick": ("adult", "adult_suggestive"), "crotchless": ("adult", "adult_clothes"),
    "butt_plug": ("adult", "adult_fetish"), "aroused": ("adult", "adult_other"),
    "spitroast": ("adult", "adult_sex"), "kodomo_doushi": ("adult", "adult_other"),
    "gaping": ("adult", "adult_anatomy"), "spanked": ("adult", "adult_fetish"),
    "defloration": ("adult", "adult_sex"), "mating_press": ("adult", "adult_sex"),
    "humiliation": ("adult", "adult_fetish"), "suspension": ("adult", "adult_fetish"),
    "bound_ankles": ("adult", "adult_fetish"), "assisted_exposure": ("adult", "adult_nudity"),
    "prone_bone": ("adult", "adult_sex"), "mouth_hold": ("action", "holding"),
    "same-sex_bathing": ("action", "daily_action"), "mixed-sex_bathing": ("action", "daily_action"),

    "vision_(genshin_impact)": ("accessories", "other_accessory"), "tacet_mark_(wuthering_waves)": ("body", "body_marks"),
    "command_spell": ("body", "body_marks"), "oripathy_lesion_(arknights)": ("body", "body_marks"),
    "vambraces": ("legwear_footwear", "armor"), "bracer": ("legwear_footwear", "armor"),
    "single_pauldron": ("legwear_footwear", "armor"), "faulds": ("legwear_footwear", "armor"),
    "kurokote": ("legwear_footwear", "armor"), "shoulder_spikes": ("legwear_footwear", "armor"),
    "assault_visor": ("legwear_footwear", "helmet_protective"),
    "yellow_ascot": ("accessories", "neckwear"), "white_ascot": ("accessories", "neckwear"),
    "red_ascot": ("accessories", "neckwear"), "black_ascot": ("accessories", "neckwear"),
    "blue_ascot": ("accessories", "neckwear"), "yellow_neckerchief": ("accessories", "neckwear"),
    "blue_neckerchief": ("accessories", "neckwear"), "black_neckerchief": ("accessories", "neckwear"),
    "white_neckerchief": ("accessories", "neckwear"), "white_wrist_cuffs": ("accessories", "handwear"),
    "gold_chain": ("accessories", "jewelry"), "purple_gem": ("accessories", "jewelry"),
    "obijime": ("accessories", "bags_belts"), "obiage": ("accessories", "bags_belts"),
    "shimenawa": ("accessories", "other_accessory"), "cowbell": ("accessories", "badges_ornaments"),
    "heart_o-ring": ("accessories", "jewelry"), "medal": ("accessories", "badges_ornaments"),
    "shoulder_boards": ("accessories", "badges_ornaments"), "tie_clip": ("accessories", "jewelry"),
    "hachimaki": ("accessories", "headwear"), "jingasa": ("accessories", "headwear"),
    "black_headband": ("accessories", "headwear"), "red_headband": ("accessories", "headwear"),
    "white_headband": ("accessories", "headwear"), "white_veil": ("accessories", "headwear"),
    "black_veil": ("accessories", "headwear"), "black_corset": ("underwear_swim", "bra_lingerie"),
    "bustier": ("underwear_swim", "bra_lingerie"), "swim_trunks": ("underwear_swim", "swimsuit"),
    "red_buruma": ("clothes_special", "school_uniform"), "blue_buruma": ("clothes_special", "school_uniform"),
    "black_apron": ("clothes_special", "occupation_uniform"), "blue_apron": ("clothes_special", "occupation_uniform"),
    "waistcoat": ("clothes_main", "tops"), "plunging_neckline": ("clothing_detail", "clothing_structure"),
    "single_off_shoulder": ("clothing_detail", "clothing_state"), "coattails": ("clothing_detail", "clothing_structure"),
    "hooded_capelet": ("clothes_main", "outerwear"), "black_shrug": ("clothes_main", "outerwear"),
    "jirai_kei": ("clothes_special", "themed_costume"), "hagoromo": ("clothes_special", "traditional_east"),

    "w": ("pose", "hand_gesture"), "\\m/": ("pose", "hand_gesture"),
    "\\||/": ("pose", "hand_gesture"), "v_over_eye": ("pose", "hand_gesture"),
    "french_kiss": ("action", "interaction"), "imminent_kiss": ("action", "interaction"),
    "kissing_cheek": ("action", "interaction"), "cheek-to-cheek": ("action", "interaction"),
    "animal_on_head": ("action", "interaction"), "animal_on_shoulder": ("action", "interaction"),
    "petting": ("action", "interaction"), "poking": ("action", "interaction"),
    "lifting_person": ("action", "holding"), "throwing": ("action", "movement"),
    "pouring": ("action", "daily_action"), "playing_games": ("action", "daily_action"),
    "playing_video_games": ("action", "daily_action"), "driving": ("action", "movement"),
    "exercising": ("action", "movement"), "showering": ("action", "daily_action"),
    "unsheathing": ("action", "combat_action"), "unsheathed": ("action", "combat_action"),
    "firing": ("action", "combat_action"), "reverse_grip": ("action", "combat_action"),
    "midair": ("action", "movement"), "reclining": ("pose", "stationary_pose"),
    "on_throne": ("pose", "stationary_pose"), "on_lap": ("pose", "stationary_pose"),
    "crossed_ankles": ("pose", "body_pose"), "flexible": ("pose", "body_pose"),
    "peeking_out": ("pose", "gaze"), "behind_another": ("pose", "body_pose"),

    "+++": ("text_meta", "comic"), "heart_of_string": ("text_meta", "symbol"),
    "mitsudomoe_(shape)": ("text_meta", "symbol"), "circle": ("text_meta", "symbol"),
    "triangle": ("text_meta", "symbol"), "pentagram": ("text_meta", "symbol"),
    "spade_(shape)": ("text_meta", "symbol"), "treble_clef": ("text_meta", "symbol"),
    "string_of_flags": ("text_meta", "symbol"), "banner": ("text_meta", "symbol"),
    "??": ("expression", "fear_surprise"), "d:": ("expression", "anger"),
    ";p": ("expression", "positive"), "3:": ("expression", "anger"),
    "u_u": ("expression", "neutral_expression"), ":>=": ("expression", "anger"),
    ":i": ("expression", "anger"), ";q": ("expression", "positive"),
    "squeans": ("expression", "neutral_expression"), "teardrop": ("expression", "sad_cry"),
    "unamused": ("expression", "anger"), "jealous": ("expression", "anger"),
    "screaming": ("expression", "fear_surprise"),

    "mind_control": ("themes", "narrative_situation"), "hypnosis": ("themes", "narrative_situation"),
    "imagining": ("themes", "narrative_situation"), "alternate_form": ("themes", "persona_variant"),
    "fusion": ("themes", "identity_change"), "super_saiyan": ("themes", "persona_variant"),
    "reverse_trap": ("themes", "identity_change"), "furry_with_non-furry": ("themes", "romance_orientation"),
    "furry_with_furry": ("themes", "romance_orientation"), "string_of_fate": ("themes", "romance_orientation"),
    "cheating_(relationship)": ("themes", "romance_orientation"), "instant_loss": ("themes", "narrative_situation"),
    "lineup": ("themes", "social_relation"), "matching_outfits": ("themes", "social_relation"),
    "slave": ("themes", "narrative_situation"), "yandere": ("people", "role_focus"),
    "tsundere": ("people", "role_focus"), "kogal": ("people", "role_focus"),
    "policewoman": ("people", "occupation"), "dancer": ("people", "occupation"),
    "sailor": ("people", "occupation"), "utaite": ("people", "occupation"),
    "ambiguous_gender": ("people", "count_gender"), "people": ("people", "count_gender"),
    "miniboy": ("people", "role_focus"), "manly": ("body", "build"),
    "shortstack": ("body", "build"), "big_belly": ("body", "chest"),
    "backboob": ("body", "chest"), "dimples_of_venus": ("body", "waist_legs"),
    "crotch": ("body", "waist_legs"), "armpit_peek": ("body", "arms_hands_feet"),
    "hairy": ("body", "body_state"), "hot": ("body", "body_state"),
    "bone": ("body", "body_state"), "fewer_digits": ("body", "body_state"),
    "bandaged_head": ("body", "body_state"), "bandaged_neck": ("body", "body_state"),
    "bandage_over_one_eye": ("body", "body_state"), "stitches": ("body", "body_marks"),
    "bite_mark": ("body", "body_marks"), "cuts": ("body", "body_marks"),
    "scratches": ("body", "body_marks"), "hickey": ("body", "body_marks"),
    "half-closed_eye": ("face", "eye_shape"), "snout": ("face", "mouth"),
    "snot": ("face", "brows_nose"), "cosmetics": ("face", "makeup"),
    "black_streaks": ("hair", "hair_color"), "cowlick": ("hair", "hair_style"),
    "ringlets": ("hair", "hair_style"), "inverted_bob": ("hair", "hair_style"),
    "hairpods": ("hair", "hair_accessory"),

    "mega_pokemon": ("creatures", "fantasy_creature"), "shiny_pokemon": ("creatures", "fantasy_creature"),
    "clothed_pokemon": ("creatures", "fantasy_creature"), "karakasa_obake": ("creatures", "fantasy_creature"),
    "nekomata": ("creatures", "fantasy_creature"), "jiangshi": ("creatures", "fantasy_creature"),
    "taur": ("people", "fantasy_person"), "erune": ("people", "fantasy_person"),
    "octoling": ("people", "fantasy_person"), "au_ra": ("people", "fantasy_person"),
    "lamia": ("people", "fantasy_person"), "raccoon_girl": ("people", "fantasy_person"),
    "tusks": ("creatures", "animal_feature"), "talons": ("creatures", "animal_feature"),
    "beak": ("creatures", "animal_feature"), "pawpads": ("creatures", "animal_feature"),
    "suction_cups": ("creatures", "animal_feature"), "starfish": ("creatures", "aquatic"),
    "chick": ("creatures", "bird"), "branch": ("creatures", "plant"),
    "thorns": ("creatures", "plant"), "clover": ("creatures", "plant"),
    "hydrangea": ("creatures", "plant"), "tulip": ("creatures", "plant"),

    "gold": ("light_effect", "palette"), "debris": ("light_effect", "particles"),
    "paint_splatter": ("light_effect", "particles"), "diffraction_spikes": ("light_effect", "optical"),
    "light_trail": ("light_effect", "optical"), "bloom": ("light_effect", "optical"),
    "contrail": ("light_effect", "other_effect"), "stage_lights": ("light_effect", "lighting"),
    "stand_(jojo)": ("light_effect", "magic_effect"), "landscape": ("outdoor_scene", "other_scene"),
    "waves": ("outdoor_scene", "water_scene"), "puddle": ("outdoor_scene", "water_scene"),
    "constellation": ("outdoor_scene", "sky_space"), "rooftop": ("indoor_scene", "urban"),
    "stage": ("indoor_scene", "commercial"), "school": ("indoor_scene", "public_indoor"),
    "open_door": ("indoor_scene", "architecture"), "doorway": ("indoor_scene", "architecture"),
    "arch": ("indoor_scene", "architecture"),

    "smoking_pipe": ("household_objects", "other_object"), "crack": ("household_objects", "other_object"),
    "broken": ("household_objects", "other_object"), "damaged": ("household_objects", "other_object"),
    "pole": ("household_objects", "tools"), "stick": ("household_objects", "tools"),
    "test_tube": ("household_objects", "tools"), "wrench": ("household_objects", "tools"),
    "needle": ("household_objects", "tools"), "shovel": ("household_objects", "tools"),
    "frying_pan": ("food_drink", "tableware"), "flask": ("household_objects", "container"),
    "cage": ("household_objects", "other_object"), "money": ("household_objects", "other_object"),
    "statue": ("household_objects", "other_object"), "rug": ("household_objects", "storage_furniture"),
    "candlestand": ("household_objects", "lighting_clock"), "stethoscope": ("household_objects", "tools"),
    "remote_control": ("culture_objects", "phone_computer"), "nintendo_switch": ("culture_objects", "phone_computer"),
    "mp3_player": ("culture_objects", "camera_media"), "earpiece": ("culture_objects", "camera_media"),
    "megaphone": ("culture_objects", "camera_media"), "shikishi": ("culture_objects", "books_paper"),
    "map": ("culture_objects", "books_paper"), "stylus": ("culture_objects", "stationery"),
    "plectrum": ("culture_objects", "music"), "drumsticks": ("culture_objects", "music"),
    "briefcase": ("accessories", "bags_belts"), "figure": ("transport_play", "toys"),
    "lifebuoy": ("transport_play", "sports"),

    "chewing_gum": ("food_drink", "dessert_snack"), "parfait": ("food_drink", "dessert_snack"),
    "macaron": ("food_drink", "dessert_snack"), "dango": ("food_drink", "staple_food"),
    "onigiri": ("food_drink", "staple_food"), "sushi": ("food_drink", "staple_food"),
    "pancake": ("food_drink", "staple_food"), "french_fries": ("food_drink", "staple_food"),
    "mochi": ("food_drink", "dessert_snack"), "omelet": ("food_drink", "staple_food"),
    "cheese": ("food_drink", "meat_seafood"), "cream": ("food_drink", "dessert_snack"),
    "ice_cube": ("food_drink", "drink"), "gourd": ("food_drink", "fruit_vegetable"),
    "sake": ("food_drink", "drink"),

    "v-fin": ("mech_scifi", "mecha"), "bangboo_(zenless_zone_zero)": ("mech_scifi", "robot_android"),
    "bolt_action": ("weapons", "firearm"), "bullet": ("weapons", "firearm"),
    "scope": ("weapons", "firearm"), "kunai": ("weapons", "blade"),
    "trident": ("weapons", "polearm"), "chainsaw": ("weapons", "blade"),
    "danmaku": ("weapons", "other_weapon"),

    "alphes_(style)": ("style", "art_style"), "painterly": ("style", "art_style"),
    "still_life": ("style", "genre"), "tokusatsu": ("style", "genre"),
    "ancient_egyptian": ("style", "era_style"), "yukkuri_shiteitte_ne": ("text_meta", "meme"),
    "pun": ("text_meta", "meme"), "thank_you": ("text_meta", "text"),
    "ranguage": ("text_meta", "text"), "profanity": ("text_meta", "text"),
    "song_name": ("text_meta", "text"), "numbered": ("text_meta", "text"),
    "brand_name_imitation": ("text_meta", "meta"), "album_cover": ("text_meta", "meta"),
    "request_inset": ("text_meta", "meta"), "collage": ("composition", "layout"),
    "pillarboxed": ("composition", "framing"), "sideways": ("composition", "camera_angle"),
    "2021": ("time_weather", "calendar"), "2022": ("time_weather", "calendar"),
    "2023": ("time_weather", "calendar"), "2024": ("time_weather", "calendar"),
    "2025": ("time_weather", "calendar"),
})

EXACT_OVERRIDES.update({
    "grapes": ("food_drink", "fruit_vegetable"), "flaccid": ("adult", "adult_anatomy"),
    "hose": ("household_objects", "tools"), "egasumi": ("outdoor_scene", "background_pattern"),
    "milestone_celebration": ("time_weather", "holiday"), "smelling": ("action", "daily_action"),
    "shide": ("accessories", "badges_ornaments"), "heart_balloon": ("household_objects", "other_object"),
    "on_shoulder": ("pose", "body_pose"), "pill": ("household_objects", "tools"),
    "head-mounted_display": ("accessories", "eyewear"), "strangling": ("action", "combat_action"),
    "1koma": ("text_meta", "comic"), "covered_abs": ("body", "chest"),
    "blowing_bubble_gum": ("action", "daily_action"), "kiseru": ("household_objects", "other_object"),
    "praying": ("pose", "hand_gesture"), "hiding": ("action", "daily_action"),
    "graffiti": ("text_meta", "text"), "princess": ("people", "role_focus"),
    "tally": ("text_meta", "text"), "path": ("outdoor_scene", "other_scene"),
    "left-handed": ("body", "arms_hands_feet"), "pinching": ("action", "interaction"),
    "uchiwa": ("household_objects", "tools"), "spill": ("light_effect", "other_effect"),
    "crossed_bandaids": ("body", "body_marks"), "neck_ruff": ("accessories", "neckwear"),
    "sode": ("legwear_footwear", "armor"), "moss": ("creatures", "plant"),
    "belly_chain": ("accessories", "jewelry"), "fivesome": ("adult", "adult_sex"),
    "dove": ("creatures", "bird"), "paint": ("style", "medium"),
    ";3": ("expression", "positive"), "come_hither": ("adult", "adult_suggestive"),
    "ladder": ("household_objects", "tools"), "abstract": ("outdoor_scene", "background_pattern"),
    "hooves": ("creatures", "animal_feature"), "carpet": ("household_objects", "storage_furniture"),
    "lotion": ("household_objects", "tools"), "sunburst": ("light_effect", "optical"),
    "wife_and_wife": ("themes", "family_relation"), "wedding": ("themes", "narrative_situation"),
    "fanny_pack": ("accessories", "bags_belts"), "neon_trim": ("light_effect", "lighting"),
    "blowing_kiss": ("action", "interaction"), "cold": ("body", "body_state"),
    "plantar_flexion": ("pose", "body_pose"), "binoculars": ("culture_objects", "camera_media"),
    "chained": ("adult", "adult_fetish"), "kabedon": ("action", "interaction"),
    "different_reflection": ("themes", "persona_variant"), "shiny": ("light_effect", "optical"),
    "shower_head": ("household_objects", "tools"), "mechabare": ("mech_scifi", "cybernetic"),
    "tombstone": ("indoor_scene", "architecture"), "shell_casing": ("weapons", "firearm"),
    "light_bulb": ("household_objects", "lighting_clock"), "duel": ("themes", "narrative_situation"),
    "patch": ("accessories", "badges_ornaments"), "skull_and_crossbones": ("text_meta", "symbol"),
    "submerged": ("action", "movement"), "laevatein_(touhou)": ("weapons", "magic_weapon"),
    "skewer": ("food_drink", "tableware"), "steering_wheel": ("transport_play", "land_vehicle"),
    "drawing_(action)": ("action", "daily_action"), "painting_(action)": ("action", "daily_action"),
    "spatula": ("food_drink", "tableware"), "full_beard": ("face", "facial_hair"),
    "ammunition": ("weapons", "firearm"), "side_up_bun": ("hair", "hair_style"),
    "impending_doom": ("themes", "narrative_situation"), "what": ("text_meta", "meme"),
    "roman_numeral": ("text_meta", "text"), "pyrokinesis": ("light_effect", "magic_effect"),
    "shaved_ice": ("food_drink", "dessert_snack"), "5koma": ("text_meta", "comic"),
    "balcony": ("indoor_scene", "architecture"), "safety_pin": ("clothing_detail", "clothing_structure"),
    "heart_maebari": ("underwear_swim", "panties_underwear"), "thrusters": ("mech_scifi", "machine"),
    "cousins": ("themes", "family_relation"), "high_contrast": ("light_effect", "palette"),
    "town": ("indoor_scene", "urban"), "talisman": ("weapons", "magic_weapon"),
    "whipped_cream": ("food_drink", "dessert_snack"), "giving": ("action", "interaction"),
    "stripper_pole": ("adult", "adult_fetish"), "turnaround": ("composition", "layout"),
    "helm": ("legwear_footwear", "helmet_protective"), "full_nelson": ("action", "combat_action"),
    "peeking": ("pose", "gaze"), "o3o": ("expression", "neutral_expression"),
    "ovum": ("adult", "adult_anatomy"), "yume_kawaii": ("style", "art_style"),
    "swing": ("transport_play", "toys"), "melting": ("light_effect", "other_effect"),
    "nape": ("body", "chest"), "disembodied_head": ("body", "body_state"),
    "enpera": ("hair", "hair_style"), "pearl_(gemstone)": ("accessories", "jewelry"),
    "futa_with_male": ("adult", "adult_sex"), "keyhole": ("household_objects", "tools"),
    "sigh": ("action", "daily_action"), "headlamp": ("accessories", "headwear"),
    "sweets": ("food_drink", "dessert_snack"), "footprints": ("outdoor_scene", "terrain_surface"),
    "reach-around": ("adult", "adult_self"), "panther_girl": ("people", "fantasy_person"),
    "counter": ("household_objects", "seating_table"), "bisexual_female": ("themes", "romance_orientation"),
    "drone": ("transport_play", "air_vehicle"), "clothes_down": ("clothing_detail", "clothing_state"),
    "tarot": ("transport_play", "games"), "fertilization": ("adult", "adult_sex"),
    "walk-in": ("themes", "narrative_situation"), "shoulder_carry": ("action", "holding"),
    "padlock": ("household_objects", "tools"), "gorget": ("legwear_footwear", "armor"),
    "green_apron": ("clothes_special", "occupation_uniform"), "gauze": ("body", "body_state"),
    "teasing": ("action", "interaction"), "stuck": ("action", "daily_action"),
    "rod_of_remorse": ("weapons", "magic_weapon"), "mallet": ("household_objects", "tools"),
    "typo": ("text_meta", "text"), "butler": ("people", "occupation"),
    "obliques": ("body", "chest"), "harem": ("themes", "romance_orientation"),
    "flaming_eye": ("light_effect", "fire_smoke"), "chandelier": ("household_objects", "lighting_clock"),
    "brown_corset": ("underwear_swim", "bra_lingerie"), "whisk": ("food_drink", "tableware"),
    "phimosis": ("adult", "adult_anatomy"), "hamster": ("creatures", "mammal"),
    "asphyxiation": ("body", "body_state"), "potato_chips": ("food_drink", "dessert_snack"),
    "toast": ("food_drink", "staple_food"), "selfcest": ("themes", "romance_orientation"),
    "world_war_ii": ("themes", "narrative_situation"), "possessed": ("themes", "persona_variant"),
    "creator_connection": ("themes", "character_connection"), "baguette": ("food_drink", "staple_food"),
    "fleeing": ("action", "movement"), "spilling": ("light_effect", "other_effect"),
    "coral": ("creatures", "aquatic"), "no_dickey": ("clothing_detail", "clothing_state"),
    "tail_wrap": ("creatures", "animal_feature"), "age_progression": ("themes", "persona_variant"),
    "multiple_piercings": ("accessories", "jewelry"), "slap_mark": ("body", "body_marks"),
    "blueberry": ("food_drink", "fruit_vegetable"), "cube": ("text_meta", "symbol"),
    "omurice": ("food_drink", "staple_food"), "cheek_pinching": ("action", "interaction"),
    "hexagram": ("text_meta", "symbol"), "tickling": ("action", "interaction"),
    "crepe": ("food_drink", "dessert_snack"), "vial": ("household_objects", "container"),
    "battery_indicator": ("text_meta", "screen_ui"), "ring_light_reflection": ("light_effect", "optical"),
    "gae_bolg_(fate)": ("weapons", "magic_weapon"), "ankle_cuffs": ("adult", "adult_fetish"),
    "holstered": ("action", "combat_action"), "wire": ("mech_scifi", "machine"),
    "g-string": ("underwear_swim", "panties_underwear"), "tokkuri": ("food_drink", "tableware"),
    "tangzhuang": ("clothes_special", "traditional_east"), "dust": ("light_effect", "particles"),
    "walkie-talkie": ("culture_objects", "camera_media"), "drawer": ("household_objects", "storage_furniture"),
    "shower_(place)": ("indoor_scene", "home_room"), "cameo": ("themes", "persona_variant"),
    "banknote": ("household_objects", "other_object"), "censored_identity": ("text_meta", "censorship"),
    "melting_popsicle": ("food_drink", "dessert_snack"), "scepter": ("weapons", "magic_weapon"),
})

# Non-sexual restraint and joke uses that intentionally override broad adult
# vocabulary.  These exceptions are important because Danbooru disambiguates
# them by suffix rather than by a separate source type.
EXACT_OVERRIDES.update({
    "bound": ("action", "interaction"), "bound_wrists": ("action", "interaction"),
    "bound_ankles": ("action", "interaction"), "bound_together": ("action", "interaction"),
    "tied_up_(nonsexual)": ("action", "interaction"), "shackles": ("household_objects", "tools"),
    "handcuffs": ("household_objects", "tools"), "rear_naked_choke": ("action", "combat_action"),
    "panel_gag": ("text_meta", "comic"), "explosion_gag": ("text_meta", "meme"),
    "sazae-san_food_gag_(meme)": ("text_meta", "meme"), "cigar": ("household_objects", "other_object"),
    "pompadour": ("hair", "hair_style"), "raincoat": ("clothes_main", "outerwear"),
    "spacecraft": ("transport_play", "air_vehicle"), "character_profile": ("text_meta", "meta"),
    "toon_(style)": ("style", "art_style"),
    "amusement_park": ("outdoor_scene", "other_scene"), "encasement": ("body", "body_state"),
    "ganguro": ("face", "makeup"), "concentrating": ("expression", "neutral_expression"),
    "zentradi": ("people", "fantasy_person"), "uranus_symbol": ("text_meta", "symbol"),
    "uranus_(planet)": ("outdoor_scene", "sky_space"), "hentai_foundry_username": ("text_meta", "meta"),
    "naked_shirt": ("clothing_detail", "clothing_state"), "naked_shoes": ("legwear_footwear", "shoes"),
    "sperm_whale": ("creatures", "aquatic"),
    "flight_deck": ("transport_play", "water_vehicle"), "feather_trim": ("clothing_detail", "clothing_structure"),
    "tuxedo": ("clothes_main", "suit"), "hiphighs": ("legwear_footwear", "stockings"),
    "sideburns_stubble": ("face", "facial_hair"), "ufo": ("transport_play", "air_vehicle"),
    "timestamp": ("text_meta", "text"), "black_wrist_cuffs": ("accessories", "handwear"),
    "swim_briefs": ("underwear_swim", "swimsuit"), "spooning": ("action", "interaction"),
    "kigurumi": ("clothes_special", "themed_costume"), "autobot": ("mech_scifi", "robot_android"),
    "cross_pasties": ("underwear_swim", "bra_lingerie"), "magical_musket_(madoka_magica)": ("weapons", "magic_weapon"),
    "aviator_sunglasses": ("accessories", "eyewear"), "pom_pom_beanie": ("accessories", "headwear"),
    "covered_pectorals": ("body", "chest"), "reverse_spitroast": ("adult", "adult_sex"),
    "tying": ("clothing_detail", "clothing_state"), "narutomaki": ("food_drink", "staple_food"),
    "maracas": ("culture_objects", "music"), "submission_hold": ("action", "combat_action"),
    "snowman": ("household_objects", "other_object"), "tengu-geta": ("legwear_footwear", "shoes"),
    "fishing_rod": ("transport_play", "sports"), "wiffle_gag": ("adult", "adult_fetish"),
    "cloth_gag": ("adult", "adult_fetish"), "lotus": ("creatures", "plant"),
    "goldfish": ("creatures", "aquatic"), "broken_horn": ("creatures", "animal_feature"),
    "panda": ("creatures", "mammal"), "plum_blossoms": ("creatures", "plant"),
    "paddle": ("transport_play", "sports"), "birdcage": ("household_objects", "other_object"),
    "boxers": ("underwear_swim", "panties_underwear"), "insignia": ("accessories", "badges_ornaments"),
    "nail_(hardware)": ("household_objects", "tools"), "palms_together": ("pose", "hand_gesture"),
    "wreath": ("accessories", "badges_ornaments"), "rubble": ("outdoor_scene", "terrain_surface"),
    "mesugaki": ("people", "role_focus"), "grabbing": ("action", "holding"),
    "incoming_gift": ("action", "interaction"), "torch": ("household_objects", "lighting_clock"),
    "jersey": ("clothes_main", "tops"), "pastry": ("food_drink", "dessert_snack"),
    "mob_x_character": ("themes", "social_relation"), "rei_no_himo": ("accessories", "other_accessory"),
    "canon_event": ("themes", "narrative_situation"), "volleyball": ("transport_play", "sports"),
    "look-alike": ("themes", "social_relation"), "dreaming": ("themes", "narrative_situation"),
    "on_swing": ("pose", "stationary_pose"), "barrel": ("household_objects", "container"),
    "gold_armlet": ("accessories", "jewelry"), "health_bar": ("text_meta", "screen_ui"),
    "lapel_pin": ("accessories", "badges_ornaments"), "chemise": ("underwear_swim", "bra_lingerie"),
    "blood_stain": ("body", "body_marks"), "samurai": ("people", "occupation"),
    "starter_pokemon_trio": ("creatures", "fantasy_creature"), "countdown": ("time_weather", "calendar"),
    "prostitution": ("adult", "adult_other"), "caustics": ("light_effect", "optical"),
    "skyline": ("indoor_scene", "urban"), "if_they_mated": ("themes", "narrative_situation"),
    "untied": ("clothing_detail", "clothing_state"), "poker_chip": ("transport_play", "games"),
    "fangs_out": ("face", "mouth"), "traffic_light": ("indoor_scene", "urban"),
    "redesign": ("themes", "persona_variant"), "white_corset": ("underwear_swim", "bra_lingerie"),
    "dinosaur": ("creatures", "reptile"), "faucet": ("household_objects", "tools"),
    "have_to_pee": ("adult", "adult_other"), "hikimayu": ("face", "makeup"),
    "respirator": ("legwear_footwear", "helmet_protective"), "fine_fabric_emphasis": ("clothing_detail", "clothing_material"),
    "menu": ("culture_objects", "books_paper"), "real_life_insert": ("text_meta", "meme"),
    "brown_apron": ("clothes_special", "occupation_uniform"), "trick_or_treat": ("time_weather", "holiday"),
    "pot": ("food_drink", "tableware"), "triforce": ("text_meta", "symbol"),
    "pet_play": ("adult", "adult_fetish"), "single_pantsleg": ("clothes_main", "bottoms"),
    "hyur": ("people", "fantasy_person"), "caterpillar_tracks": ("mech_scifi", "machine"),
    "electrokinesis": ("light_effect", "magic_effect"), "pixiv_id": ("text_meta", "meta"),
    "holly": ("creatures", "plant"), "color_connection": ("themes", "character_connection"),
    "seigaiha": ("clothing_detail", "clothing_pattern"), "prayer_beads": ("accessories", "jewelry"),
    "tripping": ("action", "movement"), "livestream": ("culture_objects", "camera_media"),
    "sprite": ("style", "medium"), "tanuki": ("creatures", "mammal"),

    # High-frequency typed compounds that must beat shorter camera/scene words.
    "bow": ("accessories", "badges_ornaments"), "bow_(weapon)": ("weapons", "bow"),
    "bow_(music)": ("culture_objects", "music"), "musical_staff": ("culture_objects", "music"),
    "team_rocket": ("themes", "persona_variant"), "club_(shape)": ("text_meta", "symbol"),
    "hitachi_magic_wand": ("adult", "adult_fetish"), "egg_vibrator": ("adult", "adult_fetish"),
    "object_insertion": ("adult", "adult_sex"), "ball_and_chain_restraint": ("adult", "adult_fetish"),
    "cherry_blossoms": ("creatures", "plant"), "water_drop": ("light_effect", "particles"),
    "soap_bubbles": ("light_effect", "particles"), "orange_nails": ("face", "makeup"),
    "orange_neckerchief": ("accessories", "neckwear"), "stained_glass": ("indoor_scene", "architecture"),
    "broken_glass": ("indoor_scene", "surface"), "against_glass": ("pose", "body_pose"),
    "hand_fan": ("household_objects", "tools"), "folding_fan": ("household_objects", "tools"),
    "folded_fan": ("household_objects", "tools"), "motor_vehicle": ("transport_play", "land_vehicle"),
    "machine_gun": ("weapons", "firearm"), "light_machine_gun": ("weapons", "firearm"),
    "heavy_machine_gun": ("weapons", "firearm"), "mechanical_pencil": ("culture_objects", "stationery"),
    "factory": ("indoor_scene", "public_indoor"), "toy_robot": ("transport_play", "toys"),
    "halo": ("light_effect", "magic_effect"), "colored_halo": ("light_effect", "magic_effect"),
    "hair_flower": ("hair", "hair_accessory"), "butterfly_hair_ornament": ("hair", "hair_accessory"),
    "horse_girl": ("people", "fantasy_person"), "cat_girl": ("people", "fantasy_person"),
    "fox_girl": ("people", "fantasy_person"), "demon_girl": ("people", "fantasy_person"),
    "monster_girl": ("people", "fantasy_person"), "wolf_girl": ("people", "fantasy_person"),
    "rabbit_girl": ("people", "fantasy_person"), "dog_girl": ("people", "fantasy_person"),
    "bat_girl": ("people", "fantasy_person"), "playboy_bunny": ("clothes_special", "themed_costume"),
    "stuffed_animal": ("transport_play", "toys"), "teddy_bear": ("transport_play", "toys"),
    "poke_ball": ("transport_play", "toys"), "basic_poke_ball": ("transport_play", "toys"),
    "card": ("culture_objects", "books_paper"), "id_card": ("culture_objects", "books_paper"),
    "bat_(animal)": ("creatures", "mammal"), "ship_turret": ("weapons", "firearm"),
    "train_conductor": ("people", "occupation"), "bus_stop": ("indoor_scene", "urban"),
    "nail_bat": ("weapons", "polearm"), "sun_hat": ("accessories", "headwear"),
    "space_helmet": ("legwear_footwear", "helmet_protective"), "beach_towel": ("household_objects", "tools"),
    "snowflake_hair_ornament": ("hair", "hair_accessory"), "evening_gown": ("clothes_main", "dress"),
    "gym_uniform": ("clothes_special", "school_uniform"), "office_lady": ("people", "occupation"),
    "office_chair": ("household_objects", "seating_table"), "cropped_jacket": ("clothes_main", "outerwear"),
    "cropped_shirt": ("clothes_main", "tops"), "framed_eyewear": ("accessories", "eyewear"),
    "asymmetrical_bangs": ("hair", "bangs"), "asymmetrical_hair": ("hair", "hair_style"),
    "asymmetrical_legwear": ("legwear_footwear", "stockings"), "asymmetrical_gloves": ("accessories", "handwear"),
    "hug_from_behind": ("action", "interaction"), "grabbing_from_behind": ("action", "interaction"),

    # Remaining popular, unambiguous database terms.
    "surrounded_by_penises": ("adult", "adult_anatomy"), "pussyjob": ("adult", "adult_sex"),
    "69": ("adult", "adult_sex"), "spanking": ("adult", "adult_fetish"),
    "anilingus": ("adult", "adult_oral"), "futa_with_futa": ("adult", "adult_sex"),
    "large_insertion": ("adult", "adult_sex"), "suppressor": ("weapons", "firearm"),
    "multiple_weapons": ("weapons", "other_weapon"), "m4_carbine": ("weapons", "firearm"),
    "spiked_armlet": ("accessories", "handwear"), "d-pad": ("culture_objects", "phone_computer"),
    "crt": ("culture_objects", "phone_computer"), "taiyaki": ("food_drink", "dessert_snack"),
    "sweet_potato": ("food_drink", "fruit_vegetable"), "lettuce": ("food_drink", "fruit_vegetable"),
    "pie": ("food_drink", "dessert_snack"), "briefs": ("underwear_swim", "panties_underwear"),
    "voice_actor": ("people", "occupation"), "ballerina": ("people", "occupation"),
    "k-pop": ("culture_objects", "music"), "concert": ("culture_objects", "music"),
    "circle_name": ("text_meta", "meta"), "product_placement": ("text_meta", "meta"),
    "drinking_glass": ("food_drink", "tableware"), "fruit": ("food_drink", "fruit_vegetable"),
    "vegetable": ("food_drink", "fruit_vegetable"), "lolita_fashion": ("clothes_special", "themed_costume"),
    "leash": ("household_objects", "tools"), "sash": ("accessories", "bags_belts"),
    "sarashi": ("underwear_swim", "bra_lingerie"), "wagashi": ("food_drink", "dessert_snack"),
    "molestation": ("adult", "adult_other"), "sleep_molestation": ("adult", "adult_other"),
    "hand_up": ("pose", "hand_gesture"), "hands_up": ("pose", "hand_gesture"),
    "arm_up": ("pose", "hand_gesture"), "both_arms_up": ("pose", "hand_gesture"),
    "crossed_arms": ("pose", "hand_gesture"), "leg_up": ("pose", "body_pose"),
    "knees_up": ("pose", "body_pose"), "girl_on_top": ("pose", "body_pose"),
    "military_vehicle": ("transport_play", "land_vehicle"), "maid_headdress": ("accessories", "headwear"),
    "nurse_cap": ("accessories", "headwear"), "military_hat": ("accessories", "headwear"),
    "chef_hat": ("accessories", "headwear"), "police_hat": ("accessories", "headwear"),
    "hair_tubes": ("hair", "hair_accessory"), "hair_bobbles": ("hair", "hair_accessory"),
    "hair_rings": ("hair", "hair_accessory"), "scar_on_face": ("body", "body_marks"),
    "blood_on_face": ("body", "body_state"), "food_on_face": ("body", "body_state"),
    "bandaid_on_face": ("body", "body_marks"), "dirty_face": ("body", "body_state"),
    "shopping_bag": ("accessories", "bags_belts"), "ceiling_light": ("household_objects", "lighting_clock"),
    "kitchen_knife": ("weapons", "blade"), "fourth_wall": ("text_meta", "meme"),
    "beachball": ("transport_play", "sports"), "seagull": ("creatures", "bird"),
    "locker_room": ("indoor_scene", "public_indoor"), "sparks": ("light_effect", "particles"),
    "halloween_costume": ("clothes_special", "themed_costume"), "wind_chime": ("household_objects", "other_object"),
    "morning_glory": ("creatures", "plant"), "night_raven_college_school_uniform": ("clothes_special", "school_uniform"),
    "night_vision_device": ("accessories", "eyewear"), "snow_leopard_girl": ("people", "fantasy_person"),
    "see-through_silhouette": ("composition", "framing"), "eyeshadow": ("face", "makeup"),
    "energy_sword": ("weapons", "magic_weapon"), "power_armor": ("legwear_footwear", "armor"),
    "white_feathers": ("creatures", "animal_feature"), "straw": ("food_drink", "tableware"),
    "blinking": ("face", "eye_shape"), "thinking": ("expression", "neutral_expression"),
    "pinky_out": ("pose", "hand_gesture"), "chain-link_fence": ("indoor_scene", "architecture"),
    "indian_style": ("pose", "body_pose"), "japanese_clothes": ("clothes_special", "traditional_east"),
    "chinese_clothes": ("clothes_special", "traditional_east"), "symbol-shaped_pupils": ("face", "eye_shape"),
    "4koma": ("text_meta", "comic"), "japanese_armor": ("legwear_footwear", "armor"),
    "holding_fruit": ("action", "holding"),
})


# Final high-frequency semantic audit.  These compounds contain a strong noun
# (hand, face, hair, shirt, ring, etc.) whose literal meaning is not the tag's
# actual purpose; exact placement prevents broad token rules from stealing them.
EXACT_OVERRIDES.update({
    # People, relationships, identity and narrative concepts.
    "parent_and_child": ("people", "relationship"),
    "mother_and_child": ("people", "relationship"),
    "father_and_child": ("people", "relationship"),
    "onee-shota": ("themes", "romance_orientation"),
    "onee-loli": ("themes", "romance_orientation"),
    "face-to-face": ("pose", "body_pose"),
    "side-by-side": ("composition", "layout"),
    "lineup": ("composition", "layout"),
    "enmaided": ("clothes_special", "occupation_uniform"),
    "animification": ("style", "art_style"),
    "alternate_species": ("themes", "identity_change"),
    "clone_harem": ("themes", "romance_orientation"),
    "gae_dearg_(fate)": ("weapons", "polearm"),
    "persona_(summon)": ("creatures", "fantasy_creature"),
    "clone_trooper": ("people", "occupation"),

    # Body-part compounds that describe poses, gestures, marks or clothing.
    "arms_behind_back": ("pose", "hand_gesture"),
    "arm_support": ("pose", "hand_gesture"),
    "own_hands_together": ("pose", "hand_gesture"),
    "outstretched_arm": ("pose", "hand_gesture"),
    "outstretched_arms": ("pose", "hand_gesture"),
    "arms_behind_head": ("pose", "hand_gesture"),
    "interlocked_fingers": ("pose", "hand_gesture"),
    "arm_at_side": ("pose", "hand_gesture"),
    "arm_behind_back": ("pose", "hand_gesture"),
    "arm_behind_head": ("pose", "hand_gesture"),
    "on_stomach": ("pose", "stationary_pose"),
    "knee_up": ("pose", "body_pose"),
    "legs_up": ("pose", "body_pose"),
    "legs_apart": ("pose", "body_pose"),
    "knees_together_feet_apart": ("pose", "body_pose"),
    "hugging_own_legs": ("pose", "body_pose"),
    "waist_apron": ("clothes_special", "occupation_uniform"),
    "skin_tight": ("clothing_detail", "clothing_structure"),
    "arm_tattoo": ("body", "body_marks"),
    "mole_on_breast": ("body", "body_marks"),

    # Face, hair, expression and gaze.
    "heterochromia": ("face", "eye_color"),
    "alternate_eye_color": ("face", "eye_color"),
    "crying_with_eyes_open": ("expression", "sad_cry"),
    "nose_blush": ("expression", "shy_blush"),
    "facial_mark": ("body", "body_marks"),
    "freckles": ("body", "body_marks"),
    "mole_under_mouth": ("body", "body_marks"),
    "mouth_mask": ("accessories", "eyewear"),
    "eye_mask": ("accessories", "eyewear"),
    "covering_own_mouth": ("pose", "hand_gesture"),
    "hand_to_own_mouth": ("pose", "hand_gesture"),
    "covering_face": ("pose", "hand_gesture"),
    "ear_piercing": ("accessories", "jewelry"),
    "animal_ear_piercing": ("accessories", "jewelry"),
    "ear_ornament": ("accessories", "other_accessory"),
    "ear_bow": ("accessories", "other_accessory"),
    "red_lips": ("face", "makeup"),
    "facial_hair": ("face", "facial_hair"),
    "hair_intakes": ("hair", "hair_style"),
    "antenna_hair": ("hair", "hair_style"),
    "curtained_hair": ("hair", "hair_style"),
    "flipped_hair": ("hair", "hair_style"),
    "hair_over_one_eye": ("hair", "bangs"),
    "forehead": ("face", "brows_nose"),
    "forehead_mark": ("body", "body_marks"),
    "eyes_visible_through_hair": ("style", "technique"),
    "drunk": ("body", "body_state"),
    "grinding": ("adult", "adult_sex"),
    "head_wreath": ("accessories", "headwear"),
    "head_rest": ("pose", "stationary_pose"),
    "head_on_pillow": ("pose", "stationary_pose"),
    "facing_away": ("pose", "body_pose"),
    "facing_another": ("pose", "body_pose"),
    "trembling": ("body", "body_state"),
    "on_head": ("action", "interaction"),

    # Actions, garments and wearable details.
    "fighting_stance": ("pose", "body_pose"),
    "flying_sweatdrops": ("expression", "fear_surprise"),
    "sheathed": ("weapons", "blade"),
    "grabbing_another's_breast": ("adult", "adult_suggestive"),
    "grabbing_another's_ass": ("adult", "adult_suggestive"),
    "grabbing_own_breast": ("adult", "adult_self"),
    "china_dress": ("clothes_special", "traditional_east"),
    "open_jacket": ("clothing_detail", "clothing_state"),
    "open_shirt": ("clothing_detail", "clothing_state"),
    "shirt_lift": ("clothing_detail", "clothing_state"),
    "skirt_lift": ("clothing_detail", "clothing_state"),
    "open_coat": ("clothing_detail", "clothing_state"),
    "no_pants": ("clothing_detail", "clothing_state"),
    "shirt_tucked_in": ("clothing_detail", "clothing_structure"),
    "frilled_shirt_collar": ("clothing_detail", "clothing_structure"),
    "casual_one-piece_swimsuit": ("underwear_swim", "swimsuit"),
    "kindergarten_uniform": ("clothes_special", "school_uniform"),
    "open_kimono": ("clothing_detail", "clothing_state"),
    "bikini_armor": ("legwear_footwear", "armor"),
    "corset": ("underwear_swim", "bra_lingerie"),
    "bridal_gauntlets": ("accessories", "handwear"),
    "hand_in_pocket": ("pose", "hand_gesture"),
    "body_fur": ("creatures", "animal_feature"),
    "white_fur": ("creatures", "animal_feature"),
    "black_collar": ("accessories", "neckwear"),
    "white_collar": ("accessories", "neckwear"),
    "lifting_own_clothes": ("clothing_detail", "clothing_state"),
    "sleeves_rolled_up": ("clothing_detail", "clothing_state"),
    "strap_slip": ("clothing_detail", "clothing_state"),
    "adjusting_clothes": ("clothing_detail", "clothing_state"),
    "blood_on_clothes": ("clothing_detail", "clothing_state"),
    "cross-laced_clothes": ("clothing_detail", "clothing_structure"),
    "o-ring": ("clothing_detail", "clothing_structure"),
    "buckle": ("clothing_detail", "clothing_structure"),
    "ribbon_trim": ("clothing_detail", "clothing_structure"),
    "armlet": ("accessories", "jewelry"),
    "swim_ring": ("transport_play", "sports"),
    "missing_headwear": ("clothing_detail", "clothing_state"),
    "neck_ribbon": ("accessories", "neckwear"),

    # Seasonal uniforms and non-sexual words that resemble adult terms.
    "winter_uniform": ("clothes_special", "school_uniform"),
    "summer_uniform": ("clothes_special", "school_uniform"),
    "gem_uniform_(houseki_no_kuni)": ("clothes_special", "school_uniform"),
    "white_day": ("time_weather", "holiday"),
    "squirting_liquid": ("light_effect", "particles"),
    "constriction": ("action", "combat_action"),
    "naked_boots": ("legwear_footwear", "boots"),
    "clothes_gag": ("household_objects", "tools"),
    "ankle_cuffs": ("accessories", "other_accessory"),
    "straitjacket": ("clothing_detail", "other_clothes"),
    "sadism": ("adult", "adult_fetish"),
    "dualshock": ("culture_objects", "phone_computer"),
    "shock_collar": ("adult", "adult_fetish"),
    "clothes_hanger": ("household_objects", "storage_furniture"),
    "coffee_grinder": ("household_objects", "tools"),
    "doppelganger": ("themes", "persona_variant"),
    "saddle": ("transport_play", "sports"),
    "cooperative_grinding": ("adult", "adult_sex"),
    "happy_facial": ("adult", "adult_fluid"),
    "happy_holidays": ("text_meta", "text"),
    "happy_meal": ("food_drink", "staple_food"),
    "happy_mille-feuille_(idolmaster)": ("clothes_special", "themed_costume"),
    "happy_party_train": ("clothes_special", "themed_costume"),
    "hello_happy_world!": ("culture_objects", "music"),

    # Natural objects that previously had no truthful semantic home.
    "gem": ("creatures", "mineral"),
    "crystal": ("creatures", "mineral"),
    "stone": ("creatures", "mineral"),
    "diamond_(gemstone)": ("creatures", "mineral"),
    "pearl_(gemstone)": ("creatures", "mineral"),
    "jade_(gemstone)": ("creatures", "mineral"),
    "opal_(gemstone)": ("creatures", "mineral"),
    "amber_(gemstone)": ("creatures", "mineral"),
    "phosphophyllite_(gemstone)": ("creatures", "mineral"),
    "turquoise_(gemstone)": ("creatures", "mineral"),
    "coal": ("creatures", "mineral"),
    "bauxite": ("creatures", "mineral"),

    # Common head compounds: only directional head movement belongs to gaze.
    "head_grab": ("action", "interaction"),
    "head_on_another's_shoulder": ("pose", "stationary_pose"),
    "head_between_breasts": ("adult", "adult_suggestive"),
    "head_only": ("people", "role_focus"),
    "head_bump": ("action", "interaction"),
    "head_on_hand": ("pose", "hand_gesture"),
    "head_chain": ("accessories", "headwear"),
    "head_on_chest": ("pose", "stationary_pose"),
    "head_on_head": ("action", "interaction"),
    "head_steam": ("expression", "anger"),
    "head_between_thighs": ("adult", "adult_suggestive"),
    "head_on_arm": ("pose", "stationary_pose"),
    "head_on_table": ("pose", "stationary_pose"),
    "head_hug": ("action", "interaction"),
    "head_and_hip_pose": ("pose", "body_pose"),
    "head_on_ass": ("adult", "adult_suggestive"),
    "head_pinned_down": ("action", "interaction"),
    "head_tattoo": ("body", "body_marks"),
    "head_mirror": ("accessories", "headwear"),
    "head_on_knees": ("pose", "stationary_pose"),
    "head_ornament": ("accessories", "headwear"),
    "head_bow": ("accessories", "headwear"),
    "head_rub": ("action", "interaction"),
    "head_hold": ("action", "interaction"),

    # Strong compound nouns discovered during the final modifier-order audit.
    "power_suit": ("legwear_footwear", "armor"),
    "power_suit_(metroid)": ("legwear_footwear", "armor"),
    "apron_lift": ("clothing_detail", "clothing_state"),
    "apron_hold": ("action", "holding"),
    "jersey_maid": ("clothes_special", "occupation_uniform"),
    "bikini_in_mouth": ("face", "mouth"),
    "hat_flower": ("accessories", "headwear"),
    "dress_flower": ("clothing_detail", "clothing_structure"),
    "leaf_hat_ornament": ("accessories", "headwear"),
    "bamboo_steamer": ("food_drink", "tableware"),
    "pool_table": ("transport_play", "games"),
    "desert_eagle": ("weapons", "firearm"),
    "walther_wa_2000": ("weapons", "firearm"),
    "steyr_iws_2000": ("weapons", "firearm"),
    "energy_gun": ("weapons", "magic_weapon"),
    "water_gun": ("transport_play", "toys"),
    "toy_gun": ("transport_play", "toys"),
    "nintendo_3ds": ("culture_objects", "phone_computer"),
    "pigeon-toed": ("pose", "body_pose"),
    "flower_in_eye": ("face", "eye_shape"),
    "flower_over_eye": ("face", "eye_shape"),
    "korean_clothes": ("clothes_special", "traditional_east"),
    "chinese_knot": ("accessories", "badges_ornaments"),
    "chinese_zodiac": ("text_meta", "symbol"),
    "chinese_bellflower": ("creatures", "plant"),
    "mobile_suit": ("mech_scifi", "mecha"),
    "stuffed_gag": ("adult", "adult_fetish"),
    "adam's_apple": ("body", "chest"),
    "keyboard_(instrument)": ("culture_objects", "music"),
    "steamed_bun": ("food_drink", "staple_food"),
    "japari_bun": ("food_drink", "staple_food"),
    "bread_bun": ("food_drink", "staple_food"),
    "hot_dog_bun": ("food_drink", "staple_food"),
    "bun_(food)": ("food_drink", "staple_food"),
    "arrow_(symbol)": ("text_meta", "symbol"),
    "arrow_(projectile)": ("weapons", "bow"),
    "arrow_print": ("clothing_detail", "clothing_pattern"),
    "arrow_tattoo": ("body", "body_marks"),
    "outside_border": ("composition", "framing"),
    "black_border": ("composition", "framing"),
    "star_(sky)": ("outdoor_scene", "sky_space"),
    "full_moon": ("outdoor_scene", "sky_space"),
    "crescent_moon": ("outdoor_scene", "sky_space"),
    "red_moon": ("outdoor_scene", "sky_space"),
    "disembodied_linked_eye": ("face", "eye_shape"),
    "reaching_towards_viewer": ("pose", "hand_gesture"),
    "crotch_seam": ("clothing_detail", "clothing_structure"),
    "fireworks": ("light_effect", "particles"),
    "aerial_fireworks": ("light_effect", "particles"),
    "poolside": ("outdoor_scene", "water_scene"),
    "sidelighting": ("light_effect", "lighting"),
    "alternate_universe": ("themes", "narrative_situation"),
    "boy_on_top": ("pose", "body_pose"),
    "suitcase": ("accessories", "bags_belts"),
    "kanzashi": ("hair", "hair_accessory"),
    "zettai_ryouiki": ("legwear_footwear", "stockings"),
    "steaming_body": ("body", "body_state"),
    "body_markings": ("body", "body_marks"),
    "arms_at_sides": ("pose", "hand_gesture"),
    "hands_in_pockets": ("pose", "hand_gesture"),
    "symbol_in_eye": ("face", "eye_shape"),
    "multiple_4koma": ("text_meta", "comic"),
    "square_4koma": ("text_meta", "comic"),
    "window_shadow": ("light_effect", "lighting"),
    "window_blinds": ("household_objects", "storage_furniture"),
    "shooting_star": ("outdoor_scene", "sky_space"),
    "down_jacket": ("clothes_main", "outerwear"),
    "squiggle": ("text_meta", "symbol"),
    "picture_frame": ("household_objects", "other_object"),
    "chalkboard": ("culture_objects", "books_paper"),
    "aiguillette": ("accessories", "badges_ornaments"),
    "black_sash": ("accessories", "bags_belts"),
    "blue_sash": ("accessories", "bags_belts"),
    "fashion": ("style", "genre"),
    "goth_fashion": ("style", "genre"),
    "reverse_bunnysuit": ("clothes_special", "themed_costume"),
    "spacesuit": ("legwear_footwear", "helmet_protective"),
    "earth_(planet)": ("outdoor_scene", "sky_space"),
    "public_nudity": ("adult", "adult_nudity"),
    "squirrel_girl": ("people", "fantasy_person"),
    "squirrel": ("creatures", "mammal"),
    "covered_face": ("body", "body_state"),
    "stitched_face": ("body", "body_marks"),
    "sticker_on_face": ("body", "body_marks"),
    "bandage_on_face": ("body", "body_marks"),
    "sink": ("household_objects", "other_object"),
    "screentones": ("style", "technique"),
    "girl_sandwich": ("themes", "social_relation"),
    "chocolate_on_body": ("body", "body_state"),
    "chocolate_on_breasts": ("body", "body_state"),
    "chocolate_on_face": ("body", "body_state"),
    "rice_paddy": ("outdoor_scene", "forest_field"),
    "rice_cooker": ("household_objects", "lighting_clock"),
    "banana_boat": ("transport_play", "sports"),
    "inkling": ("people", "fantasy_person"),
    "wind_lift": ("action", "movement"),
    "splashing": ("action", "movement"),
    "cropped_shoulders": ("composition", "framing"),
    "flashing": ("adult", "adult_nudity"),
    "color_guide": ("light_effect", "palette"),
    "cumulonimbus_cloud": ("time_weather", "weather"),
    "smokestack": ("indoor_scene", "architecture"),
    "inset_border": ("composition", "framing"),
    "asymmetrical_docking": ("adult", "adult_suggestive"),
    "symmetrical_docking": ("adult", "adult_suggestive"),
    "grabbing_own_ass": ("adult", "adult_self"),
    "holding_detached_head": ("adult", "adult_gore"),
    "pulling": ("action", "holding"),
    "beckoning": ("pose", "hand_gesture"),
    "heel_up": ("pose", "body_pose"),
    "drying": ("action", "daily_action"),
    "chewing": ("action", "daily_action"),
    "fishing": ("action", "daily_action"),
    "cheering": ("action", "daily_action"),
    "chasing": ("action", "movement"),
    "fallen_down": ("action", "movement"),
    "wrestling": ("transport_play", "sports"),
    "stepped_on": ("action", "interaction"),
    "multiple_condoms": ("adult", "adult_fetish"),
    "condom_packet_strip": ("adult", "adult_fetish"),
    "ryona": ("adult", "adult_gore"),
    "impaled": ("adult", "adult_gore"),
    "stab": ("adult", "adult_gore"),
    "dominatrix": ("adult", "adult_fetish"),
    "implied_futanari": ("themes", "identity_change"),
    "furrification": ("themes", "identity_change"),
    "inflation": ("body", "body_state"),
    "pain": ("body", "body_state"),
    "exhausted": ("body", "body_state"),
    "unconscious": ("body", "body_state"),
    "pink_blood": ("body", "body_state"),
    "doyagao": ("expression", "positive"),
    "x_x": ("face", "eye_shape"),
    "nail_art": ("face", "makeup"),
    "neck": ("body", "chest"),
    "spine": ("body", "chest"),
    "blunt_tresses": ("hair", "hair_style"),
    "east_asian": ("people", "role_focus"),
    "asian": ("people", "role_focus"),
    "wisteria": ("creatures", "plant"),
    "foliage": ("creatures", "plant"),
    "bud": ("creatures", "plant"),
    "column_lineup": ("composition", "layout"),
    "rotational_symmetry": ("composition", "layout"),
    "dotted_line": ("text_meta", "symbol"),
    "magnifying_glass": ("household_objects", "tools"),
    "notepad": ("culture_objects", "stationery"),
    "kettle": ("food_drink", "tableware"),
    "air_conditioner": ("household_objects", "lighting_clock"),
    "railroad_tracks": ("indoor_scene", "urban"),
    "nengajou": ("time_weather", "holiday"),
    "pocky_day": ("time_weather", "holiday"),
    "gym_storeroom": ("indoor_scene", "public_indoor"),
    "warship": ("transport_play", "water_vehicle"),
    "boy_sandwich": ("themes", "social_relation"),
    "faux_figurine": ("pose", "body_pose"),
    "drawing_sword": ("action", "combat_action"),
    "candy_wrapper": ("household_objects", "container"),
    "at_computer": ("action", "daily_action"),
    # Small-category cleanup: physical objects and semantic compounds that
    # previously leaked into UI/quality/underwear buckets through short words.
    "libra_(constellation)": ("outdoor_scene", "sky_space"),
    "libra_(zodiac)": ("text_meta", "symbol"),
    "wallpaper_(object)": ("indoor_scene", "surface"),
    "orb": ("light_effect", "magic_effect"),
    "interface_headset_(evangelion)": ("mech_scifi", "scifi_device"),
    "window_(computing)": ("text_meta", "screen_ui"),
    "split_screen": ("composition", "layout"),
    "through_screen": ("action", "movement"),
    "flat_screen_tv": ("culture_objects", "camera_media"),
    "screen_light": ("light_effect", "lighting"),
    "folding_screen": ("household_objects", "storage_furniture"),
    "looking_at_screen": ("pose", "gaze"),
    "window_light": ("light_effect", "lighting"),
    "bamboo_screen": ("household_objects", "storage_furniture"),
    "window_shutter": ("household_objects", "storage_furniture"),
    "open_window_shutter": ("household_objects", "storage_furniture"),
    "window_fog": ("indoor_scene", "surface"),
    "privacy_screen": ("household_objects", "storage_furniture"),
    "green_screen": ("style", "photo_3d"),
    "floating_screen": ("mech_scifi", "scifi_device"),
    "projector_screen": ("culture_objects", "camera_media"),
    "window_shopping": ("action", "daily_action"),

    # Boundary/collision audit: these names were previously stolen by a short
    # English or Chinese substring (for example 眼镜 in 眼镜蛇, 茶 in 山茶花,
    # or 剑 in a franchise title).  Keep the unambiguous corrections explicit.
    "cobra_(animal)": ("creatures", "reptile"),
    "camellia": ("creatures", "plant"),
    "sakazuki": ("food_drink", "tableware"),
    "yunomi": ("food_drink", "tableware"),
    "tankard": ("food_drink", "tableware"),
    "teaspoon": ("food_drink", "tableware"),
    "glass_teapot": ("food_drink", "tableware"),
    "side_handle_teapot": ("food_drink", "tableware"),
    "barista": ("people", "occupation"),
    "quill": ("culture_objects", "stationery"),
    "badminton": ("transport_play", "sports"),
    "shuttlecock": ("transport_play", "sports"),
    "flashbang": ("weapons", "explosive"),
    "feathered_dinosaur": ("creatures", "reptile"),
    "petal_on_head": ("hair", "hair_accessory"),
    "core_crystal_(xenoblade)": ("creatures", "mineral"),
    "saury": ("food_drink", "meat_seafood"),
    "scissorhold": ("action", "combat_action"),
    "kendama": ("transport_play", "toys"),
    "kendo": ("transport_play", "sports"),
    "gladiolus": ("creatures", "plant"),
    "swordfish": ("creatures", "aquatic"),
    "fairey_swordfish": ("transport_play", "air_vehicle"),
    "fencing": ("transport_play", "sports"),
    "yggdrasil_(sao)": ("creatures", "plant"),
    "disguised_pyra_(xenoblade)": ("people", "role_focus"),
    "scalpel": ("household_objects", "tools"),
    "trowel": ("household_objects", "tools"),
    "razor": ("household_objects", "tools"),
    "safety_razor": ("household_objects", "tools"),
    "straight_razor": ("household_objects", "tools"),
    "shears": ("household_objects", "tools"),
    "knifed": ("action", "combat_action"),
    "at_knifepoint": ("action", "combat_action"),
    "triple_wielding": ("action", "combat_action"),
    "quadruple_wielding": ("action", "combat_action"),

    # Door/railing compounds describe a pose, action, person or object rather
    # than architecture merely because their translation contains 门/栏杆.
    "against_railing": ("pose", "stationary_pose"),
    "on_railing": ("pose", "stationary_pose"),
    "against_door": ("pose", "stationary_pose"),
    "against_pillar": ("pose", "stationary_pose"),
    "opening_door": ("action", "daily_action"),
    "closing_door": ("action", "daily_action"),
    "knocking": ("action", "daily_action"),
    "slamming_door": ("action", "daily_action"),
    "through_portal": ("action", "movement"),
    "goalkeeper": ("people", "occupation"),
    "construction_worker": ("people", "occupation"),
    "doorknob": ("household_objects", "tools"),
    "door_handle": ("household_objects", "tools"),
    "doorbell": ("household_objects", "lighting_clock"),
    "doormat": ("household_objects", "other_object"),
    "valve": ("household_objects", "tools"),

    # Grabbing, holding and kissing are actions even when their object is a
    # body part or a garment with a stronger noun rule.
    "surprise_kiss": ("action", "interaction"),
    "tiptoe_kiss": ("action", "interaction"),
    "fox_shadow_puppet_kiss": ("action", "interaction"),
    "crotch_grab": ("adult", "adult_suggestive"),
    "choke_hold": ("action", "combat_action"),
    "neck_hold": ("action", "combat_action"),
    "gangsta_hold": ("action", "combat_action"),
    "leg_lift": ("pose", "body_pose"),
    "ass_lift": ("pose", "body_pose"),
    "breast_lift": ("action", "interaction"),
    "pectoral_lift": ("action", "interaction"),
    "babydoll_hold": ("pose", "body_pose"),
})

# Full small-category audit: people, relationships and expressions.  These are
# semantic compounds whose head cannot be recovered safely from a short token.
EXACT_OVERRIDES.update({
    "group_name": ("text_meta", "text"),
    "crowded": ("composition", "layout"),
    "group_profile": ("composition", "layout"),
    "fully_genderswapped_group": ("themes", "identity_change"),
    "triple_baka_(group)": ("people", "relationship"),
    "group_(toaru)": ("people", "relationship"),
    "child's_drawing": ("style", "art_style"),
    "adoptive_parent_and_adoptive_child": ("themes", "family_relation"),
    "step-parent_and_step-child": ("themes", "family_relation"),
    "onii-shota": ("themes", "romance_orientation"),
    "child_carry": ("action", "holding"),
    "baby_carry": ("action", "holding"),
    "children's_day": ("time_weather", "holiday"),
    "baby's-breath": ("creatures", "plant"),
    "old_maid_alliance_(touhou)": ("people", "relationship"),
    "the_children_(zettai_karen_children)": ("people", "relationship"),
    "emperor's_children": ("people", "relationship"),
    "adult_baby": ("adult", "adult_fetish"),
    "old_maid": ("transport_play", "games"),
    "baby_carrier": ("accessories", "other_accessory"),
    "the_vivid_old_tale_(project_sekai)": ("themes", "narrative_situation"),
    "lost_child": ("themes", "narrative_situation"),
    "family_crest": ("text_meta", "symbol"),
    "mother's_day": ("time_weather", "holiday"),
    "father's_day": ("time_weather", "holiday"),
    "sub_for_couple": ("text_meta", "text"),
    "playground_equipment_(kemono_friends_pavilion)": ("transport_play", "toys"),
    "traditional_nun": ("clothes_special", "occupation_uniform"),
    "victorian_maid": ("clothes_special", "occupation_uniform"),
    "qi_maid": ("clothes_special", "occupation_uniform"),
    "tactical_maid": ("clothes_special", "occupation_uniform"),
    "pretty_waitress_(idolmaster)": ("clothes_special", "occupation_uniform"),
    "idol_heart_incom": ("clothes_special", "themed_costume"),
    "maid_day": ("time_weather", "holiday"),
    "witch_(madoka_magica)": ("people", "fantasy_person"),
    "needle_(hollow_knight)": ("weapons", "blade"),
    "nail_(hollow_knight)": ("weapons", "blade"),
    "shiny_rod_(little_witch_academia)": ("weapons", "magic_weapon"),
    "witch's_labyrinth": ("outdoor_scene", "other_scene"),
    "artist_progress": ("text_meta", "meta"),
    "artist's_hand_in_frame": ("composition", "framing"),
    "artist_glove": ("accessories", "handwear"),
    "pin_(hollow_knight)": ("accessories", "badges_ornaments"),
    "moorish_idol": ("creatures", "aquatic"),
    "the_magician_(tarot)": ("text_meta", "symbol"),
    "mini_person": ("body", "build"),
    "minigirl": ("body", "build"),
    "miniboy": ("body", "build"),
    "giantess": ("body", "build"),
    "head_only": ("composition", "framing"),
    "superhero_landing": ("pose", "body_pose"),
    "hero_shot_(splatoon_1)": ("weapons", "firearm"),
    "heron": ("creatures", "bird"),
    "heroes'_gallery": ("composition", "layout"),
    "boku_no_hero_academia_2nd_popularity_poll": ("text_meta", "meta"),
    "type-moon_heroines": ("people", "relationship"),
    "gae_buidhe_(fate)": ("weapons", "polearm"),
    "borrowed_character": ("text_meta", "meta"),
    "cameo": ("themes", "narrative_situation"),
    "team_rocket": ("people", "relationship"),
    "personality_excrement": ("adult", "adult_fetish"),
    "fell_bullet_(e.g.o)": ("weapons", "other_weapon"),
    "everyone": ("people", "count_gender"),
    "glasgow_smile": ("body", "body_marks"),
    "the_fun_gang": ("people", "relationship"),
    "smile_(e.g.o)": ("weapons", "other_weapon"),
    "teardrop-shaped_gem": ("accessories", "jewelry"),
    "tears_of_the_tarnished_blood_(e.g.o)": ("weapons", "other_weapon"),
    "failnaught_(fate)": ("weapons", "bow"),
    "la_grondement_du_haine": ("weapons", "firearm"),
    "surprised_arms": ("pose", "hand_gesture"),
    "scared_to_sleep_alone": ("themes", "narrative_situation"),
    "trypophobia": ("themes", "narrative_situation"),
    "cats_are_scared_of_cucumbers": ("text_meta", "meme"),
    "crazy_straw": ("food_drink", "tableware"),
    "expression_chart": ("text_meta", "meta"),
    "hoyolab_sticker_redraw": ("text_meta", "meta"),
    "facial_expression_training": ("text_meta", "meta"),
    "squeans": ("text_meta", "symbol"),
    "\\(^o^)/": ("expression", "positive"),
})

EXACT_OVERRIDES.update({
    # Body compounds, pose/action predicates and object names.
    "lower_body": ("body", "waist_legs"),
    "fat_mons": ("adult", "adult_anatomy"),
    "paint_on_body": ("body", "body_marks"),
    "hole_on_body": ("body", "body_state"),
    "arrow_in_body": ("body", "body_state"),
    "blood_on_body": ("body", "body_state"),
    "exposed_muscle": ("body", "body_state"),
    "cream_on_body": ("body", "body_state"),
    "snow_on_body": ("body", "body_state"),
    "hollow_body": ("body", "body_state"),
    "growing_out_of_body": ("body", "body_state"),
    "body_switch": ("themes", "identity_change"),
    "body_modification": ("themes", "identity_change"),
    "body_control": ("themes", "identity_change"),
    "slimification": ("themes", "identity_change"),
    "undersized_pokemon": ("themes", "persona_variant"),
    "cross-body_stretch": ("pose", "body_pose"),
    "arms_across_body": ("pose", "hand_gesture"),
    "short_sideburns": ("face", "facial_hair"),
    "skinny_dipping": ("adult", "adult_nudity"),
    "size_comparison": ("themes", "social_relation"),
    "giant_hand": ("body", "arms_hands_feet"),
    "alternate_body_fluid": ("adult", "adult_fluid"),
    "body_exploration": ("adult", "adult_suggestive"),
    "fat_joke": ("text_meta", "meme"),
    "muscle_envy": ("text_meta", "meme"),
    "muscle_awe": ("text_meta", "meme"),
    "body_chain": ("accessories", "jewelry"),
    "artificial_vagina_with_body": ("adult", "adult_fetish"),
    "drying_body": ("action", "daily_action"),
    "body_soaping": ("action", "daily_action"),
    "knees_to_chest": ("pose", "body_pose"),
    "knee_to_chest": ("pose", "body_pose"),
    "arm_across_chest": ("pose", "hand_gesture"),
    "clutching_chest": ("pose", "hand_gesture"),
    "covering_chest": ("pose", "hand_gesture"),
    "chest_jewel": ("accessories", "jewelry"),
    "chest_harness": ("accessories", "other_accessory"),
    "ascot_between_breasts": ("accessories", "neckwear"),
    "neckerchief_between_breasts": ("accessories", "neckwear"),
    "chain_between_breasts": ("accessories", "jewelry"),
    "stethoscope_between_breasts": ("household_objects", "tools"),
    "gift_between_breasts": ("household_objects", "other_object"),
    "money_between_breasts": ("household_objects", "other_object"),
    "treasure_chest": ("household_objects", "container"),
    "chest_of_drawers": ("household_objects", "storage_furniture"),
    "mimic_chest": ("household_objects", "container"),
    "breast_mousepad": ("household_objects", "other_object"),
    "breast_pump": ("household_objects", "tools"),
    "toe_cleavage": ("body", "arms_hands_feet"),
    "udder": ("creatures", "animal_feature"),
    "bridal_chest_(fate)": ("weapons", "other_weapon"),
    "red_hiphighs": ("legwear_footwear", "stockings"),
    "gold_thighlet": ("accessories", "jewelry"),
    "silver_thighlet": ("accessories", "jewelry"),
    "thighlet": ("accessories", "jewelry"),
    "thigh_beads": ("accessories", "jewelry"),
    "calflet": ("accessories", "jewelry"),
    "waist_sash": ("accessories", "bags_belts"),
    "waist_tassel": ("accessories", "badges_ornaments"),
    "on_one_knee": ("pose", "stationary_pose"),
    "m_legs": ("pose", "body_pose"),
    "knees_apart_feet_together": ("pose", "body_pose"),
    "legs_folded": ("pose", "body_pose"),
    "legs_over_head": ("pose", "body_pose"),
    "v_legs": ("pose", "body_pose"),
    "hanging_legs": ("pose", "body_pose"),
    "legs_behind_head": ("pose", "body_pose"),
    "hips_in_air": ("pose", "body_pose"),
    "head_between_knees": ("pose", "body_pose"),
    "view_between_legs": ("composition", "viewpoint"),
    "lap_pov": ("composition", "viewpoint"),
    "thigh_sheath": ("weapons", "blade"),
    "hip_flask": ("household_objects", "container"),
    "hip_hop": ("style", "genre"),
    "bad_ass": ("style", "quality"),
    "good_ass_day": ("time_weather", "holiday"),
    "peg_leg": ("mech_scifi", "cybernetic"),
    "mooning": ("adult", "adult_nudity"),
    "ass_worship": ("adult", "adult_fetish"),
    "hand_puppet": ("transport_play", "toys"),
    "finger_puppet": ("transport_play", "toys"),
    "hand_net": ("household_objects", "tools"),
    "hand_saw": ("household_objects", "tools"),
    "nail_clippers": ("household_objects", "tools"),
    "hand_guard": ("weapons", "blade"),
    "right-hand_drive": ("transport_play", "land_vehicle"),
    "left-hand_drive": ("transport_play", "land_vehicle"),
    "tic-tac-toe": ("transport_play", "games"),
    "claw_foot_bathtub": ("household_objects", "other_object"),
    "dual_arm_cannons": ("weapons", "firearm"),
    "magic_arm": ("mech_scifi", "cybernetic"),
    "remington_arms": ("weapons", "firearm"),
    "pale_color": ("light_effect", "palette"),
    "pale_eye": ("face", "eye_color"),
    "rider-tan": ("themes", "persona_variant"),
    "tan_tan_pou": ("style", "art_style"),
    "tan_tattoo": ("body", "body_marks"),
    "torn_skin": ("body", "body_state"),
    "broken_skin": ("body", "body_state"),
    "fn_scar": ("weapons", "firearm"),
    "fn_scar_16": ("weapons", "firearm"),
    "fn_scar_17": ("weapons", "firearm"),
    "mole_(animal)": ("creatures", "mammal"),
    "length_markings": ("text_meta", "symbol"),
    "kill_markings": ("text_meta", "symbol"),
    "removing_bandaid": ("action", "daily_action"),
    "sweatband": ("accessories", "handwear"),
    "pocari_sweat": ("food_drink", "drink"),
    "encasement": ("themes", "narrative_situation"),
    "transformation": ("themes", "identity_change"),
    "character_transformation": ("themes", "identity_change"),
    "partial_transformation": ("themes", "identity_change"),
})

EXACT_OVERRIDES.update({
    # Face and hair compound-head corrections.
    "mechanical_eyes": ("mech_scifi", "cybernetic"),
    "eye_trail": ("light_effect", "optical"),
    "flaming_eyes": ("light_effect", "fire_smoke"),
    "electric_eyes": ("light_effect", "magic_effect"),
    "eye_beam": ("light_effect", "magic_effect"),
    "eye_print": ("text_meta", "symbol"),
    "iris_print": ("text_meta", "symbol"),
    "eye_chart": ("text_meta", "symbol"),
    "cyclops": ("people", "fantasy_person"),
    "eye_pov": ("composition", "viewpoint"),
    "eye_slugger": ("weapons", "blade"),
    "re;iris_(idolmaster)": ("themes", "social_relation"),
    "nose_art": ("style", "art_style"),
    "nose_pads": ("accessories", "eyewear"),
    "over_the_nose_gag": ("adult", "adult_fetish"),
    "pacifier": ("household_objects", "tools"),
    "toothbrush": ("household_objects", "tools"),
    "cigarette_holder": ("household_objects", "tools"),
    "mouth_guard": ("household_objects", "tools"),
    "toucan": ("creatures", "bird"),
    "platypus": ("creatures", "mammal"),
    "whitebeard_pirates_jolly_roger": ("text_meta", "symbol"),
    "stroking_beard": ("pose", "hand_gesture"),
    "applying_makeup": ("action", "daily_action"),
    "prologue_rouge_(idolmaster)": ("clothes_special", "themed_costume"),
    "sexting": ("text_meta", "text"),
    "white_armpit_hair": ("body", "body_state"),
    "twintails_day": ("time_weather", "holiday"),
    "hairstyle_switch": ("themes", "persona_variant"),
    "borrowed_hairstyle": ("themes", "persona_variant"),
    "self-borrowed_hairstyle": ("themes", "persona_variant"),
    "matching_hairstyles": ("themes", "character_connection"),
    "hairstyle_connection": ("themes", "character_connection"),
    "ponytail_holder": ("hair", "hair_accessory"),
    "fake_hair_bun": ("hair", "hair_accessory"),
    "curling_iron": ("household_objects", "tools"),
    "braided_beard": ("face", "facial_hair"),
    "forehead_jewel": ("accessories", "jewelry"),
    "forehead_protector": ("legwear_footwear", "armor"),
    "kissing_forehead": ("action", "interaction"),
    "forehead-to-forehead": ("action", "interaction"),
    "forehead_flick": ("action", "interaction"),
    "wiping_forehead": ("action", "daily_action"),
    "hand_to_forehead": ("pose", "hand_gesture"),
    "forehead_blush": ("expression", "shy_blush"),
    "happuri_(forehead_armor)": ("legwear_footwear", "armor"),
    "medium_sideburns": ("face", "facial_hair"),
    "large_forehead": ("face", "brows_nose"),
    "shiny_forehead": ("face", "brows_nose"),
    "hair_tie_on_wrist": ("accessories", "handwear"),
    "hair_tie_in_mouth": ("action", "holding"),
    "adjusting_hair_ornament": ("hair", "hair_action"),
    "torn_hair_ribbon": ("clothing_detail", "clothing_state"),
    "hair_bell": ("hair", "hair_accessory"),
    "hair_stick": ("hair", "hair_accessory"),
    "hair_extensions": ("hair", "hair_accessory"),
    "hair_brush": ("household_objects", "tools"),
    "hair_dryer": ("household_objects", "tools"),
    "hair_rollers": ("hair", "hair_accessory"),
    "hair_net": ("hair", "hair_accessory"),
    "hair_dye": ("household_objects", "tools"),
    "hair_straightener": ("household_objects", "tools"),
    "hair_clipper": ("household_objects", "tools"),
    "mechanical_hair": ("mech_scifi", "cybernetic"),
    "cable_hair": ("mech_scifi", "cybernetic"),
    "hair_weapon": ("weapons", "other_weapon"),
    "gazebo": ("indoor_scene", "architecture"),
    "gaze_on_me!_outfit_(umamusume)": ("clothes_special", "themed_costume"),
    "looking_through_scope": ("action", "combat_action"),
    "postmark": ("text_meta", "symbol"),
})

EXACT_OVERRIDES.update({
    # Pose/action predicates versus noun compounds.
    "holding_breath": ("body", "body_state"),
    "holding_back": ("themes", "narrative_situation"),
    "raised_fist": ("pose", "hand_gesture"),
    "raised_fists": ("pose", "hand_gesture"),
    "holding_stomach": ("pose", "hand_gesture"),
    "holding_belly": ("pose", "hand_gesture"),
    "holding_behind_neck": ("pose", "hand_gesture"),
    "holding_ears": ("pose", "hand_gesture"),
    "aperture_science_handheld_portal_device": ("mech_scifi", "scifi_device"),
    "sheathing": ("action", "combat_action"),
    "running_bond": ("indoor_scene", "surface"),
    "riding_crop": ("weapons", "other_weapon"),
    "falling_feathers": ("light_effect", "particles"),
    "falling_paper": ("light_effect", "particles"),
    "falling_money": ("light_effect", "particles"),
    "flying_teardrops": ("light_effect", "particles"),
    "flying_spittle": ("light_effect", "particles"),
    "flying_button": ("light_effect", "particles"),
    "flying_paper": ("light_effect", "particles"),
    "running_track": ("transport_play", "sports"),
    "floating_neckwear": ("accessories", "neckwear"),
    "flying_saucer": ("transport_play", "air_vehicle"),
    "flying_boat": ("transport_play", "air_vehicle"),
    "flying_car": ("transport_play", "air_vehicle"),
    "flying_nimbus": ("outdoor_scene", "sky_space"),
    "stirrups_(riding)": ("accessories", "other_accessory"),
    "spinning_top": ("transport_play", "toys"),
    "riding_outfit": ("clothes_special", "themed_costume"),
    "dance_studio": ("indoor_scene", "public_indoor"),
    "skating_rink": ("indoor_scene", "public_indoor"),
    "falling_star": ("outdoor_scene", "sky_space"),
    "spinning_weapon": ("action", "combat_action"),
    "flying_type_theme_(pokemon)": ("style", "genre"),
    "gibson_flying_v": ("culture_objects", "music"),
    "flying_squirrel": ("creatures", "mammal"),
    "seikan_hikou": ("text_meta", "meta"),
    "dancing_stars_on_me!": ("text_meta", "meta"),
    "aozora_jumping_heart": ("text_meta", "meta"),
    "fliegerhammer": ("weapons", "other_weapon"),
    "running_blades": ("mech_scifi", "cybernetic"),
    "heart-shaped_innertube": ("transport_play", "sports"),
    "flight_stick": ("culture_objects", "phone_computer"),
    "spinning_wheel": ("household_objects", "tools"),
    "dildo_riding": ("adult", "adult_sex"),
    "belly_riding": ("adult", "adult_fetish"),
    "splattershot_(splatoon)": ("weapons", "firearm"),
    "splattershot_pro": ("weapons", "firearm"),
    "kickboard": ("transport_play", "sports"),
    "fighting_game": ("transport_play", "games"),
    "shooting_gallery": ("transport_play", "games"),
    "archery_shooting_glove": ("accessories", "handwear"),
    "punching_bag": ("transport_play", "sports"),
    "attack_helicopter": ("transport_play", "air_vehicle"),
    "combat_ship": ("transport_play", "water_vehicle"),
    "attack_ship": ("transport_play", "water_vehicle"),
    "f-16_fighting_falcon": ("transport_play", "air_vehicle"),
    "heart_attack": ("body", "body_state"),
    "shooting_range": ("indoor_scene", "public_indoor"),
    "kick_scooter": ("transport_play", "land_vehicle"),
    "fighting_type_theme_(pokemon)": ("style", "genre"),
    "fighting_my_way_(idolmaster)": ("text_meta", "meta"),
    "hacking": ("culture_objects", "phone_computer"),
    "pillow_hug": ("action", "holding"),
    "kiss_day": ("time_weather", "holiday"),
    "kiss_chart": ("text_meta", "meta"),
    "holding_hands_is_lewd": ("text_meta", "meme"),
    "force-feeding": ("action", "daily_action"),
    "drinking_straw": ("food_drink", "tableware"),
    "cooking_pot": ("household_objects", "container"),
    "shopping_cart": ("household_objects", "container"),
    "cleaning_rag": ("household_objects", "tools"),
    "shopping_basket": ("household_objects", "container"),
    "sleeping_bag": ("household_objects", "storage_furniture"),
    "cleaning_brush": ("household_objects", "tools"),
    "drinking_fountain": ("household_objects", "lighting_clock"),
    "cooking_oil": ("food_drink", "staple_food"),
    "mixer_(cooking)": ("household_objects", "lighting_clock"),
    "shopping_district": ("indoor_scene", "commercial"),
    "cleaning_&_clearing_(blue_archive)": ("themes", "social_relation"),
    "heavy_breathing": ("body", "body_state"),
    "stuck": ("body", "body_state"),
    "after_bathing": ("body", "body_state"),
    "mind_reading": ("themes", "narrative_situation"),
    "drinking_pee": ("adult", "adult_other"),
    "drinking_from_condom": ("adult", "adult_fetish"),
    "hentai-foundry_username": ("text_meta", "meta"),
    "have_to_pee": ("body", "body_state"),
})

EXACT_OVERRIDES.update({
    # Scene, architecture and composition audit.
    "lattice": ("indoor_scene", "architecture"),
    "bathroom_scale": ("household_objects", "tools"),
    "kitchen_scale": ("household_objects", "tools"),
    "kitchen_hood": ("household_objects", "lighting_clock"),
    "toilet_seat": ("household_objects", "other_object"),
    "in_bathtub": ("pose", "stationary_pose"),
    "on_toilet": ("pose", "stationary_pose"),
    "cave_interior": ("outdoor_scene", "mountain_desert"),
    "hotel_room": ("indoor_scene", "commercial"),
    "refrigerator_interior": ("household_objects", "lighting_clock"),
    "tent_interior": ("outdoor_scene", "other_scene"),
    "colored_shoe_interior": ("legwear_footwear", "shoes"),
    "cage_interior": ("household_objects", "other_object"),
    "pink_check_school_(idolmaster)": ("themes", "social_relation"),
    "arcade_cabinet": ("transport_play", "games"),
    "arcade_stick": ("transport_play", "games"),
    "store_clerk": ("people", "occupation"),
    "mindscape_cinema_(zenless_zone_zero)": ("text_meta", "screen_ui"),
    "cafe_maid_(love_live!)": ("clothes_special", "themed_costume"),
    "arcade_(architecture)": ("indoor_scene", "architecture"),
    "behind_bars": ("pose", "body_pose"),
    "pov_behind_bars": ("composition", "viewpoint"),
    "pov_doorway": ("composition", "viewpoint"),
    "human_tower": ("pose", "body_pose"),
    "body_bridge": ("pose", "body_pose"),
    "building_sand_sculpture": ("action", "daily_action"),
    "building_snowman": ("action", "daily_action"),
    "bridge_piercing": ("body", "body_marks"),
    "bikini_bridge": ("underwear_swim", "underwear_design"),
    "lungmen_dollar": ("household_objects", "other_object"),
    "cat_tower": ("household_objects", "storage_furniture"),
    "house_of_cards": ("transport_play", "games"),
    "doll_house": ("transport_play", "toys"),
    "model_building": ("transport_play", "toys"),
    "simon_shades": ("accessories", "eyewear"),
    "myouren_temple_clan_(touhou)": ("themes", "social_relation"),
    "palace_of_dragon_(idolmaster)": ("clothes_special", "themed_costume"),
    "guilty_gear_strive_x_tower_records": ("clothes_special", "themed_costume"),
    "bishamonten's_pagoda": ("weapons", "magic_weapon"),
    "kadomatsu": ("creatures", "plant"),
    "shrine_bell": ("household_objects", "lighting_clock"),
    "on_floor": ("pose", "body_pose"),
    "on_ground": ("pose", "body_pose"),
    "against_wall": ("pose", "body_pose"),
    "through_wall": ("pose", "body_pose"),
    "hands_on_ground": ("pose", "body_pose"),
    "hand_on_ground": ("pose", "body_pose"),
    "hands_on_floor": ("pose", "body_pose"),
    "hand_on_floor": ("pose", "body_pose"),
    "hand_on_wall": ("pose", "body_pose"),
    "on_wall": ("pose", "body_pose"),
    "sitting_on_wall": ("pose", "body_pose"),
    "foot_against_wall": ("pose", "body_pose"),
    "climbing_wall": ("pose", "body_pose"),
    "playing_tabletop_game": ("action", "daily_action"),
    "ground_vehicle": ("transport_play", "land_vehicle"),
    "tactical_surface_fighter": ("mech_scifi", "mecha"),
    "ceiling_fan": ("household_objects", "lighting_clock"),
    "wall_lamp": ("household_objects", "lighting_clock"),
    "floor_lamp": ("household_objects", "lighting_clock"),
    "wall_clock": ("household_objects", "lighting_clock"),
    "wall_shelf": ("household_objects", "storage_furniture"),
    "drawing_on_fourth_wall": ("text_meta", "meme"),
    "against_fourth_wall": ("text_meta", "meme"),
    "glory_wall": ("adult", "adult_fetish"),
    "broken_glass": ("household_objects", "other_object"),
    "clothes_on_floor": ("clothing_detail", "clothing_state"),
    "wall-eyed": ("face", "eye_shape"),
    "ground_shatter": ("light_effect", "other_effect"),
    "writing_on_wall": ("text_meta", "text"),
    "phone_on_wall": ("culture_objects", "phone_computer"),
    "blood_on_ground": ("adult", "adult_gore"),
    "blood_on_wall": ("adult", "adult_gore"),
    "weapon_on_floor": ("weapons", "other_weapon"),
    "park_bench": ("household_objects", "seating_table"),
    "track_and_field": ("transport_play", "sports"),
    "jungle_gym": ("transport_play", "sports"),
    "field_radio": ("culture_objects", "camera_media"),
    "field_ration": ("food_drink", "staple_food"),
    "primrose_field_illusion": ("light_effect", "optical"),
    "garden_eel": ("creatures", "aquatic"),
    "desert_camouflage": ("clothing_detail", "clothing_pattern"),
    "bernese_mountain_dog": ("creatures", "mammal"),
    "desert_tech_mdr": ("weapons", "firearm"),
    "desert_voe_set_(zelda)": ("clothes_special", "themed_costume"),
    "sea_slug": ("creatures", "aquatic"),
    "sea_urchin": ("creatures", "aquatic"),
    "sea_turtle": ("creatures", "reptile"),
    "sea_lion": ("creatures", "mammal"),
    "sea_anemone": ("creatures", "aquatic"),
    "sea_cucumber": ("creatures", "aquatic"),
    "sea_angel": ("creatures", "aquatic"),
    "sea_slug_girl": ("people", "fantasy_person"),
    "sea_slug_ears": ("creatures", "animal_feature"),
    "ocean_sunfish": ("creatures", "aquatic"),
    "sea_serpent": ("creatures", "fantasy_creature"),
    "sea_monster": ("creatures", "fantasy_creature"),
    "pool_ladder": ("household_objects", "tools"),
    "beach_chair": ("household_objects", "seating_table"),
    "beach_mat": ("household_objects", "other_object"),
    "beach_umbrella": ("household_objects", "tools"),
    "partially_underwater_shot": ("composition", "camera_angle"),
    "pool_of_blood": ("adult", "adult_gore"),
    "saliva_pool": ("adult", "adult_fluid"),
    "cleaning_pool": ("action", "daily_action"),
    "twilight_(e.g.o)": ("legwear_footwear", "armor"),
    "dawnmaker_(honkai:_star_rail)": ("weapons", "magic_weapon"),
    "sunset_nostalgie_(idolmaster)": ("themes", "social_relation"),
    "calendar_(object)": ("household_objects", "other_object"),
    "calendar_(medium)": ("style", "medium"),
    "release_date": ("text_meta", "meta"),
    "date_pun": ("text_meta", "meme"),
    "inverse_spirit_(date_a_live)": ("themes", "persona_variant"),
    "top_of_moe_2020": ("text_meta", "meta"),
    "over_shoulder": ("action", "holding"),
    "igote": ("clothing_detail", "other_clothes"),
    "lens_eye": ("face", "eye_shape"),
    "wet_lens": ("light_effect", "optical"),
    "blur_censor": ("text_meta", "censorship"),
    "blurry_halo": ("light_effect", "magic_effect"),
    "art_program_in_frame": ("text_meta", "screen_ui"),
    "security_camera": ("culture_objects", "camera_media"),
    "purple_babydoll": ("underwear_swim", "bra_lingerie"),
    "red_babydoll": ("underwear_swim", "bra_lingerie"),
    "see-through_babydoll": ("underwear_swim", "bra_lingerie"),
    "see-through_bodystocking": ("underwear_swim", "bodysuit_leotard"),
    "see-through_silhouette": ("light_effect", "optical"),
    "atmospheric_perspective": ("style", "technique"),
    "bad_perspective": ("style", "quality"),
    "fisheye": ("light_effect", "optical"),
    "sideways": ("composition", "layout"),
    "upside-down": ("composition", "layout"),
    "zooming_out": ("composition", "focus"),
    "x-ray": ("style", "technique"),
    "sword_school_reunion_(touken_ranbu)": ("themes", "narrative_situation"),
    "fire_hydrant": ("household_objects", "tools"),
    "traffic_light": ("household_objects", "lighting_clock"),
    "traffic_mirror": ("household_objects", "other_object"),
    "street_snap": ("style", "photo_3d"),
    "urban_legend": ("themes", "narrative_situation"),
    "computer_tower": ("culture_objects", "phone_computer"),
    "gingerbread_house": ("food_drink", "dessert_snack"),
    "life_at_the_hakurei_shrine_(touhou)": ("themes", "narrative_situation"),
    "pyramid_(geometry)": ("text_meta", "symbol"),
    "sand_castle": ("transport_play", "toys"),
    "under_bridge": ("outdoor_scene", "other_scene"),
    "tombstone": ("household_objects", "other_object"),
    "breaking_through_wall": ("action", "movement"),
    "through_ground": ("action", "movement"),
    "japan_ground_self-defense_force": ("themes", "social_relation"),
    "people's_liberation_army_ground_force": ("themes", "social_relation"),
    "russian_ground_forces": ("themes", "social_relation"),
    "ukrainian_ground_forces": ("themes", "social_relation"),
    "window_fog": ("light_effect", "optical"),
    "toilet": ("household_objects", "other_object"),
    "bathtub": ("household_objects", "other_object"),
    "empty_bathtub": ("household_objects", "other_object"),
    "wooden_bathtub": ("household_objects", "other_object"),
    "ofuro": ("household_objects", "other_object"),
})

EXACT_OVERRIDES.update({
    # Lighting/effects/style and text-meta qualifier collisions.
    "fox_shadow_puppet": ("pose", "hand_gesture"),
    "double_fox_shadow_puppet": ("pose", "hand_gesture"),
    "dog_shadow_puppet": ("pose", "hand_gesture"),
    "shadow_puppet": ("pose", "hand_gesture"),
    "shadow_hands": ("pose", "hand_gesture"),
    "lighting_cigarette": ("action", "daily_action"),
    "shadow_(persona)": ("creatures", "fantasy_creature"),
    "dark_cure_(yes!_precure_5)": ("themes", "persona_variant"),
    "living_shadow": ("creatures", "fantasy_creature"),
    "dark_orb_(madoka_magica)": ("light_effect", "magic_effect"),
    "moonlight_greatsword": ("weapons", "magic_weapon"),
    "ultra_beam": ("light_effect", "magic_effect"),
    "shadow_censor": ("text_meta", "censorship"),
    "bonfire_(dark_souls)": ("light_effect", "fire_smoke"),
    "bonbori_(lighting)": ("household_objects", "lighting_clock"),
    "paint_palette": ("household_objects", "tools"),
    "makeup_palette": ("household_objects", "tools"),
    "colorful_festival_(project_sekai)": ("text_meta", "meta"),
    "palette_swap": ("themes", "persona_variant"),
    "vomiting_rainbows": ("action", "daily_action"),
    "racing_colors": ("clothes_special", "occupation_uniform"),
    "flame-tipped_tail": ("creatures", "animal_feature"),
    "flame_print": ("clothing_detail", "clothing_pattern"),
    "steam_censor": ("text_meta", "censorship"),
    "breathing_fire": ("action", "daily_action"),
    "blowing_smoke": ("action", "daily_action"),
    "steam_locomotive": ("transport_play", "land_vehicle"),
    "fire_truck": ("transport_play", "land_vehicle"),
    "fire_extinguisher": ("household_objects", "tools"),
    "smoke_grenade": ("weapons", "explosive"),
    "dancer_(fire_emblem:_three_houses)": ("people", "occupation"),
    "fire_elemental": ("creatures", "fantasy_creature"),
    "fire_hydrant": ("household_objects", "tools"),
    "fire_flower": ("creatures", "plant"),
    "burning_clothes": ("clothing_detail", "clothing_state"),
    "wing_clan_(breath_of_fire)": ("themes", "social_relation"),
    "thirteen_flame-chasers_(honkai_impact)": ("themes", "social_relation"),
    "burning_love_(phrase)": ("text_meta", "text"),
    "fire_stone": ("household_objects", "other_object"),
    "sparkler": ("household_objects", "other_object"),
    "shiny_and_normal": ("themes", "persona_variant"),
    "glitter_makeup": ("face", "makeup"),
    "eye_glitter": ("face", "makeup"),
    "tinsel": ("accessories", "badges_ornaments"),
    "sparkle_facial_mark": ("body", "body_marks"),
    "plucking_petals": ("action", "daily_action"),
    "glitch_art": ("style", "art_style"),
    "distortion_(project_moon)": ("themes", "persona_variant"),
    "glitch_censor": ("text_meta", "censorship"),
    "restaurant": ("indoor_scene", "commercial"),
    "binaural_microphone": ("culture_objects", "camera_media"),
    "glowstick": ("culture_objects", "music"),
    "penlight_(glowstick)": ("culture_objects", "music"),
    "monster_energy": ("food_drink", "drink"),
    "energy_drink": ("food_drink", "drink"),
    "magical_boy": ("people", "fantasy_person"),
    "spartan_(halo)": ("people", "fantasy_person"),
    "holy_quintet": ("themes", "social_relation"),
    "afterglow_(bang_dream!)": ("themes", "social_relation"),
    "power_connection": ("themes", "character_connection"),
    "power_bottom": ("adult", "adult_other"),
    "power_item_(touhou)": ("transport_play", "games"),
    "energy_tank": ("transport_play", "games"),
    "power_fist": ("weapons", "magic_weapon"),
    "power_strip": ("household_objects", "tools"),
    "power_drill": ("household_objects", "tools"),
    "power_tool": ("household_objects", "tools"),
    "power_cord": ("household_objects", "tools"),
    "familiar_(madoka_magica)": ("creatures", "fantasy_creature"),
    "doppel_(madoka_magica)": ("themes", "persona_variant"),
    "unison_(nanoha)": ("themes", "persona_variant"),
    "energy_(pokemon_tcg)": ("transport_play", "games"),
    "luminous_(madoka_magica)": ("culture_objects", "music"),
    "power_armor_(fallout)": ("legwear_footwear", "armor"),
    "halo_ornament": ("accessories", "badges_ornaments"),
    "power_level": ("text_meta", "screen_ui"),
    "unconventional_sound_effect": ("text_meta", "comic"),
    "status_effect": ("text_meta", "screen_ui"),
    "red-eye_effect": ("light_effect", "optical"),
    "spill": ("action", "daily_action"),
    "spilling": ("action", "daily_action"),
    "pastel_colors": ("light_effect", "palette"),
    "ink_tank_(splatoon)": ("weapons", "other_weapon"),
    "ink_stamp": ("culture_objects", "stationery"),
    "acrylic_stand_(object)": ("transport_play", "toys"),
    "suisai_sekai": ("culture_objects", "music"),
    "shading_eyes": ("pose", "hand_gesture"),
    "sketchbook": ("culture_objects", "stationery"),
    "maruman_sketchbook": ("culture_objects", "stationery"),
    "sketching": ("action", "daily_action"),
    "sketch_background": ("outdoor_scene", "background_pattern"),
    "cover_sketch": ("text_meta", "meta"),
    "western_dragon": ("creatures", "fantasy_creature"),
    "cowgirl_(western)": ("people", "occupation"),
    "sheriff_(western)": ("people", "occupation"),
    "samurai_jacket_(cyberpunk)": ("clothes_special", "themed_costume"),
    "black_gothic_dress_(idolmaster)": ("clothes_special", "themed_costume"),
    "gothic_princess_(idolmaster)": ("clothes_special", "themed_costume"),
    "gothic_architecture": ("indoor_scene", "architecture"),
    "hololive_fantasy": ("themes", "social_relation"),
    "historical_name_connection": ("themes", "character_connection"),
    "historical_connection": ("themes", "character_connection"),
    "historical_event": ("themes", "narrative_situation"),
    "vintage_microphone": ("culture_objects", "music"),
    "retronia_(fate)": ("themes", "persona_variant"),
    "wallpaper_(object)": ("household_objects", "other_object"),
    "photo_(object)": ("culture_objects", "camera_media"),
    "photo_album": ("culture_objects", "camera_media"),
    "photo_shoot": ("action", "daily_action"),
    "photographer": ("people", "occupation"),
    "idle_animation": ("style", "photo_3d"),
    "photo_booth": ("indoor_scene", "commercial"),
    "pastel_palettes_(bang_dream!)": ("themes", "social_relation"),
    "ink_on_face": ("body", "body_marks"),
    "pencil_case": ("household_objects", "container"),
    "pencil_mustache": ("face", "facial_hair"),
    "hatching": ("action", "daily_action"),
    "sketch_inset": ("composition", "layout"),
    "chibi_inset": ("composition", "layout"),
    "punkish_gothic_(idolmaster)": ("clothes_special", "themed_costume"),
    "animation_paper": ("style", "medium"),
    "deku's_photo_of_hagakure_toru": ("culture_objects", "camera_media"),
    "sakura_photograph_(idolmaster)": ("text_meta", "meta"),
    "shadow_(shadows_house)": ("people", "fantasy_person"),
    "flare": ("weapons", "explosive"),
    "contrast_(idolmaster)": ("culture_objects", "music"),
    "colorful_background": ("outdoor_scene", "background_pattern"),
    "colorful_clouds": ("outdoor_scene", "sky_space"),
    "colorful_cloudy_sky": ("outdoor_scene", "sky_space"),
    "playing_card_theme": ("style", "genre"),
    "poke_ball_theme": ("style", "genre"),
    "color_guide": ("text_meta", "meta"),
    "4th_match_flame_(e.g.o)": ("legwear_footwear", "armor"),
    "under_fire": ("action", "combat_action"),
    "particle_cannon_case": ("weapons", "firearm"),
    "sparkle_background": ("outdoor_scene", "background_pattern"),
    "sparkle_print": ("clothing_detail", "clothing_pattern"),
    "squirting_liquid": ("action", "daily_action"),
    "distortion": ("style", "technique"),
    "motion_lines": ("text_meta", "comic"),
    "speed_lines": ("text_meta", "comic"),
    "static": ("text_meta", "screen_ui"),
    "sunburst": ("outdoor_scene", "background_pattern"),
    "energy_drain": ("action", "combat_action"),
    "summoning": ("action", "daily_action"),
    "standing_on_magic_circle": ("pose", "body_pose"),
    "on_magic_circle": ("pose", "body_pose"),
    "stand_(jojo)": ("creatures", "fantasy_creature"),
    "unlimited_blade_works_(reality_marble)": ("outdoor_scene", "other_scene"),
    "fake_halo": ("accessories", "headwear"),
    "mechanical_halo": ("accessories", "headwear"),
    "ring_of_light_(blue_archive)": ("accessories", "headwear"),
})

EXACT_OVERRIDES.update({
    "text_messaging": ("action", "daily_action"),
    "sign_language": ("pose", "hand_gesture"),
    "juumonji_yari": ("weapons", "polearm"),
    "letter_balloon": ("household_objects", "other_object"),
    "incoming_letter": ("action", "daily_action"),
    "speech_stab": ("text_meta", "comic"),
    "falchion_(fire_emblem)": ("weapons", "blade"),
    "yato_(fire_emblem)": ("weapons", "blade"),
    "tyrfing_(fire_emblem)": ("weapons", "blade"),
    "areadbhar_(fire_emblem)": ("weapons", "polearm"),
    "aymr_(fire_emblem)": ("weapons", "blade"),
    "laguz_(fire_emblem)": ("people", "fantasy_person"),
    "golden_deer_(fire_emblem)": ("themes", "social_relation"),
    "training_wear_(fire_emblem)": ("clothes_special", "themed_costume"),
    "training_outfit_(fire_emblem)": ("clothes_special", "themed_costume"),
    "sage_outfit_(fire_emblem)": ("clothes_special", "themed_costume"),
    "pareo_swimsuit_(fire_emblem)": ("underwear_swim", "swimsuit"),
    "dark_mage_(fire_emblem)": ("people", "occupation"),
    "emblem_(fire_emblem_engage)": ("accessories", "jewelry"),
    "ok_sign": ("pose", "hand_gesture"),
    "shaka_sign": ("pose", "hand_gesture"),
    "double_ok_sign": ("pose", "hand_gesture"),
    "fig_sign": ("pose", "hand_gesture"),
    "power_symbol-shaped_pupils": ("face", "eye_shape"),
    "diamond_in_eye": ("face", "eye_shape"),
    "cross_in_eye": ("face", "eye_shape"),
    "cross-laced_corset": ("clothing_detail", "clothing_structure"),
    "barcode_scanner": ("culture_objects", "phone_computer"),
    "cross_pendant": ("accessories", "jewelry"),
    "american_flag_neckwear": ("accessories", "neckwear"),
    "flag_patch": ("accessories", "badges_ornaments"),
    "head_flag": ("accessories", "headwear"),
    "wet_floor_sign": ("household_objects", "other_object"),
    "operation_crossroads": ("themes", "narrative_situation"),
    "solar_panel": ("mech_scifi", "machine"),
    "paneled_background": ("outdoor_scene", "background_pattern"),
    "comically_large_ears": ("face", "ears"),
    "bubble_filter": ("text_meta", "censorship"),
    "speech_bubble_censor": ("text_meta", "censorship"),
    "heart_bubbles": ("light_effect", "particles"),
    "western_comics_(style)": ("style", "art_style"),
    "screen": ("culture_objects", "camera_media"),
    "cracked_screen": ("culture_objects", "phone_computer"),
    "broken_screen": ("culture_objects", "phone_computer"),
    "window_shutter": ("indoor_scene", "architecture"),
    "screen_zoom": ("composition", "focus"),
    "interface_censor": ("text_meta", "censorship"),
    "mosaic_art": ("style", "technique"),
    "signing": ("action", "daily_action"),
    "step_and_repeat": ("outdoor_scene", "background_pattern"),
    "reference_sheet": ("composition", "layout"),
    "reference_inset": ("text_meta", "meta"),
    "real_life_insert": ("text_meta", "meta"),
    "alternate_costume": ("themes", "persona_variant"),
    "official_alternate_costume": ("themes", "persona_variant"),
    "alternate_hairstyle": ("themes", "persona_variant"),
    "official_alternate_hairstyle": ("themes", "persona_variant"),
    "personification": ("themes", "identity_change"),
    "creature_and_personification": ("themes", "identity_change"),
    "object_and_personification": ("themes", "identity_change"),
    "vehicle_and_personification": ("themes", "identity_change"),
    "crossover": ("themes", "narrative_situation"),
    "in-franchise_crossover": ("themes", "narrative_situation"),
    "multiple_crossover": ("themes", "narrative_situation"),
    "east-west_crossover": ("themes", "narrative_situation"),
    "role_reversal": ("themes", "identity_change"),
    "sternritter": ("themes", "social_relation"),
    "intersection": ("indoor_scene", "urban"),
    "cross_(weapon)": ("weapons", "other_weapon"),
    "cross_calibur": ("weapons", "magic_weapon"),
    "cross_punisher": ("weapons", "other_weapon"),
    "crusader_(tank)": ("transport_play", "land_vehicle"),
    "triangle-shaped_hair": ("hair", "hair_style"),
    "crux_(constellation)": ("outdoor_scene", "sky_space"),
    "training_wear_(fire_emblem_engage)": ("clothes_special", "themed_costume"),
    "training_outfit_(fire_emblem_engage)": ("clothes_special", "themed_costume"),
    "sage_outfit_(fire_emblem_engage)": ("clothes_special", "themed_costume"),
    "dark_mage_(fire_emblem_awakening)": ("people", "occupation"),
    "cross_calibur_(fate)": ("weapons", "magic_weapon"),
    "abstract": ("style", "art_style"),
    "granblue_fantasy_(style)": ("style", "art_style"),
})

EXACT_OVERRIDES.update({
    # Clothing/accessory/object heads.
    "bismarck_(coat_of_arms)": ("text_meta", "symbol"),
    "coat_of_arms": ("text_meta", "symbol"),
    "coat_rack": ("household_objects", "storage_furniture"),
    "record_jacket": ("culture_objects", "music"),
    "feather_boa": ("accessories", "neckwear"),
    "bulletproof_vest": ("legwear_footwear", "armor"),
    "life_vest": ("legwear_footwear", "armor"),
    "load_bearing_vest": ("legwear_footwear", "armor"),
    "hospital_gown": ("clothes_special", "occupation_uniform"),
    "lab_coat": ("clothes_special", "occupation_uniform"),
    "firefighter_jacket": ("clothes_special", "occupation_uniform"),
    "military_coat": ("clothes_special", "occupation_uniform"),
    "military_jacket": ("clothes_special", "occupation_uniform"),
    "hazmat_suit": ("legwear_footwear", "helmet_protective"),
    "normal_suit_(gundam)": ("legwear_footwear", "helmet_protective"),
    "normal_suit_(metroid)": ("legwear_footwear", "helmet_protective"),
    "flight_suit": ("legwear_footwear", "helmet_protective"),
    "diving_suit": ("legwear_footwear", "helmet_protective"),
    "pilot_suit": ("legwear_footwear", "helmet_protective"),
    "racing_suit": ("legwear_footwear", "helmet_protective"),
    "power_suit": ("mech_scifi", "mecha"),
    "power_suit_(metroid)": ("mech_scifi", "mecha"),
    "mobile_armor": ("mech_scifi", "mecha"),
    "magitek_armor": ("mech_scifi", "mecha"),
    "gimp_suit": ("adult", "adult_fetish"),
    "onesie": ("clothes_special", "sleep_casual"),
    "spandex": ("clothing_detail", "clothing_material"),
    "nice_knee_socks_day": ("time_weather", "holiday"),
    "tights_day": ("time_weather", "holiday"),
    "glasses_day": ("time_weather", "holiday"),
    "christmas_stocking": ("household_objects", "other_object"),
    "barefoot": ("body", "body_state"),
    "barefoot_sandals_(jewelry)": ("accessories", "jewelry"),
    "getabako": ("household_objects", "storage_furniture"),
    "sushi_geta": ("food_drink", "tableware"),
    "shoejob": ("adult", "adult_sex"),
    "type_91_armor-piercing_shell": ("weapons", "firearm"),
    "cotton_ball": ("household_objects", "tools"),
    "cotton_swab": ("household_objects", "tools"),
    "transparent_hand": ("body", "arms_hands_feet"),
    "transparent_ball": ("transport_play", "sports"),
    "transparent_innertube": ("transport_play", "sports"),
    "transparent_seat": ("household_objects", "seating_table"),
    "transparent_umbrella": ("household_objects", "tools"),
    "transparent_weapon": ("weapons", "other_weapon"),
    "transparent_censoring": ("text_meta", "censorship"),
    "button_prompt": ("text_meta", "screen_ui"),
    "fake_play_button": ("text_meta", "screen_ui"),
    "pause_button": ("text_meta", "screen_ui"),
    "play_button": ("text_meta", "screen_ui"),
    "push-button": ("text_meta", "screen_ui"),
    "book_strap": ("culture_objects", "books_paper"),
    "guitar_strap": ("culture_objects", "music"),
    "pocket_watch": ("accessories", "jewelry"),
    "collar_chain_(jewelry)": ("accessories", "jewelry"),
    "collar_jewel": ("accessories", "jewelry"),
    "pendant_collar": ("accessories", "jewelry"),
    "strap-on": ("adult", "adult_fetish"),
    "dental_gag": ("adult", "adult_fetish"),
    "chastity_cage_strap": ("adult", "adult_fetish"),
    "condom_thigh_strap": ("adult", "adult_fetish"),
    "vibrator_in_thigh_strap": ("adult", "adult_fetish"),
    "hairdressing": ("hair", "hair_action"),
    "stripper": ("people", "occupation"),
    "clitoral_hood": ("adult", "adult_anatomy"),
    "open_car_hood": ("transport_play", "land_vehicle"),
    "parka": ("clothes_main", "outerwear"),
    "bottle_cap": ("household_objects", "container"),
    "drawn_crown": ("text_meta", "symbol"),
    "straw_hats_jolly_roger": ("text_meta", "symbol"),
    "boxing_ring": ("transport_play", "sports"),
    "wrestling_ring": ("transport_play", "sports"),
    "pon_de_ring": ("food_drink", "dessert_snack"),
    "planetary_ring": ("outdoor_scene", "sky_space"),
    "jewelpet_(creature)": ("creatures", "fantasy_creature"),
    "jewelry_box": ("household_objects", "container"),
    "cable_tie": ("household_objects", "tools"),
    "cuff_links": ("accessories", "jewelry"),
    "unit_patch": ("accessories", "badges_ornaments"),
    "bean_bag_chair": ("household_objects", "seating_table"),
    "bag_of_chips": ("food_drink", "dessert_snack"),
    "conveyor_belt": ("mech_scifi", "machine"),
    "jetpack": ("mech_scifi", "scifi_device"),
    "rider_belt": ("mech_scifi", "scifi_device"),
    "blood_bag": ("household_objects", "container"),
    "body_bag": ("household_objects", "container"),
    "trash_bag": ("household_objects", "container"),
    "pastry_bag": ("household_objects", "container"),
    "compound_bow": ("weapons", "bow"),
    "drawing_bow": ("action", "combat_action"),
    "ribbon_baton": ("transport_play", "sports"),
    "red_ribbon_army": ("themes", "social_relation"),
})

EXACT_OVERRIDES.update({
    # Weapon names and short multi-meaning object words.
    "palette_knife": ("culture_objects", "stationery"),
    "nail_gun": ("household_objects", "tools"),
    "sword_print": ("clothing_detail", "clothing_pattern"),
    "blade_lineage_(identity)": ("themes", "persona_variant"),
    "unlimited_blade_works_(reality_marble)": ("light_effect", "magic_effect"),
    "after-school_sweets_club": ("themes", "social_relation"),
    "make-up_work_club": ("themes", "social_relation"),
    "ninjutsu_research_club": ("themes", "social_relation"),
    "chaos_(warhammer)": ("themes", "social_relation"),
    "imperium_of_man_(warhammer)": ("themes", "social_relation"),
    "inquisition_(warhammer)": ("themes", "social_relation"),
    "ultramarines_(warhammer)": ("themes", "social_relation"),
    "golf_club": ("transport_play", "sports"),
    "juggling_club": ("transport_play", "toys"),
    "toy_hammer": ("transport_play", "toys"),
    "bubble_wand": ("transport_play", "toys"),
    "hammer_and_sickle": ("text_meta", "symbol"),
    "whip_marks": ("body", "body_marks"),
    "rocket_ship": ("transport_play", "air_vehicle"),
    "team_rainbow_rocket": ("themes", "social_relation"),
    "wandenreich": ("themes", "social_relation"),
    "missile_trail": ("light_effect", "fire_smoke"),
    "face_shield": ("legwear_footwear", "helmet_protective"),
    "traffic_barrier": ("indoor_scene", "urban"),
    "weapon_name": ("text_meta", "text"),
    "weapon_case": ("household_objects", "container"),
    "weapon_tassel": ("accessories", "badges_ornaments"),
    "jian": ("weapons", "blade"),
    "tachi": ("weapons", "blade"),
    "kama": ("weapons", "blade"),
    "sai": ("weapons", "blade"),
    "stiletto": ("weapons", "blade"),
    "pike": ("weapons", "polearm"),
    "chui": ("weapons", "polearm"),
    "ball_and_chain": ("weapons", "polearm"),
    "rpg": ("weapons", "explosive"),
    "mortar": ("weapons", "explosive"),
    "nuclear_weapon": ("weapons", "explosive"),
    "magazine_(weapon)": ("weapons", "firearm"),
    "clip_(weapon)": ("weapons", "firearm"),
    "slingshot": ("weapons", "bow"),
})

EXACT_OVERRIDES.update({
    # Food and utensils versus colors, props and actions.
    "orange_(fruit)": ("food_drink", "fruit_vegetable"),
    "orange_slice": ("food_drink", "fruit_vegetable"),
    "orange_peel": ("food_drink", "fruit_vegetable"),
    "orange_juice": ("food_drink", "drink"),
    "rice_(plant)": ("creatures", "plant"),
    "rice_planting": ("action", "daily_action"),
    "bread_eating_race": ("action", "daily_action"),
    "rice_shower_(umamusume)_(cosplay)": ("text_meta", "cosplay"),
    "food-themed_pillow": ("household_objects", "storage_furniture"),
    "carrot-shaped_pillow": ("household_objects", "storage_furniture"),
    "food_name": ("text_meta", "text"),
    "food_packaging": ("household_objects", "container"),
    "food_wrapper": ("household_objects", "container"),
    "pizza_box": ("household_objects", "container"),
    "food_stand": ("indoor_scene", "commercial"),
    "food_truck": ("transport_play", "land_vehicle"),
    "pizza_cutter": ("household_objects", "tools"),
    "soup_ladle": ("food_drink", "tableware"),
    "egg_implantation": ("body", "body_state"),
    "egg_laying": ("body", "body_state"),
    "pokemon_egg": ("creatures", "other_creature"),
    "yoshi_egg": ("creatures", "other_creature"),
    "egg_carton": ("household_objects", "container"),
    "good_meat_day": ("time_weather", "holiday"),
    "meat_day": ("time_weather", "holiday"),
    "nissin_cup_noodle_seafood": ("food_drink", "staple_food"),
    "cheese": ("food_drink", "staple_food"),
    "cake_print": ("clothing_detail", "clothing_pattern"),
    "chocolate_print": ("clothing_detail", "clothing_pattern"),
    "donut_print": ("clothing_detail", "clothing_pattern"),
    "cake_stand": ("food_drink", "tableware"),
    "parfait_glass": ("food_drink", "tableware"),
    "ice_cream_scoop_(utensil)": ("food_drink", "tableware"),
    "candy_jar": ("household_objects", "container"),
    "cookie_jar": ("household_objects", "container"),
    "candy_store": ("indoor_scene", "commercial"),
    "cookie_cutter": ("household_objects", "tools"),
    "donut_innertube": ("transport_play", "sports"),
    "chocolate_milk": ("food_drink", "drink"),
    "hot_chocolate": ("food_drink", "drink"),
    "choco_girl": ("people", "fantasy_person"),
    "coffee_table": ("household_objects", "seating_table"),
    "molotov_cocktail": ("weapons", "explosive"),
    "ho-kago_tea_time": ("themes", "social_relation"),
    "tea_party_(blue_archive)": ("themes", "social_relation"),
    "tea_party": ("themes", "narrative_situation"),
    "water_balloon": ("transport_play", "toys"),
    "water_yoyo": ("transport_play", "toys"),
    "water_boiler": ("household_objects", "lighting_clock"),
    "water_cooler": ("household_objects", "lighting_clock"),
    "water_wheel": ("mech_scifi", "machine"),
    "water_tank": ("household_objects", "container"),
    "water_censor": ("text_meta", "censorship"),
    "water_elemental": ("creatures", "fantasy_creature"),
    "water_fight": ("action", "interaction"),
    "water_slide": ("transport_play", "sports"),
    "water_type_theme_(pokemon)": ("style", "genre"),
    "bowl_cut": ("hair", "hair_style"),
    "bust_cup": ("body", "chest"),
    "cup_size": ("body", "chest"),
    "license_plate": ("text_meta", "symbol"),
    "suction_cup_dildo": ("adult", "adult_fetish"),
    "utensil_rack": ("household_objects", "storage_furniture"),

    # Electronics, print and music.
    "mixing_console": ("culture_objects", "music"),
    "stone_tablet": ("culture_objects", "books_paper"),
    "phone_number": ("text_meta", "text"),
    "phone_booth": ("indoor_scene", "urban"),
    "camera_feed": ("composition", "viewpoint"),
    "recording_studio": ("indoor_scene", "public_indoor"),
    "radio_booth": ("indoor_scene", "public_indoor"),
    "static": ("text_meta", "screen_ui"),
    "livestream": ("text_meta", "meta"),
    "tv_show": ("text_meta", "meta"),
    "drum_magazine": ("weapons", "firearm"),
    "dual_drum_magazine": ("weapons", "firearm"),
    "extended_magazine": ("weapons", "firearm"),
    "librarian": ("people", "occupation"),
    "secretary": ("people", "occupation"),
    "bookstore": ("indoor_scene", "commercial"),
    "calligraphy": ("text_meta", "text"),
    "cursive": ("text_meta", "text"),
    "seal_script": ("text_meta", "text"),
    "chalkboard": ("household_objects", "other_object"),
    "staple": ("culture_objects", "stationery"),
    "stapler": ("culture_objects", "stationery"),
    "oil-paper_umbrella": ("household_objects", "tools"),
    "paper_towel": ("household_objects", "tools"),
    "toilet_paper": ("household_objects", "tools"),
    "brush_stroke": ("style", "technique"),
    "nail_polish_brush": ("household_objects", "tools"),
    "trim_brush": ("household_objects", "tools"),
    "paintbrush_rack": ("household_objects", "storage_furniture"),
    "champagne_flute": ("food_drink", "tableware"),
    "trumpet_creeper": ("creatures", "plant"),
    "drum_(container)": ("household_objects", "container"),
    "music_stand": ("household_objects", "seating_table"),
    "piano_bench": ("household_objects", "seating_table"),
    "sheet_music": ("culture_objects", "books_paper"),
    "musical_staff": ("text_meta", "symbol"),
    "weaponized_instrument": ("weapons", "other_weapon"),
    "love_guitar_rod": ("weapons", "other_weapon"),
})

EXACT_OVERRIDES.update({
    "bench_press": ("action", "movement"),
    "bedwetting": ("body", "body_state"),
    "table_of_contents": ("culture_objects", "books_paper"),
    "rear-view_mirror": ("transport_play", "land_vehicle"),
    "side-view_mirror": ("transport_play", "land_vehicle"),
    "traffic_mirror": ("household_objects", "other_object"),
    "mirror_image": ("composition", "layout"),
    "through_mirror": ("composition", "layout"),
    "dandelion_clock": ("creatures", "plant"),
    "oven_mitts": ("accessories", "handwear"),
    "sky_lantern": ("time_weather", "holiday"),
    "joint_lock": ("action", "combat_action"),
    "leg_lock": ("action", "combat_action"),
    "key_frame": ("text_meta", "meta"),
    "kingdom_key": ("weapons", "magic_weapon"),
    "box_truck": ("transport_play", "land_vehicle"),
    "dialogue_box": ("text_meta", "comic"),
    "box_art": ("text_meta", "meta"),
    "fake_box_art": ("text_meta", "meta"),
    "box_body": ("body", "build"),
    "full-package_futanari": ("adult", "adult_anatomy"),
    "jack-in-the-box": ("transport_play", "toys"),
    "karaoke_box": ("indoor_scene", "commercial"),
    "beyblade": ("transport_play", "toys"),
    "american_football_(object)": ("transport_play", "sports"),
    "portal": ("light_effect", "magic_effect"),
    "snowman": ("time_weather", "holiday"),
    "sticker": ("text_meta", "symbol"),
    "external_fuel_tank": ("household_objects", "container"),
    "oxygen_tank": ("household_objects", "container"),
    "propane_tank": ("household_objects", "container"),
    "scuba_tank": ("household_objects", "container"),
    "stasis_tank": ("mech_scifi", "scifi_device"),
    "tank_shell": ("weapons", "firearm"),
    "unmanned_aerial_vehicle": ("transport_play", "air_vehicle"),
    "train_(clothing)": ("clothing_detail", "clothing_structure"),
    "bus_stop_shelter": ("indoor_scene", "urban"),
    "aircraft_carrier": ("transport_play", "water_vehicle"),
    "jet_ski": ("transport_play", "water_vehicle"),
    "living_fleshlight": ("adult", "adult_fetish"),
    "crystal_ball": ("mech_scifi", "scifi_device"),
    "occult_ball": ("light_effect", "magic_effect"),
    "disco_ball": ("household_objects", "lighting_clock"),
    "yarn_ball": ("household_objects", "other_object"),
    "bat_signal": ("text_meta", "symbol"),
    "spiked_ball_and_chain": ("weapons", "polearm"),
    "spiked_bat": ("weapons", "polearm"),
    "steel_ball_(jojo)": ("weapons", "other_weapon"),
    "game_over": ("text_meta", "screen_ui"),
    "game_show": ("culture_objects", "camera_media"),
    "strip_game": ("adult", "adult_suggestive"),
    "strip_mahjong": ("adult", "adult_suggestive"),
    "twitter_strip_game": ("adult", "adult_suggestive"),
    "video_game_cover": ("culture_objects", "books_paper"),
    "animatronic": ("mech_scifi", "robot_android"),
    "dollhouse_view": ("composition", "viewpoint"),
    "swing": ("outdoor_scene", "other_scene"),

    # Creature-themed objects and franchise names.
    "corn_dog": ("food_drink", "staple_food"),
    "hot_dog": ("food_drink", "staple_food"),
    "gummy_bear": ("food_drink", "dessert_snack"),
    "bucket_of_chicken": ("food_drink", "meat_seafood"),
    "chicken_nuggets": ("food_drink", "meat_seafood"),
    "fried_chicken": ("food_drink", "meat_seafood"),
    "shrimp_tempura": ("food_drink", "meat_seafood"),
    "canned_fish": ("food_drink", "meat_seafood"),
    "grilled_fish": ("food_drink", "meat_seafood"),
    "tiger_i": ("transport_play", "land_vehicle"),
    "tiger_ii": ("transport_play", "land_vehicle"),
    "f-15_eagle": ("transport_play", "air_vehicle"),
    "volkswagen_beetle": ("transport_play", "land_vehicle"),
    "cz_scorpion_evo_3": ("weapons", "firearm"),
    "heat_hawk": ("weapons", "blade"),
    "butterfly_swords": ("weapons", "blade"),
    "wolf's_gravestone": ("weapons", "magic_weapon"),
    "bird_of_paradise_flower": ("creatures", "plant"),
    "tiger_lily": ("creatures", "plant"),
    "spider_lily": ("creatures", "plant"),
    "white_spider_lily": ("creatures", "plant"),
    "penguin_logistics": ("themes", "social_relation"),
    "fox_platoon": ("themes", "social_relation"),
    "rabbit_platoon": ("themes", "social_relation"),
    "rabbit_youkai_group": ("themes", "social_relation"),
    "ikea_shark": ("transport_play", "toys"),
    "fish_tank": ("household_objects", "container"),
    "whale_tail_(clothing)": ("clothing_detail", "clothing_structure"),
    "jellyfish_cut": ("hair", "hair_style"),
    "fish-shaped_pupils": ("face", "eye_shape"),
    "butterfly-shaped_pupils": ("face", "eye_shape"),
    "rabbit-shaped_pupils": ("face", "eye_shape"),
    "bug_spray": ("household_objects", "tools"),
    "butterfly_net": ("household_objects", "tools"),
    "bug_bite": ("body", "body_marks"),
    "angel_trumpet": ("creatures", "plant"),
    "monstera": ("creatures", "plant"),
    "angel_statue": ("household_objects", "other_object"),
    "angelfish": ("creatures", "aquatic"),
    "demon_core": ("mech_scifi", "scifi_device"),
    "dragon_dildo": ("adult", "adult_fetish"),
    "dragon_fruit": ("food_drink", "fruit_vegetable"),
    "evangelion_(mecha)": ("mech_scifi", "mecha"),
    "fairy_(girls_frontline)": ("mech_scifi", "robot_android"),
    "robot_dragon": ("mech_scifi", "robot_android"),
    "mushroom_cloud": ("light_effect", "fire_smoke"),
    "slime_censor": ("text_meta", "censorship"),
    "year_of_the_dragon": ("time_weather", "holiday"),
    "compass_rose": ("text_meta", "symbol"),
    "crescent_rose": ("weapons", "blade"),
    "bamboo_broom": ("household_objects", "tools"),
    "bamboo_fence": ("indoor_scene", "architecture"),
    "super_leaf": ("transport_play", "toys"),
    "super_mushroom": ("transport_play", "toys"),
    "vine_whip": ("weapons", "polearm"),

    # Mechanical categories.
    "metal_gear_(robot)": ("mech_scifi", "mecha"),
    "super_robot": ("mech_scifi", "mecha"),
    "robot_joints": ("mech_scifi", "cybernetic"),
    "robotic_vacuum_cleaner": ("household_objects", "lighting_clock"),
    "sewing_machine": ("household_objects", "lighting_clock"),
    "washing_machine": ("household_objects", "lighting_clock"),
    "top-load_washing_machine": ("household_objects", "lighting_clock"),
    "vending_machine": ("household_objects", "lighting_clock"),
    "gumball_machine": ("household_objects", "lighting_clock"),
    "gunpla": ("transport_play", "toys"),
    "mecha_musume": ("people", "fantasy_person"),
    "mecha_danshi": ("people", "fantasy_person"),
    "kanohi": ("accessories", "eyewear"),
    "gear_fifth": ("themes", "persona_variant"),
    "exercise_machine": ("transport_play", "sports"),
    "ski_gear": ("transport_play", "sports"),
    "scuba_gear": ("legwear_footwear", "helmet_protective"),
    "slave_gear": ("adult", "adult_fetish"),
    "slot_machine": ("transport_play", "games"),
    "time_machine": ("mech_scifi", "scifi_device"),
    "three-dimensional_maneuver_gear": ("mech_scifi", "scifi_device"),
    "in_washing_machine": ("pose", "body_pose"),
    "at_field": ("light_effect", "magic_effect"),
    "field_of_blades": ("weapons", "magic_weapon"),
    "dock_(tail)": ("creatures", "animal_feature"),
    "pool_party_(league_of_legends)": ("clothes_special", "themed_costume"),
    "sea_spray": ("light_effect", "particles"),
    "falling_star": ("text_meta", "symbol"),
    "flying_nimbus": ("light_effect", "magic_effect"),
    "pegasus": ("creatures", "fantasy_creature"),
    "red_clouds": ("clothing_detail", "clothing_pattern"),
    "backpacking_stove": ("household_objects", "tools"),
    "tent_interior": ("indoor_scene", "public_indoor"),
    "birthday_sash": ("accessories", "bags_belts"),
    "christmas_lights": ("household_objects", "lighting_clock"),
    "christmas_ornaments": ("accessories", "badges_ornaments"),
    "christmas_present": ("household_objects", "container"),
    "christmas_star": ("accessories", "badges_ornaments"),
    "christmas_tree": ("creatures", "plant"),
    "christmas_wreath": ("accessories", "badges_ornaments"),
    "easter_egg": ("household_objects", "other_object"),
    "halloween_bucket": ("household_objects", "container"),
    "sky_lantern": ("household_objects", "lighting_clock"),
    "snowman": ("household_objects", "other_object"),
    "christmas_ornaments_in_hair": ("hair", "hair_accessory"),
    "christmas_tree_print": ("clothing_detail", "clothing_pattern"),
    "decorating_christmas_tree": ("action", "daily_action"),
    "happy_anniversary": ("text_meta", "text"),
    "happy_birthday": ("text_meta", "text"),
    "happy_easter": ("text_meta", "text"),
    "happy_halloween": ("text_meta", "text"),
    "happy_new_year": ("text_meta", "text"),
    "happy_valentine": ("text_meta", "text"),
    "happy_white_day": ("text_meta", "text"),
    "merry_christmas": ("text_meta", "text"),
    "trick_or_treat": ("text_meta", "text"),
    "christmas_nightmare_(e.g.o)": ("legwear_footwear", "armor"),
    "festival_jinbei": ("clothes_special", "themed_costume"),
    "sanbaka_anniversary_outfit": ("clothes_special", "themed_costume"),
    "bloom_festival_(project_sekai)": ("text_meta", "meta"),
    "birthday_connection": ("themes", "character_connection"),
})

# Last-wins consistency fixes where an older high-visibility override appeared
# earlier in the file.  Keeping this short block at the end makes precedence
# explicit and testable.
EXACT_OVERRIDES.update({
    "unlimited_blade_works_(reality_marble)": ("outdoor_scene", "other_scene"),
    "babydoll_hold": ("action", "holding"),
    "blacked_(phrase)": ("adult", "adult_fetish"),
    "number_four_(asl)": ("pose", "hand_gesture"),
    "letter": ("culture_objects", "books_paper"),
    "love_letter": ("culture_objects", "books_paper"),
    "placard": ("culture_objects", "books_paper"),
    "sand_writing": ("action", "daily_action"),
    "sexting": ("adult", "adult_other"),
    "?_block": ("transport_play", "games"),
    "american_flag_background": ("outdoor_scene", "background_pattern"),
    "flag_background": ("outdoor_scene", "background_pattern"),
    "star_symbol_background": ("outdoor_scene", "background_pattern"),
    "eye_print": ("clothing_detail", "clothing_pattern"),
    "iris_print": ("clothing_detail", "clothing_pattern"),
    "logo_print": ("clothing_detail", "clothing_pattern"),
    "japari_symbol_print": ("clothing_detail", "clothing_pattern"),
    "archon_mark": ("body", "body_marks"),
    "cutie_mark": ("body", "body_marks"),
    "bat_signal": ("light_effect", "lighting"),
    "death_flag": ("text_meta", "meme"),
    "watson_cross": ("pose", "body_pose"),
    "waving_flag": ("action", "holding"),
    "speech_stab": ("action", "interaction"),
    "phone_light": ("light_effect", "lighting"),
    "push-button": ("household_objects", "tools"),
    "anime_screenshot_inset": ("composition", "layout"),
    "game_screenshot_inset": ("composition", "layout"),
    "screenshot_inset": ("composition", "layout"),
    "aozora_jumping_heart": ("culture_objects", "music"),
    "dancing_stars_on_me!": ("culture_objects", "music"),
    "fighting_my_way_(idolmaster)": ("culture_objects", "music"),
    "seikan_hikou": ("culture_objects", "music"),
    "key_frame": ("style", "photo_3d"),
    "hair_lift": ("hair", "hair_action"),
    "pelvic_curtain_lift": ("clothing_detail", "clothing_state"),
    "bulge_lift": ("adult", "adult_suggestive"),
    "bandana_around_neck": ("accessories", "neckwear"),
    "hooded_shrug": ("clothes_main", "outerwear"),
    "no_headgear": ("clothing_detail", "clothing_state"),
    "ahoge_wag": ("hair", "hair_action"),
    "official_alternate_hair_color": ("themes", "persona_variant"),
    "hair_half_undone": ("hair", "hair_action"),
    "matching_hairstyle": ("themes", "character_connection"),
    "glaive_(polearm)": ("weapons", "polearm"),
    "nata_(tool)": ("household_objects", "tools"),
    "pencil_sharpener": ("household_objects", "tools"),
    "sword_clash": ("action", "combat_action"),
    "knife_in_head": ("adult", "adult_gore"),
    "skull_and_crossed_swords": ("text_meta", "symbol"),
    "imperium_of_man": ("relationships", "social_relation"),
    "ultramarines": ("relationships", "social_relation"),
    "after-school_sweets_club_(blue_archive)": ("relationships", "social_relation"),
    "make-up_work_club_(blue_archive)": ("relationships", "social_relation"),
    "ninjutsu_research_club_(blue_archive)": ("relationships", "social_relation"),
    "friendship_club_(princess_connect!)": ("relationships", "social_relation"),
    "cocked_hammer": ("weapons", "firearm"),
    "golden_egg_(splatoon)": ("recreation", "games"),
    "ice_cream_sandwich": ("food_drink", "dessert_snack"),
    "cracking_egg": ("action", "daily_action"),
    "suspicious_egg_dish": ("food_drink", "staple_food"),
    "shrine_bell": ("culture_objects", "music"),
    "drinking_fountain": ("household_objects", "appliance"),
    "doorbell": ("household_objects", "appliance"),
    "kitchen_hood": ("household_objects", "appliance"),
    "lantern_(e.g.o)": ("weapons", "other_weapon"),
    "lamp_(e.g.o)": ("weapons", "other_weapon"),
    "candle_on_head": ("accessories", "other_accessory"),
    "blowing_candle": ("action", "daily_action"),
    "mechanical_wings": ("mech_scifi", "cybernetic"),
    "energy_wings": ("light_effect", "magic_effect"),
    "crystal_wings": ("light_effect", "magic_effect"),
    "licking_paw": ("action", "interaction"),
    # Final compound-word collision audit.
    "computer_mouse": ("digital_media", "phone_computer"),
    "iphone": ("digital_media", "phone_computer"),
    "phone_with_ears": ("digital_media", "phone_computer"),
    "rabbit_ear_smartphone_case": ("digital_media", "phone_computer"),
    "animal_ear_headphones": ("digital_media", "camera_media"),
    "cat_ear_headphones": ("digital_media", "camera_media"),
    "in-ear_earphones": ("digital_media", "camera_media"),
    "detached_magazine_(weapon)": ("weapons", "firearm"),
    "see-through_magazine_(weapon)": ("weapons", "firearm"),
    "undersized_breast_cup": ("body", "chest"),
    "oversized_breast_cup": ("body", "chest"),
    "anemone_(flower)": ("nature", "plant"),
    "lotion_bottle": ("household_objects", "container"),
    "perfume_bottle": ("household_objects", "container"),
    "soap_bottle": ("household_objects", "container"),
    "shampoo_bottle": ("household_objects", "container"),
    "spray_bottle": ("household_objects", "container"),
    "nail_polish_bottle": ("household_objects", "container"),
    "pill_bottle": ("household_objects", "container"),
    "medicine_bottle": ("household_objects", "container"),
    "tank_(container)": ("household_objects", "container"),
    "wax_seal": ("accessories", "badges_ornaments"),
    "purity_seal": ("accessories", "badges_ornaments"),
    "piercing_hole": ("accessories", "jewelry"),
    "plug_(piercing)": ("accessories", "jewelry"),
    "snakebite_(piercing)": ("accessories", "jewelry"),
    "purple_babydoll": ("clothes_special", "sleep_casual"),
    "skirt_flip": ("clothing_detail", "clothing_state"),
    "skirt_caught_on_object": ("clothing_detail", "clothing_state"),
    "panty_lift": ("clothing_detail", "clothing_state"),
    "breast_curtain": ("clothes_special", "themed_costume"),
    "breast_curtains": ("clothes_special", "themed_costume"),
    "single_breast_curtain": ("clothes_special", "themed_costume"),
    "long_breast_curtain": ("clothes_special", "themed_costume"),
    "box_tie": ("adult", "adult_fetish"),
    "unicorn": ("creatures", "fantasy_creature"),
    "mimic_chest": ("creatures", "fantasy_creature"),
    "tactical_playboy_bunny": ("clothes_special", "themed_costume"),
    "grilled_eel": ("food_drink", "meat_seafood"),
    "my_dear_vampire_(idolmaster)": ("clothes_special", "themed_costume"),
    "slime_(substance)": ("adult", "adult_fetish"),
    "balloon_animal": ("recreation", "toys"),
    "crystal_ball": ("household_objects", "other_object"),
    "gem_(steven_universe)": ("people", "fantasy_person"),
    "sailor_senshi": ("relationships", "social_relation"),
    "the_sword_sharpened_with_tears_(e.g.o)": ("weapons", "magic_weapon"),
    "standing_restraints": ("adult", "adult_fetish"),
})


# High-frequency tags that reached the conservative alphabetical fallback even
# though their database descriptions make their meaning unambiguous.  This list
# is deliberately explicit: obscure franchise terms stay conservative, while
# visible everyday tags receive a precise home.
EXACT_OVERRIDES.update({
    "sweatdrop": ("expression", "fear_surprise"),
    "small_sweatdrop": ("expression", "fear_surprise"),
    "very_sweaty": ("body", "body_state"),
    "polka_dot": ("clothing_detail", "clothing_pattern"),
    "tiger_stripes": ("clothing_detail", "clothing_pattern"),
    "single_vertical_stripe": ("clothing_detail", "clothing_pattern"),
    "single_horizontal_stripe": ("clothing_detail", "clothing_pattern"),
    "single_stripe": ("clothing_detail", "clothing_pattern"),
    "calico_(pattern)": ("clothing_detail", "clothing_pattern"),
    "meandros": ("clothing_detail", "clothing_pattern"),
    "yagasuri": ("clothing_detail", "clothing_pattern"),
    "hair_over_shoulder": ("hair", "hair_action"),
    "hair_flaps": ("hair", "hair_style"),
    "hair_spread_out": ("hair", "hair_action"),
    "hair_down": ("hair", "hair_action"),
    "tentacle_hair": ("hair", "hair_style"),
    "hair_slicked_back": ("hair", "hair_style"),
    "hair_up": ("hair", "hair_style"),
    "big_hair": ("hair", "hair_style"),
    "hair_pulled_back": ("hair", "hair_style"),
    "parted_hair": ("hair", "hair_style"),
    "pointy_hair": ("hair", "hair_style"),
    "fiery_hair": ("hair", "hair_style"),
    "fluffy_hair": ("hair", "hair_style"),
    "hair_on_horn": ("hair", "hair_action"),
    "prehensile_hair": ("hair", "hair_style"),
    "blood_in_hair": ("hair", "hair_action"),
    "lone_nape_hair": ("hair", "hair_style"),
    "side_drill": ("hair", "hair_style"),
    "snake_hair": ("hair", "hair_style"),
    "alternate_hair_color": ("themes", "persona_variant"),
    "alternate_hair_length": ("themes", "persona_variant"),
    "official_alternate_hair_length": ("themes", "persona_variant"),
    "charm_(object)": ("accessories", "other_accessory"),
    "plugsuit_(evangelion)": ("clothes_special", "themed_costume"),
    "power_lines": ("indoor_scene", "urban"),
    "doll_joints": ("body", "body_state"),
    "leaf_on_head": ("accessories", "headwear"),
    "flower_knot": ("accessories", "badges_ornaments"),
    "dog_tags": ("accessories", "neckwear"),
    "radio_antenna": ("digital_media", "camera_media"),
    "drink_carton": ("food_drink", "tableware"),
    "milk_carton": ("food_drink", "tableware"),
    "flower_wreath": ("accessories", "headwear"),
    "armpit_hair": ("body", "body_state"),
    "chess_piece": ("recreation", "games"),
    "oppai_loli": ("people", "age"),
    "towel_around_neck": ("accessories", "neckwear"),
    "painting_(object)": ("culture_objects", "books_paper"),
    "drawing_(object)": ("culture_objects", "books_paper"),
    "e.g.o_(project_moon)": ("weapons", "other_weapon"),
    "cat_paws": ("creatures", "claw_scale"),
    "reflective_liquid": ("light_effect", "optical"),
    "spider_web": ("creatures", "insect"),
    "towel_on_head": ("accessories", "headwear"),
    "too_many": ("composition", "subject_focus"),
    "shouji": ("indoor_scene", "architecture"),
    "flower_pot": ("household_objects", "container"),
    "lily_pad": ("nature", "plant"),
    "chips_(food)": ("food_drink", "dessert_snack"),
    "bird_on_head": ("creatures", "bird"),
    "fluffy": ("style", "quality"),
    "smell": ("light_effect", "other_effect"),
    "four-leaf_clover": ("nature", "plant"),
    "food_on_head": ("action", "interaction"),
    "bread_slice": ("food_drink", "bakery"),
    "seashell": ("creatures", "aquatic"),
    "monsterification": ("themes", "identity_change"),
    "lemon_slice": ("food_drink", "fruit_vegetable"),
    "single_hair_tube": ("hair", "hair_accessory"),
    "turtle_shell": ("creatures", "claw_scale"),
    "ouji_fashion": ("clothes_special", "themed_costume"),
    "ace_(playing_card)": ("recreation", "games"),
    "claw_(weapon)": ("weapons", "blade"),
    "rocket_launcher": ("weapons", "explosive"),
    "millennium_cheerleader_outfit_(blue_archive)": ("clothes_special", "sports_uniform"),
    "liquid": ("light_effect", "other_effect"),
    "ankle_lace-up": ("legwear_footwear", "shoes"),
    "champion's_tunic_(zelda)": ("clothes_main", "tops"),
    "bird_on_shoulder": ("creatures", "bird"),
    "choko_(cup)": ("food_drink", "tableware"),
    "overgrown": ("outdoor_scene", "forest_field"),
    "digitigrade": ("body", "body_state"),
    "streamers": ("accessories", "badges_ornaments"),
    "digging_your_own_grave": ("themes", "narrative_situation"),
    "star_sticker": ("accessories", "badges_ornaments"),
    "pokemon_on_head": ("creatures", "fantasy_creature"),
    "intravenous_drip": ("household_objects", "tools"),
    "potion": ("household_objects", "container"),
    "when_you_see_it": ("meta_info", "meme"),
    "youkai_(youkai_watch)": ("creatures", "fantasy_creature"),
    "ring_hair_extensions": ("hair", "hair_accessory"),
    "ugly_bastard": ("people", "role_focus"),
    "open_window": ("indoor_scene", "architecture"),
    "destruction": ("action", "combat_action"),
    "mimikaki": ("household_objects", "tools"),
    "oc_x_canon": ("relationships", "romance_orientation"),
    "sangvis_ferri": ("relationships", "group_faction"),
    "diadem": ("accessories", "headwear"),
    "tablecloth": ("household_objects", "other_object"),
    "failure": ("themes", "narrative_situation"),
    "sword_over_shoulder": ("action", "holding"),
    "used_tissue": ("household_objects", "other_object"),
    "sig_sauer": ("weapons", "firearm"),
    "gibson_les_paul": ("culture_objects", "music"),
    "wheel": ("mech_scifi", "machine"),
    "double_w": ("pose", "hand_gesture"),
    "shoulder_peek": ("clothing_detail", "clothing_state"),
    "snap-fit_buckle": ("clothing_detail", "clothing_structure"),
    "broken_heart": ("text_meta", "symbol"),
    "caution_tape": ("household_objects", "other_object"),
    "cheek_press": ("action", "interaction"),
    "mini-hakkero": ("weapons", "magic_weapon"),
    "delinquent": ("people", "role_focus"),
    "party_popper": ("household_objects", "other_object"),
    "official_alternate_color": ("themes", "persona_variant"),
    "tube": ("household_objects", "container"),
    "crotch_rub": ("adult", "adult_self"),
    "ketchup": ("food_drink", "staple_food"),
    "tissue": ("household_objects", "other_object"),
    "setsubun": ("time_weather", "holiday"),
    "pointless_condom": ("adult", "adult_fetish"),
    "dust_cloud": ("light_effect", "particles"),
    "handkerchief": ("accessories", "other_accessory"),
    "syrup": ("food_drink", "dessert_snack"),
    "berry": ("food_drink", "fruit_vegetable"),
    "left-to-right_manga": ("meta_info", "meta"),
    "mascot": ("people", "role_focus"),
    "veranda": ("indoor_scene", "architecture"),
    "kappougi": ("clothes_special", "traditional_east"),
    "stroking_own_chin": ("pose", "hand_gesture"),
    "spitting": ("action", "daily_action"),
    "told_you_not_to_do_that": ("meta_info", "meme"),
    "weighing_scale": ("household_objects", "tools"),
    "single_epaulette": ("clothing_detail", "clothing_structure"),
    "plume": ("accessories", "headwear"),
    "cat_on_head": ("creatures", "mammal"),
    "completely_unamused": ("expression", "neutral_expression"),
    "tree_stump": ("outdoor_scene", "forest_field"),
    "drum_set": ("culture_objects", "music"),
    "reins": ("recreation", "sports"),
    "bowing": ("pose", "body_pose"),
    "ferris_wheel": ("indoor_scene", "architecture"),
    "stadium": ("indoor_scene", "architecture"),
    "phonograph": ("culture_objects", "music"),
    "lighter": ("household_objects", "tools"),
    "sticker_(medium)": ("style", "medium"),
    "voyeurism": ("adult", "adult_fetish"),
    "wiping_face": ("action", "daily_action"),
    "cat_teaser": ("recreation", "toys"),
    "grenade_pin": ("weapons", "explosive"),
    "tent": ("outdoor_scene", "other_scene"),
    "bikesuit": ("clothes_special", "sports_uniform"),
    "pink_wrist_cuffs": ("accessories", "handwear"),
    "underbutt": ("adult", "adult_nudity"),
    "centauroid": ("creatures", "fantasy_creature"),
    "zeon": ("relationships", "group_faction"),
    "crew_neck": ("clothing_detail", "clothing_structure"),
    "visible_air": ("light_effect", "other_effect"),
    "hanging": ("pose", "body_pose"),
    "fireplace": ("household_objects", "appliance"),
    "on_rock": ("pose", "stationary_pose"),
    "circle_cut": ("meta_info", "meta"),
    "lily_of_the_valley": ("nature", "plant"),
    "union_jack": ("text_meta", "symbol"),
    "icing": ("food_drink", "dessert_snack"),
    "square_neckline": ("clothing_detail", "clothing_structure"),
    "cucumber": ("food_drink", "fruit_vegetable"),
    "mark_under_eye": ("body", "body_marks"),
    "graveyard": ("outdoor_scene", "other_scene"),
    "portrait_(object)": ("culture_objects", "books_paper"),
    "stove": ("household_objects", "appliance"),
    "you're_doing_it_wrong": ("meta_info", "meme"),
    "artificial_eye": ("body", "body_state"),
    "puppet_strings": ("household_objects", "other_object"),
    "flashlight": ("household_objects", "lighting_clock"),
    "shimaidon_(sex)": ("adult", "adult_sex"),
    "pointer": ("household_objects", "tools"),
    "hydrokinesis": ("light_effect", "magic_effect"),
    "takoyaki": ("food_drink", "staple_food"),
    "shards": ("light_effect", "particles"),
    "log": ("outdoor_scene", "forest_field"),
    "flock": ("creatures", "bird"),
    "pokemon_on_shoulder": ("creatures", "fantasy_creature"),
    "ritual_baton": ("household_objects", "tools"),
    "tempura": ("food_drink", "staple_food"),
    "budget_sarashi": ("underwear_swim", "bra_lingerie"),
    "shiba_inu": ("creatures", "mammal"),
    "sweet_lolita": ("clothes_special", "themed_costume"),
    "chemical_structure": ("text_meta", "symbol"),
    "character_charm": ("accessories", "badges_ornaments"),
    "origami": ("culture_objects", "books_paper"),
    "jack-o'_challenge": ("pose", "body_pose"),
    "pancake_stack": ("food_drink", "dessert_snack"),
    "fireflies": ("creatures", "insect"),
    "lube": ("adult", "adult_fetish"),
    "thread": ("household_objects", "tools"),
    "bandaged_wrist": ("body", "body_marks"),
    "mega_stone": ("household_objects", "other_object"),
    "drill": ("household_objects", "tools"),
    "extra": ("meta_info", "meta"),
    "determined": ("expression", "neutral_expression"),
    "hagoita": ("recreation", "sports"),
    "popcorn": ("food_drink", "dessert_snack"),
    "gauze_on_face": ("body", "body_marks"),
    "cheek_squash": ("body", "body_state"),
    "dumbbell": ("recreation", "sports"),
    "gusset": ("clothing_detail", "clothing_structure"),
    "shin_guards": ("clothes_special", "helmet_protective"),
    "watermelon_slice": ("food_drink", "fruit_vegetable"),
    "coffin": ("household_objects", "container"),
    "screw": ("mech_scifi", "machine"),
    "ramune": ("food_drink", "drink"),
    "harvin": ("people", "fantasy_person"),
    "juban": ("clothes_special", "traditional_east"),
    "glutton": ("people", "role_focus"),
    "crime_prevention_buzzer": ("household_objects", "tools"),
    "39": ("text_meta", "text"),
    "tarot_(medium)": ("style", "medium"),
    "traditional_youkai": ("creatures", "fantasy_creature"),
    "character_age": ("meta_info", "meta"),
    "coin_on_string": ("household_objects", "other_object"),
    "plap": ("text_meta", "comic"),
    "shinsengumi": ("relationships", "group_faction"),
    "curtsey": ("pose", "body_pose"),
    "yes": ("text_meta", "text"),
    "virtual_graduation_commemoration": ("time_weather", "holiday"),
    "flower_on_head": ("accessories", "headwear"),
    "accidental_exposure": ("adult", "adult_nudity"),
    "height": ("body", "build"),
    "rolling_suitcase": ("accessories", "bags_belts"),
    "animal_on_lap": ("action", "interaction"),
    "round-bottom_flask": ("household_objects", "container"),
    "in_the_face": ("action", "interaction"),
    "dowsing_rod": ("household_objects", "tools"),
    "pizza_slice": ("food_drink", "staple_food"),
    "telekinesis": ("light_effect", "magic_effect"),
    "mahjong_tile": ("recreation", "games"),
    "on_person": ("pose", "stationary_pose"),
    "broken_chain": ("household_objects", "other_object"),
    "fountain": ("outdoor_scene", "water_scene"),
    "pikmin_(creature)": ("creatures", "fantasy_creature"),
    "happi": ("clothes_special", "traditional_east"),
    "crate": ("household_objects", "container"),
    "globe": ("household_objects", "other_object"),
    "sunscreen": ("household_objects", "tools"),
    "tankini": ("underwear_swim", "swimsuit"),
    "asymmetrical_dual_wielding": ("action", "combat_action"),
    "bendy_straw": ("food_drink", "tableware"),
    "kusazuri": ("clothes_special", "armor"),
    "moon_(ornament)": ("accessories", "badges_ornaments"),
    "gauze_on_cheek": ("body", "body_marks"),
    "ofuda_on_head": ("accessories", "headwear"),
    "fortissimo": ("culture_objects", "music"),
    "detective": ("people", "occupation"),
    "spear_the_gungnir": ("weapons", "magic_weapon"),
    "ajirogasa": ("accessories", "headwear"),
    "clapping": ("action", "interaction"),
    "pinned": ("action", "interaction"),
    "confession": ("themes", "narrative_situation"),
    "arrow_through_heart": ("text_meta", "symbol"),
    "cheek_bulge": ("face", "mouth"),
    "ballet": ("recreation", "sports"),
    "traffic_cone": ("household_objects", "other_object"),
    "shaking": ("action", "movement"),
    "slapping": ("action", "interaction"),
    "gold_coin": ("household_objects", "other_object"),
    "struggling": ("action", "movement"),
    "april_fools": ("time_weather", "holiday"),
    "bad_proportions": ("style", "quality"),
    "furigana": ("text_meta", "text"),
    "cropped_head": ("body", "body_state"),
    "akeome": ("text_meta", "text"),
    "torpedo_tubes": ("weapons", "explosive"),
    "wheat": ("nature", "plant"),
    "lalafell": ("people", "fantasy_person"),
    "cutting_board": ("household_objects", "tools"),
    "squinting": ("face", "eye_shape"),
    "multiple_heads": ("body", "body_state"),
    "animal_skull": ("creatures", "other_creature"),
    "canvas_(object)": ("culture_objects", "stationery"),
    "yin_yang_orb": ("weapons", "magic_weapon"),
    "holed_coin": ("household_objects", "other_object"),
    "chinstrap": ("clothing_detail", "clothing_structure"),
    "cooler": ("household_objects", "container"),
    "just_the_tip": ("adult", "adult_sex"),
    "puffy_cheeks": ("face", "mouth"),
    "round_window": ("indoor_scene", "architecture"),
    "tutu": ("clothes_special", "sports_uniform"),
    "neck_tassel": ("accessories", "neckwear"),
    "feral_instincts": ("themes", "narrative_situation"),
    "spiked_shell": ("creatures", "claw_scale"),
    "duster": ("household_objects", "tools"),
    "paper_kabuto": ("accessories", "headwear"),
    "forehead_protector": ("accessories", "headwear"),
    "teacher_and_student": ("relationships", "social_relation"),
    "knight_(chess)": ("recreation", "games"),
    "idol_heroes_(idolmaster)": ("relationships", "group_faction"),
    "japan_national_police": ("relationships", "group_faction"),
})

EXACT_OVERRIDES.update({
    "jimiko": ("people", "role_focus"),
    "viera": ("people", "fantasy_person"),
    "cockpit": ("transport_play", "air_vehicle"),
    "blank_stare": ("expression", "neutral_expression"),
    "lava": ("outdoor_scene", "terrain_surface"),
    "weight_conscious": ("expression", "neutral_expression"),
    "hitting": ("action", "combat_action"),
    "misleading_thumbnail": ("meta_info", "meta"),
    "gamepad": ("recreation", "games"),
    "electric_plug": ("household_objects", "appliance"),
    "kouhaku_nawa": ("accessories", "badges_ornaments"),
    "tanzaku": ("culture_objects", "books_paper"),
    "y2k_fashion": ("style", "era_style"),
    "frottage": ("adult", "adult_sex"),
    "comforting": ("action", "interaction"),
    "pendulum": ("household_objects", "clock"),
    "rayman_limbs": ("body", "body_state"),
    "ema": ("culture_objects", "books_paper"),
    "golden_week": ("time_weather", "holiday"),
    "hexagon": ("text_meta", "symbol"),
    "saw": ("household_objects", "tools"),
    "chart": ("text_meta", "text"),
    "champagne": ("food_drink", "drink"),
    "h&k_hk416": ("weapons", "firearm"),
    "tribal": ("style", "genre"),
    "single_shoulder_pad": ("clothes_special", "armor"),
    "school_briefcase": ("accessories", "bags_belts"),
    "noose": ("household_objects", "other_object"),
    "pouring_onto_self": ("action", "daily_action"),
    "snail": ("creatures", "aquatic"),
    "mechanization": ("themes", "identity_change"),
    "dropping": ("action", "holding"),
    "kaiju": ("creatures", "fantasy_creature"),
    "heart-shaped_buckle": ("clothing_detail", "clothing_structure"),
    "prototype_design": ("themes", "persona_variant"),
    "dandelion": ("nature", "plant"),
    "yarn": ("household_objects", "tools"),
    "earth_(ornament)": ("accessories", "badges_ornaments"),
    "dumpling": ("food_drink", "staple_food"),
    "berry_(pokemon)": ("food_drink", "fruit_vegetable"),
    "sidesaddle": ("pose", "body_pose"),
    "overcoat": ("clothes_main", "outerwear"),
    "scarlet_devil_mansion": ("indoor_scene", "architecture"),
    "self-harm": ("adult", "adult_gore"),
    "multiple_traps": ("people", "count_gender"),
    "honeycomb_(pattern)": ("clothing_detail", "clothing_pattern"),
    "torpedo_launcher": ("weapons", "explosive"),
    "crumbs": ("food_drink", "dessert_snack"),
    "wig": ("hair", "hair_accessory"),
    "heartbeat": ("text_meta", "comic"),
    "<|>_<|>": ("expression", "neutral_expression"),
    "astronaut": ("people", "occupation"),
    "picnic": ("action", "daily_action"),
    "ace_of_hearts": ("recreation", "games"),
    "pink_sash": ("accessories", "bags_belts"),
    "audience": ("people", "count_gender"),
    "perversion_of_canon": ("adult", "adult_other"),
    "salaryman": ("people", "occupation"),
    "glass_shards": ("light_effect", "particles"),
    "uvula": ("face", "mouth"),
    "sponge": ("household_objects", "tools"),
    "borrowed_design": ("themes", "persona_variant"),
    "umamusume_horse_relations": ("relationships", "social_relation"),
    "futa_on_male": ("adult", "adult_sex"),
    "sick": ("body", "body_state"),
    "sundae": ("food_drink", "dessert_snack"),
    "liquid_hair": ("hair", "hair_style"),
    "headless": ("body", "body_state"),
    "jester": ("people", "occupation"),
    "asa_no_ha_(pattern)": ("clothing_detail", "clothing_pattern"),
    "makizushi": ("food_drink", "staple_food"),
    "streetwear": ("clothes_special", "themed_costume"),
    "crane_(machine)": ("mech_scifi", "machine"),
    "easel": ("culture_objects", "stationery"),
    "bad_end": ("themes", "narrative_situation"),
    "hourglass": ("household_objects", "clock"),
    "snowball": ("recreation", "toys"),
    "shikigami": ("creatures", "fantasy_creature"),
    "adapted_turret": ("weapons", "firearm"),
    "dakimakura_(object)": ("household_objects", "seating_table"),
    "musou_isshin_(genshin_impact)": ("weapons", "magic_weapon"),
    "napkin": ("food_drink", "tableware"),
    "void_face": ("body", "body_state"),
    "haniwa_(statue)": ("household_objects", "other_object"),
    "tegaki": ("meta_info", "meta"),
    "crystal_hair": ("hair", "hair_style"),
    "kanabou": ("weapons", "blunt_chain"),
    "condensation": ("light_effect", "particles"),
    "snorkel": ("clothes_special", "helmet_protective"),
    "levitation": ("action", "movement"),
    "messy": ("body", "body_state"),
    "elezen": ("people", "fantasy_person"),
    "powering_up": ("light_effect", "magic_effect"),
    "boxer_briefs": ("underwear_swim", "panties_underwear"),
    "kuji-in": ("pose", "hand_gesture"),
    "henshin": ("themes", "identity_change"),
    "paper_stack": ("culture_objects", "books_paper"),
    "punk": ("style", "genre"),
    "k/da_(league_of_legends)": ("relationships", "group_faction"),
    "race_fetishism": ("adult", "adult_fetish"),
    "vocaloid_append": ("clothes_special", "themed_costume"),
    "morning_after": ("adult", "adult_other"),
    "drugs": ("household_objects", "other_object"),
    "pennant": ("text_meta", "symbol"),
    "flashback": ("themes", "narrative_situation"),
    "slashing": ("action", "combat_action"),
    "balancing": ("pose", "body_pose"),
    "eggplant": ("food_drink", "fruit_vegetable"),
    "heart_(organ)": ("body", "chest"),
    "pickaxe": ("household_objects", "tools"),
    "medallion": ("accessories", "jewelry"),
    "super_saiyan_1": ("themes", "persona_variant"),
    "cheekbones": ("face", "brows_nose"),
    "hair_strand": ("hair", "hair_style"),
    "hamaya": ("weapons", "bow"),
    "bartender": ("people", "occupation"),
    "marshmallow_(site)": ("text_meta", "screen_ui"),
    "opened_by_self": ("clothing_detail", "clothing_state"),
    "heart_pendant": ("accessories", "jewelry"),
    "freediving": ("action", "movement"),
    "yo-yo": ("recreation", "toys"),
    "native_american": ("clothes_special", "traditional_world"),
    "wrist_wrap": ("accessories", "handwear"),
    "m1911": ("weapons", "firearm"),
    "like_and_retweet": ("text_meta", "screen_ui"),
    "clown": ("people", "role_focus"),
    "embroidery": ("clothing_detail", "clothing_pattern"),
    "gills": ("creatures", "claw_scale"),
    "butter": ("food_drink", "dairy_ingredient"),
    "reaching_towards_another": ("action", "interaction"),
    "hauchiwa": ("weapons", "magic_weapon"),
    "uncommon_stimulation": ("adult", "adult_fetish"),
    "honey": ("food_drink", "dessert_snack"),
    "pentacle": ("accessories", "jewelry"),
    "bandolier": ("accessories", "bags_belts"),
    "covering_one_eye": ("pose", "hand_gesture"),
    "dorsal_fin": ("creatures", "claw_scale"),
    "frontal_wedgie": ("adult", "adult_clothes"),
    "cerise_bouquet": ("relationships", "group_faction"),
    "sequential": ("composition", "layout"),
    "devil_fruit_power": ("light_effect", "magic_effect"),
    "captured": ("themes", "narrative_situation"),
    "fanning_self": ("action", "daily_action"),
    "accurate_lolita_coord": ("clothes_special", "themed_costume"),
    "blowing_bubbles": ("action", "daily_action"),
    "seaweed": ("nature", "plant"),
    "blood_drip": ("body", "body_state"),
    "paint_splatter_on_face": ("body", "body_marks"),
    "uchikake": ("clothes_special", "traditional_east"),
    "winged_heart": ("text_meta", "symbol"),
    "potato": ("food_drink", "fruit_vegetable"),
    "untying": ("clothing_detail", "clothing_state"),
    "telescope": ("digital_media", "camera_media"),
    "mat": ("recreation", "sports"),
    "barbed_wire": ("indoor_scene", "architecture"),
    "bored": ("expression", "neutral_expression"),
    "han'eri": ("clothing_detail", "clothing_structure"),
    "coconut": ("food_drink", "fruit_vegetable"),
})

EXACT_OVERRIDES.update({
    "through_medium": ("composition", "layout"),
    "nejiri_hachimaki": ("accessories", "headwear"),
    "chastity_cage": ("adult", "adult_fetish"),
    "mira-cra_park!": ("relationships", "group_faction"),
    "\\o/": ("expression", "positive"),
    "camcorder": ("digital_media", "camera_media"),
    "sand_sculpture": ("culture_objects", "stationery"),
    "yordle": ("people", "fantasy_person"),
    "watermelon_bar": ("food_drink", "dessert_snack"),
    "\\n/": ("pose", "hand_gesture"),
    "aquarium": ("indoor_scene", "public_indoor"),
    "objectification": ("themes", "identity_change"),
    "cd": ("digital_media", "camera_media"),
    "tengu": ("creatures", "fantasy_creature"),
    "kesa": ("clothes_special", "traditional_east"),
    "blind": ("body", "body_state"),
    "toilet_use": ("action", "daily_action"),
    "breastfeeding": ("action", "interaction"),
    "kishimen_hair": ("hair", "hair_style"),
    "dorsiflexion": ("pose", "body_pose"),
    "eldritch_abomination": ("creatures", "fantasy_creature"),
    "smoking_barrel": ("weapons", "firearm"),
    "black_babydoll": ("clothes_special", "sleep_casual"),
    "white_babydoll": ("clothes_special", "sleep_casual"),
    "zabuton": ("household_objects", "seating_table"),
    "pump_action": ("weapons", "firearm"),
    "spoiler_(automobile)": ("transport_play", "land_vehicle"),
    "juxtaposition": ("composition", "layout"),
    "glomp": ("action", "interaction"),
    "lyre": ("culture_objects", "music"),
    "age_regression": ("themes", "identity_change"),
    "fish_skeleton": ("creatures", "aquatic"),
    "hair_vines": ("hair", "hair_style"),
    "hedgehog_boy": ("people", "fantasy_person"),
    "red_corset": ("underwear_swim", "bra_lingerie"),
    "side-tie_peek": ("adult", "adult_clothes"),
    "chalice": ("food_drink", "tableware"),
    "mullet": ("hair", "hair_style"),
    "in_palm": ("action", "interaction"),
    "racecar": ("transport_play", "land_vehicle"),
    "laundry": ("household_objects", "other_object"),
    "panicking": ("expression", "fear_surprise"),
    "truth": ("meta_info", "meme"),
    "dirt": ("outdoor_scene", "terrain_surface"),
    "fitness_gym": ("indoor_scene", "public_indoor"),
    "glock": ("weapons", "firearm"),
    "corn": ("food_drink", "fruit_vegetable"),
    "propeller": ("mech_scifi", "machine"),
    "swiss_roll": ("food_drink", "dessert_snack"),
    "futa_without_balls": ("adult", "adult_anatomy"),
    "amplifier": ("culture_objects", "music"),
    "portal_(object)": ("mech_scifi", "scifi_device"),
    "cartoon_bone": ("household_objects", "other_object"),
    "archery": ("recreation", "sports"),
    "heckler_&_koch": ("weapons", "firearm"),
    "kine": ("household_objects", "tools"),
    "lighthouse": ("indoor_scene", "architecture"),
    "person_and_animalization": ("themes", "identity_change"),
    "umbrella_over_shoulder": ("action", "holding"),
    "long_neck": ("body", "body_state"),
    "tongs": ("household_objects", "tools"),
    "hunched_over": ("pose", "body_pose"),
    "brain": ("body", "chest"),
    "bullet_hole": ("weapons", "firearm"),
    "long_earlobes": ("face", "ears"),
    "stone_stairs": ("indoor_scene", "architecture"),
    "weightlifting": ("action", "movement"),
    "merchandise": ("meta_info", "meta"),
    "houndstooth": ("clothing_detail", "clothing_pattern"),
    "blood_on_bandages": ("body", "body_marks"),
    "teruterubouzu": ("accessories", "other_accessory"),
    "hanten_(clothes)": ("clothes_special", "traditional_east"),
    "ready_to_draw": ("action", "combat_action"),
    "amulet": ("accessories", "jewelry"),
    "decepticon": ("relationships", "group_faction"),
    "intestines": ("adult", "adult_gore"),
    "white_sarong": ("clothes_special", "traditional_world"),
    "pet": ("creatures", "other_creature"),
    "kikkoumon": ("clothing_detail", "clothing_pattern"),
    "curled_up": ("pose", "body_pose"),
    "chimera": ("creatures", "fantasy_creature"),
    "hair_color_connection": ("themes", "character_connection"),
    "oda_uri": ("text_meta", "symbol"),
    "affectionate": ("action", "interaction"),
    "sticky_note": ("culture_objects", "books_paper"),
    "casting_spell": ("action", "combat_action"),
    "spaghetti": ("food_drink", "staple_food"),
    "double_vertical_stripe": ("clothing_detail", "clothing_pattern"),
    "torn_bodystocking": ("clothing_detail", "clothing_state"),
    "wallet_chain": ("accessories", "bags_belts"),
    "beretta_92": ("weapons", "firearm"),
    "food_bite": ("food_drink", "staple_food"),
    "thermometer": ("household_objects", "tools"),
    "groom": ("people", "role_focus"),
    "ar-15": ("weapons", "firearm"),
    "bulletin_board": ("household_objects", "storage_furniture"),
    "doily": ("household_objects", "other_object"),
    "pushing": ("action", "movement"),
    "single_tear": ("expression", "sad_cry"),
    "mannequin": ("household_objects", "other_object"),
    "invisible_man": ("adult", "adult_other"),
    "gyaruo": ("people", "role_focus"),
    "consensual_tentacles": ("adult", "adult_sex"),
    "boar": ("creatures", "mammal"),
    "fuuin_no_tsue": ("weapons", "magic_weapon"),
    "blake_bloom_(wuthering_waves)": ("accessories", "badges_ornaments"),
    "facepalm": ("pose", "hand_gesture"),
    "circled_9": ("text_meta", "symbol"),
    "...?": ("expression", "fear_surprise"),
    "mind_break": ("adult", "adult_other"),
    "sprinkles": ("food_drink", "dessert_snack"),
    "super_saiyan_4": ("themes", "persona_variant"),
    "mitre": ("accessories", "headwear"),
    "post-apocalypse": ("style", "genre"),
    "koi": ("creatures", "aquatic"),
    "brick": ("indoor_scene", "surface"),
    "electrical_outlet": ("household_objects", "appliance"),
    "handprint": ("text_meta", "symbol"),
})

# Final post-audit corrections.  This block intentionally wins over older
# exploratory mappings above.
EXACT_OVERRIDES.update({
    "mob_x_character": ("relationships", "romance_orientation"),
    "yaoi_(object)": ("relationships", "romance_orientation"),
    "group_(toaru)": ("relationships", "group_faction"),
    "inseki": ("relationships", "family_relation"),
    "pet": ("relationships", "social_relation"),
    "sandwiched": ("pose", "body_pose"),
    "girl_sandwich": ("pose", "body_pose"),
    "boy_sandwich": ("pose", "body_pose"),
    "kurokumo_clan_(identity)_(project_moon)": ("themes", "persona_variant"),
    "shoulder_pads": ("clothes_special", "helmet_protective"),
    "life_vest": ("clothes_special", "helmet_protective"),
    "bulletproof_vest": ("clothes_special", "helmet_protective"),
    "load_bearing_vest": ("clothes_special", "helmet_protective"),
    "wrist_guards": ("clothes_special", "helmet_protective"),
    "ear_protection": ("clothes_special", "helmet_protective"),
    "no_armor": ("clothing_detail", "clothing_state"),
    "unworn_armor": ("clothing_detail", "clothing_state"),
    "blood_on_armor": ("clothing_detail", "clothing_state"),
    "chaps": ("clothes_main", "bottoms"),
    "gaiters": ("legwear_footwear", "stockings"),
    "thighhigh_gaiters": ("legwear_footwear", "stockings"),
    "metal_wrist_cuffs": ("adult", "adult_fetish"),
    "red_wrist_cuffs": ("accessories", "handwear"),
    "purple_wrist_cuffs": ("accessories", "handwear"),
    "grey_wrist_cuffs": ("accessories", "handwear"),
    "fur-trimmed_wrist_cuffs": ("accessories", "handwear"),
    "flight_suit": ("clothes_special", "occupation_uniform"),
    "racing_suit": ("clothes_special", "sports_uniform"),
    "snorkel": ("recreation", "sports"),
    "kettle_helm": ("clothes_special", "helmet"),
    "armored_personnel_carrier": ("transport_play", "land_vehicle"),
    "jumpsuit_around_waist": ("clothing_detail", "clothing_state"),
    "pelvic_curtain": ("adult", "adult_clothes"),
    "breast_curtain": ("adult", "adult_clothes"),
    "breast_curtains": ("adult", "adult_clothes"),
    "single_breast_curtain": ("adult", "adult_clothes"),
    "long_breast_curtain": ("adult", "adult_clothes"),
    "costume_switch": ("themes", "narrative_situation"),
    "vocaloid_append": ("themes", "persona_variant"),
    "costume_chart": ("meta_info", "meta"),
    "festival_jinbei": ("clothes_special", "traditional_east"),
    "training_wear_(fire_emblem_engage)": ("clothes_special", "sports_uniform"),
    "training_outfit_(fire_emblem_engage)": ("clothes_special", "sports_uniform"),
    "streetwear": ("clothes_special", "sleep_casual"),
    "black_babydoll": ("underwear_swim", "bra_lingerie"),
    "white_babydoll": ("underwear_swim", "bra_lingerie"),
    "purple_babydoll": ("underwear_swim", "bra_lingerie"),
    "blue_babydoll": ("underwear_swim", "bra_lingerie"),
    "green_babydoll": ("underwear_swim", "bra_lingerie"),
    "cupless_babydoll": ("underwear_swim", "bra_lingerie"),
    "bow_babydoll": ("underwear_swim", "bra_lingerie"),
    "nike_(company)": ("text_meta", "brand"),
    "honda": ("text_meta", "brand"),
    "adidas": ("text_meta", "brand"),
    "converse": ("text_meta", "brand"),
    "heckler_&_koch": ("text_meta", "brand"),
    "sig_sauer": ("text_meta", "brand"),
    "fender_musical_instruments_corporation": ("text_meta", "brand"),
    "wallet": ("accessories", "bags_belts"),
    "war": ("themes", "narrative_situation"),
    "blue_sarong": ("clothes_special", "traditional_world"),
    "white_sarong": ("clothes_special", "traditional_world"),
    "playstation_portable": ("digital_media", "phone_computer"),
    "excalibur_morgan_(fate)": ("weapons", "magic_weapon"),
    "omikuji": ("culture_objects", "books_paper"),
    "plant_roots": ("nature", "plant"),
    "wakizashi": ("weapons", "blade"),
    "clothes_tug": ("clothing_detail", "clothing_state"),
    "conductor_baton": ("culture_objects", "music"),
    "lord_camelot_(fate)": ("weapons", "shield"),
    "mochi_trail": ("food_drink", "staple_food"),
    "hedgehog": ("creatures", "mammal"),
    "how_to": ("meta_info", "meta"),
    "mast": ("transport_play", "water_vehicle"),
    "reindeer": ("creatures", "mammal"),
    "storefront": ("indoor_scene", "commercial"),
    "hanging_light": ("household_objects", "lighting_clock"),
    "king_(chess)": ("recreation", "games"),
    "waiter": ("people", "occupation"),
    "maneki-neko": ("household_objects", "other_object"),
    "missile_pod": ("weapons", "explosive"),
    "papers": ("culture_objects", "books_paper"),
    "tag": ("text_meta", "text"),
    "disembodied_eye": ("face", "eye_shape"),
    "ace_of_spades": ("recreation", "games"),
    "melon": ("food_drink", "fruit_vegetable"),
    "paper_crane": ("culture_objects", "books_paper"),
    "toilet_stall": ("indoor_scene", "public_indoor"),
    "spit_take": ("action", "daily_action"),
    "theft": ("action", "daily_action"),
    "on_roof": ("outdoor_scene", "other_scene"),
    "crocodilian": ("creatures", "reptile"),
    "lute_(instrument)": ("culture_objects", "music"),
    "pokemon_move": ("light_effect", "magic_effect"),
    "jockstrap": ("underwear_swim", "panties_underwear"),
    "blacked_female": ("adult", "adult_sex"),
    "tuanshan": ("accessories", "other_accessory"),
    "recorder": ("culture_objects", "music"),
    "hairjob": ("adult", "adult_fetish"),
    "masochism": ("adult", "adult_fetish"),
    "tokyo_(city)": ("indoor_scene", "urban"),
    "rounded_corners": ("composition", "border"),
    "grill": ("household_objects", "appliance"),
    "zora": ("people", "fantasy_person"),
    "red_oni": ("creatures", "fantasy_creature"),
    "gerudo": ("people", "fantasy_person"),
    "ticket": ("culture_objects", "books_paper"),
    "onmyouji": ("people", "occupation"),
    "seatbelt": ("transport_play", "land_vehicle"),
    "urethral_insertion": ("adult", "adult_sex"),
    "raimon": ("relationships", "group_faction"),
    "beans": ("food_drink", "fruit_vegetable"),
    "diaper": ("underwear_swim", "panties_underwear"),
    "single_head_wing": ("creatures", "wing_feather"),
    "changpao": ("clothes_special", "traditional_east"),
    "sugar_cube": ("food_drink", "dessert_snack"),
    "acorn": ("nature", "plant"),
    "clueless": ("expression", "neutral_expression"),
    "kono_lolicon_domome": ("meta_info", "meme"),
    "misunderstanding": ("themes", "narrative_situation"),
    "rook_(chess)": ("recreation", "games"),
    "tentacles_on_male": ("adult", "adult_fetish"),
    "zero_gravity": ("action", "movement"),
    "chocobo": ("creatures", "fantasy_creature"),
    "mob_face": ("face", "eye_shape"),
    "earth_federation": ("relationships", "group_faction"),
    "kessoku_band": ("relationships", "group_faction"),
    "dollchestra": ("relationships", "group_faction"),
    "ao_dai": ("clothes_special", "traditional_world"),
    "cat_on_shoulder": ("action", "interaction"),
    "dragging": ("action", "holding"),
    "horseshoe": ("household_objects", "tools"),
    "food_art": ("style", "medium"),
    "marshmallow": ("food_drink", "dessert_snack"),
    "lovestruck": ("expression", "positive"),
    "blowing": ("action", "daily_action"),
    "splatter": ("light_effect", "particles"),
    "spreader_bar": ("adult", "adult_fetish"),
    "surrounded": ("composition", "layout"),
    "thermos": ("food_drink", "tableware"),
    "bib": ("accessories", "neckwear"),
    "duel_disk": ("recreation", "games"),
    "whiteboard": ("culture_objects", "books_paper"),
    "wide_brim": ("clothing_detail", "clothing_structure"),
    "mithra_(ff11)": ("people", "fantasy_person"),
    "naturally_detached_hair": ("hair", "hair_action"),
    "detached_hair": ("hair", "hair_action"),
    "folded_hair": ("hair", "hair_style"),
    "starry_hair": ("hair", "hair_action"),
    "bunching_hair": ("hair", "hair_action"),
    "hair_flip": ("hair", "hair_action"),
    "liquid_hair": ("hair", "hair_action"),
    "crystal_hair": ("hair", "hair_action"),
    "hair_vines": ("hair", "hair_action"),
    "marking_on_cheek": ("body", "body_marks"),
    "torture": ("adult", "adult_gore"),
    "<o>_<o>": ("face", "eye_shape"),
    "broad_shoulders": ("body", "build"),
    "long_neck": ("body", "build"),
    "gun_to_head": ("action", "combat_action"),
    "weasel_girl": ("people", "fantasy_person"),
    "ladybug": ("creatures", "insect"),
    "grenade_launcher": ("weapons", "explosive"),
    "public_use": ("adult", "adult_fetish"),
    "chained_wrists": ("adult", "adult_fetish"),
    "futasub": ("adult", "adult_fetish"),
    "policeman": ("people", "occupation"),
    "wizard": ("people", "occupation"),
    "onion": ("food_drink", "fruit_vegetable"),
    "radish": ("food_drink", "fruit_vegetable"),
    "ivy": ("nature", "plant"),
    "bubble_tea_challenge": ("meta_info", "meme"),
    "good_end": ("themes", "narrative_situation"),
    "queen_(chess)": ("recreation", "games"),
    "bishop_(chess)": ("recreation", "games"),
    "army": ("relationships", "group_faction"),
    "hanetsuki": ("recreation", "sports"),
    "karaoke": ("action", "daily_action"),
    "playing": ("action", "daily_action"),
    "triplets": ("relationships", "family_relation"),
    "cracked_glass": ("light_effect", "optical"),
    "propeller_fighter": ("transport_play", "air_vehicle"),
    "airship": ("transport_play", "air_vehicle"),
    "cobblestone": ("outdoor_scene", "terrain_surface"),
    "copy_ability": ("light_effect", "magic_effect"),
    "nissin_cup_noodle": ("food_drink", "staple_food"),
    "salad": ("food_drink", "staple_food"),
    "kamaboko": ("food_drink", "meat_seafood"),
    "double_horizontal_stripe": ("clothing_detail", "clothing_pattern"),
    "ferret": ("creatures", "mammal"),
    "puppy": ("creatures", "mammal"),
    "nintendo_ds": ("digital_media", "phone_computer"),
    "game_boy": ("digital_media", "phone_computer"),
    "aestus_estus": ("weapons", "magic_weapon"),
    "croissant": ("food_drink", "bakery"),
    "hashtag": ("text_meta", "symbol"),
    "kikumon": ("text_meta", "symbol"),
    "seal_impression": ("text_meta", "symbol"),
    "foam": ("light_effect", "particles"),
    "ipod": ("digital_media", "camera_media"),
    "vinyl_record": ("culture_objects", "music"),
    "carousel": ("recreation", "toys"),
    "trophy": ("recreation", "sports"),
    "pelt": ("clothing_detail", "clothing_material"),
    "color_timer": ("mech_scifi", "scifi_device"),
    "cola": ("food_drink", "drink"),
    "whiskey": ("food_drink", "drink"),
    "collared_shrug": ("clothes_main", "outerwear"),
    "lipgloss": ("face", "makeup"),
    "muzzle_flash": ("light_effect", "fire_smoke"),
    "cigarette_pack": ("household_objects", "container"),
    "booth_seating": ("household_objects", "seating_table"),
    "wa_lolita": ("clothes_special", "themed_costume"),
    "couter": ("clothes_special", "armor"),
    "massage": ("action", "interaction"),
    "grave": ("outdoor_scene", "other_scene"),
    "chakram": ("weapons", "blade"),
    "pubic_stubble": ("adult", "adult_anatomy"),
    "cyber_fashion": ("style", "genre"),
    "van": ("transport_play", "land_vehicle"),
    "item_(toaru)": ("relationships", "group_faction"),
    "awakening_(toaru)": ("light_effect", "magic_effect"),
    "shosei": ("people", "role_focus"),
    "voile": ("indoor_scene", "public_indoor"),
    "against_bookshelf": ("pose", "body_pose"),
    "on_book": ("pose", "body_pose"),
    "stapled": ("adult", "adult_gore"),
    "paper_texture": ("style", "medium"),
    "credit_card": ("culture_objects", "books_paper"),
    "gift_card": ("culture_objects", "books_paper"),
    "business_card": ("culture_objects", "books_paper"),
    "calling_card": ("culture_objects", "books_paper"),
    "graphics_card": ("digital_media", "phone_computer"),
    "energy_tank": ("mech_scifi", "scifi_device"),
    "test_card": ("text_meta", "screen_ui"),
    "simple_bat": ("creatures", "mammal"),
    "dragon_ball_(object)": ("recreation", "toys"),
    "hello_happy_world!": ("relationships", "group_faction"),
    "k-pop": ("style", "genre"),
    "mjolnir_(marvel)": ("weapons", "blunt_chain"),
    "chui_(weapon)": ("weapons", "blunt_chain"),
    "three_section_staff": ("weapons", "blunt_chain"),
    "mage_staff": ("weapons", "magic_weapon"),
    "hecate's_staff_(fate)": ("weapons", "magic_weapon"),
    "staff_(ff10)": ("weapons", "magic_weapon"),
    "field_of_blades": ("outdoor_scene", "other_scene"),
    "explosive": ("light_effect", "fire_smoke"),
    "boom_barrier": ("indoor_scene", "urban"),
    "danmaku": ("light_effect", "particles"),
    "weapon_connection": ("themes", "character_connection"),
    "steel_ball_(jojo)": ("weapons", "blunt_chain"),
    "chain_weapon": ("weapons", "blunt_chain"),
    "combat_ship_(eve_online)": ("transport_play", "air_vehicle"),
    "attack_ship_(eve_online)": ("transport_play", "air_vehicle"),
    "splattershot_pro_(splatoon)": ("weapons", "firearm"),
    "flying_kick": ("action", "combat_action"),
    "spinning_bird_kick": ("action", "combat_action"),
    "striker_unit": ("mech_scifi", "scifi_device"),
    "striped_innertube": ("recreation", "sports"),
    "duck_innertube": ("recreation", "sports"),
    "on_head": ("pose", "body_pose"),
    "animal_on_head": ("pose", "body_pose"),
    "animal_on_shoulder": ("pose", "body_pose"),
    "incoming_letter": ("culture_objects", "books_paper"),
    "fan_speaking": ("meta_info", "meme"),
    "squirting_liquid": ("adult", "adult_fluid"),
    "writing_on_ass": ("text_meta", "text"),
    "nengajou": ("culture_objects", "books_paper"),
    "earthquake": ("outdoor_scene", "other_scene"),
    "caldari_state": ("relationships", "group_faction"),
    "amarr_empire": ("relationships", "group_faction"),
    "gallente_federation": ("relationships", "group_faction"),
    "minmatar_republic": ("relationships", "group_faction"),
    "poke_ball": ("recreation", "games"),
    "poke_ball_(basic)": ("recreation", "games"),
    "ultra_ball": ("recreation", "games"),
    "hisuian_poke_ball": ("recreation", "games"),
    "dusk_ball": ("recreation", "games"),
    "great_ball": ("recreation", "games"),
    "luxury_ball": ("recreation", "games"),
    "master_ball": ("recreation", "games"),
    "dive_ball": ("recreation", "games"),
    "premier_ball": ("recreation", "games"),
    "love_ball": ("recreation", "games"),
    "quick_ball": ("recreation", "games"),
    "nest_ball": ("recreation", "games"),
    "heal_ball": ("recreation", "games"),
    "beast_ball": ("recreation", "games"),
    "moon_ball": ("recreation", "games"),
    "nontraditional_poke_ball": ("recreation", "games"),
    "waist_poke_ball": ("accessories", "bags_belts"),
    "throwing_poke_ball": ("action", "combat_action"),
    "open_poke_ball": ("action", "holding"),
    "toy_car": ("recreation", "toys"),
    "toy_train": ("recreation", "toys"),
    "model_tank": ("recreation", "toys"),
    "remote_control_vehicle": ("recreation", "toys"),
    "paper_airplane": ("recreation", "toys"),
    "toy_airplane": ("recreation", "toys"),
    "model_airplane": ("recreation", "toys"),
    "paper_boat": ("recreation", "toys"),
    "model_ship": ("recreation", "toys"),
    "toy_boat": ("recreation", "toys"),

    # Final high-frequency semantic audit.  These are deliberately exact
    # because many are short/ambiguous words whose fragments would make an
    # unsafe global rule (for example ``folder``, ``cast`` and ``stain``).
    "stain": ("indoor_scene", "surface"),
    "height_chart": ("relationships", "comparison"),
    "tape_measure": ("household_objects", "tools"),
    "crowbar": ("household_objects", "tools"),
    "saiyan": ("people", "fantasy_person"),
    "amesuku_gyaru": ("clothes_special", "themed_costume"),
    "sheikah": ("people", "fantasy_person"),
    "abuse": ("action", "combat_action"),
    "netnavi": ("people", "fantasy_person"),
    "motherly": ("relationships", "social_relation"),
    "otaku": ("people", "role_focus"),
    "desi": ("people", "role_focus"),
    "cream_on_face": ("body", "body_marks"),
    "nazi": ("relationships", "group_faction"),
    "breaking": ("action", "combat_action"),
    "hedgehog_girl": ("people", "fantasy_person"),
    "dudou": ("underwear_swim", "bra_lingerie"),
    "hole": ("indoor_scene", "surface"),
    "wrist_cutting": ("adult", "adult_gore"),
    "materia": ("nature", "mineral"),
    "elevator": ("indoor_scene", "architecture"),
    "dissolving": ("light_effect", "other_effect"),
    "folder": ("culture_objects", "books_paper"),
    "sneezing": ("action", "daily_action"),
    "isometric": ("composition", "viewpoint"),
    "broken_window": ("indoor_scene", "surface"),
    "hungry": ("body", "body_state"),
    "fidgeting": ("action", "daily_action"),
    "stats": ("text_meta", "screen_ui"),
    "stopwatch": ("household_objects", "clock"),
    "gunblade": ("weapons", "magic_weapon"),
    "animal_genitalia_on_humanoid": ("adult", "adult_anatomy"),
    "menu_board": ("text_meta", "text"),
    "crawling": ("action", "movement"),
    "animal_head": ("people", "fantasy_person"),
    "kinchaku": ("accessories", "bags_belts"),
    "mummy": ("creatures", "fantasy_creature"),
    "cross-eyed": ("face", "eye_shape"),
    "casino": ("indoor_scene", "commercial"),
    "motoyui": ("hair", "hair_accessory"),
    "rice_on_face": ("body", "body_marks"),
    "double_\\m/": ("pose", "hand_gesture"),
    "minotaur": ("creatures", "fantasy_creature"),
    "chessboard": ("recreation", "games"),
    "chrysanthemum": ("nature", "plant"),
    "inktober": ("meta_info", "meta"),
    "guard_rail": ("indoor_scene", "urban"),
    "amazon_position": ("adult", "adult_sex"),
    "abandoned": ("outdoor_scene", "other_scene"),
    "legband": ("accessories", "other_accessory"),
    "corsage": ("accessories", "badges_ornaments"),
    "crane_(animal)": ("creatures", "bird"),
    "player_2": ("themes", "persona_variant"),
    "meta": ("meta_info", "meta"),
    "first_aid_kit": ("household_objects", "tools"),
    "drugged": ("body", "body_state"),
    "josou_seme": ("adult", "adult_other"),
    "scratching_head": ("pose", "hand_gesture"),
    "cauldron": ("household_objects", "container"),
    "scylla": ("creatures", "fantasy_creature"),
    "creature_on_head": ("pose", "body_pose"),
    "pankou": ("clothing_detail", "clothing_structure"),
    "protecting": ("action", "interaction"),
    "nissan": ("text_meta", "brand"),
    "baton_(weapon)": ("weapons", "blunt_chain"),
    "roasted_sweet_potato": ("food_drink", "staple_food"),
    "shotgun_shell": ("weapons", "firearm"),
    "unconventional_steed": ("action", "movement"),
    "clothesline": ("household_objects", "tools"),
    "haramaki": ("clothes_main", "tops"),
    "braces": ("face", "mouth"),
    "hoyofair": ("meta_info", "meta"),
    "odaibako": ("digital_media", "phone_computer"),
    "poleyn": ("clothes_special", "armor"),
    "prank": ("action", "interaction"),
    "mundane_made_awesome": ("meta_info", "meme"),
    "extra_faces": ("body", "body_state"),
    "ashtray": ("household_objects", "container"),
    "cork": ("household_objects", "container"),
    "h&k_ump": ("weapons", "firearm"),
    "gathers": ("clothing_detail", "clothing_structure"),
    "broccoli": ("food_drink", "fruit_vegetable"),
    "emo_fashion": ("clothes_special", "themed_costume"),
    "kaleidostick": ("weapons", "magic_weapon"),
    "foreplay": ("adult", "adult_suggestive"),
    "chikan": ("adult", "adult_fetish"),
    "arachne": ("people", "fantasy_person"),
    "murder": ("action", "combat_action"),
    "shield_on_back": ("weapons", "shield"),
    "red_carpet": ("indoor_scene", "surface"),
    "jeweled_branch_of_hourai": ("household_objects", "other_object"),
    "duckling": ("creatures", "bird"),
    "oversized_limbs": ("body", "body_state"),
    "multiple_hair_clips": ("hair", "hair_accessory"),
    "inflatable_raft": ("transport_play", "water_vehicle"),
    "bullying": ("action", "combat_action"),
    "fist_bump": ("action", "interaction"),
    "net": ("household_objects", "tools"),
    "tamagoyaki": ("food_drink", "staple_food"),
    "frozen": ("body", "body_state"),
    "front-to-back": ("composition", "layout"),
    "united_states": ("outdoor_scene", "other_scene"),
    "dynamax": ("themes", "identity_change"),
    "valkyrie": ("people", "fantasy_person"),
    "out_of_character": ("meta_info", "meta"),
    "mount_fuji": ("outdoor_scene", "mountain_desert"),
    "lead_pipe": ("weapons", "blunt_chain"),
    "flower_on_liquid": ("nature", "plant"),
    "chihaya_(clothing)": ("clothes_special", "traditional_east"),
    "qixiong_ruqun": ("clothes_special", "traditional_east"),
    "onbashira": ("indoor_scene", "architecture"),
    "clothes": ("clothing_detail", "other_clothes"),
    "shrugging": ("pose", "body_pose"),
    "sewing": ("action", "daily_action"),
    "gymnastics": ("recreation", "sports"),
    "face_down": ("pose", "body_pose"),
    "mutton_chops": ("face", "facial_hair"),
    "in_heat": ("body", "body_state"),
    "grid": ("composition", "layout"),
    "dogeza": ("pose", "stationary_pose"),
    "lap_pillow_invitation": ("action", "interaction"),
    "toyota": ("text_meta", "brand"),
    "skull_on_head": ("pose", "body_pose"),
    "x3": ("text_meta", "symbol"),
    "scratching_cheek": ("pose", "hand_gesture"),
    "surfing": ("recreation", "sports"),
    "sauce": ("food_drink", "staple_food"),
    "suicide": ("adult", "adult_gore"),
    "pee_stain": ("adult", "adult_fluid"),
    "blue_corset": ("underwear_swim", "bra_lingerie"),
    "jam": ("food_drink", "dessert_snack"),
    "incense_burner": ("household_objects", "container"),
    "optical_sight": ("weapons", "firearm"),
    "cart": ("transport_play", "land_vehicle"),
    "star_guardian_(league_of_legends)": ("clothes_special", "themed_costume"),
    "vertical_foregrip": ("weapons", "firearm"),
    "gingerbread_man": ("food_drink", "bakery"),
    "catchphrase": ("text_meta", "text"),
    "soviet": ("relationships", "group_faction"),
    "paper_on_head": ("pose", "body_pose"),
    "invisible": ("light_effect", "optical"),
    "circle_formation": ("composition", "layout"),
    "billboard": ("indoor_scene", "urban"),
    "clownfish": ("creatures", "aquatic"),
    "cabbage": ("food_drink", "fruit_vegetable"),
    "multiple_riders": ("action", "movement"),
    "kagami_mochi": ("food_drink", "staple_food"),
    "unused_tire": ("household_objects", "other_object"),
    "tonfa": ("weapons", "blunt_chain"),
    "girly_boy": ("themes", "identity_change"),
    "wyvern": ("creatures", "fantasy_creature"),
    "p90": ("weapons", "firearm"),
    "tapir_girl": ("people", "fantasy_person"),
    "searchlight": ("household_objects", "lighting_clock"),
    "scouter": ("mech_scifi", "scifi_device"),
    "pitcher_(container)": ("food_drink", "tableware"),
    "male_on_futa": ("adult", "adult_sex"),
    "chuunibyou": ("people", "role_focus"),
    "mane": ("creatures", "animal_feature"),
    "coffee_pot": ("food_drink", "tableware"),
    "virtual_pet_(toy)": ("recreation", "toys"),
    "dating": ("relationships", "romance_orientation"),
    "japan": ("outdoor_scene", "other_scene"),
    "volleyball_net": ("recreation", "sports"),
    "microwave": ("household_objects", "appliance"),
    "marriage_proposal": ("relationships", "romance_orientation"),
    "obidome": ("accessories", "badges_ornaments"),
    "mg42": ("weapons", "firearm"),
    "keep_out": ("text_meta", "text"),
    "ambiguous_red_liquid": ("adult", "adult_fluid"),
    "holomyth": ("relationships", "group_faction"),
    "firelock": ("weapons", "firearm"),
    "neo_zeon": ("relationships", "group_faction"),
    "fishing_line": ("recreation", "sports"),
    "decora": ("clothes_special", "themed_costume"),
    "accident": ("themes", "narrative_situation"),
    "urinal": ("household_objects", "other_object"),
    "measuring": ("action", "daily_action"),
    "joy-con": ("digital_media", "phone_computer"),
    "blood_on_neck": ("body", "body_marks"),
    "pushing_away": ("action", "interaction"),
    "kotoyoro": ("time_weather", "holiday"),
    "red_star": ("text_meta", "symbol"),
    "raspberry": ("food_drink", "fruit_vegetable"),
    "multitasking": ("action", "daily_action"),
    "model_kit": ("recreation", "toys"),
    "half-erect": ("adult", "adult_anatomy"),
    "rust": ("indoor_scene", "surface"),
    "pink_tulip": ("nature", "plant"),
    "nyan": ("text_meta", "comic"),
    "sharingan": ("face", "eye_shape"),
    "test_plugsuit_(evangelion)": ("clothes_special", "occupation_uniform"),
    "fern": ("nature", "plant"),
    "pawn_(chess)": ("recreation", "games"),
    "compass": ("household_objects", "tools"),
    "trash": ("household_objects", "other_object"),
    "prison": ("indoor_scene", "public_indoor"),
    "caliburn_(fate)": ("weapons", "magic_weapon"),
    "tea_set": ("food_drink", "tableware"),
    "kaname-ishi": ("nature", "mineral"),
    "pinching_own_belly": ("pose", "hand_gesture"),
    "sabaton": ("clothes_special", "armor"),
    "spines": ("creatures", "animal_feature"),
    "candelabra": ("household_objects", "lighting_clock"),
    "aunt_and_niece": ("relationships", "family_relation"),
    "red_shrug": ("clothes_main", "outerwear"),
    "creature_on_shoulder": ("pose", "body_pose"),
    "toddlercon": ("adult", "adult_other"),
    "kitten": ("creatures", "mammal"),
    "tripod": ("household_objects", "tools"),
    "crushing": ("action", "combat_action"),
    "armbinder": ("adult", "adult_fetish"),
    "anglerfish": ("creatures", "aquatic"),
    "locomotive": ("transport_play", "land_vehicle"),
    "erlenmeyer_flask": ("household_objects", "tools"),
    "absolutely_everyone": ("people", "count_gender"),
    "carapace": ("creatures", "animal_feature"),
    "toggles": ("clothing_detail", "clothing_structure"),
    "cleft_chin": ("face", "mouth"),
    "gao": ("text_meta", "comic"),
    "bridle": ("household_objects", "tools"),
    "squidbeak_splatoon": ("relationships", "group_faction"),
    "square": ("text_meta", "symbol"),
    "flirting": ("action", "interaction"),
    "prison_cell": ("indoor_scene", "public_indoor"),
    "graduation": ("themes", "narrative_situation"),
    "rerebrace": ("clothes_special", "armor"),
    "race_bib": ("recreation", "sports"),
    "heropin": ("themes", "narrative_situation"),
    "cutting": ("action", "daily_action"),
    "oar": ("household_objects", "tools"),
    "shoulder_guard": ("clothes_special", "armor"),
    "awning": ("indoor_scene", "architecture"),
    "keyblade": ("weapons", "magic_weapon"),
    "scoop_neck": ("clothing_detail", "clothing_structure"),
    "nihonga": ("style", "medium"),
    "black_hiphighs": ("legwear_footwear", "stockings"),
    "strong": ("body", "build"),
    "collared_halterneck": ("clothing_detail", "clothing_structure"),
    "cash_register": ("household_objects", "appliance"),
    "wafer_stick": ("food_drink", "dessert_snack"),
    "vacuum_cleaner": ("household_objects", "appliance"),
    "hishaku": ("household_objects", "tools"),
    "battle_damage": ("body", "body_state"),
    "sewing_needle": ("household_objects", "tools"),
    "ehoumaki": ("food_drink", "staple_food"),
    "cassock": ("clothes_special", "occupation_uniform"),
    "spiral": ("text_meta", "symbol"),
    "female_butler": ("people", "occupation"),
    "bathhouse": ("indoor_scene", "commercial"),
    "playable_command_(touhou)": ("text_meta", "screen_ui"),
    "village": ("outdoor_scene", "other_scene"),
    "warrior": ("people", "occupation"),
    "drowning": ("body", "body_state"),
    "heart_sticker": ("accessories", "badges_ornaments"),
    "wheelbarrow": ("transport_play", "land_vehicle"),
    "cast": ("body", "body_state"),

    # Corrections for several exact overrides whose English word or fan
    # translation obscures the actual tag meaning.
    "blood_on_bandages": ("body", "body_state"),
    "telescope": ("household_objects", "tools"),
    "teruterubouzu": ("household_objects", "other_object"),
    "invisible_man": ("people", "fantasy_person"),
    "blake_bloom_(wuthering_waves)": ("nature", "plant"),
    "cracked_glass": ("indoor_scene", "surface"),
})


EXACT_OVERRIDES.update({
    # Second pass over the remaining high-frequency long tail.
    "dragon_bean_(arknights)": ("people", "fantasy_person"),
    "starting_future_(umamusume)": ("clothes_special", "sports_uniform"),
    "hypocrisy": ("themes", "narrative_situation"),
    "midriff_sarashi": ("underwear_swim", "bra_lingerie"),
    "thumbs_down": ("pose", "hand_gesture"),
    "monk": ("people", "occupation"),
    "entangled": ("body", "body_state"),
    "fleur-de-lis": ("text_meta", "symbol"),
    "martial_arts": ("recreation", "sports"),
    "nudist": ("adult", "adult_nudity"),
    "strawberry_slice": ("food_drink", "fruit_vegetable"),
    "pixel_heart": ("text_meta", "symbol"),
    "stomping": ("action", "combat_action"),
    "disguise": ("themes", "identity_change"),
    "closet": ("household_objects", "storage_furniture"),
    "arrancar": ("people", "fantasy_person"),
    "playground": ("outdoor_scene", "other_scene"),
    "ankle_wrap": ("legwear_footwear", "stockings"),
    "shihakusho": ("clothes_special", "occupation_uniform"),
    "classic_lolita": ("clothes_special", "themed_costume"),
    "clothes_pin": ("household_objects", "tools"),
    "snow_globe": ("recreation", "toys"),
    "chili_pepper": ("food_drink", "fruit_vegetable"),
    "cello": ("culture_objects", "music"),
    "pregnancy_test": ("household_objects", "tools"),
    "hanami": ("action", "daily_action"),
    "exoskeleton": ("mech_scifi", "cybernetic"),
    "bonsai": ("nature", "plant"),
    "peril": ("themes", "narrative_situation"),
    "hook": ("weapons", "other_weapon"),
    "familiar": ("creatures", "fantasy_creature"),
    "design_speculation": ("meta_info", "meta"),
    "biting_neck": ("action", "interaction"),
    "star_balloon": ("recreation", "toys"),
    "immobilization": ("adult", "adult_fetish"),
    "balance_scale": ("household_objects", "tools"),
    "selfie_stick": ("digital_media", "camera_media"),
    "ai-generated_art_(topic)": ("meta_info", "meta"),
    "raccoon_boy": ("people", "fantasy_person"),
    "congratulations": ("text_meta", "text"),
    "joystick": ("recreation", "games"),
    "panzer_iv": ("transport_play", "land_vehicle"),
    "flower_trim": ("clothing_detail", "clothing_structure"),
    "troll_face": ("meta_info", "meme"),
    "sayagata": ("clothing_detail", "clothing_pattern"),
    "patterned": ("clothing_detail", "clothing_pattern"),
    "lolidom": ("adult", "adult_other"),
    "cat_on_lap": ("action", "interaction"),
    "black_vs_white": ("light_effect", "palette"),
    "armpit_hair_peek": ("body", "body_marks"),
    "curious": ("expression", "neutral_expression"),
    "audio_jack": ("digital_media", "camera_media"),
    "tambourine": ("culture_objects", "music"),
    "memosprite": ("creatures", "fantasy_creature"),
    "shuangyaji": ("hair", "hair_style"),
    "grand_scale": ("composition", "shot"),
    "orca_girl": ("people", "fantasy_person"),
    "boutonniere": ("accessories", "badges_ornaments"),
    "small_chastity_cage": ("adult", "adult_fetish"),
    "prostration": ("pose", "stationary_pose"),
    "blue_shrug": ("clothes_main", "outerwear"),
    "worm": ("creatures", "other_creature"),
    "tart_(food)": ("food_drink", "bakery"),
    "squeezing": ("action", "interaction"),
    "psychic": ("people", "fantasy_person"),
    "digital_dissolve": ("light_effect", "other_effect"),
    "tsumami_kanzashi": ("hair", "hair_accessory"),
    "lime_slice": ("food_drink", "fruit_vegetable"),
    "wood": ("nature", "plant"),
    "weights": ("recreation", "sports"),
    "shark_fin": ("creatures", "claw_scale"),
    "piledriver_(sex)": ("adult", "adult_sex"),
    "game_development_department_(blue_archive)": ("relationships", "group_faction"),
    "translucent_bunnysuit": ("adult", "adult_clothes"),
    "baking": ("action", "daily_action"),
    "cardiogram": ("text_meta", "screen_ui"),
    "buried": ("body", "body_state"),
    "brass_knuckles": ("weapons", "blunt_chain"),
    "hotpot": ("food_drink", "staple_food"),
    "mud": ("outdoor_scene", "terrain_surface"),
    "super_saiyan_blue": ("themes", "persona_variant"),
    "organs": ("adult", "adult_anatomy"),
    "travel_attendant": ("people", "occupation"),
    "wreckage": ("outdoor_scene", "other_scene"),
    "prince": ("people", "role_focus"),
    "long_toenails": ("body", "arms_hands_feet"),
    "cockroach": ("creatures", "insect"),
    "worldwide_miku": ("themes", "persona_variant"),
    "heart-shaped_boob_challenge": ("meta_info", "meme"),
    "guimpe": ("clothes_main", "tops"),
    "cute_&_girly_(idolmaster)": ("clothes_special", "themed_costume"),
    "cupboard": ("household_objects", "storage_furniture"),
    "jug_(bottle)": ("food_drink", "tableware"),
    "gun_on_back": ("weapons", "firearm"),
    "cryokinesis": ("light_effect", "magic_effect"),
    "fireball": ("light_effect", "magic_effect"),
    "masu": ("food_drink", "tableware"),
    "a-pose": ("pose", "body_pose"),
    "remembering": ("themes", "narrative_situation"),
    "wind_turbine": ("mech_scifi", "machine"),
    "magnet": ("household_objects", "tools"),
    "battleship": ("transport_play", "water_vehicle"),
    "railroad_crossing": ("indoor_scene", "urban"),
    "implied_pregnancy": ("body", "body_state"),
    "aeug": ("relationships", "group_faction"),
    "flippers": ("recreation", "sports"),
    "plant_hair": ("hair", "hair_action"),
    "diorama": ("recreation", "toys"),
    "z-ring": ("accessories", "jewelry"),
    "wok": ("food_drink", "tableware"),
    "elvaan": ("people", "fantasy_person"),
    "bipod": ("weapons", "firearm"),
    "kappa": ("creatures", "fantasy_creature"),
    "tomato_slice": ("food_drink", "fruit_vegetable"),
    "sexual_coaching": ("adult", "adult_sex"),
    "fishnet_bodystocking": ("underwear_swim", "bodysuit_leotard"),
    "dream_soul": ("light_effect", "magic_effect"),
    "swirl": ("light_effect", "optical"),
    "shippou_(pattern)": ("clothing_detail", "clothing_pattern"),
    "pin": ("accessories", "other_accessory"),
    "cue_stick": ("recreation", "sports"),
    "bolt_(hardware)": ("household_objects", "tools"),
    "bamboo_shoot": ("food_drink", "fruit_vegetable"),
    "gigantamax": ("themes", "identity_change"),
    "iridescent": ("light_effect", "palette"),
    "plumeria": ("nature", "plant"),
    "fading": ("light_effect", "other_effect"),
    "orca": ("creatures", "aquatic"),
    "menacing_(jojo)": ("text_meta", "comic"),
    "party": ("themes", "narrative_situation"),
    "breaker_gorgon": ("accessories", "eyewear"),
    "ruining_the_glorious_moment": ("meta_info", "meme"),
    "flailing": ("action", "movement"),
    "season_connection": ("themes", "character_connection"),
    "credits_page": ("meta_info", "meta"),
    "cowboy": ("people", "occupation"),
    "concrete": ("indoor_scene", "surface"),
    "patterned_hair": ("hair", "hair_action"),
    "on_stairs": ("pose", "body_pose"),
    "mojyo": ("people", "role_focus"),
    "large_syringe": ("household_objects", "tools"),
    "uncle_and_niece": ("relationships", "family_relation"),
    "alcohol_carton": ("household_objects", "container"),
    "sukusuku_hakutaku": ("recreation", "toys"),
    "yaopei": ("accessories", "other_accessory"),
    "fist_pump": ("pose", "hand_gesture"),
    "fakemon": ("creatures", "fantasy_creature"),
    "xiangyun": ("clothing_detail", "clothing_pattern"),
    "price_tag": ("text_meta", "text"),
    "mizu_happi": ("clothes_special", "traditional_east"),
    "manta_ray": ("creatures", "aquatic"),
    "visual_novel": ("style", "medium"),
    "convertible": ("transport_play", "land_vehicle"),
    "kanshou_&_bakuya_(fate)": ("weapons", "magic_weapon"),
    "casing_ejection": ("action", "combat_action"),
    "tank_turret": ("mech_scifi", "machine"),
    "blob": ("creatures", "fantasy_creature"),
    "sway_back": ("pose", "body_pose"),
    "shaking_head": ("pose", "body_pose"),
    "reloading": ("action", "combat_action"),
    "mimic": ("creatures", "fantasy_creature"),
    "fusuma": ("indoor_scene", "architecture"),
    "musket": ("weapons", "firearm"),
    "comedic_sweatdrop": ("text_meta", "comic"),
    "animal_around_neck": ("pose", "body_pose"),
    "tentacle_girl": ("people", "fantasy_person"),
    "gesugao": ("expression", "anger"),
    "band_(music)": ("relationships", "group_faction"),
    "film_strip": ("digital_media", "camera_media"),
    "school_gym": ("indoor_scene", "public_indoor"),
    "barbell": ("recreation", "sports"),
    "mechanic": ("people", "occupation"),
    "groceries": ("food_drink", "staple_food"),
    "boxing": ("recreation", "sports"),
    "translucent": ("light_effect", "optical"),
    "tacet_discord_(wuthering_waves)": ("creatures", "fantasy_creature"),
    "recurring_image": ("meta_info", "meta"),
    "sanbaka_(nijisanji)": ("relationships", "group_faction"),
    "lane_line": ("indoor_scene", "urban"),
    "wiping": ("action", "daily_action"),
    "banana_peel": ("food_drink", "fruit_vegetable"),
    "species_connection": ("themes", "character_connection"),
    "announcement_celebration": ("meta_info", "meta"),
    ":c": ("expression", "sad_cry"),
    "sounding": ("adult", "adult_fetish"),
    "canteen": ("household_objects", "container"),
    "asahi_breweries": ("text_meta", "brand"),
    "rattle": ("recreation", "toys"),
    "muffin": ("food_drink", "bakery"),
    "telstar": ("mech_scifi", "scifi_device"),
    "food_insertion": ("adult", "adult_fetish"),
    "diving": ("recreation", "sports"),
    "iv_stand": ("household_objects", "tools"),
    "grilling": ("action", "daily_action"),
    "country_connection": ("themes", "character_connection"),
    "bouncing": ("action", "movement"),
    "mistletoe": ("nature", "plant"),
    "liquor": ("food_drink", "drink"),
    "nipple-to-nipple": ("adult", "adult_sex"),
    "minigun": ("weapons", "firearm"),
    "shinigami": ("people", "fantasy_person"),
    "russo-ukrainian_war": ("themes", "narrative_situation"),
    "mansion": ("indoor_scene", "architecture"),
    "dirt_road": ("outdoor_scene", "terrain_surface"),
    "blue_blood": ("body", "body_state"),
    "standard_bearer": ("people", "occupation"),
    "namekian": ("people", "fantasy_person"),
    "sukeban": ("people", "role_focus"),
    "priestess": ("people", "occupation"),
    "pillory": ("adult", "adult_fetish"),
    "clothes_theft": ("action", "interaction"),
    "zenra": ("adult", "adult_nudity"),
    "lifeguard": ("people", "occupation"),
    "hair_over_face": ("hair", "bangs"),
    "binary": ("text_meta", "text"),
    "slouching": ("pose", "body_pose"),
    "black_bustier": ("underwear_swim", "bra_lingerie"),
    "severed_hair": ("hair", "hair_action"),
    "w_over_eye": ("body", "body_marks"),
    "beretta_1301": ("weapons", "firearm"),
    "arguing": ("action", "interaction"),
    "variable_fighter": ("transport_play", "air_vehicle"),
    "crisis_management_form_(machikado_mazoku)": ("themes", "persona_variant"),
    "amazon_warrior": ("people", "occupation"),
    "fender_jazz_bass": ("culture_objects", "music"),
    "cuisses": ("clothes_special", "armor"),
    "rosary": ("accessories", "jewelry"),
    "lance_of_longinus_(evangelion)": ("weapons", "magic_weapon"),
    "halfling": ("people", "fantasy_person"),
    "black_sarong": ("clothes_special", "traditional_world"),
    "yellow_tulip": ("nature", "plant"),
    "wet_face": ("body", "body_state"),
    "mauser_98": ("weapons", "firearm"),
    "flattop": ("hair", "hair_style"),
    "ainu": ("people", "role_focus"),
    "on_rooftop": ("pose", "body_pose"),
    "major_injury_underreaction": ("expression", "neutral_expression"),
    "beaker": ("household_objects", "tools"),
    "flintlock": ("weapons", "firearm"),
    "map_(object)": ("culture_objects", "books_paper"),
    "relaxing": ("action", "daily_action"),
    "puzzle_piece": ("recreation", "games"),
    "felyne": ("creatures", "fantasy_creature"),
    "bruised_eye": ("body", "body_marks"),
    "blue_oni": ("creatures", "fantasy_creature"),
    "to_be_continued": ("text_meta", "text"),
    "primarch": ("people", "fantasy_person"),
    "evoker": ("weapons", "magic_weapon"),
    "bell-bottoms": ("clothes_main", "bottoms"),
    "crossed_wrists": ("pose", "hand_gesture"),
    "stahlhelm": ("clothes_special", "helmet"),
    "shoulder_patch": ("accessories", "badges_ornaments"),

    # Revisions prompted by the same domain audit.
    "x3": ("expression", "positive"),
    "cast": ("clothes_special", "helmet_protective"),
    "grid": ("outdoor_scene", "background_pattern"),
    "searchlight": ("light_effect", "lighting"),
    "nihonga": ("style", "art_style"),
})


EXACT_OVERRIDES.update({
    # Third pass: remaining unambiguous objects, actions and named concepts.
    "don't_say_\"lazy\"": ("meta_info", "meme"),
    "mtu_virus": ("themes", "identity_change"),
    "ambrosia_(dungeon_meshi)": ("weapons", "magic_weapon"),
    "action": ("themes", "narrative_situation"),
    "paralyzer": ("weapons", "firearm"),
    "condenser_unit": ("household_objects", "appliance"),
    "ak-47": ("weapons", "firearm"),
    "mosin-nagant": ("weapons", "firearm"),
    "trapped": ("body", "body_state"),
    "ai_ai_gasa": ("relationships", "romance_orientation"),
    "biwa_lute": ("culture_objects", "music"),
    "wakamezake": ("adult", "adult_fetish"),
    "revealing_layer": ("clothing_detail", "clothing_state"),
    "miracle_mallet": ("weapons", "magic_weapon"),
    "popsicle_stick": ("household_objects", "other_object"),
    "toothpick": ("household_objects", "tools"),
    "sextuplets": ("relationships", "family_relation"),
    "rabbit_on_head": ("pose", "body_pose"),
    "circular_saw": ("household_objects", "tools"),
    "yakisoba": ("food_drink", "staple_food"),
    "screw_in_head": ("mech_scifi", "cybernetic"),
    "time_stop": ("light_effect", "magic_effect"),
    "pendant_watch": ("household_objects", "clock"),
    "chimera_(honkai:_star_rail)": ("creatures", "fantasy_creature"),
    "mousetrap": ("household_objects", "tools"),
    "foregrip": ("weapons", "firearm"),
    "seraph": ("people", "fantasy_person"),
    ";(": ("expression", "sad_cry"),
    "bull": ("creatures", "mammal"),
    "kiwi_slice": ("food_drink", "fruit_vegetable"),
    "purple_corset": ("underwear_swim", "bra_lingerie"),
    "kriss_vector": ("weapons", "firearm"),
    "feixianji_(hairstyle)": ("hair", "hair_style"),
    "person_on_head": ("pose", "body_pose"),
    "racing": ("recreation", "sports"),
    "typing": ("action", "daily_action"),
    "udon": ("food_drink", "staple_food"),
    "kyuudou": ("recreation", "sports"),
    "tile_roof": ("indoor_scene", "architecture"),
    "shout_lines": ("text_meta", "comic"),
    "tactile_paving": ("indoor_scene", "urban"),
    "joker_(playing_card)": ("recreation", "games"),
    "control_rod_(touhou)": ("weapons", "magic_weapon"),
    "crutch": ("household_objects", "tools"),
    "pear": ("food_drink", "fruit_vegetable"),
    "problem_solver_68_(blue_archive)": ("relationships", "group_faction"),
    "neta": ("meta_info", "meme"),
    "fishbowl": ("household_objects", "container"),
    "poison": ("body", "body_state"),
    "oran_berry": ("food_drink", "fruit_vegetable"),
    "military_operator": ("people", "occupation"),
    "clinging": ("action", "interaction"),
    "cbt": ("adult", "adult_fetish"),
    "oyakodon_(sex)": ("adult", "adult_sex"),
    "limiter_(tsukumo_sana)": ("accessories", "other_accessory"),
    "bisexual_male": ("relationships", "romance_orientation"),
    "senbei": ("food_drink", "dessert_snack"),
    "too_literal": ("meta_info", "meme"),
    "jiaozi": ("food_drink", "staple_food"),
    "bellflower": ("nature", "plant"),
    "furious": ("expression", "anger"),
    "spiked_headband": ("accessories", "headwear"),
    "hatsumode": ("time_weather", "holiday"),
    "tiefling": ("people", "fantasy_person"),
    "gold_buckle": ("clothing_detail", "clothing_structure"),
    "nagatekkou": ("accessories", "handwear"),
    "dynamite": ("weapons", "explosive"),
    "vomiting": ("body", "body_state"),
    "drawing_on_another's_face": ("action", "interaction"),
    "gryffindor": ("relationships", "group_faction"),
    "seed": ("nature", "plant"),
    "soy_sauce": ("food_drink", "staple_food"),
    "spurs": ("accessories", "other_accessory"),
    "underworld_(ornament)": ("accessories", "badges_ornaments"),
    "dullahan": ("creatures", "fantasy_creature"),

    # Corrections found while reviewing the second-pass destinations.
    "oversized_limbs": ("body", "build"),
    "drowning": ("action", "movement"),
    "spines": ("creatures", "claw_scale"),
    "carapace": ("creatures", "claw_scale"),
    "test_plugsuit_(evangelion)": ("underwear_swim", "bodysuit_leotard"),
    "skull_on_head": ("accessories", "headwear"),
    "paper_on_head": ("accessories", "headwear"),
    "jeweled_branch_of_hourai": ("accessories", "badges_ornaments"),
    "haramaki": ("clothing_detail", "other_clothes"),
    "tank_turret": ("weapons", "firearm"),
    "shark_fin": ("accessories", "headwear"),
    "patterned_hair": ("hair", "hair_style"),
    "plant_hair": ("hair", "hair_style"),
    "animal_around_neck": ("accessories", "neckwear"),
    "sukusuku_hakutaku": ("themes", "persona_variant"),
    "pin": ("household_objects", "tools"),
    "wood": ("household_objects", "other_object"),

    # Existing-rule regression fixes discovered by scanning every populated
    # category after the folder split.
    "water": ("outdoor_scene", "water_scene"),
    "in_water": ("outdoor_scene", "water_scene"),
    "shallow_water": ("outdoor_scene", "water_scene"),
    "on_water": ("outdoor_scene", "water_scene"),
    "grey_background": ("outdoor_scene", "background_plain"),
    "blue_background": ("outdoor_scene", "background_plain"),
    "pink_background": ("outdoor_scene", "background_plain"),
    "yellow_background": ("outdoor_scene", "background_plain"),
    "red_background": ("outdoor_scene", "background_plain"),
    "green_background": ("outdoor_scene", "background_plain"),
    "purple_background": ("outdoor_scene", "background_plain"),
    "brown_background": ("outdoor_scene", "background_plain"),
    "orange_background": ("outdoor_scene", "background_plain"),
    "aqua_background": ("outdoor_scene", "background_plain"),
    "dark_background": ("outdoor_scene", "background_plain"),
    "cropped_torso": ("composition", "framing"),
    "cropped_legs": ("composition", "framing"),
    "cropped_arms": ("composition", "framing"),
    "cropped_head": ("composition", "framing"),
    "breasts_out": ("adult", "adult_nudity"),
    "one_breast_out": ("adult", "adult_nudity"),
    "joints": ("body", "arms_hands_feet"),
    "armpit_hair": ("body", "arms_hands_feet"),
    "hugging_object": ("action", "holding"),
    "food_on_face": ("body", "body_marks"),
    "pelvic_curtain": ("clothing_detail", "clothing_structure"),
    "floating_object": ("light_effect", "other_effect"),
})


EXACT_OVERRIDES.update({
    # Fourth pass over the now mostly specialised long tail.
    "heavy": ("body", "body_state"),
    "unkempt": ("hair", "hair_action"),
    "texture": ("style", "medium"),
    "sleigh": ("transport_play", "land_vehicle"),
    "regional_and_normal": ("themes", "persona_variant"),
    "female_rimming_male": ("adult", "adult_oral"),
    "hiding_behind_another": ("action", "interaction"),
    "blowhole": ("creatures", "animal_feature"),
    "rubik's_cube": ("recreation", "games"),
    "spray_paint": ("culture_objects", "stationery"),
    "yandere_trance": ("expression", "anger"),
    "ankle_garter": ("accessories", "other_accessory"),
    "inward_v": ("pose", "body_pose"),
    "burnt": ("body", "body_state"),
    "en_pointe": ("pose", "stationary_pose"),
    "hatsumoude": ("time_weather", "holiday"),
    "stacking": ("action", "daily_action"),
    "you're_not_helping": ("meta_info", "meme"),
    "saint_quartz_(fate)": ("nature", "mineral"),
    "tofu": ("food_drink", "staple_food"),
    "dirigible": ("transport_play", "air_vehicle"),
    "snow_on_head": ("body", "body_marks"),
    "chisel": ("household_objects", "tools"),
    "kagura_suzu": ("culture_objects", "music"),
    "crucifixion": ("adult", "adult_gore"),
    "calvin_klein": ("text_meta", "brand"),
    "catching": ("action", "holding"),
    "reindeer_girl": ("people", "fantasy_person"),
    "mygo!!!!!_(bang_dream!)": ("relationships", "group_faction"),
    "oversized_forearms": ("body", "build"),
    "persimmon": ("food_drink", "fruit_vegetable"),
    "neck_garter": ("accessories", "neckwear"),
    "cocktail_shaker": ("food_drink", "tableware"),
    "originium_arts_(arknights)": ("light_effect", "magic_effect"),
    "stone_walkway": ("outdoor_scene", "terrain_surface"),
    "brand_of_the_exalt": ("body", "body_marks"),
    "email_address": ("text_meta", "text"),
    "carton": ("household_objects", "container"),
    "clarent_(fate)": ("weapons", "magic_weapon"),
    "conch": ("creatures", "aquatic"),
    "glands_of_montgomery": ("adult", "adult_anatomy"),
    "hay": ("nature", "plant"),
    "hedge": ("nature", "plant"),
    "bell_pepper": ("food_drink", "fruit_vegetable"),
    "other_with_female": ("people", "count_gender"),
    "beehive_hairdo": ("hair", "hair_style"),
    "sprout": ("nature", "plant"),
    "signpost": ("indoor_scene", "urban"),
    "washing": ("action", "daily_action"),
    "siren_(azur_lane)": ("people", "fantasy_person"),
    "red_tulip": ("nature", "plant"),
    "load_bearing_equipment": ("clothes_special", "helmet_protective"),
    "fly": ("creatures", "insect"),
    "daikon": ("food_drink", "fruit_vegetable"),
    "pink_sarong": ("clothes_special", "traditional_world"),
    "naizuri": ("adult", "adult_sex"),
    "rina-chan_board": ("accessories", "eyewear"),
    "laser_sight": ("weapons", "firearm"),
    "slide": ("recreation", "toys"),
    "pitchfork": ("weapons", "polearm"),
    "windsock": ("household_objects", "tools"),
    "vodka": ("food_drink", "drink"),
    "eggshell": ("food_drink", "dairy_ingredient"),
    "fanning_face": ("action", "daily_action"),
    "waffle": ("food_drink", "bakery"),
    "foodgasm": ("adult", "adult_suggestive"),
    "plackart": ("clothes_special", "armor"),
    "queen": ("people", "role_focus"),
    "animal_charm": ("accessories", "jewelry"),
    "turret": ("weapons", "firearm"),
    "sobbing": ("expression", "sad_cry"),
    "black_keys_(type-moon)": ("weapons", "magic_weapon"),
    "apple_slice": ("food_drink", "fruit_vegetable"),
    "senkou_hanabi": ("light_effect", "fire_smoke"),
    "swallowing": ("action", "daily_action"),
    "lion_mane": ("creatures", "animal_feature"),
    "white_tulip": ("nature", "plant"),
    "flagpole": ("indoor_scene", "urban"),
    "keyring": ("accessories", "other_accessory"),
    "crosshair": ("text_meta", "screen_ui"),
    "usb": ("digital_media", "phone_computer"),
    "shakujou": ("weapons", "polearm"),
    "chiton": ("clothes_special", "traditional_world"),
    "himejoshi": ("people", "role_focus"),
    "fever": ("body", "body_state"),
    "gorilla": ("creatures", "mammal"),
    "swing_set": ("recreation", "toys"),
    "shoujo_kitou-chuu": ("meta_info", "meme"),
    "suikawari": ("recreation", "games"),
    "tendril": ("nature", "plant"),
    "initial": ("text_meta", "text"),
    "lampshade": ("household_objects", "lighting_clock"),
    "on_tree_stump": ("pose", "body_pose"),
    "tanghulu": ("food_drink", "dessert_snack"),
    "stocks": ("adult", "adult_fetish"),
    "cheese_trail": ("food_drink", "dairy_ingredient"),
    "lei": ("accessories", "neckwear"),

    # Final destination corrections from cross-agent wiki comparison.
    "dragon_bean_(arknights)": ("themes", "persona_variant"),
    "mtu_virus": ("meta_info", "meme"),
    "breaker_gorgon": ("themes", "persona_variant"),
    "implied_pregnancy": ("themes", "narrative_situation"),
    "organs": ("adult", "adult_gore"),
    "wakamezake": ("adult", "adult_oral"),
})


EXACT_OVERRIDES.update({
    # Fifth pass: high-confidence everyday, cultural and franchise-independent
    # concepts that were still visible at the top of the conservative bucket.
    "delivery": ("action", "daily_action"),
    "pomegranate": ("food_drink", "fruit_vegetable"),
    "laurels": ("accessories", "headwear"),
    "greenhouse": ("indoor_scene", "architecture"),
    "symbiote": ("creatures", "fantasy_creature"),
    "tantrum": ("expression", "anger"),
    "comiket": ("meta_info", "meta"),
    "ankleband": ("accessories", "other_accessory"),
    "blood_spray": ("adult", "adult_gore"),
    "paperclip": ("culture_objects", "stationery"),
    "kittysuit": ("clothes_special", "themed_costume"),
    "golem": ("creatures", "fantasy_creature"),
    "glory_hole": ("adult", "adult_fetish"),
    "condom_left_inside": ("adult", "adult_sex"),
    "moe_moe_kyun!": ("meta_info", "meme"),
    "housewife": ("people", "occupation"),
    "cheek_rest": ("pose", "hand_gesture"),
    "dome": ("indoor_scene", "architecture"),
    "cat's_cradle": ("recreation", "games"),
    "alternate_shiny_pokemon": ("themes", "persona_variant"),
    "science_babies": ("themes", "narrative_situation"),
    "heart_straw": ("food_drink", "tableware"),
    "horse_racing_track": ("recreation", "sports"),
    "sword_tassel": ("accessories", "badges_ornaments"),
    "sinking": ("action", "movement"),
    "chibi_on_head": ("pose", "body_pose"),
    "interview": ("action", "daily_action"),
    "welsh_corgi": ("creatures", "mammal"),
    "measurements": ("action", "daily_action"),
    "toasting_(gesture)": ("action", "interaction"),
    "fender_telecaster": ("culture_objects", "music"),
    "training": ("recreation", "sports"),
    "tucked_money": ("action", "holding"),
    "egg_yolk": ("food_drink", "dairy_ingredient"),
    "bakeneko": ("creatures", "fantasy_creature"),
    "cd_case": ("household_objects", "container"),
    ":s": ("expression", "fear_surprise"),
    "intimidating": ("expression", "anger"),
    "scratching": ("action", "daily_action"),
    "dizi": ("culture_objects", "music"),
    "eotech": ("weapons", "firearm"),
    "shogi": ("recreation", "games"),
    "iei": ("culture_objects", "books_paper"),
    "after_battle": ("themes", "narrative_situation"),
    "oonusa": ("accessories", "other_accessory"),
    "red_sun": ("text_meta", "symbol"),
    "pitching": ("recreation", "sports"),
    "icicle": ("time_weather", "weather"),
    "imitating": ("action", "interaction"),
    "whistling": ("action", "daily_action"),
    "cowering": ("pose", "body_pose"),
    "crinoline": ("underwear_swim", "underwear_design"),
    "mailbox_(incoming_mail)": ("household_objects", "container"),
    "stamp_mark": ("text_meta", "symbol"),
    "camping": ("outdoor_scene", "forest_field"),
    "wide_face": ("body", "build"),
    "germany": ("outdoor_scene", "other_scene"),
    "can't_be_this_cute": ("meta_info", "meme"),
    "lectern": ("household_objects", "seating_table"),
    "aztec": ("people", "role_focus"),
    "apologizing": ("action", "interaction"),
    "mamemaki": ("time_weather", "holiday"),
    "garland_(decoration)": ("accessories", "badges_ornaments"),
    "against_window": ("pose", "body_pose"),
    "on_crescent": ("pose", "body_pose"),
    "basketball_hoop": ("recreation", "sports"),
    "flat_chastity_cage": ("adult", "adult_fetish"),
    "soba": ("food_drink", "staple_food"),
    "accidental_pervert": ("adult", "adult_suggestive"),
    "violence": ("action", "combat_action"),
    "natural_wedgie": ("clothing_detail", "clothing_state"),
    "salmon_run_(splatoon)": ("recreation", "games"),
    "scolding": ("action", "interaction"),
    "russia": ("outdoor_scene", "other_scene"),
    "nuzzle": ("action", "interaction"),
    "yoga": ("recreation", "sports"),
    "rowboat": ("transport_play", "water_vehicle"),
    "single_sode": ("clothing_detail", "clothing_structure"),
    "multicolored_stripes": ("clothing_detail", "clothing_pattern"),
    "enema": ("adult", "adult_fetish"),
    "black_liquid": ("light_effect", "other_effect"),
    "chipmunk_girl": ("people", "fantasy_person"),
    "genre_connection": ("themes", "character_connection"),
    "cracking_knuckles": ("pose", "hand_gesture"),
    "cymbals": ("culture_objects", "music"),
    "rolling": ("action", "movement"),
    "gambeson": ("clothes_special", "armor"),
    "ruyi_jingu_bang": ("weapons", "magic_weapon"),
    "compact_(cosmetics)": ("face", "makeup"),
    "middle_part": ("hair", "hair_style"),
    "drain_(object)": ("household_objects", "other_object"),
    "toothpaste": ("household_objects", "tools"),
    "kite": ("recreation", "toys"),
    "mazda": ("text_meta", "brand"),
    "implied_nudity": ("adult", "adult_nudity"),
    "komainu_boy": ("people", "fantasy_person"),
    "pansy": ("nature", "plant"),
    "yuki_onna": ("people", "fantasy_person"),
    "rooster": ("creatures", "bird"),
    "irezumi": ("body", "body_marks"),
    "followers_favorite_challenge": ("meta_info", "meme"),
    "shindan_maker": ("meta_info", "meta"),
    "hashitsuki_nata": ("weapons", "blade"),
    "mint": ("nature", "plant"),
    "empty_picture_frame": ("household_objects", "other_object"),
    "super_saiyan_2": ("themes", "persona_variant"),
    "despair": ("expression", "sad_cry"),
    "kosode": ("clothes_special", "traditional_east"),
    "canopy_(aircraft)": ("transport_play", "air_vehicle"),
    "koinobori": ("time_weather", "holiday"),
    "handrail": ("indoor_scene", "architecture"),
    "rubbing": ("action", "interaction"),
    "kamina_shades": ("accessories", "eyewear"),
    "squat_toilet": ("household_objects", "other_object"),
    "traffic_baton": ("household_objects", "tools"),
    "satellite_dish": ("digital_media", "camera_media"),
    "shiromuku": ("clothes_special", "traditional_east"),
})


EXACT_OVERRIDES.update({
    # Sixth pass: current high-frequency tail after the previous audit batches.
    "dragon_bubble_(arknights)": ("themes", "persona_variant"),
    "cornrows": ("hair", "hair_style"),
    "mami_mogu_mogu": ("meta_info", "meme"),
    "pony_(animal)": ("creatures", "mammal"),
    "tickle_torture": ("adult", "adult_fetish"),
    "luxury_(idolmaster)": ("clothes_special", "themed_costume"),
    "milkshake": ("food_drink", "drink"),
    "jackal_boy": ("people", "fantasy_person"),
    "tuna": ("food_drink", "meat_seafood"),
    "kimi_to_semi_blue_(idolmaster)": ("clothes_special", "themed_costume"),
    "electrocution": ("action", "combat_action"),
    "mousepad_(object)": ("digital_media", "phone_computer"),
    "bakery": ("indoor_scene", "commercial"),
    "colored_condom": ("adult", "adult_fetish"),
    "hanafuda": ("recreation", "games"),
    "military_fatigues": ("clothes_special", "occupation_uniform"),
    "too_many_cats": ("meta_info", "meme"),
    "cream_puff": ("food_drink", "bakery"),
    "orchid": ("nature", "plant"),
    "angels_of_delusion": ("relationships", "group_faction"),
    "hane_(hanetsuki)": ("recreation", "sports"),
    "twig": ("nature", "plant"),
    "stuffing": ("food_drink", "staple_food"),
    "throat_bulge": ("adult", "adult_oral"),
    "black_bandages": ("clothes_special", "helmet_protective"),
    "panda_boy": ("people", "fantasy_person"),
    "slytherin": ("relationships", "group_faction"),
    "boombox": ("digital_media", "camera_media"),
    "numbers_(nanoha)": ("relationships", "group_faction"),
    "lgbt_pride": ("relationships", "romance_orientation"),
    "hidden_face": ("composition", "framing"),
    "baseball_stadium": ("recreation", "sports"),
    "nori_(seaweed)": ("food_drink", "fruit_vegetable"),
    "queen_(playing_card)": ("recreation", "games"),
    "tailjob": ("adult", "adult_sex"),
    "red_panda_girl": ("people", "fantasy_person"),
    "traffic": ("indoor_scene", "urban"),
    "nigirizushi": ("food_drink", "staple_food"),
    "very_hairy": ("body", "body_state"),
    "depth_charge": ("weapons", "explosive"),
    "digital_thermometer": ("household_objects", "tools"),
    "game_boy_(original)": ("digital_media", "phone_computer"),
    "confrontation": ("action", "combat_action"),
    "puzzle": ("recreation", "games"),
    "songover": ("meta_info", "meta"),
    "kidnapping": ("action", "combat_action"),
    "incense": ("household_objects", "other_object"),
    "sail": ("transport_play", "water_vehicle"),
    "perverted_utility": ("adult", "adult_fetish"),
    "bunting": ("accessories", "badges_ornaments"),
    "pinky_swear": ("pose", "hand_gesture"),
    "suneate": ("clothes_special", "armor"),
    "red_bull": ("text_meta", "brand"),
    "exposed_bone": ("adult", "adult_gore"),
    "arisaka": ("weapons", "firearm"),
    "multiple_monitors": ("digital_media", "phone_computer"),
    "so_moe_i'm_gonna_die!": ("meta_info", "meme"),
    "diagram": ("text_meta", "screen_ui"),
    "trolling": ("meta_info", "meme"),
    "snowboard": ("recreation", "sports"),
    "hot_air_balloon": ("transport_play", "air_vehicle"),
    "nerv": ("relationships", "group_faction"),
    "stirring": ("action", "daily_action"),
    "coughing": ("action", "daily_action"),
    "turkey_(food)": ("food_drink", "meat_seafood"),
    "...!": ("text_meta", "comic"),
    "coffee_maker": ("household_objects", "appliance"),
    "weasel": ("creatures", "mammal"),
    "starfighter": ("transport_play", "air_vehicle"),
    "at_gunpoint": ("action", "combat_action"),
    "brick_road": ("outdoor_scene", "terrain_surface"),
    "kataginu": ("clothes_special", "traditional_east"),
    "clam": ("food_drink", "meat_seafood"),
    "arched_window": ("indoor_scene", "architecture"),
    "floating_head": ("body", "body_state"),
    "reverse_netorare": ("adult", "adult_other"),
    "carnation": ("nature", "plant"),
    "heavenly_boat_maanna": ("transport_play", "air_vehicle"),
    "horrified": ("expression", "fear_surprise"),
    "strong_zero": ("food_drink", "drink"),
    "target": ("recreation", "sports"),
    "paint_tube": ("culture_objects", "stationery"),
    "ipod_nano": ("digital_media", "camera_media"),
    "shaved_head": ("hair", "hair_style"),
    "garnish": ("food_drink", "staple_food"),
    "millennium_puzzle": ("accessories", "neckwear"),
    "vomit": ("adult", "adult_fluid"),
    "medicine": ("household_objects", "tools"),
    "grease_(mechanical)": ("mech_scifi", "machine"),
    "gelatin": ("food_drink", "dairy_ingredient"),
    "animal_skeleton": ("creatures", "other_creature"),
    "shish_kebab": ("food_drink", "staple_food"),
    "string_of_light_bulbs": ("household_objects", "lighting_clock"),
    "sliding": ("action", "movement"),
    "rose_bush": ("nature", "plant"),
    "chao_(sonic)": ("creatures", "fantasy_creature"),
    "yabi_fashion": ("clothes_special", "themed_costume"),
    "imperial_japanese_navy": ("relationships", "group_faction"),
    "radar": ("mech_scifi", "scifi_device"),
    "pinecone": ("nature", "plant"),
    "cattail": ("nature", "plant"),
    "virtual_reality": ("mech_scifi", "scifi_device"),
    "cassette_player": ("digital_media", "camera_media"),
    "cassette_tape": ("digital_media", "camera_media"),
    "spasm": ("body", "body_state"),
    "spraying": ("action", "daily_action"),
    "dj": ("people", "occupation"),
    "gerbera": ("nature", "plant"),
    "chinstrap_beard": ("face", "facial_hair"),
    "kneeless_merfolk": ("people", "fantasy_person"),
    "flesh": ("adult", "adult_gore"),
    "peeling": ("action", "daily_action"),
    "byakugan": ("face", "eye_shape"),
    "sunken_cheeks": ("face", "brows_nose"),
    "railgun": ("weapons", "firearm"),
    "ethereal_(zenless_zone_zero)": ("creatures", "fantasy_creature"),
})


EXACT_OVERRIDES.update({
    # Independently reviewed continuation of the long tail.  Grouped exact
    # entries keep the audit readable without introducing risky substring rules.
    **dict.fromkeys(("other_with_male",), ("people", "count_gender")),
    **dict.fromkeys(("toddler",), ("people", "age")),
    **dict.fromkeys(("fujoshi", "prisoner", "banchou"), ("people", "role_focus")),
    **dict.fromkeys(("tour_guide", "firefighter", "flight_attendant"), ("people", "occupation")),
    **dict.fromkeys(("panda_girl", "togruta", "ferret_girl", "rito", "hume", "slug_girl", "komainu_girl"), ("people", "fantasy_person")),
    **dict.fromkeys(("rivalry", "teamwork"), ("relationships", "social_relation")),
    **dict.fromkeys(("u.n._spacy", "ave_mujica_(bang_dream!)", "inner_senshi", "s.e.e.s", "paradeus", "sos_brigade", "wehrmacht", "noctchill_(idolmaster)", "bnw_(umamusume)"), ("relationships", "group_faction")),
    **dict.fromkeys(("bimbofication", "foodification", "petrification"), ("themes", "identity_change")),
    **dict.fromkeys(("official_alternate_design", "fatter_than_canon", "alternate_size", "alternate_height"), ("themes", "persona_variant")),
    **dict.fromkeys(("mixed_signals", "kidnapped", "rejection", "taking_shelter", "bait_and_switch", "in_cage", "threat", "clumsy", "for_adoption"), ("themes", "narrative_situation")),
    **dict.fromkeys(("stage_connection",), ("themes", "character_connection")),
    **dict.fromkeys(("emaciated", "big_head", "weight_gain", "weight"), ("body", "build")),
    **dict.fromkeys(("back_muscles", "deltoids"), ("body", "chest")),
    **dict.fromkeys(("triceps",), ("body", "arms_hands_feet")),
    **dict.fromkeys(("fainting",), ("body", "body_state")),
    **dict.fromkeys(("heart_on_cheek",), ("body", "body_marks")),
    **dict.fromkeys(("huadian",), ("face", "makeup")),
    **dict.fromkeys(("connected_beard",), ("face", "facial_hair")),
    **dict.fromkeys(("living_hair", "impossible_hair", "translucent_hair"), ("hair", "hair_action")),
    **dict.fromkeys(("veiny_face", "dx"), ("expression", "anger")),
    **dict.fromkeys((";<", "disappointed"), ("expression", "sad_cry")),
    **dict.fromkeys(("resting",), ("pose", "stationary_pose")),
    **dict.fromkeys(("against_fence",), ("pose", "body_pose")),
    **dict.fromkeys(("mudra", "bent_v"), ("pose", "hand_gesture")),
    **dict.fromkeys(("picking_up",), ("action", "holding")),
    **dict.fromkeys(("faceplant",), ("action", "movement")),
    **dict.fromkeys(("catfight", "uppercut", "trampling", "headlock", "clash"), ("action", "combat_action")),
    **dict.fromkeys(("pinching_another's_belly", "tickling_sides", "begging", "imminent_bite", "biting_cheek", "food_theft", "snowball_fight"), ("action", "interaction")),
    **dict.fromkeys(("knitting", "watering", "sweeping", "tasting"), ("action", "daily_action")),
    **dict.fromkeys(("orange_tabard",), ("clothes_main", "tops")),
    **dict.fromkeys(("red_sarong",), ("clothes_main", "bottoms")),
    **dict.fromkeys(("bodycon",), ("clothes_main", "dress")),
    **dict.fromkeys(("gerudo_set_(zelda)",), ("clothes_special", "themed_costume")),
    **dict.fromkeys(("jinbaori", "jinbei_(clothes)"), ("clothes_special", "traditional_east")),
    **dict.fromkeys(("dou", "barding", "single_vambrace"), ("clothes_special", "armor")),
    **dict.fromkeys(("c-string",), ("underwear_swim", "panties_underwear")),
    **dict.fromkeys(("super_highleg",), ("underwear_swim", "underwear_design")),
    **dict.fromkeys(("low-cut",), ("clothing_detail", "clothing_structure")),
    **dict.fromkeys(("colored_stripes",), ("clothing_detail", "clothing_pattern")),
    **dict.fromkeys(("clothes_in_front", "clothes_on_and_off", "unfastened"), ("clothing_detail", "clothing_state")),
    **dict.fromkeys(("pixel_sunglasses",), ("accessories", "eyewear")),
    **dict.fromkeys(("silver_armlet",), ("accessories", "jewelry")),
    **dict.fromkeys(("stopwatch_around_neck", "sign_around_neck"), ("accessories", "neckwear")),
    **dict.fromkeys(("furoshiki",), ("accessories", "bags_belts")),
    **dict.fromkeys(("omamori",), ("accessories", "badges_ornaments")),
    **dict.fromkeys(("accessories",), ("accessories", "other_accessory")),
    **dict.fromkeys(("mushroom_on_head",), ("accessories", "headwear")),
    **dict.fromkeys(("sig_556", "artillery", "sig_mpx", "m16a1"), ("weapons", "firearm")),
    **dict.fromkeys(("rpg_(weapon)",), ("weapons", "explosive")),
    **dict.fromkeys(("bident",), ("weapons", "polearm")),
    **dict.fromkeys(("nunchaku",), ("weapons", "blunt_chain")),
    **dict.fromkeys(("tsuba_(guard)",), ("weapons", "blade")),
    **dict.fromkeys(("hoshi_no_tsue", "sword_of_st._catherine_(fate)", "staff_of_selection_(fate)", "masamune_(ff7)"), ("weapons", "magic_weapon")),
    **dict.fromkeys(("boomerang",), ("weapons", "other_weapon")),
    **dict.fromkeys(("tako-san_wiener", "ikayaki", "aburaage", "mayonnaise"), ("food_drink", "staple_food")),
    **dict.fromkeys(("salmon",), ("creatures", "aquatic")),
    **dict.fromkeys(("sakura_mochi", "pie_slice"), ("food_drink", "dessert_snack")),
    **dict.fromkeys(("pecha_berry", "coffee_beans", "pea_pod"), ("food_drink", "fruit_vegetable")),
    **dict.fromkeys(("mortar_(bowl)", "salt_shaker", "utensil"), ("food_drink", "tableware")),
    **dict.fromkeys(("battery",), ("household_objects", "appliance")),
    **dict.fromkeys(("fish_hook", "pliers", "knitting_needle", "pincushion", "rubber_band", "adjustable_wrench", "spool", "rod"), ("household_objects", "tools")),
    **dict.fromkeys(("hongbao", "lunchbox", "postbox_(outgoing_mail)"), ("household_objects", "container")),
    **dict.fromkeys(("chabudai",), ("household_objects", "seating_table")),
    **dict.fromkeys(("display_case",), ("household_objects", "storage_furniture")),
    **dict.fromkeys(("treasure", "koban_(gold)"), ("household_objects", "other_object")),
    **dict.fromkeys(("payphone", "poketch"), ("digital_media", "phone_computer")),
    **dict.fromkeys(("digital_walkman",), ("digital_media", "camera_media")),
    **dict.fromkeys(("binder", "postage_stamp", "academic_test"), ("culture_objects", "books_paper")),
    **dict.fromkeys(("shamisen", "ocarina"), ("culture_objects", "music")),
    **dict.fromkeys(("rhythmic_gymnastics", "kung_fu", "ring-con", "tennis_court", "racetrack", "push-ups", "yoga_mat"), ("recreation", "sports")),
    **dict.fromkeys(("ace_of_diamonds", "poker", "uno_(game)", "king_(playing_card)"), ("recreation", "games")),
    **dict.fromkeys(("roller_coaster", "marionette", "gashapon"), ("recreation", "toys")),
    **dict.fromkeys(("subway", "carriage"), ("transport_play", "land_vehicle")),
    **dict.fromkeys(("biplane",), ("transport_play", "air_vehicle")),
    **dict.fromkeys(("ship's_wheel",), ("transport_play", "water_vehicle")),
    **dict.fromkeys(("wolf_paws",), ("creatures", "animal_feature")),
    **dict.fromkeys(("pincers", "dragon_claw"), ("creatures", "claw_scale")),
    **dict.fromkeys(("tiger_cub", "multiple_cats", "chinchilla_(animal)", "red_panda"), ("creatures", "mammal")),
    **dict.fromkeys(("long-tailed_tit",), ("creatures", "bird")),
    **dict.fromkeys(("sacabambaspis", "butterflyfish", "axolotl"), ("creatures", "aquatic")),
    **dict.fromkeys(("caterpillar",), ("creatures", "insect")),
    **dict.fromkeys(("tyrannosaurus_rex",), ("creatures", "reptile")),
    **dict.fromkeys(("daffodil",), ("nature", "plant")),
    **dict.fromkeys(("ice_crystal", "pebble"), ("nature", "mineral")),
    **dict.fromkeys(("exhaust",), ("mech_scifi", "machine")),
    **dict.fromkeys(("core", "chronal_accelerator_(overwatch)", "electrodes"), ("mech_scifi", "scifi_device")),
    **dict.fromkeys(("simulacrum_(titanfall)",), ("mech_scifi", "robot_android")),
    **dict.fromkeys(("bubble_bath",), ("indoor_scene", "home_room")),
    **dict.fromkeys(("sports_hall", "kindergarten"), ("indoor_scene", "public_indoor")),
    **dict.fromkeys(("yatai", "supermarket"), ("indoor_scene", "commercial")),
    **dict.fromkeys(("escalator", "cathedral", "noren", "truss"), ("indoor_scene", "architecture")),
    **dict.fromkeys(("sett",), ("indoor_scene", "surface")),
    **dict.fromkeys(("cut-in", "recursion"), ("composition", "layout")),
    **dict.fromkeys(("flaming_skull",), ("light_effect", "fire_smoke")),
    **dict.fromkeys(("x-ray_vision",), ("light_effect", "optical")),
    **dict.fromkeys(("hemokinesis", "kamehameha_(dragon_ball)"), ("light_effect", "magic_effect")),
    **dict.fromkeys(("sculpture",), ("style", "medium")),
    **dict.fromkeys(("anachronism",), ("style", "era_style")),
    **dict.fromkeys(("overexposure",), ("style", "photo_3d")),
    **dict.fromkeys(("poi", "price", "kansaiben", "shochuumimai"), ("text_meta", "text")),
    **dict.fromkeys(("four-pointed_star", "drawn_heart", "cut-here_line", "star_of_life", "reichsadler"), ("text_meta", "symbol")),
    **dict.fromkeys(("graph",), ("text_meta", "screen_ui")),
    **dict.fromkeys(("nico_nico_nii", "caramelldansen", "charisma_break", "number_pun", "sugoi_dekai", "mukyuu", "homu"), ("meta_info", "meme")),
    **dict.fromkeys(("profile_picture",), ("meta_info", "meta")),
    **dict.fromkeys(("mons_pubis", "prolapse"), ("adult", "adult_anatomy")),
    **dict.fromkeys(("mounting",), ("adult", "adult_sex")),
    **dict.fromkeys(("yellow_blood", "black_blood", "poop"), ("adult", "adult_fluid")),
    **dict.fromkeys(("unusual_insertion", "okamoto_condoms", "prostate_milking", "cuffed"), ("adult", "adult_fetish")),
    **dict.fromkeys(("pelvic_curtain_aside",), ("adult", "adult_clothes")),
    **dict.fromkeys(("hanged", "human_head", "cannibalism", "implied_murder", "imminent_suicide"), ("adult", "adult_gore")),
    **dict.fromkeys(("virgin", "sexual_harassment", "forced", "aphrodisiac"), ("adult", "adult_other")),
    **dict.fromkeys(("kupaa",), ("adult", "adult_suggestive")),
})


EXACT_OVERRIDES.update({
    # Eighth pass: named designs, in-universe items and the remaining ordinary
    # terms with a single well-supported meaning in the local database.
    "v4x": ("themes", "persona_variant"),
    "bokura_wa_ima_no_naka_de": ("clothes_special", "themed_costume"),
    "natsuiro_egao_de_1_2_jump!": ("clothes_special", "themed_costume"),
    "hasu_no_daisankaku": ("relationships", "group_faction"),
    "super_star_(mario)": ("recreation", "games"),
    "yamaha": ("text_meta", "brand"),
    "anna_miller": ("clothes_special", "occupation_uniform"),
    "spots": ("clothing_detail", "clothing_pattern"),
    "n_corp._fanatic_(identity)_(project_moon)": ("themes", "persona_variant"),
    "kundala_(fate)": ("accessories", "jewelry"),
    "coco's": ("text_meta", "brand"),
    "mexico": ("outdoor_scene", "other_scene"),
    "fabulous": ("expression", "positive"),
    "grass_root_youkai_network": ("relationships", "group_faction"),
    "gate_of_babylon_(fate)": ("weapons", "magic_weapon"),
    "grandfather_and_grandson": ("relationships", "family_relation"),
    "charging_forward": ("action", "movement"),
    "osmanthus": ("nature", "plant"),
    "matcha_(food)": ("food_drink", "drink"),
    "swinging_on_swing": ("action", "movement"),
    "wuthering_heights_(identity)_(project_moon)": ("themes", "persona_variant"),
    "sitrus_berry": ("food_drink", "fruit_vegetable"),
    "alternate_design": ("themes", "persona_variant"),
    "tsuki_ni_kawatte_oshioki_yo": ("meta_info", "meme"),
    "genie": ("people", "fantasy_person"),
    "praying_mantis": ("creatures", "insect"),
    "kantele": ("culture_objects", "music"),
    "bomber": ("transport_play", "air_vehicle"),
    "mochitsuki": ("action", "daily_action"),
    "draw_this_in_your_style_challenge": ("meta_info", "meta"),
    "oden": ("food_drink", "staple_food"),
    "stinger": ("creatures", "claw_scale"),
    "tamagotchi_(virtual_pet)": ("recreation", "toys"),
    "scrape": ("body", "body_marks"),
    "bear_trap": ("household_objects", "tools"),
    "six_fanarts_challenge": ("meta_info", "meta"),
    "thumb_sucking": ("action", "daily_action"),
    "phantom_thief": ("people", "occupation"),
    "sheikah_slate": ("mech_scifi", "scifi_device"),
    "andon": ("household_objects", "lighting_clock"),
    "clam_shell": ("creatures", "aquatic"),
    "apple_pie": ("food_drink", "bakery"),
    "grandmother_and_granddaughter": ("relationships", "family_relation"),
    "archaic_set_(zelda)": ("clothes_special", "themed_costume"),
    "cold_pack": ("household_objects", "tools"),
    "faceoff": ("action", "combat_action"),
    "togenashi_togeari": ("relationships", "group_faction"),
    "wrestler": ("people", "occupation"),
    "wet_spot": ("indoor_scene", "surface"),
    "404_(girls'_frontline)": ("relationships", "group_faction"),
    "manhole_cover": ("indoor_scene", "urban"),
    "go_(board_game)": ("recreation", "games"),
    "ipad": ("digital_media", "phone_computer"),
    "hair_branch": ("hair", "hair_accessory"),
    "disintegration": ("light_effect", "other_effect"),
    "wiping_blood": ("action", "daily_action"),
    "zanshomimai": ("time_weather", "holiday"),
    "parachute": ("transport_play", "air_vehicle"),
    "oiran": ("people", "occupation"),
    "bent_back": ("pose", "body_pose"),
    "colorpoint_(pattern)": ("creatures", "animal_feature"),
    "france": ("outdoor_scene", "other_scene"),
    "keytar": ("culture_objects", "music"),
    "autofacial": ("adult", "adult_self"),
    "handlebar": ("transport_play", "land_vehicle"),
    "baking_sheet": ("food_drink", "tableware"),
    "silent_princess": ("nature", "plant"),
    "kanoko_(pattern)": ("clothing_detail", "clothing_pattern"),
    "decorations": ("accessories", "badges_ornaments"),
    "indian": ("people", "role_focus"),
    "china": ("outdoor_scene", "other_scene"),
    "melusine_(genshin_impact)": ("people", "fantasy_person"),
    "pink_diamond_765_(idolmaster)": ("clothes_special", "themed_costume"),
    "lizardman": ("people", "fantasy_person"),
    "celebration": ("themes", "narrative_situation"),
    "spiked_knuckles": ("weapons", "blunt_chain"),
    "ovum_with_heart": ("adult", "adult_anatomy"),
    "dandelion_seed": ("nature", "plant"),
    "is_that_so": ("meta_info", "meme"),
    "yuanlingpao": ("clothes_special", "traditional_east"),
    "progression": ("meta_info", "meta"),
    "fisting": ("adult", "adult_sex"),
    "capybara": ("creatures", "mammal"),
    "charging_device": ("household_objects", "appliance"),
    "kavacha_(fate)": ("clothes_special", "armor"),
    "human_stacking": ("action", "interaction"),
    "asmr": ("digital_media", "camera_media"),
    "myrtenaster": ("weapons", "magic_weapon"),
    "nightmare": ("themes", "narrative_situation"),
    "vs": ("text_meta", "symbol"),
    "mandibles": ("creatures", "claw_scale"),
    "double_chin": ("body", "build"),
    "stakes_of_purgatory": ("weapons", "magic_weapon"),
    "tupet": ("hair", "hair_accessory"),
    "throwing_needles": ("action", "combat_action"),
})


EXACT_OVERRIDES.update({
    # Ninth pass: the next high-confidence slice after all earlier removals.
    "hooked_on_heel": ("pose", "body_pose"),
    "meditation": ("pose", "stationary_pose"),
    "shampoo": ("household_objects", "tools"),
    "nest": ("outdoor_scene", "forest_field"),
    "doujigiri_yasutsuna_(fate)": ("weapons", "magic_weapon"),
    "tiger_paws": ("creatures", "claw_scale"),
    "t-pose": ("pose", "body_pose"),
    "change_in_common_sense": ("themes", "narrative_situation"),
    "25-ji_nightcord_de._(project_sekai)": ("relationships", "group_faction"),
    "matches": ("household_objects", "tools"),
    "giving_birth": ("body", "body_state"),
    "tokyo_big_sight": ("indoor_scene", "architecture"),
    "aunt_and_nephew": ("relationships", "family_relation"),
    "h&k_mp5": ("weapons", "firearm"),
    "techwear": ("clothes_special", "themed_costume"),
    "undone_sarashi": ("clothing_detail", "clothing_state"),
    "marble_(toy)": ("recreation", "toys"),
    "weeds": ("nature", "plant"),
    "highway": ("indoor_scene", "urban"),
    "harpoon": ("weapons", "polearm"),
    "lamb": ("creatures", "mammal"),
    "air_jordan": ("legwear_footwear", "shoes"),
    "gold_osmanthus": ("nature", "plant"),
    "holocouncil": ("relationships", "group_faction"),
    "sleeveless_duster": ("clothes_main", "outerwear"),
    "relay_baton": ("recreation", "sports"),
    "falcon": ("creatures", "bird"),
    "tamaranean": ("people", "fantasy_person"),
    "cashier": ("people", "occupation"),
    "flute_tassel": ("accessories", "badges_ornaments"),
    "cockroach_girl": ("people", "fantasy_person"),
    "pretzel": ("food_drink", "bakery"),
    "nendoroid": ("recreation", "toys"),
    "garlean": ("people", "fantasy_person"),
    "chestnut": ("food_drink", "fruit_vegetable"),
    "crustacean": ("creatures", "aquatic"),
    "beaten": ("body", "body_state"),
    "evolution": ("themes", "identity_change"),
    "starting_block": ("recreation", "sports"),
    "euphonium": ("culture_objects", "music"),
    ";t": ("expression", "sad_cry"),
    "knot": ("household_objects", "tools"),
    "bible_(object)": ("culture_objects", "books_paper"),
    "pink_corset": ("underwear_swim", "bra_lingerie"),
    "yen": ("text_meta", "symbol"),
    "feather_duster": ("household_objects", "tools"),
    "fainted": ("body", "body_state"),
    "kayari_buta": ("household_objects", "other_object"),
    "staff_of_homa_(genshin_impact)": ("weapons", "magic_weapon"),
    "stealth_flashing": ("adult", "adult_nudity"),
    "laundromat": ("indoor_scene", "commercial"),
    "konpeitou": ("food_drink", "dessert_snack"),
    "draenei": ("people", "fantasy_person"),
    "mauser_c96": ("weapons", "firearm"),
    "epiphyllum": ("nature", "plant"),
    "chupa_chups": ("food_drink", "dessert_snack"),
    "exposed_brain": ("adult", "adult_gore"),
    "beam": ("light_effect", "lighting"),
    "flamingo": ("creatures", "bird"),
    "contortion": ("pose", "body_pose"),
    "headshot": ("adult", "adult_gore"),
    "merfolk_out_of_environment": ("body", "body_state"),
    "italy": ("outdoor_scene", "other_scene"),
    "uu~": ("text_meta", "comic"),
    "butterfly_on_head": ("accessories", "headwear"),
    "ace_of_clubs": ("recreation", "games"),
    "back_cover": ("culture_objects", "books_paper"),
    "hearing_aid": ("mech_scifi", "cybernetic"),
    "super_soaker": ("recreation", "toys"),
    "dew_drop": ("light_effect", "particles"),
    "lemonade": ("food_drink", "drink"),
    "satellite": ("mech_scifi", "scifi_device"),
    "alter_servant": ("themes", "persona_variant"),
    "well": ("indoor_scene", "architecture"),
    "lifting_covers": ("action", "holding"),
    "moriya's_iron_rings": ("weapons", "magic_weapon"),
    "locket": ("accessories", "jewelry"),
    "mutation": ("themes", "identity_change"),
    "craft_essence_(fate)": ("recreation", "games"),
    "cuntboy_with_male": ("adult", "adult_sex"),
    "peafowl": ("creatures", "bird"),
    "stargazing": ("action", "daily_action"),
    "super_saiyan_3": ("themes", "persona_variant"),
    "green_corset": ("underwear_swim", "bra_lingerie"),
    "komainu": ("creatures", "fantasy_creature"),
    "ovaries": ("adult", "adult_anatomy"),
    "injection": ("action", "daily_action"),
    "light_switch": ("household_objects", "appliance"),
    "dr_pepper": ("food_drink", "drink"),
    "originium_(arknights)": ("nature", "mineral"),
    "mercedes-benz": ("text_meta", "brand"),
    "hula_hoop": ("recreation", "sports"),
    "giggling": ("expression", "positive"),
    "washbowl": ("household_objects", "container"),
    "dog_paws": ("creatures", "claw_scale"),
})


EXACT_OVERRIDES.update({
    # Cross-check corrections and a few adjacent high-confidence entries.
    "edel_note": ("relationships", "group_faction"),
    "faceoff": ("relationships", "comparison"),
    "vs": ("relationships", "comparison"),
    "charging_forward": ("action", "combat_action"),
    "headshot": ("action", "combat_action"),
    ";t": ("expression", "neutral_expression"),
    "hooked_on_heel": ("clothing_detail", "clothing_state"),
    "kundala_(fate)": ("accessories", "neckwear"),
    "hearing_aid": ("accessories", "other_accessory"),
    "butterfly_on_head": ("creatures", "insect"),
    "tupet": ("food_drink", "dessert_snack"),
    "staff_of_homa_(genshin_impact)": ("weapons", "polearm"),
    "throwing_needles": ("weapons", "other_weapon"),
    "light_switch": ("household_objects", "lighting_clock"),
    "yen": ("household_objects", "other_object"),
    "charging_device": ("digital_media", "phone_computer"),
    "gate_of_babylon_(fate)": ("light_effect", "magic_effect"),
    "mochitsuki": ("time_weather", "holiday"),
    "celebration": ("time_weather", "holiday"),
    "zanshomimai": ("time_weather", "season"),
    "progression": ("composition", "layout"),
    "asmr": ("style", "genre"),
    "air_jordan": ("text_meta", "brand"),
    "chupa_chups": ("text_meta", "brand"),
    "dr_pepper": ("text_meta", "brand"),
    "wet_spot": ("adult", "adult_fluid"),
    "change_in_common_sense": ("adult", "adult_fetish"),
    "human_stacking": ("adult", "adult_fetish"),
    "koonago": ("adult", "adult_fetish"),
    "stealth_flashing": ("adult", "adult_suggestive"),
    "cupping_glass": ("action", "holding"),
    "neck_warmer": ("accessories", "neckwear"),
    "crosier": ("accessories", "other_accessory"),
    "lever_action": ("weapons", "firearm"),
    "pangu_terminal_(wuthering_waves)": ("mech_scifi", "scifi_device"),
    "spring_(object)": ("mech_scifi", "machine"),
    "salmonid": ("creatures", "fantasy_creature"),
    "bonfire": ("light_effect", "fire_smoke"),
    "fake_ad": ("meta_info", "meme"),
    "vhs_artifacts": ("style", "photo_3d"),
    "autoarousal": ("adult", "adult_fluid"),
    "human_toilet": ("adult", "adult_fetish"),

    # Restore only the proper names whose local description is genuinely too
    # ambiguous to justify a semantic folder.
    "anna_miller": ("other", "other_a_e"),
    "bokura_wa_ima_no_naka_de": ("other", "other_a_e"),
    "natsuiro_egao_de_1_2_jump!": ("other", "other_k_o"),
    "spots": ("other", "other_p_t"),
    "beam": ("other", "other_a_e"),
    "knot": ("other", "other_k_o"),
})


EXACT_OVERRIDES.update({
    # Eleventh pass: independent audit of the next current long-tail window.
    **dict.fromkeys(("king", "viking", "modeling"), ("people", "role_focus")),
    **dict.fromkeys(("satyr", "roegadyn"), ("people", "fantasy_person")),
    **dict.fromkeys(("quintuplets", "grandfather_and_granddaughter"), ("relationships", "family_relation")),
    **dict.fromkeys(("love_triangle",), ("relationships", "romance_orientation")),
    **dict.fromkeys(("master_and_servant",), ("relationships", "social_relation")),
    **dict.fromkeys(("bust_chart", "polar_opposites"), ("relationships", "comparison")),
    **dict.fromkeys(("fleet", "rabbit_platoon_(blue_archive)", "holoadvent", "yakuza", "marching_band", "u's_2nd_years"), ("relationships", "group_faction")),
    **dict.fromkeys(("crime_prevention_buzzer_threat", "coronavirus_pandemic"), ("themes", "narrative_situation")),
    **dict.fromkeys(("thick_neck",), ("body", "build")),
    **dict.fromkeys(("paint_stains", "rope_marks"), ("body", "body_marks")),
    **dict.fromkeys(("anatomical_nonsense",), ("body", "body_state")),
    **dict.fromkeys(("flower-shaped_hair",), ("hair", "hair_style")),
    **dict.fromkeys(("confident",), ("expression", "positive")),
    **dict.fromkeys(("d;", "roaring"), ("expression", "anger")),
    **dict.fromkeys(("spicy", "traumatized"), ("expression", "fear_surprise")),
    **dict.fromkeys(("waiting",), ("pose", "stationary_pose")),
    **dict.fromkeys(("tossing",), ("action", "holding")),
    **dict.fromkeys(("landing",), ("action", "movement")),
    **dict.fromkeys(("headbutt", "suplex"), ("action", "combat_action")),
    **dict.fromkeys(("stalking", "teaching", "held_down", "belly-to-belly", "patting"), ("action", "interaction")),
    **dict.fromkeys(("shaving", "clothed_bath", "burp"), ("action", "daily_action")),
    **dict.fromkeys(("zhijupao", "aoqun"), ("clothes_special", "traditional_east")),
    **dict.fromkeys(("gold_saint",), ("clothes_special", "armor")),
    **dict.fromkeys(("green_suspenders",), ("clothing_detail", "clothing_structure")),
    **dict.fromkeys(("wrinkled_fabric",), ("clothing_detail", "clothing_material")),
    **dict.fromkeys(("bucket_on_head", "tenugui", "sandogasa"), ("accessories", "headwear")),
    **dict.fromkeys(("stethoscope_around_neck",), ("accessories", "neckwear")),
    **dict.fromkeys(("towel_on_one_shoulder",), ("accessories", "other_accessory")),
    **dict.fromkeys(("ak-12", "h&k_mp7", "dragunov_svd", "sig_p220/p226", "an-94", "gunpod", "barrett_m82", "pgm_hecate_ii"), ("weapons", "firearm")),
    **dict.fromkeys(("lasso",), ("weapons", "blunt_chain")),
    **dict.fromkeys(("detonator", "lit_fuse"), ("weapons", "explosive")),
    **dict.fromkeys(("stake",), ("weapons", "other_weapon")),
    **dict.fromkeys(("fried_egg_on_toast", "stew", "breakfast", "nabe"), ("food_drink", "staple_food")),
    **dict.fromkeys(("sashimi", "ikura_(food)"), ("food_drink", "meat_seafood")),
    **dict.fromkeys(("jelly_bean",), ("food_drink", "dessert_snack")),
    **dict.fromkeys(("mustard",), ("food_drink", "dairy_ingredient")),
    **dict.fromkeys(("latte_art",), ("food_drink", "drink")),
    **dict.fromkeys(("fender_jazzmaster", "pop_filter", "fender_precision_bass", "trombone"), ("culture_objects", "music")),
    **dict.fromkeys(("pages", "cardboard", "diary", "death_note_(object)"), ("culture_objects", "books_paper")),
    **dict.fromkeys(("clothes_rack",), ("household_objects", "storage_furniture")),
    **dict.fromkeys(("paint_roller", "armillary_sphere", "sewing_pin"), ("household_objects", "tools")),
    **dict.fromkeys(("bug_cage",), ("household_objects", "container")),
    **dict.fromkeys(("portable_stove",), ("household_objects", "appliance")),
    **dict.fromkeys(("shower_curtain", "scarecrow"), ("household_objects", "other_object")),
    **dict.fromkeys(("game_boy_advance", "pokedex"), ("digital_media", "phone_computer")),
    **dict.fromkeys(("walkman",), ("digital_media", "camera_media")),
    **dict.fromkeys(("jet_airliner",), ("transport_play", "air_vehicle")),
    **dict.fromkeys(("taxi",), ("transport_play", "land_vehicle")),
    **dict.fromkeys(("jigsaw_puzzle",), ("recreation", "games")),
    **dict.fromkeys(("inflatable_orca", "bubble_pipe", "character_snowman"), ("recreation", "toys")),
    **dict.fromkeys(("bear_paws", "crab_claw"), ("creatures", "claw_scale")),
    **dict.fromkeys(("piglet", "koala", "alpaca", "tapir"), ("creatures", "mammal")),
    **dict.fromkeys(("peacock", "too_many_birds", "ostrich"), ("creatures", "bird")),
    **dict.fromkeys(("ogre", "cerberus"), ("creatures", "fantasy_creature")),
    **dict.fromkeys(("poinsettia", "willow", "reeds"), ("nature", "plant")),
    **dict.fromkeys(("crystal_shards",), ("nature", "mineral")),
    **dict.fromkeys(("steel_beam", "muntins"), ("indoor_scene", "architecture")),
    **dict.fromkeys(("tropical",), ("outdoor_scene", "other_scene")),
    **dict.fromkeys(("big_dipper",), ("outdoor_scene", "sky_space")),
    **dict.fromkeys(("through_window",), ("composition", "framing")),
    **dict.fromkeys(("stack",), ("composition", "layout")),
    **dict.fromkeys(("power-up",), ("light_effect", "magic_effect")),
    **dict.fromkeys(("psychedelic",), ("style", "art_style")),
    **dict.fromkeys(("test_score", "no"), ("text_meta", "text")),
    **dict.fromkeys(("small_stellated_dodecahedron", "celtic_knot"), ("text_meta", "symbol")),
    **dict.fromkeys(("bmw",), ("text_meta", "brand")),
    **dict.fromkeys(("love_confessions_in_gensokyo", "yaranaika", "shinkon_santaku", "ayaya~"), ("meta_info", "meme")),
    **dict.fromkeys(("kodomo_no_hi", "lion_dance"), ("time_weather", "holiday")),
    **dict.fromkeys(("large_bulge",), ("adult", "adult_anatomy")),
    **dict.fromkeys(("ball_busting", "scat", "rope_around_neck", "feminization"), ("adult", "adult_fetish")),
    **dict.fromkeys(("fanning_crotch", "tanline_peek", "bulge_press"), ("adult", "adult_suggestive")),
    **dict.fromkeys(("implied_prostitution",), ("adult", "adult_other")),
    **dict.fromkeys(("teabag",), ("adult", "adult_oral")),
    **dict.fromkeys(("bisected",), ("adult", "adult_gore")),
    **dict.fromkeys(("jedi",), ("people", "fantasy_person")),
    "see-through_pelvic_curtain": ("adult", "adult_clothes"),
})


EXACT_OVERRIDES.update({
    # Last ordinary terms before the remaining list becomes predominantly
    # proper names or genuinely multi-purpose concepts.
    "height_mark": ("relationships", "comparison"),
    "brazil": ("outdoor_scene", "other_scene"),
    "on_railroad_tracks": ("pose", "body_pose"),
    "shiitake": ("food_drink", "fruit_vegetable"),
    "tarutaru": ("people", "fantasy_person"),
    "creamer_(vessel)": ("food_drink", "tableware"),
    "luger_p08": ("weapons", "firearm"),
    "ukraine": ("outdoor_scene", "other_scene"),
    "billiards": ("recreation", "sports"),
    "swaddled": ("body", "body_state"),
    "avalon_(fate)": ("weapons", "magic_weapon"),
    "optical_illusion": ("light_effect", "optical"),
    "jizou": ("indoor_scene", "architecture"),
    "stroking_another's_chin": ("action", "interaction"),
    "marijuana": ("nature", "plant"),
    "drainpipe": ("indoor_scene", "architecture"),
    "manlification": ("themes", "identity_change"),
    "cartridge": ("weapons", "firearm"),
    "gauge": ("accessories", "jewelry"),
    "block_(object)": ("recreation", "toys"),
    "netorase": ("adult", "adult_other"),
    "game_cartridge": ("recreation", "games"),
    "light_in_heart": ("light_effect", "magic_effect"),
    "symphogear_pendant": ("accessories", "neckwear"),
    "carrot_slice": ("food_drink", "fruit_vegetable"),
})


EXACT_OVERRIDES.update({
    # Final wiki-verified corrections for misleading English/Chinese aliases.
    "telstar": ("recreation", "sports"),
    "gauge": ("household_objects", "tools"),
    "mustard": ("food_drink", "staple_food"),
    "gelatin": ("food_drink", "dessert_snack"),
    "battery": ("mech_scifi", "machine"),
    "poison": ("household_objects", "other_object"),
    "snow_on_head": ("body", "body_state"),
    "red_sun": ("outdoor_scene", "sky_space"),
})


EXACT_OVERRIDES.update({
    # Final freeze pass: only concepts whose database descriptions state an
    # unambiguous object, action, species, garment or relationship.
    "branded": ("body", "body_marks"),
    "applying_sunscreen": ("action", "daily_action"),
    "galaxia_(sword)": ("weapons", "magic_weapon"),
    "on_cloud": ("pose", "body_pose"),
    "planter": ("household_objects", "container"),
    "rags": ("clothing_detail", "clothing_state"),
    "t-back": ("underwear_swim", "panties_underwear"),
    "too_many_bows": ("accessories", "badges_ornaments"),
    "fart": ("adult", "adult_fluid"),
    "pipa_(instrument)": ("culture_objects", "music"),
    "rectangle": ("text_meta", "symbol"),
    "shibuya_(tokyo)": ("indoor_scene", "urban"),
    "belly_rub": ("action", "interaction"),
    "mooncake": ("food_drink", "bakery"),
    "stance": ("pose", "stationary_pose"),
    "gecko": ("creatures", "reptile"),
    "hirabitai": ("hair", "hair_accessory"),
    "mafia": ("relationships", "group_faction"),
    "nut_(food)": ("food_drink", "fruit_vegetable"),
    "rusty_trombone": ("adult", "adult_oral"),
    "suspenders_gap": ("clothing_detail", "clothing_structure"),
    "kourindou": ("indoor_scene", "commercial"),
    "nopon": ("creatures", "fantasy_creature"),
    "on_branch": ("pose", "body_pose"),
    "photobomb": ("action", "interaction"),
    "ankle_bell": ("accessories", "jewelry"),
    "cowl_neck": ("clothing_detail", "clothing_structure"),
    "midnight_bliss": ("themes", "identity_change"),
    "nodding": ("pose", "gaze"),
    "brown_egyptian_cat-eared_loli_(trend)": ("style", "genre"),
    "flannel": ("clothing_detail", "clothing_material"),
    "oiled": ("body", "body_state"),
    "aerial_battle": ("action", "combat_action"),
    "destroyer": ("transport_play", "water_vehicle"),
    "fender_mustang": ("culture_objects", "music"),
    "lace-up": ("clothing_detail", "clothing_structure"),
    "magic_trick": ("action", "daily_action"),
    "barn": ("indoor_scene", "architecture"),
    "firefly": ("creatures", "insect"),
    "flaming_head": ("light_effect", "fire_smoke"),
    "koi_dance": ("action", "daily_action"),
    "virtuous_contract": ("weapons", "magic_weapon"),
    "hymen": ("adult", "adult_anatomy"),
    "nissan_skyline": ("transport_play", "land_vehicle"),
    "sig_mcx": ("weapons", "firearm"),
    "three_sizes": ("relationships", "comparison"),
    "typewriter": ("culture_objects", "books_paper"),
    "conductor": ("people", "occupation"),
    "curled_ends": ("hair", "hair_style"),
    "exhaust_pipe": ("mech_scifi", "machine"),
    "frontbend": ("pose", "body_pose"),
    "song_of_broken_pines_(genshin_impact)": ("weapons", "magic_weapon"),
    "blueprint_(object)": ("culture_objects", "books_paper"),
    "chaos_emerald": ("nature", "mineral"),
    "dobermann": ("creatures", "mammal"),
    "ford": ("text_meta", "brand"),
    "geokinesis": ("light_effect", "magic_effect"),
    "squishing": ("body", "body_state"),
    "weird_route_(deltarune)": ("themes", "narrative_situation"),
    "charger": ("digital_media", "phone_computer"),
    "fanning": ("action", "daily_action"),
    "multicolored_polka_dots": ("clothing_detail", "clothing_pattern"),
    "pal_(creature)": ("creatures", "fantasy_creature"),
    "salt": ("food_drink", "dairy_ingredient"),
    "wagon": ("transport_play", "land_vehicle"),
    "bust_measuring": ("action", "daily_action"),
    "lego": ("recreation", "toys"),
    "ripping": ("action", "daily_action"),
    "slipping": ("action", "movement"),
    "underbarrel_grenade_launcher": ("weapons", "explosive"),
    "caution": ("text_meta", "text"),
    "rolling_pin": ("household_objects", "tools"),
    "taco": ("food_drink", "staple_food"),
    "warp_pipe": ("mech_scifi", "scifi_device"),
    "irasutoya_challenge": ("meta_info", "meta"),
    "m1903_springfield": ("weapons", "firearm"),
    "mont_blanc_(food)": ("food_drink", "dessert_snack"),
    "united_kingdom": ("outdoor_scene", "other_scene"),
    "crash": ("action", "combat_action"),
    "croquette": ("food_drink", "staple_food"),
    "ribboned_xiao_guan": ("accessories", "headwear"),
    "sit-up": ("recreation", "sports"),
    "template": ("meta_info", "meta"),
    "complex_exterior": ("outdoor_scene", "other_scene"),
    "grasshopper": ("creatures", "insect"),
    "ultra_instinct": ("themes", "persona_variant"),
    "harisen": ("household_objects", "tools"),
    "parasite": ("creatures", "other_creature"),
    "tear_arcana_rod": ("weapons", "magic_weapon"),
    "battle_standard": ("accessories", "badges_ornaments"),
    "dizzy": ("body", "body_state"),
    "himation": ("clothes_special", "traditional_world"),
    "i_heart...": ("text_meta", "text"),
    "lanchester_smg": ("weapons", "firearm"),
    "single_handcuff": ("adult", "adult_fetish"),
    "pony_play": ("adult", "adult_fetish"),
    "recruitment_(blue_archive)": ("recreation", "games"),
    "vent_(object)": ("indoor_scene", "architecture"),
    "ai_arctic_warfare": ("weapons", "firearm"),
    "circuit_board": ("mech_scifi", "machine"),
    "formula_racer": ("transport_play", "land_vehicle"),
    "gardening": ("action", "daily_action"),
    "kerchief": ("accessories", "neckwear"),
    "brain_freeze": ("body", "body_state"),
    "blue_swim_trunks": ("underwear_swim", "swimsuit"),
    "kooribata": ("text_meta", "text"),
    "release_celebration": ("meta_info", "meta"),
    "sound_wave": ("light_effect", "optical"),
    "sumo": ("recreation", "sports"),
    "twister": ("recreation", "games"),
    "block_(minecraft)": ("recreation", "games"),
    "knotting": ("adult", "adult_sex"),
    "stellated_octahedron": ("text_meta", "symbol"),
    "world_war_i": ("themes", "narrative_situation"),
    "banana_slice": ("food_drink", "fruit_vegetable"),
    "extra_digits": ("body", "body_state"),
    "famicom": ("digital_media", "phone_computer"),
    "streetcar": ("transport_play", "land_vehicle"),
    "biting_head": ("action", "interaction"),
    "mercury_(element)": ("nature", "mineral"),
    "dart": ("recreation", "sports"),
    "reverse_ryona": ("adult", "adult_gore"),
    "silence_glaive": ("weapons", "magic_weapon"),
    "stingray": ("creatures", "aquatic"),
    "vs_seeker": ("recreation", "games"),
    "cicada": ("creatures", "insect"),
    "dollar_bill": ("culture_objects", "books_paper"),
    "engulfing_lightning_(genshin_impact)": ("weapons", "magic_weapon"),
    "great_pyrenees": ("creatures", "mammal"),
    "uncle_and_nephew": ("relationships", "family_relation"),
    "walkman_nw-s203f": ("digital_media", "camera_media"),
    "blood_trail": ("adult", "adult_gore"),
    "dragonstone": ("nature", "mineral"),
    "element_bending": ("light_effect", "magic_effect"),
    "ukulele": ("culture_objects", "music"),
    "dahlia": ("nature", "plant"),
    "ermine": ("creatures", "mammal"),
    "ferrari": ("text_meta", "brand"),
    "fossil": ("nature", "mineral"),
    "implied_bisexual": ("relationships", "romance_orientation"),
    "rinnegan": ("face", "eye_shape"),
    "seven-segment_display": ("text_meta", "screen_ui"),
    "slingshot_(weapon)": ("weapons", "other_weapon"),
    "canards": ("transport_play", "air_vehicle"),
    "hamster_girl": ("people", "fantasy_person"),
    "lid": ("household_objects", "container"),
    "animal_on_back": ("pose", "body_pose"),
    "dna": ("text_meta", "symbol"),
    "gift_wrapping": ("household_objects", "container"),
    "prostate": ("adult", "adult_anatomy"),
    "m14": ("weapons", "firearm"),
    "projectile_trail": ("light_effect", "particles"),
    "dilapidated": ("outdoor_scene", "other_scene"),
    "rpg-7": ("weapons", "explosive"),
    "stutter": ("body", "body_state"),
    "boar_boy": ("people", "fantasy_person"),
    "husky": ("creatures", "mammal"),
    "insult": ("action", "interaction"),
    "sled": ("transport_play", "land_vehicle"),
    "torn": ("clothing_detail", "clothing_state"),
    "la_manchaland_(identity)_(project_moon)": ("themes", "persona_variant"),
    "relationship_graph": ("relationships", "comparison"),
    "cigarette_butt": ("household_objects", "other_object"),
    "distress": ("expression", "fear_surprise"),
    "gat_(hat)": ("accessories", "headwear"),
    "scaffolding": ("indoor_scene", "architecture"),
    "splatoonification": ("themes", "identity_change"),
    "execution": ("adult", "adult_gore"),
    "mac-10/11": ("weapons", "firearm"),
    "mp40": ("weapons", "firearm"),
    "new_generations_(idolmaster)": ("relationships", "group_faction"),
    "wonderlands_x_showtime_(project_sekai)": ("relationships", "group_faction"),
    "h&k_p30": ("weapons", "firearm"),
    "monado": ("weapons", "magic_weapon"),
    "snow_shelter": ("indoor_scene", "architecture"),
    "trellis": ("indoor_scene", "architecture"),
    "wimple": ("accessories", "headwear"),
    "yakitori": ("food_drink", "staple_food"),
    "forced_exposure": ("adult", "adult_nudity"),
    "stalactite": ("nature", "mineral"),
    "warp_star": ("transport_play", "air_vehicle"),
    "kiritanpo_(food)": ("food_drink", "staple_food"),
    "octagram": ("text_meta", "symbol"),
    "swaying": ("action", "movement"),
    "bolter": ("weapons", "firearm"),
    "grandmother_and_grandson": ("relationships", "family_relation"),
    "gyate_gyate": ("meta_info", "meme"),
    "hair_undone": ("hair", "hair_action"),
    "itabag": ("accessories", "bags_belts"),
    "ouendan": ("relationships", "group_faction"),
    "shoulder-to-shoulder": ("relationships", "comparison"),
    "boss_fight": ("action", "combat_action"),
    "dripping_eye": ("light_effect", "other_effect"),
    "hoe": ("household_objects", "tools"),
    "porsche": ("text_meta", "brand"),
    "goldfish_scooping": ("recreation", "games"),
    "h&k_psg1": ("weapons", "firearm"),
    "jack_(playing_card)": ("recreation", "games"),
    "magnolia": ("nature", "plant"),
    "pepperoni": ("food_drink", "meat_seafood"),
    "piston": ("mech_scifi", "machine"),
    "stereo": ("digital_media", "camera_media"),
    "tehepero": ("expression", "positive"),
    "transformer": ("household_objects", "appliance"),
    "black_sun": ("outdoor_scene", "sky_space"),
    "playstation_vita": ("digital_media", "phone_computer"),
    "qilin_(mythology)": ("creatures", "fantasy_creature"),
    "arrest": ("themes", "narrative_situation"),
    "m4_sherman": ("transport_play", "land_vehicle"),
    "moire": ("light_effect", "optical"),
    "searching": ("action", "daily_action"),
    "late_for_school": ("themes", "narrative_situation"),
    "shield_module": ("mech_scifi", "scifi_device"),
    "alraune": ("people", "fantasy_person"),
    "babywearing": ("action", "holding"),
    "clima-tact": ("weapons", "magic_weapon"),
    "criss-cross_strings": ("clothing_detail", "clothing_structure"),
    "liu_association_south_(identity)_(project_moon)": ("themes", "persona_variant"),
    "heel_pop": ("clothing_detail", "clothing_state"),
    "ageplay": ("adult", "adult_fetish"),
    "decantering": ("action", "daily_action"),
    "shotadom": ("adult", "adult_other"),
    "blood_drop": ("adult", "adult_fluid"),
    "smelling_hair": ("action", "interaction"),
    "bottle_to_cheek": ("action", "interaction"),
    "corn_cob": ("food_drink", "fruit_vegetable"),
    "a6m_zero": ("transport_play", "air_vehicle"),
    "garlic": ("food_drink", "fruit_vegetable"),
    "vespa": ("transport_play", "land_vehicle"),
    "clockwork": ("mech_scifi", "machine"),
    "conjoined": ("body", "body_state"),
    "cramped": ("body", "body_state"),
    "floppy_disk": ("digital_media", "phone_computer"),
    "ichimegasa": ("accessories", "headwear"),
    "irony": ("themes", "narrative_situation"),
    "bedtime_story": ("action", "daily_action"),
    "choir_outfit_(utdr)": ("clothes_special", "occupation_uniform"),
    "juggling": ("action", "daily_action"),
    "playstation_5": ("digital_media", "phone_computer"),
    "pomeranian_(dog)": ("creatures", "mammal"),
    "sesame_seeds": ("food_drink", "fruit_vegetable"),
    ";>": ("expression", "positive"),
    "hololive_gamers": ("relationships", "group_faction"),
    "loose_bandages": ("clothing_detail", "clothing_state"),
    "propaganda": ("text_meta", "text"),
    "splat_roller_(splatoon)": ("weapons", "other_weapon"),
    "ad_(object)": ("text_meta", "brand"),
    "atom": ("text_meta", "symbol"),
    "broken_pillar": ("indoor_scene", "architecture"),
    "diner": ("indoor_scene", "commercial"),
    "gibson_sg": ("culture_objects", "music"),
    "purple_buruma": ("clothes_special", "sports_uniform"),
    "waffle_cone": ("food_drink", "bakery"),
    "lobotomy_corporation_(identity)_(project_moon)": ("themes", "persona_variant"),
    "newhalf_with_female": ("adult", "adult_sex"),
    "uneven_footing": ("pose", "stationary_pose"),
    "akm": ("weapons", "firearm"),
    "lee-enfield": ("weapons", "firearm"),
    "bioluminescence": ("light_effect", "lighting"),
    "hatchet_(axe)": ("weapons", "blade"),
    "salt": ("food_drink", "staple_food"),
    "ad_(object)": ("text_meta", "text"),
    "transformer": ("mech_scifi", "machine"),
})


EXACT_OVERRIDES.update({
    # Dedicated condiment bucket added during the final food/material audit.
    "salt": ("food_drink", "seasoning"),
    "mustard": ("food_drink", "seasoning"),
    "ketchup": ("food_drink", "seasoning"),
    "sauce": ("food_drink", "seasoning"),
    "soy_sauce": ("food_drink", "seasoning"),
    "mayonnaise": ("food_drink", "seasoning"),
    "wasabi": ("food_drink", "seasoning"),
    "hot_sauce": ("food_drink", "seasoning"),
    "tomato_sauce": ("food_drink", "seasoning"),
    "pepper_(spice)": ("food_drink", "seasoning"),
    "maple_syrup": ("food_drink", "dessert_snack"),
    "strawberry_syrup": ("food_drink", "dessert_snack"),
    "green_bell_pepper": ("food_drink", "fruit_vegetable"),
    "red_pepper": ("food_drink", "fruit_vegetable"),
    "habanero_pepper": ("food_drink", "fruit_vegetable"),
    "swiss_cheese": ("food_drink", "dairy_ingredient"),
    "sliced_cheese": ("food_drink", "dairy_ingredient"),
    "cheese_wheel": ("food_drink", "dairy_ingredient"),
    "pepper_shaker": ("food_drink", "tableware"),
    "honey_dipper": ("food_drink", "tableware"),
    "butter_knife": ("food_drink", "tableware"),
    "battle_standard": ("text_meta", "symbol"),
    "canards": ("mech_scifi", "machine"),
    "fart": ("adult", "adult_other"),
})


EXACT_OVERRIDES.update({
    # v7 semantic audit: actual ornaments woven into hair or worn on the head.
    "ribbon_in_braid": ("accessories", "hair_accessory"),
    "ribbon_braid": ("accessories", "hair_accessory"),
    "flower_in_braid": ("accessories", "hair_accessory"),
    "flower_braid": ("accessories", "hair_accessory"),
    "single_hair_ring": ("accessories", "hair_accessory"),
    "hair_belt": ("accessories", "hair_accessory"),
    "head_ornament": ("accessories", "hair_accessory"),
    "head_bow": ("accessories", "hair_accessory"),
    "torn_hair_ribbon": ("accessories", "hair_accessory"),
    # A wound, not a hairstyle despite the word "forehead".
    "blood_from_forehead": ("body", "body_state"),
    "anti-eyebrow_piercing": ("accessories", "jewelry"),
    "eyebrow_piercing": ("accessories", "jewelry"),
    "nose_piercing": ("accessories", "jewelry"),
    "nostril_piercing": ("accessories", "jewelry"),
    "mole_on_nose": ("body", "body_marks"),
    "kissing_nose": ("action", "interaction"),

    # v7 accessory-boundary audit.  These placements follow what the object is
    # and where it is worn, rather than whichever body-part word appears first.
    "choker": ("accessories", "jewelry"),
    "choker_jewel": ("accessories", "jewelry"),
    "spiked_armlet": ("accessories", "jewelry"),
    "dog_tags": ("accessories", "jewelry"),
    "millennium_puzzle": ("accessories", "jewelry"),
    "kundala_(fate)": ("accessories", "jewelry"),
    "symphogear_pendant": ("accessories", "jewelry"),
    "pocket_watch": ("household_objects", "clock"),
    "goggles_around_neck": ("accessories", "neckwear"),
    "mask_around_neck": ("accessories", "neckwear"),
    "eyewear_around_neck": ("accessories", "neckwear"),
    "scarf_on_head": ("accessories", "headwear"),
    "necktie_on_head": ("accessories", "headwear"),
    "headwear_with_attached_mittens": ("accessories", "headwear"),
    "bag_over_head": ("accessories", "headwear"),
    "bag_on_head": ("accessories", "headwear"),
    "candle_on_head": ("accessories", "headwear"),
    "arm_scarf": ("accessories", "handwear"),
    "necktie_around_wrists": ("accessories", "handwear"),

    # Actions whose object happens to be an accessory.
    "looking_over_eyewear": ("pose", "gaze"),
    "hand_on_eyewear": ("pose", "hand_gesture"),
    "hands_on_eyewear": ("pose", "hand_gesture"),
    "finger_on_eyewear": ("pose", "hand_gesture"),
    "hand_on_goggles": ("pose", "hand_gesture"),
    "hand_on_mask": ("pose", "hand_gesture"),
    "hat_tip": ("pose", "hand_gesture"),
    "hat_tug": ("pose", "hand_gesture"),
    "adjusting_hood": ("action", "daily_action"),
    "adjusting_goggles": ("action", "daily_action"),
    "putting_on_jewelry": ("action", "daily_action"),
    "adjusting_earrings": ("action", "daily_action"),
    "putting_on_earrings": ("action", "daily_action"),
    "adjusting_bowtie": ("action", "daily_action"),
    "tying_necktie": ("action", "daily_action"),
    "adjusting_bow": ("action", "daily_action"),
    "adjusting_hair_ornament": ("action", "daily_action"),
    "tying_headband": ("action", "daily_action"),
    "from_hat_trick": ("action", "daily_action"),

    # English compounds that are not accessories in their documented sense.
    "conveyor_belt_sushi": ("food_drink", "staple_food"),
    "dilation_belt": ("adult", "adult_fetish"),
    "in_bag": ("themes", "narrative_situation"),
    "handkerchief": ("household_objects", "tools"),
    "tuanshan": ("household_objects", "tools"),
    "stirrups_(riding)": ("recreation", "sports"),
    "spurs": ("recreation", "sports"),
    "oonusa": ("weapons", "magic_weapon"),
    "crosier": ("weapons", "polearm"),
    "baby_carrier": ("household_objects", "other_object"),
    # The database wiki defines this entry as the brewing pouch, not the sexual
    # slang meaning suggested by the previous translation.
    "teabag": ("food_drink", "drink"),
})


EXACT_OVERRIDES.update({
    # v7 predicate audit: these tags describe actions or gestures; their body,
    # face, hair or garment noun is only the action's object.
    **dict.fromkeys((
        "poking_another's_breast", "covering_another's_breasts", "biting_another's_finger",
        "biting_another's_hand", "hugging_with_one_arm", "covering_another's_eyes",
        "covering_another's_mouth", "biting_another's_lip", "biting_ear",
        "covering_with_blanket", "biting_another's_tail", "biting_shoulder", "poking_belly",
        "mutual_cheek_pinching", "brushing_another's_teeth", "blowing_in_ear",
        "brushing_another's_hair", "drying_another's_hair", "adjusting_another's_hair",
        "cutting_another's_hair", "tying_another's_hair",
    ), ("action", "interaction")),
    **dict.fromkeys((
        "biting_arm", "biting_own_finger", "biting_finger", "nail_biting", "biting_own_lip",
        "biting_own_tongue", "biting_own_tail", "biting_own_thumb", "biting_hair", "wiping_sweat",
        "rubbing_eyes", "wiping_mouth", "wiping_tears", "smelling_clothes", "smelling_flower",
        "brushing_teeth", "dishwashing", "brushing_tail", "adjusting_hair", "tying_hair",
        "tucking_hair", "twirling_hair", "brushing_hair", "hair_lift", "hairdressing", "drying_hair",
        "cutting_hair", "ruffling_hair", "bunching_hair", "hair_flip", "drying_own_hair",
        "brushing_own_hair", "cutting_own_hair", "untying_hair", "braiding_hair",
        "braiding_own_hair", "wringing_skirt", "wringing_clothes", "drying_clothes",
    ), ("action", "daily_action")),
    **dict.fromkeys((
        "covering_body", "covering_one_breast", "covering_ass", "covering_own_eyes",
        "covering_own_ears", "covering_head", "covering_own_face", "poking_own_breast",
        "scratching_stomach", "pulling_own_ear", "scratching_chin", "hand_over_own_mouth",
        "hand_over_eye", "snapping_fingers", "shouting_with_hands", "patting_lap", "hand_wave",
    ), ("pose", "hand_gesture")),
    "hugging_own_leg": ("pose", "body_pose"),
    **dict.fromkeys(("opening_eyes", "closing_eyes", "blinking"), ("pose", "gaze")),
    "eye_poke": ("action", "combat_action"),
    **dict.fromkeys((
        "removing_thighhigh", "biting_glove", "adjusting_footwear", "putting_on_footwear",
        "adjusting_shoe", "tying_footwear", "tying_apron", "pinching_sleeves", "removing_pasties",
        "bikini_tug", "panty_tug", "pantyhose_tug", "jacket_tug", "trying_on_clothes",
        "changing_clothes", "opening_another's_clothes", "cutting_clothes", "tearing_clothes",
        "removing_wig",
    ), ("action", "clothing_action")),
    **dict.fromkeys(("smelling_ass", "smelling_armpit", "smelling_feet", "smelling_underwear"), ("adult", "adult_fetish")),
    "breast_biting": ("adult", "adult_oral"),
    **dict.fromkeys(("biting_clothes", "pillow_bite"), ("adult", "adult_suggestive")),
    "snake_bite": ("body", "body_marks"),
})


EXACT_OVERRIDES.update({
    # v7 semantic recovery from the conservative "other" buckets.
    **dict.fromkeys((
        "sneaking", "breakdance", "following", "pouncing", "rowing", "swinging", "backflip",
        "dribbling_(basketball)", "dip_(dance_move)", "slam_dunk_(basketball)", "somersault",
        "skydive", "dive", "acrobatics", "takeoff", "snake_box_sneak", "headbanging",
        "para_para", "wiggling",
    ), ("action", "movement")),
    **dict.fromkeys((
        "tackle", "crotch_stomping", "whipping", "spell", "chop", "kneeing", "elbowing",
        "predation", "overhead_swing", "smack", "sword_fight", "shoving",
    ), ("action", "combat_action")),
    "tug": ("action", "holding"),
    **dict.fromkeys((
        "snoot_challenge", "caress", "calling", "bumping", "pushing_down", "squeezing_cheeks",
        "bearhug", "helping", "rescue", "patting_back", "goodbye", "covering_another's_crotch",
        "shaving_another", "fed_by_viewer", "kiss_from_behind", "meeting", "stroking",
        "mutual_cheek_pinching", "footsies", "praise", "blood_sucking",
    ), ("action", "interaction")),
    **dict.fromkeys((
        "digging", "opening", "repairing", "drawing_on_air", "drawing", "buying_condoms",
        "chopping", "turning_page", "slurping", "applying_bandages", "first_aid", "mixing",
        "barking", "checking_pulse", "coin_flip", "drumming", "counting", "nibbling",
        "brushing", "decorating", "rock_balancing", "drawing_on_own_face", "whisking",
        "chugging", "wringing", "harvest", "kneading_dough", "unwrapping", "pecking", "ragequit",
    ), ("action", "daily_action")),
    **dict.fromkeys((
        "flick", "can_to_cheek", "palmar_flexion", "objection", "fan_over_face",
        "scratching_chin", "wrist_extended", "fist_shaking",
    ), ("pose", "hand_gesture")),
    **dict.fromkeys(("backbend", "dab_(dance)", "squat_(exercise)", "planking", "narrative_formation"), ("pose", "body_pose")),
    **dict.fromkeys(("pantsing", "buttoning", "superman_exposure"), ("action", "clothing_action")),
    "victory": ("expression", "positive"),
    "flinch": ("expression", "fear_surprise"),
    "growling": ("expression", "anger"),
    "mourning": ("expression", "sad_cry"),
    "denial": ("expression", "neutral_expression"),
    **dict.fromkeys(("recharging", "hiccup"), ("body", "body_state")),
    "bitten": ("body", "body_marks"),
    **dict.fromkeys(("shrinking", "mega_evolution"), ("themes", "identity_change")),
    **dict.fromkeys((
        "cheating_(competitive)", "blackmail", "interrupted", "revenge", "betrayal",
        "domestic_violence", "pizza_delivery",
    ), ("themes", "narrative_situation")),
    **dict.fromkeys(("hurdle", "capoeira", "horseback_archery", "dodgeball"), ("recreation", "sports")),
})


EXACT_OVERRIDES.update({
    # v7 chest/torso audit: explicit activities and external objects leave the
    # body-attribute library before the remaining anatomy is split by region.
    **dict.fromkeys((
        "breast_sucking", "double_breast_sucking", "mutual_breast_sucking",
        "sucking_on_multiple_breasts", "sucking_own_breasts",
    ), ("adult", "adult_oral")),
    **dict.fromkeys(("bound_breasts", "bound_torso"), ("adult", "adult_bondage")),
    "breast_smother": ("adult", "adult_fetish"),
    **dict.fromkeys((
        "breast_biting", "breast_massage", "breast_on_breast", "breast-to-pectoral_docking",
        "pectoral_docking", "covering_another's_breasts", "face_between_breasts", "face_to_breasts",
        "face_to_pecs", "head_between_pecs", "poking_another's_breast", "poking_own_breast",
        "slapping_breasts", "tickling_breasts", "navel_stimulation", "breasts_on_another's_back",
        "grabbed_breast_over_shoulder", "cream_on_breasts", "breast_press", "spread_armpit",
    ), ("adult", "adult_suggestive")),
    **dict.fromkeys(("breast_curtain_lift", "torso_flash"), ("adult", "adult_nudity")),
    "navel_insertion": ("adult", "adult_other"),
    **dict.fromkeys(("hole_in_chest", "hole_in_stomach", "severed_torso", "disembodied_torso", "heart_out_of_chest"), ("sensitive", "gore")),
    **dict.fromkeys(("blood_on_breasts", "blood_on_stomach", "bandaged_chest", "bandaged_torso", "mole_under_breast"), ("body", "body_marks")),
    **dict.fromkeys((
        "bottle_between_breasts", "can_between_breasts", "card_between_breasts", "food_between_breasts",
        "food_on_breasts", "gun_between_breasts", "phone_between_breasts", "sword_between_breasts",
        "condom_between_breasts", "hose_between_breasts", "tentacle_between_breasts",
        "animal_between_breasts", "animal_on_chest", "person_between_breasts", "between_breasts",
        "between_pectorals",
    ), ("action", "holding")),
    "head_on_another's_stomach": ("action", "interaction"),
    **dict.fromkeys((
        "arm_between_breasts", "arm_under_breasts", "arms_under_breasts", "breast_suppress",
        "covering_one_breast", "scratching_stomach",
    ), ("pose", "hand_gesture")),
    **dict.fromkeys((
        "breast_rest", "breasts_on_glass", "breasts_squeezed_together", "pectoral_press",
        "pectoral_squeeze", "carried_breast_rest",
    ), ("pose", "body_pose")),
    **dict.fromkeys(("chest_guard", "chest_protector"), ("clothes_special", "helmet_protective")),
    "chest_rig": ("accessories", "bags_belts"),
    "flower_on_chest": ("accessories", "badges_ornaments"),
    "stomach_jewel": ("accessories", "jewelry"),
    "chest_(furniture)": ("household_objects", "storage_furniture"),
    **dict.fromkeys(("breasts_day", "stomach_day", "good_breasts_day", "flat_chest_joke", "oppai_mochi"), ("meta_info", "meme")),
})


EXACT_OVERRIDES.update({
    # v7 waist/leg audit.
    **dict.fromkeys((
        "leg_warmers", "white_leg_warmers", "black_leg_warmers", "pink_leg_warmers",
        "striped_leg_warmers", "single_leg_warmer", "blue_leg_warmers", "grey_leg_warmers",
        "red_leg_warmers", "purple_leg_warmers", "fur_leg_warmers", "yellow_leg_warmers",
        "brown_leg_warmers", "belted_leg_warmers", "green_leg_warmers", "orange_leg_warmers",
    ), ("legwear_footwear", "stockings")),
    **dict.fromkeys(("knee_pads", "single_knee_pad", "knee_guards", "knee_brace", "leg_cast"), ("clothes_special", "helmet_protective")),
    **dict.fromkeys((
        "bandaged_leg", "gauze_on_knee", "gauze_on_leg", "scraped_knee", "thigh_marking",
        "sticker_on_leg", "ofuda_on_leg", "bandaged_waist", "bandaged_knees",
    ), ("body", "body_marks")),
    **dict.fromkeys((
        "clothes_around_waist", "towel_around_waist", "clothes_between_thighs",
        "buruma_around_one_leg", "towel_on_legs", "ass_peek", "thigh_peek",
    ), ("clothing_detail", "open_wear")),
    "removing_thighhigh": ("action", "clothing_action"),
    "hip_vent": ("clothing_detail", "cutout_slit"),
    "empire_waist": ("clothing_detail", "other_structure"),
    **dict.fromkeys((
        "bound_legs", "bound_thighs", "bound_knees", "bound_leg", "chained_legs", "locked_legs",
    ), ("adult", "adult_bondage")),
    **dict.fromkeys(("spread_ass", "spreading_own_ass"), ("adult", "adult_self")),
    **dict.fromkeys((
        "spreading_another's_ass", "covering_ass", "face_in_ass", "ass-to-ass", "food_in_ass",
        "thigh_straddling", "leg_on_another's_shoulder", "legs_on_another's_shoulders",
        "sword_between_thighs", "bulge_to_ass",
    ), ("adult", "adult_suggestive")),
    **dict.fromkeys(("smelling_ass", "ass_smack"), ("adult", "adult_fetish")),
    **dict.fromkeys(("ass_shake", "swaying_hip", "trembling_legs", "swinging_legs"), ("action", "movement")),
    **dict.fromkeys((
        "hand_between_own_legs", "hand_between_legs", "hand_between_thighs", "arm_on_knee",
        "elbow_on_knee", "arms_on_knees", "elbows_on_knees", "arm_on_thigh", "elbow_on_thigh",
        "arm_on_own_leg", "arm_around_leg", "hugging_own_leg", "patting_lap",
    ), ("pose", "hand_gesture")),
    **dict.fromkeys((
        "arm_around_another's_waist", "arms_around_another's_waist", "tickling_legs",
    ), ("action", "interaction")),
    **dict.fromkeys((
        "book_on_lap", "pokemon_on_lap", "animal_on_leg", "bird_on_leg", "food_on_legs", "chocolate_on_legs",
    ), ("action", "holding")),
    "pov_legs": ("composition", "subject_focus"),
    **dict.fromkeys(("bird_legs", "chicken_leg", "animal_legs", "goat_legs"), ("creatures", "fur_feature")),
    "wheeled_leg(s)": ("mech_scifi", "cybernetic"),
    **dict.fromkeys(("multiple_legs", "extra_legs", "reverse-jointed_legs", "bad_leg", "convenient_leg"), ("body", "body_state")),
    **dict.fromkeys((
        "tail_around_own_leg", "tail_between_legs", "tail_around_another's_leg",
        "tail_around_another's_waist", "tail_around_own_waist",
    ), ("creatures", "tails")),
    **dict.fromkeys((
        "legs_together", "leg_between_thighs", "leg_wrap", "arms_between_legs", "arm_between_legs",
        "outstretched_leg", "outstretched_legs", "over_the_knee", "separated_legs", "thighs_together",
        "hands_under_legs", "arm_across_waist", "hand_around_waist", "hand_wrapped_around_waist",
        "head_on_knee",
    ), ("pose", "body_pose")),
})


EXACT_OVERRIDES.update({
    # v7 arm/hand/foot audit.
    **dict.fromkeys((
        "arm_warmers", "striped_arm_warmers", "black_arm_warmers", "pink_arm_warmers",
        "single_arm_warmer", "white_arm_warmers", "purple_arm_warmers", "blue_arm_warmers",
        "red_arm_warmers", "brown_arm_warmers", "grey_arm_warmers", "yellow_arm_warmers",
        "green_arm_warmers", "mismatched_arm_warmers", "fur-trimmed_arm_warmers", "arm_garter",
        "arm_cuffs", "metal_arm_cuffs", "bandana_around_arm", "hand_wraps", "inflatable_armbands",
        "cross-laced_armwear", "black_arm_garter",
    ), ("accessories", "handwear")),
    "foot_wraps": ("legwear_footwear", "socks"),
    **dict.fromkeys(("arm_guards", "elbow_pads", "single_elbow_pad", "arm_sling", "single_arm_guard"), ("clothes_special", "helmet_protective")),
    **dict.fromkeys((
        "bandaged_arm", "bandaged_hand", "bandaged_fingers", "bandaged_foot", "sticker_on_arm",
        "taped_hands", "taped_arms", "gauze_on_arm",
    ), ("body", "body_marks")),
    **dict.fromkeys((
        "bound_arms", "bound_toes", "bound_feet", "bound_fingers", "chain_around_arm",
        "hand_gagged", "hand_chains",
    ), ("adult", "adult_bondage")),
    **dict.fromkeys(("foot_worship", "foot_massage", "toe_sucking"), ("adult", "adult_fetish")),
    **dict.fromkeys((
        "knives_between_fingers", "ofuda_between_fingers", "food_on_hand", "chocolate_on_hand",
        "card_between_fingers", "needles_between_fingers", "chocolate_on_foot", "between_fingers",
        "between_toes", "towel_on_arm", "bugles_on_fingers",
    ), ("action", "holding")),
    **dict.fromkeys((
        "applying_manicure", "painting_fingernails", "painting_toenails", "hand_milking",
        "breathing_on_hands", "warming_hands",
    ), ("action", "daily_action")),
    **dict.fromkeys(("armbar", "hand_sonic"), ("action", "combat_action")),
    "arm_wrestling": ("recreation", "sports"),
    **dict.fromkeys(("pov_hands", "feet_only", "surrounded_by_hands", "surrounded_by_feet"), ("composition", "subject_focus")),
    "cropped_arm": ("composition", "framing"),
    "censored_feet": ("meta_info", "censorship"),
    "hand_size_difference": ("relationships", "comparison"),
    "clock_hands": ("household_objects", "clock"),
    **dict.fromkeys(("hand_jewel", "ring_on_every_finger"), ("accessories", "jewelry")),
    **dict.fromkeys(("wrong_foot", "bad_arm"), ("style", "quality")),
    **dict.fromkeys((
        "drill_hand", "blade_arm", "false_arm", "hook_hand", "nobiiru_arm", "arm_slave_(mecha)",
    ), ("mech_scifi", "cybernetic")),
    "winged_arms": ("creatures", "wing_feather"),
    **dict.fromkeys((
        "webbed_hands", "webbed_feet", "clawed_feet", "clawed_hands", "tentacles_as_hands",
        "tentacle_arm", "spiked_arm", "tentacle_pit", "elbow_spikes",
    ), ("creatures", "claw_scale")),
    **dict.fromkeys(("cat_feet", "fluffy_hands"), ("creatures", "fur_feature")),
    "feather_fingers": ("creatures", "wing_feather"),
    **dict.fromkeys((
        "disembodied_hand", "extra_arms", "no_feet", "convenient_arm", "asymmetrical_arms",
        "skeletal_arm", "skeletal_hand", "extra_hands", "separated_arms", "giant_hand",
        "ghost_hands", "no_hands", "too_many_hands", "convenient_hand", "no_fingers",
        "transparent_hand", "missing_finger", "no_toes", "hand_eye",
    ), ("body", "body_state")),
    **dict.fromkeys((
        "hand_in_own_hair", "outstretched_hand", "open_hand", "own_hands_clasped", "open_hands",
        "steepled_fingers", "hands_in_own_hair", "middle_finger", "spread_fingers", "curled_fingers",
        "index_fingers_together", "guiding_hand", "hand_rest", "cupping_hands", "offering_hand",
        "index_fingers_raised", "hand_grip", "hand_to_head", "fingers_to_cheeks", "l_hand",
        "x_fingers", "string_around_finger", "hand_over_face", "ball_hands", "peeking_through_fingers",
        "hand_gesture", "fist_in_hand", "double_middle_finger", "cupping_hand", "crossed_fingers",
        "hands_clasped_in_delight", "hover_hand", "hand_over_heart", "head_on_hands", "face_in_hands",
        "triangle_hands", "twiddling_fingers", "fingers_between_toes", "elbow_on_arm",
        "fourth_position_of_the_arms", "paint_on_fingers", "fingers_to_cheek", "circle_hands",
        "flower_hands", "tapping_finger",
    ), ("pose", "hand_gesture")),
    **dict.fromkeys((
        "v_arms", "spread_arms", "feet_up", "locked_arms", "w_arms", "spread_toes", "toe_scrunch",
        "foot_up", "arm_held_back", "arm_wrap", "arm_around_back", "arm_above_head", "arm_over_head",
        "foot_dangle", "arms_around_back", "heart_arms", "x_arms", "arm_on_own_head",
        "one_arm_handstand", "arm_over_shoulder", "heart_arms_duo", "wiggling_toes", "hand_around_neck",
        "toes_up", "outstretched_crossed_arms", "foot_up_heel_up", "hand_to_hand", "airplane_arms",
        "arms_on_head", "between_feet", "arms_around_self", "head_arms", "outstretched_foot",
        "arm_rest", "elbow_rest", "arm_across_neck",
    ), ("pose", "body_pose")),
    **dict.fromkeys((
        "arm_around_shoulder", "hand_in_another's_hair", "arm_around_another's_back", "bird_on_hand",
        "butterfly_on_hand", "animal_on_arm", "bird_on_arm", "animal_on_hand", "tickling_feet",
        "tickling_armpits", "arms_around_another's_back", "foot_on_another's_head",
        "foot_on_another's_face", "hands_in_another's_hair", "pokemon_on_arm", "arm_on_another's_head",
        "feet_on_another's_face", "elbow_on_another's_shoulder", "taking_another's_hand",
        "hanging_on_arm", "arm_behind_another's_back", "foot_on_another's_back",
        "offering_hand_to_another", "insect_on_finger", "foot_on_head", "snake_wrapped_around_arm",
        "foot_kabedon", "arms_around_neck", "arm_around_neck",
    ), ("action", "interaction")),
    "tail_around_arm": ("creatures", "tails"),
    "wheel_o_feet": ("composition", "layout"),
    "flaming_hand": ("light_effect", "magic_effect"),
    **dict.fromkeys((
        "red_hands", "black_hands", "blue_hands", "purple_hands", "green_hands", "yellow_hands",
        "red_feet", "golden_arms", "light-skinned_palms", "green_arm",
    ), ("body", "skin")),
})


EXACT_OVERRIDES.update({
    # v7 final predicate pass and plant-compound audit.
    **dict.fromkeys((
        "arms_around_neck", "arm_around_shoulder", "hand_in_another's_hair", "arm_around_waist",
        "arms_around_waist", "arm_over_shoulder", "hand_over_another's_mouth", "tickling_feet",
        "tickling_armpits", "tickling_stomach", "tickling_legs", "giving_food", "sharing_food",
        "giving_flower", "hugging_another's_tail", "foot_kabedon", "arm_on_another's_head",
    ), ("action", "interaction")),
    **dict.fromkeys((
        "applying_lipstick", "applying_manicure", "painting_fingernails", "painting_toenails",
        "breathing_on_hands", "warming_hands", "hand_milking", "recording_audio", "eating_flower",
    ), ("action", "daily_action")),
    **dict.fromkeys(("ass_shake", "climbing_tree"), ("action", "movement")),
    **dict.fromkeys((
        "hand_in_own_hair", "hand_between_own_legs", "hand_between_legs", "index_fingers_together",
        "fingers_to_cheeks", "ofuda_between_fingers", "twiddling_fingers", "hand_on_own_tail",
    ), ("pose", "hand_gesture")),
    **dict.fromkeys(("arm_rest", "flexing", "arm_over_head", "ass_support", "wiggling_toes"), ("pose", "body_pose")),
    "peeking_through_fingers": ("pose", "gaze"),
    "headwear_switch": ("themes", "persona_variant"),
    **dict.fromkeys(("breast_press", "spread_armpit"), ("adult", "adult_suggestive")),
    "spread_ass": ("adult", "adult_self"),
    "spitting_in_another's_mouth": ("adult", "adult_oral"),
    "ass_smack": ("adult", "adult_fetish"),

    **dict.fromkeys(("on_grass", "in_tree", "against_tree", "sitting_in_tree", "on_flower", "on_tree", "behind_tree", "hanging_from_tree"), ("pose", "body_pose")),
    "under_tree": ("outdoor_scene", "forest_field"),
    "smelling_flower": ("action", "daily_action"),
    **dict.fromkeys((
        "neck_flower", "horn_flower", "wrist_flower", "ear_flower", "ankle_flower", "tail_flower", "bow_flower",
    ), ("accessories", "badges_ornaments")),
    "footwear_flower": ("clothing_detail", "trim_detail"),
    "super_saiyan_rose": ("themes", "persona_variant"),
    **dict.fromkeys(("soccer_field", "baseball_field"), ("recreation", "sports")),
    **dict.fromkeys((
        "karate_gi", "raimon_soccer_uniform", "satogahama_baseball_uniform",
        "karasuno_volleyball_uniform", "japanese_national_soccer_team_uniform",
        "ooarai_volleyball_uniform", "nekoma_volleyball_uniform",
    ), ("clothes_special", "sports_uniform")),
    "rabbit_youkai_group_(touhou)": ("relationships", "group_faction"),

    # Wiki-audited animal-feature homonyms and compounds.  These exact entries
    # prevent wearable ears, hairstyles, audio gear and actions from being
    # mistaken for anatomy merely because their names mention an ear or tail.
    **dict.fromkeys((
        "fake_animal_ears", "mickey_mouse_ears", "minnie_mouse_ears",
        "fake_horns", "fake_antlers",
    ), ("accessories", "headwear")),
    **dict.fromkeys(("hair_ears", "raccoon_tails_(hairstyle)"), ("hair", "hair_style")),
    **dict.fromkeys(("headphones_for_animal_ears", "earphones_on_animal_ears"), ("digital_media", "audio_device")),
    "playing_with_another's_ears": ("action", "interaction"),
    **dict.fromkeys(("flapping_ears", "flapping"), ("action", "movement")),
    "innertube_with_ears": ("recreation", "sports"),
    "tail_insertion": ("adult", "adult_sex"),
    "implied_tail_plug": ("adult", "adult_toys"),
    "tail_bell": ("accessories", "badges_ornaments"),
    "bandaged_tail": ("body", "body_marks"),
    **dict.fromkeys(("foxtail", "dock_(tail)"), ("creatures", "tails")),
    **dict.fromkeys(("talons", "suction_cups"), ("creatures", "claw_scale")),
    "hirschgeweih_antennas": ("mech_scifi", "machine"),
})


EXACT_OVERRIDES.update({
    # v7 adult-anatomy cleanup: ordinary chest traits and internal organs use
    # the normal body library; explicit exposure or fetish actions remain adult.
    **dict.fromkeys((
        "nipples", "puffy_nipples", "large_areolae", "inverted_nipples", "areolae", "dark_nipples",
        "no_nipples", "huge_nipples", "colored_nipples", "light_areolae", "dark_areolae",
        "blue_nipples", "nipple_indents", "small_nipples", "glands_of_montgomery", "purple_nipples",
        "long_nipples", "green_nipples", "light_nipples", "single_inverted_nipple", "black_nipples",
        "nipple_hair", "grey_nipples", "glowing_nipples", "extra_nipples",
    ), ("body", "breast_chest")),
    **dict.fromkeys(("nipple_rings", "nipple_bar"), ("accessories", "jewelry")),
    **dict.fromkeys(("bandaids_on_nipples", "mole_on_areola"), ("body", "body_marks")),
    **dict.fromkeys((
        "covered_nipples", "areola_slip", "nipple_slip", "censored_nipples", "covering_nipples",
        "covering_one_nipple",
    ), ("adult", "adult_nudity")),
    **dict.fromkeys(("nipple_cutout", "tape_on_nipples", "ofuda_on_nipples", "condom_on_nipples", "nipple_sleeves"), ("adult", "adult_clothes")),
    **dict.fromkeys(("chocolate_on_nipples", "spread_nipple"), ("adult", "adult_suggestive")),
    "tied_nipples": ("adult", "adult_bondage"),
    **dict.fromkeys(("uterus", "cervix", "ovum", "ovaries", "prostate", "ovum_with_heart"), ("body", "internal_organs")),
    "twitching_womb": ("body", "body_state"),
})


EXACT_OVERRIDES.update({
    # v7 global body-detail unification.  Region-specific legacy overrides used
    # to scatter the same concept across chest, arms and legs.
    **dict.fromkeys((
        "body_hair", "alternate_body_hair", "hairy", "very_hairy", "chest_hair",
        "sparse_chest_hair", "thick_chest_hair", "chest_hair_peek", "armpit_hair",
        "armpit_hair_peek", "excessive_armpit_hair", "colored_armpit_hair",
        "mismatched_armpit_hair", "white_armpit_hair", "arm_hair", "thick_arm_hair",
        "sparse_arm_hair", "leg_hair", "sparse_leg_hair", "thick_leg_hair", "back_hair",
        "stomach_hair",
    ), ("body", "body_hair")),
    **dict.fromkeys((
        "mole_on_thigh", "mole_on_ass", "mole_on_stomach", "mole_above_mouth", "mole_on_arm",
        "mole_on_chest", "mole_on_leg", "mole_on_forehead", "mole_beside_mouth", "body_freckles",
        "ass_freckles", "shoulder_freckles", "breast_freckles", "chest_freckles",
        "thigh_freckles", "no_freckles", "arm_freckles",
    ), ("body", "mole_freckle")),
    "bridge_piercing": ("accessories", "jewelry"),
    **dict.fromkeys((
        "black_bandages", "bandages_over_eyes", "loose_bandages", "gauze_over_eye",
        "bandaged_ankle", "bandaged_ear", "too_many_bandaids", "bandaged_horn", "torn_bandages",
    ), ("body", "bandage_patch")),
    "bandages_over_mouth": ("sensitive", "restraint"),
    "bandages_over_clothes": ("clothing_detail", "other_clothes"),
    **dict.fromkeys((
        "food_on_body", "food_on_breasts", "food_on_legs", "ice_cream_on_face", "food_on_hair",
        "chocolate_on_hand", "chocolate_on_legs", "chocolate_on_ass", "paint_on_fingers",
    ), ("body", "surface_stain")),
    "chocolate_on_foot": ("adult", "adult_fetish"),
    **dict.fromkeys((
        "blood", "bleeding", "blood_stain", "blood_splatter", "blood_spray", "blood_trail",
        "blood_drop", "blood_drip", "pool_of_blood", "bath_of_blood", "raining_blood",
        "pink_blood", "blue_blood", "yellow_blood", "black_blood", "purple_blood", "green_blood",
        "gold_blood", "white_blood", "fake_blood", "stylized_blood", "dried_blood",
        "bloody_handprints", "smeared_blood", "menstrual_blood", "spitting_blood", "coughing_blood",
        "nosebleed", "excessive_nosebleed", "blood_from_mouth", "blood_from_eyes",
        "blood_from_forehead", "blood_from_neck", "blood_in_hair", "blood_in_water",
        "blood_on_face", "blood_on_cheek", "blood_on_mouth", "blood_on_tongue", "blood_on_teeth",
        "blood_on_neck", "blood_on_shoulder", "blood_on_back", "blood_on_chest", "blood_on_stomach",
        "blood_on_breasts", "blood_on_arm", "blood_on_hand", "blood_on_hands", "blood_on_leg",
        "blood_on_feet", "blood_on_body", "blood_on_ground", "blood_on_wall", "blood_on_snow",
        "blood_on_bandages", "blood_on_clothes", "blood_on_armor", "blood_on_dress",
        "blood_on_shoes", "blood_on_flower", "blood_on_mask", "blood_on_eyewear",
        "blood_on_weapon", "blood_on_knife", "blood_on_axe", "blood_halo", "blood_in_mouth",
        "blood_on_gloves", "bloody_wings",
    ), ("sensitive", "blood")),
    "barefoot": ("body", "feet_toes"),
    "cannibalism": ("sensitive", "vore"),
    "multiple_tattoos": ("body", "tattoo_mark"),
    "scarab": ("creatures", "insect"),
    **dict.fromkeys((
        "blood_edge_(stellar_blade)", "rakuyo_(bloodborne)", "thorn_(elizabeth_rose_bloodflame)",
    ), ("weapons", "blade")),
    "blood_angels": ("relationships", "group_faction"),
    "blood_type": ("meta_info", "meta"),
})


# v8 semantic audit: high-use tags whose English head is ambiguous or is a
# franchise/name rather than an ordinary noun.  Their bundled Chinese/wiki
# definitions were reviewed individually; exact routing is safer than a broad
# substring rule that could damage unrelated tags.
EXACT_OVERRIDES.update({
    "knot": ("household_objects", "rope_lock"),
    "beam": ("light_effect", "other_effect"),
    "fluff": ("animal_traits", "fur_feature"),
    "genocide_route_(undertale)": ("themes", "narrative_situation"),
    "listen!!": ("culture_objects", "music"),
    "umapyoi_densetsu": ("culture_objects", "music"),
    "natsuiro_egao_de_1_2_jump!": ("culture_objects", "music"),
    "mogyutto_\"love\"_de_sekkin_chuu!": ("culture_objects", "music"),
    "snow_halation": ("culture_objects", "music"),
    "holy_grail_(fate)": ("household_objects", "other_object"),
    "grief_seed": ("household_objects", "other_object"),
    "plank": ("household_objects", "tools"),
    "hoop": ("recreation", "sports"),
    "meatball": ("food_drink", "staple_food"),
    "olive": ("food_drink", "fruit_vegetable"),
    "uzi": ("weapons", "firearm"),
    "tonguejob": ("adult", "adult_oral"),
    "urine_meter": ("adult", "adult_theme"),
    "erhu": ("culture_objects", "music"),
    "lightning_glare": ("light_effect", "optical"),
    "meltrandi": ("people", "fantasy_person"),
    "quiff": ("hair", "hair_style"),
    "6koma": ("text_meta", "comic"),
    "instant_soba": ("food_drink", "staple_food"),
    "instant_udon": ("food_drink", "staple_food"),
    "izakaya": ("indoor_scene", "commercial"),
    "multiple_insertions": ("adult_kink", "adult_insertion"),
    "smartwatch": ("digital_media", "phone_device"),
    "spas-12": ("weapons", "firearm"),
    "coin_(ornament)": ("accessories", "badges_ornaments"),
    "guarana_antarctica": ("food_drink", "drink"),
    "sphinx": ("creatures", "fantasy_creature"),
    "back_peek": ("adult_body", "adult_clothes"),
    "basketball_court": ("outdoor_scene", "other_scene"),
    "drifting": ("action", "movement"),
    "dying_message": ("text_meta", "text"),
    "ragnell": ("weapons", "blade"),
    "shanghai_neckline": ("clothing_detail", "collar_detail"),
    "arched_soles": ("body", "feet_toes"),
    "cat_stretch": ("pose", "body_pose"),
    "star_pendant": ("jewelry_accessories", "necklace_choker"),
    "yuujo": ("people", "occupation"),
    "ham": ("food_drink", "meat_seafood"),
    "jin_(headwear)": ("head_accessories", "hats_caps"),
    "mantis_girl": ("people", "fantasy_person"),
    "platform": ("indoor_scene", "public_indoor"),
    "browning_m2": ("weapons", "firearm"),
    "furry_and_humanization": ("themes", "identity_change"),
    "cheetah_girl": ("people", "fantasy_person"),
    "snoring": ("body_detail", "body_state"),
    "suomi_kp/-31": ("weapons", "firearm"),
    "t-34": ("transport_play", "land_vehicle"),
    "hover_bike": ("transport_play", "land_vehicle"),
    "messy_sleeper": ("pose", "stationary_pose"),
    "red_suspenders": ("accessories", "bags_belts"),
    "shipwreck": ("transport_play", "water_vehicle"),
    "doritos": ("food_drink", "dessert_snack"),
    "golden_shower": ("adult_kink", "adult_excretion"),
    "h&k_g3": ("weapons", "firearm"),
    "hime_lolita": ("clothing_appearance", "fashion_style"),
    "tsuchinoko": ("creatures", "reptile"),
    "blacksmith": ("people", "occupation"),
    "dreamcatcher": ("household_objects", "other_object"),
    "digivice": ("mech_scifi", "scifi_device"),
    "horizontal_bar": ("recreation", "sports"),
    "isopod": ("creatures", "aquatic"),
    "damage_numbers": ("text_meta", "screen_ui"),
    "test_tube_rack": ("household_objects", "tools"),
    "turnip": ("food_drink", "fruit_vegetable"),
    "acronym": ("text_meta", "text"),
    "nut_(hardware)": ("household_objects", "tools"),
    "sword_in_front_of_face": ("action", "combat_action"),
    "railroad_signal": ("urban_architecture", "urban"),
    "third_wheel": ("relationships", "comparison"),
    "wainscoting": ("urban_architecture", "surface"),
    "wolf_pelt": ("animal_traits", "fur_feature"),
    "karate": ("action", "combat_action"),
    "ea_(fate)": ("weapons", "blade"),
    "jamadhar": ("weapons", "blade"),
    "sleepover": ("themes", "narrative_situation"),
    "trick-or-treating": ("time_weather", "holiday"),
    "chameleon": ("creatures", "reptile"),
    "churro": ("food_drink", "dessert_snack"),
    "dazed": ("body_detail", "body_state"),
    "flour": ("food_drink", "dairy_ingredient"),
    "necrophilia": ("adult_kink", "adult_taboo"),
    "omnic": ("mech_scifi", "robot_android"),
    "display": ("indoor_scene", "commercial"),
    "human_meat_consumption": ("sensitive", "vore"),
    "twi'lek": ("people", "fantasy_person"),
    "uroko_(pattern)": ("clothing_appearance", "clothing_pattern"),
    "winged_unicorn": ("creatures", "fantasy_creature"),
    "miniature": ("recreation", "toys"),
    "railgun_(misaka_mikoto)": ("weapons", "magic_weapon"),
    "applying_pedicure": ("action", "daily_action"),
    "pile_of_skulls": ("sensitive", "gore"),
    "toy_block": ("recreation", "toys"),
    "fishing_net": ("household_objects", "tools"),
    "high_up": ("composition", "camera_angle"),
    "skylight": ("urban_architecture", "architecture"),
    "firewood": ("household_objects", "other_object"),
    "piloting": ("action", "daily_action"),
    "jogging": ("action", "movement"),
    "bust_(sculpture)": ("household_objects", "other_object"),
    "dirty_talk": ("adult", "adult_theme"),
    "savannah": ("outdoor_scene", "forest_field"),
    "skis": ("recreation", "sports"),
    "fly_agaric": ("nature", "plant"),
    "golden_retriever": ("creatures", "mammal"),
    "ice_cream_bar": ("food_drink", "dessert_snack"),
    "french_girly": ("clothing_appearance", "fashion_style"),
    "otter_girl": ("people", "fantasy_person"),
    "death": ("sensitive", "injury_death"),
    "dying": ("sensitive", "injury_death"),
    "imminent_death": ("sensitive", "injury_death"),
    "implied_death": ("sensitive", "injury_death"),
    "domestic_violence": ("sensitive", "injury_death"),
    **dict.fromkeys(("slave", "captured", "kidnapped", "in_cage", "arrest"), ("sensitive", "restraint")),
})


# v11 semantic audit: move only the remaining terms whose bundled aliases and
# descriptions identify one clear concept.  Deliberately ambiguous adjectives
# and object heads (spots, ornate, guide, handle, wax...) stay in the fallback
# library instead of being forced into a misleading category.
EXACT_OVERRIDES.update({
    "luminosite_eternelle": ("light_effect", "magic_energy"),
    "meni_shuki_rush-sshu!": ("expression", "positive"),
    "saigyouji_yuyuko's_fan_design": ("background", "background_pattern"),
    "i'll_teach_you_everything_(chainsaw_man)": ("themes", "narrative_situation"),
    "sunshower_(e.g.o)": ("weapons", "magic_weapon"),
    "abbreviated_karakusa": ("background", "background_pattern"),
    "sanbou": ("household_objects", "other_object"),
    "tear_troughs": ("face", "face_shape"),
    "waffen-ss": ("relationships", "group_faction"),
    "alpha_pokemon": ("themes", "persona_variant"),
    "muzzle_device": ("weapons", "firearm"),
    "candle_wax": ("household_objects", "other_object"),
    "nyoro~n": ("text_meta", "comic"),
    "taunting": ("action", "interaction"),
    "polyamory": ("relationships", "romance_orientation"),
    "scuba": ("recreation", "sports"),
    "chevrolet": ("text_meta", "brand"),
    "lamborghini": ("text_meta", "brand"),
    "fake_censor": ("meta_info", "censorship"),
    "hasu_no_sanrenka": ("relationships", "group_faction"),
    "holox": ("relationships", "group_faction"),
    "triad_primus_(idolmaster)": ("relationships", "group_faction"),
    "aqours_2nd_years": ("relationships", "group_faction"),
    "lotus_pod": ("nature", "flower_species"),
    "mizura": ("hair", "hair_style"),
    "oval_image": ("composition", "border"),
    "h&k_usp": ("weapons", "firearm"),
    "lappet": ("head_accessories", "headpiece"),
    "zombification": ("themes", "identity_change"),
    "eel_boy": ("people", "fantasy_person"),
    "healing": ("light_effect", "magic_energy"),
    "oshi-katsu": ("action", "daily_action"),
    "nattou": ("food_drink", "staple_food"),
    "postcard": ("culture_objects", "books_paper"),
    "rake": ("household_objects", "tools"),
    "samoyed_(dog)": ("creatures", "mammal"),
    "awestruck": ("expression", "fear_surprise"),
    "grey_corset": ("underwear_swim", "bra_lingerie"),
    "mosquito_coil": ("household_objects", "other_object"),
    "nakai_(waitress)": ("people", "occupation"),
    "teleportation": ("action", "movement"),
    "tennis_net": ("recreation", "sports"),
    "cool_&_sexy_(idolmaster)": ("franchise_clothes", "idol_outfit"),
    "milk_churn": ("household_objects", "container"),
    "physical_examination": ("action", "daily_action"),
    "ravenclaw": ("relationships", "group_faction"),
    "airpods": ("digital_media", "audio_device"),
    "bad_neck": ("style", "quality"),
    "barmaid": ("people", "occupation"),
    "blue_hawaii": ("food_drink", "drink"),
    "dvd_case": ("household_objects", "container"),
    "effects_pedal": ("digital_media", "audio_device"),
    "geass": ("light_effect", "magic_energy"),
    "german_suplex": ("action", "combat_action"),
    "gladiator": ("people", "role_focus"),
    "biometal": ("mech_scifi", "scifi_device"),
    "kamui_(kill_la_kill)": ("franchise_clothes", "franchise_outfit"),
    "snort": ("expression", "anger"),
    "gargoyle": ("creatures", "fantasy_creature"),
    "museum": ("indoor_scene", "public_indoor"),
    "videocassette": ("digital_media", "camera_video"),
    "autocannon": ("weapons", "firearm"),
    "onee_gyaru": ("clothing_appearance", "fashion_style"),
    "pickle": ("food_drink", "fruit_vegetable"),
    "sneer": ("expression", "anger"),
    "codpiece": ("protective_clothes", "torso_armor"),
    "golden_hour": ("light_effect", "lighting"),
    "pineapple_slice": ("food_drink", "fruit_vegetable"),
    "ryokan": ("indoor_scene", "commercial"),
    "sprite_art": ("style", "medium"),
    "newhalf_with_male": ("adult", "adult_sex"),
    "hippopotamus": ("creatures", "mammal"),
    "pensive": ("expression", "neutral_expression"),
    "sig_516": ("weapons", "firearm"),
    "h&k_g36": ("weapons", "firearm"),
    "fn_fal": ("weapons", "firearm"),
    "basin": ("household_objects", "container"),
    "blade_to_throat": ("action", "combat_action"),
    "mapo_tofu": ("food_drink", "staple_food"),
    "alpaca_girl": ("people", "fantasy_person"),
    "apple_core": ("food_drink", "fruit_vegetable"),
    "knightmare_frame": ("mech_scifi", "mecha"),
    "mazda_rx-7": ("transport_play", "land_vehicle"),
    "toaster": ("household_objects", "appliance"),
    "tweezers": ("household_objects", "tools"),
    "civilight_eterna": ("head_accessories", "headpiece"),
    "keffiyeh": ("traditional_clothes", "traditional_central_west"),
    "pile_bunker": ("weapons", "magic_weapon"),
    "poverty": ("themes", "narrative_situation"),
    "spiked_thighlet": ("jewelry_accessories", "bracelet_anklet"),
    "treadmill": ("recreation", "sports"),
    "unibrow": ("face", "eyebrows"),
    "bloated": ("body_detail", "body_state"),
    "cd_player": ("digital_media", "audio_device"),
    "in_coffin": ("pose", "stationary_pose"),
    "queen_of_hearts_(playing_card)": ("recreation", "games"),
    "valkyrie_(ensemble_stars!)": ("relationships", "group_faction"),
    "expectation_vs._reality": ("meta_info", "meme"),
    "exposed_gusset": ("adult_body", "adult_clothes"),
    "heavy_metal": ("style", "genre"),
    "j-core": ("style", "genre"),
    "pull_out": ("adult", "adult_sex"),
    "solemn_lament_(e.g.o)": ("weapons", "firearm"),
    "daifuku": ("food_drink", "dessert_snack"),
    "ohogao": ("adult", "adult_response"),
    "pokegear": ("digital_media", "phone_device"),
    "troll_(homestuck)": ("people", "fantasy_person"),
    "inkbrush_(splatoon)": ("weapons", "other_weapon"),
    "male_yandere": ("people", "role_focus"),
    "raver": ("people", "role_focus"),
    "splattershot_jr._(splatoon)": ("weapons", "firearm"),
    "starpiece_memories_(idolmaster)": ("franchise_clothes", "idol_outfit"),
    "animal_balloon": ("recreation", "toys"),
    "bakuzan": ("weapons", "blade"),
    "coach": ("people", "occupation"),
    "globus_cruciger": ("symbols", "religious_symbol"),
    "oyster": ("food_drink", "meat_seafood"),
    "snot_trail": ("body_detail", "body_function"),
    "carrot_pin": ("accessories", "badges_ornaments"),
    "competition": ("themes", "narrative_situation"),
    "mail": ("culture_objects", "books_paper"),
    "ppsh-41": ("weapons", "firearm"),
    "yunjian": ("traditional_clothes", "traditional_china"),
    "implied_erection": ("adult", "adult_response"),
    "photon_ray_(fate)": ("weapons", "blade"),
    "film_reel": ("digital_media", "camera_video"),
    "forearms": ("body", "arms_hands"),
    "fuse": ("weapons", "explosive"),
    "id_(fate/grand_order)": ("character", "letter_i"),
    "scene_fashion": ("clothing_appearance", "fashion_style"),
    "soybean": ("food_drink", "fruit_vegetable"),
    "golf": ("recreation", "sports"),
    "unlikely_accident": ("themes", "narrative_situation"),
    "aerokinesis": ("light_effect", "magic_energy"),
    "handlebar_mustache": ("face", "facial_hair"),
    "outer_senshi": ("relationships", "group_faction"),
    "school_gateway": ("building_parts", "fence_gate"),
    "scribble": ("style", "technique"),
    "slave_brand": ("body_detail", "tattoo_mark"),
    "stone_pillar": ("building_parts", "frame_structure"),
    "bren_lmg": ("weapons", "firearm"),
    "frisbee": ("recreation", "sports"),
    "green_tabard": ("clothes_main", "vest_top"),
    "inkling_(swim_form)": ("themes", "persona_variant"),
    "plug_gag": ("adult_kink", "adult_toys"),
    "pokemon_battle": ("action", "combat_action"),
    "quincy_(bleach)": ("people", "fantasy_person"),
    "too_many_butterflies": ("creatures", "insect"),
    "crossed_out": ("meta_info", "censorship"),
    "danmaku_comments": ("text_meta", "screen_ui"),
    "saya_(scabbard)": ("weapons", "other_weapon"),
    "shichirin": ("household_objects", "appliance"),
    "batter": ("food_drink", "dairy_ingredient"),
    "changmingsuo": ("jewelry_accessories", "necklace_choker"),
    "char_siu": ("food_drink", "meat_seafood"),
    "char-siu": ("food_drink", "meat_seafood"),
    "em-2": ("weapons", "firearm"),
    "manjuu_abuse_(azur_lane)": ("meta_info", "meme"),
    "primogem": ("recreation", "games"),
    "slap_mark_on_face": ("body_detail", "scar_wound"),
    "sunbathing": ("action", "daily_action"),
    "clarinet": ("culture_objects", "music"),
    "color_switch": ("light_effect", "palette"),
    "pedestrian_lights": ("urban_architecture", "urban"),
    "super_famicom": ("digital_media", "game_device"),
    "country_lolita": ("clothing_appearance", "fashion_style"),
    "ichininmae_no_lady": ("meta_info", "meme"),
    "vegetation": ("nature", "grass_crop"),
    "mailman": ("people", "occupation"),
    "hut": ("urban_architecture", "residential"),
    "double_bass": ("culture_objects", "music"),
    "gamecube": ("digital_media", "game_device"),
    "gardening_shears": ("household_objects", "tools"),
    "soil": ("outdoor_scene", "terrain_surface"),
    "splat_charger_(splatoon)": ("weapons", "firearm"),
    "okonomiyaki": ("food_drink", "staple_food"),
    "pullcart": ("transport_play", "land_vehicle"),
    "skull_head": ("body", "anatomy_anomaly"),
    "slipper_bathtub": ("household_objects", "care_cleaning"),
    "taiwan": ("outdoor_scene", "other_scene"),
    "performance_juxtaposition": ("adult", "adult_theme"),
    "pouring_onto_another": ("action", "interaction"),
    "shoulder_massage": ("action", "interaction"),
    "twerking": ("action", "movement"),
    "airgetlam_(fate)": ("weapons", "magic_weapon"),
    "raft": ("transport_play", "water_vehicle"),
    "stance_(vehicle)": ("transport_play", "land_vehicle"),
    "wii_remote": ("digital_media", "game_device"),
    "dorayaki": ("food_drink", "dessert_snack"),
    "homework": ("action", "daily_action"),
    "leppa_berry": ("food_drink", "fruit_vegetable"),
    "necromancer": ("people", "role_focus"),
    "roe": ("food_drink", "meat_seafood"),
    "ancestor_and_descendant": ("relationships", "family_relation"),
})

EXACT_OVERRIDES.update({
    "a_world_underneath": ("copyright", "letter_a"),
    "sore_wa_bokutachi_no_kiseki": ("culture_objects", "music"),
    "unyu": ("text_meta", "comic"),
    "black_panther": ("creatures", "mammal"),
    "lambent_light": ("weapons", "magic_weapon"),
    "avalon_le_fae_(fate/grand_order)": ("themes", "narrative_situation"),
    "faerie_knights_(fate)": ("relationships", "group_faction"),
    "chinese_empire": ("themes", "narrative_situation"),
    "wink_star": ("light_effect", "particles"),
    "brain_injection": ("sensitive", "gore"),
    "caldari_state_(eve_online)": ("relationships", "group_faction"),
    "dinosaur_boy": ("people", "fantasy_person"),
    "index_(identity)_(project_moon)": ("themes", "persona_variant"),
    "finch": ("creatures", "bird"),
    "original_remodel_(kantai_collection)": ("themes", "persona_variant"),
    "covered_underboob": ("adult_body", "adult_clothes"),
    "crew_cut": ("hair", "hair_style"),
    "jam_(umamusume)": ("relationships", "group_faction"),
    "party_horn": ("recreation", "toys"),
    "pentagon_(shape)": ("symbols", "shape_math"),
    "pop-up_headlights": ("mech_scifi", "machine"),
    "cs/ls06": ("weapons", "firearm"),
    "e16a_zuiun": ("transport_play", "air_vehicle"),
    "funeral": ("themes", "narrative_situation"),
    "gondola": ("transport_play", "water_vehicle"),
    "mian_guan": ("traditional_clothes", "traditional_china"),
    "moon_stick_(sailor_moon)": ("weapons", "magic_weapon"),
    "packet": ("household_objects", "container"),
    "paper_chain": ("accessories", "badges_ornaments"),
    "pedestal": ("household_objects", "other_object"),
    "prydwen_(fate)": ("weapons", "magic_weapon"),
    "black_suspenders": ("accessories", "bags_belts"),
    "french_cruller": ("food_drink", "dessert_snack"),
    "grumpy": ("expression", "anger"),
    "penguin_chick": ("creatures", "bird"),
    "rhongomyniad_(fate)": ("weapons", "polearm"),
    "zuiyin": ("body_detail", "tattoo_mark"),
    "chimame-tai": ("relationships", "group_faction"),
    "entry_plug": ("mech_scifi", "scifi_device"),
    "extendable_limbs": ("body", "limb_variation"),
    "marching_band_baton": ("culture_objects", "music"),
    "multiple_dogs": ("creatures", "mammal"),
    "polygamy": ("relationships", "romance_orientation"),
    "remington_870": ("weapons", "firearm"),
    "sandstar": ("light_effect", "magic_energy"),
    "serving": ("action", "daily_action"),
    "chopped_spring_onion": ("food_drink", "seasoning"),
    "sequins": ("clothing_detail", "trim_detail"),
    "cursed_energy_(jujutsu_kaisen)": ("light_effect", "magic_energy"),
    "double-sided_wrench": ("household_objects", "tools"),
    "earmuffs_around_neck": ("head_accessories", "headpiece"),
    "nen_(hunter_x_hunter)": ("light_effect", "magic_energy"),
    "sewer_grate": ("urban_architecture", "surface"),
    "smash_invitation": ("culture_objects", "books_paper"),
    "synthesizer": ("culture_objects", "music"),
    "zoo": ("outdoor_scene", "other_scene"),
    "lekku_(anatomy)": ("body", "anatomy_anomaly"),
    "vitarka_mudra": ("pose", "hand_gesture"),
    "white_devil": ("themes", "persona_variant"),
    "aks-74u": ("weapons", "firearm"),
    "animegao": ("head_accessories", "face_mask"),
    "heart_cure_watch": ("mech_scifi", "scifi_device"),
    "imminent_netorare": ("adult", "adult_theme"),
    "katsu_(food)": ("food_drink", "meat_seafood"),
    "chibi_on_shoulder": ("composition", "layout"),
    "gas": ("light_effect", "fire_smoke"),
    "ice_pack": ("household_objects", "care_cleaning"),
    "pot_on_head": ("head_accessories", "headpiece"),
    "u's_1st_years": ("relationships", "group_faction"),
    "arc_reactor": ("mech_scifi", "scifi_device"),
    "cucumber_slice": ("food_drink", "fruit_vegetable"),
    "drawing_on_sand": ("action", "daily_action"),
    "extreme_gaping": ("adult_kink", "adult_insertion"),
    "lipps_(idolmaster)": ("relationships", "group_faction"),
    "twirl_baton": ("recreation", "sports"),
    "corrugated_galvanized_iron_sheet": ("building_parts", "roof_exterior"),
    "familymart": ("text_meta", "brand"),
    "frappuccino": ("food_drink", "drink"),
    "playstation_2": ("digital_media", "game_device"),
    "dinosaur_girl": ("people", "fantasy_person"),
    "dough": ("food_drink", "dairy_ingredient"),
    "gambling": ("recreation", "games"),
    "gold_headband": ("head_accessories", "hairband_ribbon"),
    "mural": ("style", "medium"),
    "sight_magnifier": ("weapons", "firearm"),
    "dinner": ("food_drink", "staple_food"),
    "duijin_ruqun": ("traditional_clothes", "traditional_china"),
    "flyer": ("culture_objects", "books_paper"),
    "genkan": ("indoor_scene", "home_room"),
    "gyuudon": ("food_drink", "staple_food"),
    "recruiters_(disney)": ("relationships", "group_faction"),
    "yume_no_tsue": ("weapons", "magic_weapon"),
    "age_switch": ("themes", "identity_change"),
    "choujuu_gigaku": ("relationships", "group_faction"),
    "excalibur_(fate/prototype)": ("weapons", "blade"),
    "gith_(d&d)": ("people", "fantasy_person"),
    "tied_drawstring": ("clothing_detail", "fastener"),
    "colosseum": ("urban_architecture", "tower_landmark"),
    "head_spikes": ("body", "anatomy_anomaly"),
    "mascot_head": ("meta_info", "cosplay"),
    "royal_guard_set_(zelda)": ("franchise_clothes", "franchise_armor"),
    "star_pin": ("jewelry_accessories", "gem_brooch"),
    "tassets": ("protective_clothes", "leg_armor"),
    "tawawa_challenge": ("meta_info", "meme"),
    "tnt": ("weapons", "explosive"),
    "triangle_(instrument)": ("culture_objects", "music"),
    "venus_flytrap": ("nature", "unusual_plant"),
    "whisp": ("creatures", "fantasy_creature"),
    "chipmunk": ("creatures", "mammal"),
    "circus": ("outdoor_scene", "other_scene"),
    "day_and_night": ("time_weather", "time_day"),
    "marble_(stone)": ("nature", "mineral"),
    "marigold": ("nature", "flower_species"),
    "progress_bar": ("text_meta", "screen_ui"),
    "speculum": ("household_objects", "tools"),
    "subdermal_port": ("mech_scifi", "cybernetic"),
    "kabedon_on_viewer": ("action", "interaction"),
    "tricycle": ("transport_play", "land_vehicle"),
    "brown_bodystocking": ("underwear_swim", "bodysuit_leotard"),
    "cabin": ("urban_architecture", "residential"),
    "clapperboard": ("digital_media", "camera_video"),
    "daxiushan": ("traditional_clothes", "traditional_china"),
    "feigning_sleep": ("action", "daily_action"),
    "go_back!": ("text_meta", "comic"),
    "goron": ("people", "fantasy_person"),
})

# v12 skin-word collision audit.  These tags contain "skin" or "fang", but
# their actual concepts are a pose/state, mouth detail, garment or injury.
EXACT_OVERRIDES.update({
    "skin_fangs": ("face", "oral_detail"),
    "long_fangs": ("face", "oral_detail"),
    "deep_skin": ("body_detail", "body_state"),
    "skindentation": ("body_detail", "body_state"),
    "turn_pale": ("expression", "fear_surprise"),
    "skin_seams": ("body", "anatomy_anomaly"),
    "light-skinned_soles": ("body_detail", "skin"),
    "legskin": ("underwear_swim", "male_swim"),
    "skinned": ("sensitive", "gore"),
    "sand_on_skin": ("body_detail", "surface_stain"),
    "sunburn": ("body_detail", "skin"),
    "golden_arms": ("body", "anatomy_anomaly"),

    # Hair, eye and ear compounds whose head describes an action, symbol or
    # accessory rather than the body feature itself.
    **dict.fromkeys(("tall_hair", "low-tied_hair_ring", "multi-tied_hair", "expressive_hair"), ("hair", "hair_style")),
    "bangs_blown_up": ("hair", "hair_action"),
    **dict.fromkeys(("paint_in_hair", "ink_on_face", "dirty_feet", "dirty_hands"), ("body_detail", "surface_stain")),
    **dict.fromkeys((
        "blonde_facial_hair", "black_facial_hair", "white_facial_hair", "purple_facial_hair",
        "brown_facial_hair", "grey_facial_hair", "red_facial_hair", "blue_facial_hair",
    ), ("face", "facial_hair")),
    "hair_over_eyes": ("hair", "bangs"),
    "mark_under_both_eyes": ("body_detail", "tattoo_mark"),
    "eye_black": ("face", "makeup"),
    "eye_injury": ("body_detail", "scar_wound"),
    "goggles_on_eyes": ("head_accessories", "eyewear"),
    "veil_over_eyes": ("head_accessories", "headwrap_veil"),
    "hand_over_another's_eyes": ("action", "interaction"),
    "liquid_from_eyes": ("body_detail", "body_function"),
    "eye_drops": ("household_objects", "care_cleaning"),
    **dict.fromkeys(("eye_of_horus", "eye_of_providence"), ("symbols", "religious_symbol")),
    "eye_of_senri": ("symbols", "general_symbol"),
    "eyes_of_horus_(warhammer_40k)": ("symbols", "emblem"),
    **dict.fromkeys(("averting_eyes", "rolling_eyes", "upturned_eyes", "downturned_eyes", "downcast_eyes"), ("pose", "gaze")),
    "mob_face": ("face", "face_shape"),
    "eyelash_ornament": ("face", "makeup"),
    **dict.fromkeys(("flower_over_eye", "butterfly_over_eye"), ("face", "makeup")),
    "helmet_over_eyes": ("protective_clothes", "combat_helmet"),
    "hood_over_eyes": ("clothing_appearance", "open_wear"),
    **dict.fromkeys(("ears_up", "ears_back", "ear_tufts"), ("animal_traits", "animal_ears")),
    **dict.fromkeys(("rabbit_ear_headwear", "mismatched_ear_covers"), ("head_accessories", "headpiece")),
    "ear_wreath": ("jewelry_accessories", "earrings"),
    **dict.fromkeys(("pencil_behind_ear", "object_behind_ear"), ("action", "holding")),
    "ear_blush": ("expression", "shy_blush"),

    # "In mouth" tags are primarily held objects, gestures or explicit acts;
    # only actual lip/mouth shapes remain in face/mouth.
    **dict.fromkeys((
        "popsicle_in_mouth", "pocky_in_mouth", "ribbon_in_mouth", "utensil_in_mouth",
        "stalk_in_mouth", "lollipop_in_mouth", "toast_in_mouth", "flower_over_mouth",
        "flower_to_mouth", "glove_in_mouth", "smoking_pipe_in_mouth", "fish_in_mouth",
        "necktie_in_mouth", "plectrum_in_mouth", "eyewear_in_mouth", "knife_in_mouth",
        "chopsticks_in_mouth", "leaf_in_mouth", "pill_in_mouth", "snorkel_in_mouth",
        "unlit_cigarette_in_mouth", "thermometer_in_mouth", "pen_to_mouth",
        "grenade_pin_in_mouth", "petal_in_mouth", "necklace_in_mouth", "bullet_in_mouth",
        "string_in_mouth", "book_to_mouth", "sword_in_mouth", "feather_in_mouth",
        "hair_in_own_mouth",
    ), ("action", "holding")),
    **dict.fromkeys(("shirt_in_mouth", "dress_in_mouth", "skirt_in_mouth"), ("action", "clothing_action")),
    "hair_in_another's_mouth": ("action", "interaction"),
    **dict.fromkeys((
        "v_over_mouth", "middle_w", "fingers_to_mouth", "thumb_to_mouth", "pinky_to_mouth",
        "x_fingers_over_mouth", "hand_in_mouth",
    ), ("pose", "hand_gesture")),
    **dict.fromkeys(("over_the_mouth_gag", "gag_around_neck"), ("adult_kink", "adult_bondage")),
    **dict.fromkeys(("mouth_insertion", "tentacle_in_mouth", "hand_in_another's_mouth"), ("adult_kink", "adult_insertion")),
    "ass-to-mouth": ("adult", "adult_oral"),
    "gun_in_mouth": ("sensitive", "injury_death"),
    **dict.fromkeys(("panties_in_mouth", "leash_in_mouth"), ("adult_kink", "adult_fetish")),
    "mouth_beam": ("light_effect", "magic_energy"),
    "mouthful_mode": ("themes", "persona_variant"),
    "lip_ring": ("jewelry_accessories", "piercing"),
    **dict.fromkeys(("scarf_over_mouth", "bandana_over_mouth"), ("head_accessories", "face_mask")),
    "hair_over_mouth": ("hair", "bangs"),
    "beard_over_mouth": ("face", "facial_hair"),
    "cleft_chin": ("face", "face_shape"),
    "foaming_at_the_mouth": ("body_detail", "body_function"),
    **dict.fromkeys(("stomach_mouth", "hand_mouth", "misplaced_mouth", "disembodied_mouth"), ("body", "anatomy_anomaly")),
    "fan_to_mouth": ("action", "daily_action"),
    "mouth_submerged": ("composition", "framing"),

    # Saliva is a bodily function or surface material, not tooth/tongue anatomy.
    **dict.fromkeys(("saliva", "drooling", "mouth_drool", "saliva_pool", "excessive_saliva"), ("body_detail", "body_function")),
    **dict.fromkeys(("saliva_on_breasts", "saliva_on_hand"), ("body_detail", "surface_stain")),
    "saliva_swap": ("adult", "adult_oral"),
    "teeth_print": ("body_detail", "scar_wound"),
    "toothbrush_in_mouth": ("action", "daily_action"),
    "pill_on_tongue": ("action", "holding"),
    "cat's_tongue": ("body_detail", "body_state"),
    **dict.fromkeys(("disembodied_tongue", "extra_tongue", "tongue_scarf"), ("body", "anatomy_anomaly")),

    # Body-part words used by actions, clothing, props or adult predicates.
    **dict.fromkeys(("snake_wrapped_around_body", "tickling_navel", "braiding_another's_hair"), ("action", "interaction")),
    "kinniku_buster": ("action", "combat_action"),
    "thigh_cutting": ("sensitive", "injury_death"),
    "single_elbow_glove": ("accessories", "handwear"),
    "soaking_feet": ("action", "daily_action"),
    **dict.fromkeys(("sweaty_feet", "sweaty_foot", "sweaty_armpits", "smelly_armpits"), ("body_detail", "body_function")),
    "toe_seam": ("clothing_detail", "other_structure"),
    "shaved_body": ("body_detail", "body_hair"),
    "body_tube": ("mech_scifi", "scifi_device"),
    "giant_skeleton": ("creatures", "fantasy_creature"),
    **dict.fromkeys((
        "navel_hair", "thick_navel_hair", "sparse_navel_hair", "nipple_hair", "ass_hair",
        "sparse_ass_hair", "thick_ass_hair", "hand_hair", "foot_hair",
    ), ("body_detail", "body_hair")),
    **dict.fromkeys(("fake_nails", "gem-studded_nails"), ("body", "arms_hands")),
    **dict.fromkeys(("manboobs", "sideboob", "underboob", "backboob", "bouncing_pecs"), ("body", "breast_chest")),
    **dict.fromkeys(("wide_face", "double_chin"), ("face", "face_shape")),
    "breast_slip": ("adult_body", "adult_clothes"),
    "breast_cutouts": ("clothing_detail", "cutout_slit"),
    **dict.fromkeys(("breast_padding", "undersized_breast_cup", "oversized_breast_cup"), ("underwear_swim", "bra_lingerie")),
    "pov_breasts": ("composition", "viewpoint"),
    "heart_on_chest": ("body_detail", "tattoo_mark"),
    **dict.fromkeys(("chest_eye", "box_body"), ("body", "anatomy_anomaly")),
    **dict.fromkeys(("breasts_on_head", "breast_contest", "cleavage_reach", "cheek-to-breast", "ass_press"), ("action", "interaction")),
    "breast_envy": ("expression", "anger"),
    "breast_awe": ("expression", "fear_surprise"),
    **dict.fromkeys(("ass_on_glass", "ass_rest"), ("pose", "body_pose")),
    "rope_around_waist": ("accessories", "bags_belts"),
    **dict.fromkeys(("heavy_breathing", "nose_bubble", "runny_nose", "stutter", "snoring"), ("body_detail", "body_function")),

    # Adult anatomy buckets retain anatomy only; acts, toys and metadata move.
    "glansjob": ("adult", "adult_hand"),
    **dict.fromkeys(("tentacle_on_penis", "penis_in_thighhigh", "pussy_grip", "clitoral_stimulation"), ("adult", "adult_sex")),
    "penis_in_glove": ("adult", "adult_self"),
    "small_penis_humiliation": ("adult_kink", "adult_power"),
    "peeing_on_penis": ("adult_kink", "adult_excretion"),
    "penis_chart": ("meta_info", "meta"),
    "artificial_vagina": ("adult_kink", "adult_toys"),
    "foot_pussy": ("adult_kink", "adult_fetish"),
    "public_indecency": ("adult", "adult_theme"),
    "zenra": ("adult_kink", "adult_fetish"),
    "hand_shadow_covering_breasts_(meme)": ("meta_info", "meme"),
    **dict.fromkeys(("hair_on_penis", "testicle_hair", "anal_hair"), ("adult_body", "pubic_hair")),
    "huge_penis": ("adult_body", "penis"),

    # Makeup actions and transferred lipstick marks.
    "applying_own_makeup": ("action", "daily_action"),
    "applying_another's_makeup": ("action", "interaction"),
    **dict.fromkeys((
        "lipstick_mark_on_face", "lipstick_mark_on_breast", "lipstick_mark_on_neck",
        "lipstick_mark_on_stomach", "lipstick_mark_on_leg", "lipstick_mark_on_ass",
        "lipstick_mark_on_chest", "lipstick_mark_on_shoulder", "lipstick_mark_on_cheek",
        "lipstick_mark_on_arm", "too_many_lipstick_marks",
    ), ("body_detail", "surface_stain")),
    "lipstick_ring": ("adult", "adult_oral"),
    "back_peek": ("clothing_appearance", "open_wear"),
    "exposed_gusset": ("clothing_appearance", "damaged_dirty"),

    # Cross-folder noun collisions found during the full catalog pass.
    "chest_sarashi": ("underwear_swim", "bra_lingerie"),
    "night_clothes": ("clothes_main", "sleepwear"),
    "button_badge": ("accessories", "badges_ornaments"),
    "garter_belt": ("underwear_swim", "bra_lingerie"),
    "formal_clothes": ("outerwear_suits", "formal_suit"),
    "leg_wrap": ("body_detail", "bandage_patch"),
    "two-tone_eyes": ("face", "eye_color"),
    "mismatched_eyes": ("face", "eye_color"),
    **dict.fromkeys(("tusks", "grills"), ("face", "oral_detail")),
    **dict.fromkeys(("paw_pose", "single_paw_pose", "one_paw_pose"), ("pose", "hand_gesture")),
    "hugging_own_tail": ("action", "holding"),
    **dict.fromkeys(("nontraditional_playboy_bunny", "male_playboy_bunny"), ("uniform_costume", "themed_costume")),
    "vaulting_horse": ("recreation", "sports"),
    "paw_stick": ("weapons", "blunt_chain"),
    "skull": ("body", "internal_organs"),
    "armored_trooper": ("mech_scifi", "mecha"),
    "angel_mort": ("franchise_clothes", "franchise_uniform"),
    "fairy_tale_(love_live!)": ("franchise_clothes", "idol_outfit"),
    "fairy_sword_arondight": ("weapons", "magic_weapon"),
    "disguised_pyra_(xenoblade)": ("franchise_clothes", "franchise_outfit"),
    "fairy_kei": ("clothing_appearance", "fashion_style"),
    "siren_(azur_lane)": ("relationships", "group_faction"),
    "enamel_leather_dark_nurse": ("uniform_costume", "themed_costume"),
    "modeling": ("action", "daily_action"),
    "lily_servant": ("themes", "persona_variant"),

    **dict.fromkeys((
        "tootsuki_saryou_ryouri_gakuen_uniform", "st._feles_gakuen_uniform",
        "thors_military_academy_class_vii_uniform", "thors_military_academy_branch_campus_uniform",
        "st._hilde_academy_of_magic_uniform", "ooarai_military_uniform",
    ), ("franchise_clothes", "school_variant")),
    **dict.fromkeys((
        "gem_uniform_(houseki_no_kuni)", "limbus_kindergarten_uniform", "roswaal_mansion_maid_uniform",
        "tracen_training_uniform",
    ), ("franchise_clothes", "franchise_uniform")),
    "tracen_winter_coat": ("franchise_clothes", "franchise_outfit"),

    "explosive": ("weapons", "explosive"),
    "rocket": ("transport_play", "air_vehicle"),
    "bazooka_(gundam)": ("weapons", "explosive"),
    "titans_(gundam)": ("relationships", "group_faction"),
    "innovators_(gundam_00)": ("people", "fantasy_person"),
    "on_mecha": ("pose", "body_pose"),
    "power_suit": ("protective_clothes", "protective_suit"),
    "power_suit_(metroid)": ("franchise_clothes", "franchise_armor"),
    "slave_gear_(tsmg_nao!)": ("adult_kink", "adult_bondage"),
    "game_link_cable": ("digital_media", "game_device"),
    "flight_stick": ("mech_scifi", "machine"),
    "spike_ball": ("weapons", "blunt_chain"),
    "super_mushroom": ("recreation", "games"),
    "pear-shaped_figure": ("body", "build"),
    "stuffed_food": ("food_drink", "staple_food"),
    "lichtenberg_figure": ("light_effect", "other_effect"),
    "toy_sword": ("recreation", "toys"),
    "rondel": ("protective_clothes", "arm_armor"),
    "fliegerhammer": ("weapons", "explosive"),
    "standing_on_sword": ("pose", "stationary_pose"),
    **dict.fromkeys(("hand_on_blade", "hand_to_blade"), ("pose", "arm_pose")),
    "pointing_sword": ("action", "combat_action"),
    "apartment": ("urban_architecture", "residential"),
    **dict.fromkeys(("exit_sign", "restroom_symbol", "men's_toilet_symbol", "women's_toilet_symbol", "emergency_exit"), ("symbols", "general_symbol")),
    "courtyard": ("outdoor_scene", "other_scene"),
    **dict.fromkeys(("hut", "cabin"), ("urban_architecture", "residential")),
    "falling_flower": ("light_effect", "particles"),
    "hand_grip": ("household_objects", "other_object"),
    "shared_food": ("action", "interaction"),
    "reactive_armor": ("mech_scifi", "machine"),

    **dict.fromkeys((
        "pov_crotch", "female_pov", "futanari_pov", "pov_peephole", "viewer_on_leash",
        "pov_stomped", "taker_pov", "pov_dating", "pov_adoring", "character_pov",
        "multiple_pov", "pov_bullying",
    ), ("composition", "viewpoint")),

    # Restore neckline/lapel details and wearable jewelry to their specific
    # user-facing categories instead of miscellaneous structure/gem buckets.
    **dict.fromkeys((
        "lapels", "notched_lapels", "plaid_lapels", "contrast_lapels", "peaked_lapels",
        "shawl_lapels", "v-neck", "crew_neck", "scoop_neck", "cowl_neck",
    ), ("clothing_detail", "collar_detail")),
    "skin_tight": ("clothing_detail", "silhouette_fit"),
    "single_sode": ("protective_clothes", "shoulder_armor"),
    "ribbon-trimmed_clothes": ("clothing_detail", "trim_detail"),
    **dict.fromkeys(("floating_clothes", "folded_clothes"), ("clothing_appearance", "unworn_missing")),
    **dict.fromkeys(("borrowed_clothes", "shared_clothes"), ("themes", "narrative_situation")),
    "clutching_clothes": ("action", "clothing_action"),

    **dict.fromkeys((
        "pendant", "heart_pendant", "cross_pendant", "symphogear_pendant", "prayer_beads",
        "rosary", "string_of_pearls", "lariat_(necklace)", "pendant_collar", "dog_tags",
        "medallion", "amulet", "gold_chain",
    ), ("jewelry_accessories", "necklace_choker")),
    **dict.fromkeys((
        "thighlet", "gold_thighlet", "silver_thighlet", "thigh_beads", "calflet",
        "ankle_bell", "barefoot_sandals_(jewelry)",
    ), ("jewelry_accessories", "bracelet_anklet")),
    **dict.fromkeys(("tie_clip", "cuff_links"), ("accessories", "badges_ornaments")),

    "group_picture": ("composition", "layout"),
    **dict.fromkeys(("gyaru", "kogal", "gyaruo"), ("clothing_appearance", "fashion_style")),
    # This is an object depicting girls' love, not the lily flower.
    "yuri_(object)": ("culture_objects", "books_paper"),
    "batter": ("food_drink", "bakery"),
    "tan_tattoo": ("body_detail", "tattoo_mark"),
    **dict.fromkeys(("hair_over_breasts", "hair_between_breasts", "hair_over_one_breast"), ("hair", "hair_action")),
    "chest_tuft": ("body_detail", "body_hair"),
    "lazy_eye": ("face", "eye_shape"),
    "w": ("pose", "hand_gesture"),
    "hands_in_opposite_sleeves": ("pose", "arm_pose"),
    "collar_tug": ("action", "clothing_action"),
    **dict.fromkeys(("cleaning_eyewear", "looking_for_glasses"), ("action", "daily_action")),

    **dict.fromkeys(("weapon_over_shoulder", "weapon_across_shoulders", "sword_on_back", "gun_on_back"), ("action", "holding")),
    **dict.fromkeys(("swinging_weapon", "cocking_gun"), ("action", "combat_action")),
    "hand_to_weapon": ("pose", "arm_pose"),
    **dict.fromkeys(("weapon_between_legs", "foot_on_weapon"), ("pose", "leg_pose")),
    "cork_gun": ("recreation", "toys"),
    "wand_in_head": ("head_accessories", "themed_hair_ornament"),
    "cat_o'_nine_tails": ("weapons", "blunt_chain"),
    **dict.fromkeys(("funnels_(gundam)", "bit_(gundam)", "fin_funnels"), ("weapons", "other_weapon")),

    "stuffing": ("recreation", "toys"),
    "boy_and_girl_sandwich": ("action", "interaction"),
    **dict.fromkeys(("flipping_food", "blowing_on_food", "throwing_food"), ("action", "daily_action")),
    "snow_strawberry_(idolmaster)": ("franchise_clothes", "idol_outfit"),
    "tomato_(sword)": ("weapons", "blade"),
    "invisible_chair": ("pose", "stationary_pose"),
    **dict.fromkeys(("human_chair", "yukadon", "bed_invitation", "lap_pillow", "breast_pillow", "arm_pillow"), ("action", "interaction")),
    "pushing_wheelchair": ("action", "movement"),
    "knights_of_the_round_table_(fate)": ("relationships", "group_faction"),
    "keyhole": ("building_parts", "door_window"),
    "object_namesake": ("meta_info", "meme"),
    "object_through_head": ("sensitive", "injury_death"),

    "tailcoat_playboy_bunny": ("uniform_costume", "themed_costume"),
    "downward_dog": ("pose", "body_pose"),
    "apple_rabbit": ("food_drink", "fruit_vegetable"),
    **dict.fromkeys(("large_teddy_bear", "toy_mouse", "inflatable_whale", "inflatable_dolphin"), ("recreation", "toys")),
    **dict.fromkeys(("riding_animal", "riding_bird", "riding_dragon", "snow_angel"), ("action", "movement")),
    "sitting_on_animal": ("pose", "body_pose"),
    **dict.fromkeys(("hanging_sign", "open_sign"), ("indoor_scene", "commercial")),
    "barn": ("urban_architecture", "public_building"),
})


# v15 exhaustive tag-by-tag audit, pass 1. Every entry below was checked
# against its English name, bundled Chinese alias and wiki summary.
EXACT_OVERRIDES.update({
    "bras_d'honneur": ("pose", "hand_gesture"),
    "headband_around_neck": ("accessories", "neckwear"),
    "blanket_veil": ("head_accessories", "headwrap_veil"),
    **dict.fromkeys(("snowflake_pendant", "acorn_pendant", "gold_pendant", "pendant_watch"), ("jewelry_accessories", "necklace_choker")),
    **dict.fromkeys(("heart-shift_bracelets", "multiple_anklets"), ("jewelry_accessories", "bracelet_anklet")),
    "onion_rings": ("food_drink", "dessert_snack"),
    "olympic_rings": ("symbols", "emblem"),
    "multi-lane_road": ("urban_architecture", "urban"),
    "ryouran!_victory_road_(love_live!)": ("franchise_clothes", "idol_outfit"),
    "too_many_weapons": ("weapons", "other_weapon"),
    "bomb_item_(touhou)": ("recreation", "games"),
    "mouse_on_head": ("action", "interaction"),
    "smother": ("sensitive", "restraint"),
    "hookah": ("household_objects", "other_object"),
    "mummification_(bound)": ("sensitive", "restraint"),
    "yakisobapan": ("food_drink", "bakery"),
    "altar": ("indoor_scene", "public_indoor"),
    "karaginu_mo": ("traditional_clothes", "traditional_japan"),
    "lotus_root": ("food_drink", "fruit_vegetable"),
    "pecjob": ("adult", "adult_sex"),
    "watermelon_seeds": ("food_drink", "fruit_vegetable"),
    "wrists_extended": ("pose", "arm_pose"),
    "camel": ("creatures", "mammal"),
    "hope's_dusk_(apex_legends)": ("weapons", "blade"),
    "judge": ("people", "occupation"),
    "parakeet": ("creatures", "bird"),
    "stepping_stones": ("outdoor_scene", "terrain_surface"),
    "tsuzumi": ("culture_objects", "music"),
    "urethral_beads": ("adult_kink", "adult_toys"),
    "yukari_is_merry_theory_(touhou)": ("meta_info", "meme"),
    "corner": ("building_parts", "surface"),
    "creeparka": ("franchise_clothes", "franchise_outfit"),
    "evolution_stone": ("recreation", "games"),
    "osugaki": ("people", "age"),
    "queue": ("action", "daily_action"),
    "uraeus": ("head_accessories", "headpiece"),
    "itasha": ("transport_play", "land_vehicle"),
    "politics": ("themes", "narrative_situation"),
    "serving_dome": ("food_drink", "tableware"),
    "statue_of_liberty": ("urban_architecture", "tower_landmark"),
    "tsukumogami": ("creatures", "fantasy_creature"),
    "taller_than_canon": ("themes", "persona_variant"),
    "vortex": ("light_effect", "optical"),
    "yari": ("weapons", "polearm"),
    "doghouse": ("urban_architecture", "residential"),
    "earth_eleven": ("relationships", "group_faction"),
    "harlequin": ("people", "occupation"),
    "saishi": ("head_accessories", "headpiece"),
    "water_world": ("outdoor_scene", "water_scene"),
    **dict.fromkeys(("awakening_(sennen_sensou_aigis)", "bad_end_precure"), ("themes", "persona_variant")),
    "jiaoling_ruqun": ("traditional_clothes", "traditional_china"),
    "security_shutter": ("building_parts", "door_window"),
    "1up": ("recreation", "games"),
    "arena": ("urban_architecture", "public_building"),
    "bola_(weapon)": ("weapons", "other_weapon"),
    "hishimochi": ("food_drink", "dessert_snack"),
    "hole_in_head": ("body", "anatomy_anomaly"),
    "tokarev_tt-33": ("weapons", "firearm"),
    "yogurt": ("food_drink", "dairy_ingredient"),
    "dodecagram": ("symbols", "shape_math"),
    "waltz_(dance)": ("action", "movement"),
    "barre": ("recreation", "sports"),
    "tam_(ragnarok_online)": ("head_accessories", "hats_caps"),
    "gasp": ("expression", "fear_surprise"),
    "heartsteel_(league_of_legends)": ("relationships", "group_faction"),
    "mango": ("food_drink", "fruit_vegetable"),
    "seabird": ("creatures", "bird"),
    "slip_showing": ("clothing_appearance", "open_wear"),
    "automail": ("mech_scifi", "cybernetic"),
    "blank_page": ("text_meta", "text"),
    "nissan_skyline_gt-r": ("transport_play", "land_vehicle"),
    "bard": ("people", "occupation"),
    "fanta": ("food_drink", "drink"),
    "german_shepherd": ("creatures", "mammal"),
    "jackal_girl": ("people", "fantasy_person"),
    "poi_(goldfish_scoop)": ("recreation", "games"),
    "taishou": ("time_weather", "calendar"),
    "towel_rack": ("household_objects", "storage_furniture"),
    "blender_(object)": ("household_objects", "appliance"),
    "calamity_queller_(genshin_impact)": ("weapons", "polearm"),
    "cockatiel": ("creatures", "bird"),
    "e-liter_4k_(splatoon)": ("weapons", "firearm"),
    "meowing": ("action", "daily_action"),
    "stepping_on_non-human": ("action", "interaction"),
    "2024_pokemon_teraleak": ("meta_info", "meta"),
    "ashiyu": ("indoor_scene", "public_indoor"),
    "drawing_on_another": ("action", "interaction"),
    "harmonica": ("culture_objects", "music"),
    "holojustice": ("relationships", "group_faction"),
    "junk": ("household_objects", "other_object"),
    "mandrake": ("nature", "unusual_plant"),
    "anpan": ("food_drink", "bakery"),
    "lolibaba": ("people", "age"),
    "2011_tohoku_earthquake_and_tsunami": ("themes", "narrative_situation"),
    "chireiden": ("urban_architecture", "public_building"),
    "counters_(nikke)": ("relationships", "group_faction"),
    "edamame": ("food_drink", "fruit_vegetable"),
    "electric_kettle": ("household_objects", "appliance"),
    "fusion_dance": ("action", "movement"),
    "kokeshi": ("recreation", "toys"),
    "palm-fist_greeting": ("pose", "hand_gesture"),
    "partially_immersed": ("pose", "body_pose"),
    "black_fundoshi": ("traditional_clothes", "traditional_japan"),
    "chonmage": ("hair", "hair_style"),
    "convention": ("indoor_scene", "public_indoor"),
    "receipt": ("culture_objects", "books_paper"),
    "ak-74m": ("weapons", "firearm"),
    "bedroll": ("household_objects", "other_object"),
    "car_crash": ("sensitive", "injury_death"),
    "dartboard": ("recreation", "games"),
    "sandbag": ("recreation", "sports"),
    "snowboarding": ("action", "movement"),
    "ice_shard": ("light_effect", "particles"),
    "phasmophobia": ("expression", "fear_surprise"),
    "against_rock": ("pose", "body_pose"),
    "floorplan": ("composition", "layout"),
    "go-kart": ("transport_play", "land_vehicle"),
    "karakusa_(pattern)": ("background", "background_pattern"),
    "label": ("clothing_detail", "other_structure"),
    "plastic_wrap": ("household_objects", "container"),
    "podium": ("household_objects", "other_object"),
    "small_head": ("face", "face_shape"),
    "titan_(titanfall)": ("mech_scifi", "mecha"),
    "face_in_crotch": ("adult", "adult_sex"),
    "gibson_brands_inc": ("text_meta", "brand"),
    "nissan_silvia": ("transport_play", "land_vehicle"),
    "sai_(weapon)": ("weapons", "blade"),
    "rebreather": ("protective_clothes", "civilian_helmet"),
    "wrist_blades": ("weapons", "blade"),
})

# v15 exhaustive tag-by-tag audit, pass 2: high-frequency fallback terms.
EXACT_OVERRIDES.update({
    "science": ("themes", "narrative_situation"),
    "chemistry": ("themes", "narrative_situation"),
    "crushed": ("sensitive", "injury_death"),
    "bird_nest": ("creatures", "bird"),
    "catfish": ("creatures", "aquatic"),
    "mosquito": ("creatures", "insect"),
    "buddhism": ("themes", "narrative_situation"),
    "christianity": ("themes", "narrative_situation"),
    "unwanted_creampie": ("sensitive", "sexual_violence"),
    "wireless": ("digital_media", "computer_device"),
    "trailer": ("text_meta", "screen_ui"),
    "thompson/center_contender": ("weapons", "firearm"),
    "disheveled": ("hair", "hair_action"),
    "dynamo_roller_(splatoon)": ("weapons", "other_weapon"),
    ";|": ("expression", "neutral_expression"),
    "mixed_maids": ("people", "occupation"),
    "triple_ryuunen": ("meta_info", "meme"),
    "sprout_on_head": ("head_accessories", "themed_hair_ornament"),
    **dict.fromkeys(("game_boy_advance_(original)", "xbox_360", "game_boy_color", "sega_dreamcast", "playstation_1", "dualsense"), ("digital_media", "game_device")),
    "hopping": ("action", "movement"),
    **dict.fromkeys(("winchester_model_1887", "smith_&_wesson_m&p", "n-zap_(splatoon)", "m1_garand", "fn_five-seven", "qbz-95", "iwi_tavor"), ("weapons", "firearm")),
    "yellow_happi": ("traditional_clothes", "traditional_japan"),
    "apron_tug": ("action", "clothing_action"),
    "baluster": ("building_parts", "stairs_railing"),
    "fatherly": ("themes", "narrative_situation"),
    "kanchou": ("adult", "adult_hand"),
    "webcam": ("digital_media", "camera_video"),
    "arabesque_(pose)": ("pose", "leg_pose"),
    "cloaca": ("adult_body", "genital_variation"),
    "dryad": ("people", "fantasy_person"),
    "eldar": ("people", "fantasy_person"),
    "radar_dish": ("mech_scifi", "scifi_device"),
    "shadaloo_dolls": ("relationships", "group_faction"),
    "spring_rider": ("recreation", "toys"),
    "white_bustier": ("underwear_swim", "bra_lingerie"),
    "zippo_lighter": ("household_objects", "other_object"),
    "katsuyamamage": ("hair", "hair_style"),
    "kawaii_boku_to_142's_(idolmaster)": ("relationships", "group_faction"),
    "linea_nigra": ("body_detail", "skin"),
    "politician": ("people", "occupation"),
    "pterosaur": ("creatures", "reptile"),
    "swirling": ("light_effect", "optical"),
    "wavy_ends": ("hair", "hair_style"),
    "around_corner": ("pose", "body_pose"),
    "dustpan": ("household_objects", "care_cleaning"),
    "ember_celica_(rwby)": ("weapons", "firearm"),
    "white_negligee": ("underwear_swim", "bra_lingerie"),
    "bitchsuit": ("adult_body", "adult_clothes"),
    "folded_stock": ("weapons", "firearm"),
    "penguin_logistics_(arknights)": ("relationships", "group_faction"),
    "plain": ("outdoor_scene", "forest_field"),
    "stormtrooper": ("people", "role_focus"),
    "tera_orb": ("recreation", "games"),
    "haki_(one_piece)": ("light_effect", "glow_aura"),
    "honeypot": ("household_objects", "container"),
    "male_spitroast": ("adult", "adult_sex"),
    "roulette": ("recreation", "games"),
    "visual_kei": ("clothing_appearance", "fashion_style"),
    "ascii_art": ("text_meta", "text"),
    "babylonia_(fate/grand_order)": ("themes", "narrative_situation"),
    "in_snow_globe": ("composition", "framing"),
    "macintosh": ("digital_media", "computer_device"),
    "moai": ("urban_architecture", "tower_landmark"),
    "walkure_(macross_delta)": ("relationships", "group_faction"),
    "affinity_sunglasses_(blue_archive)": ("head_accessories", "eyewear"),
    "alarm_siren": ("household_objects", "other_object"),
    "nightshirt": ("clothes_main", "sleepwear"),
    "otoshidama": ("household_objects", "other_object"),
    "volumen_hydragyrum_(fate)": ("weapons", "magic_weapon"),
    "anti-rain_(girls'_frontline)": ("relationships", "group_faction"),
    "cinderella_bust": ("underwear_swim", "bra_lingerie"),
    "mandragora": ("nature", "unusual_plant"),
    "royal_navy": ("relationships", "group_faction"),
    "tri_rod": ("weapons", "magic_weapon"),
    "amarr_empire_(eve_online)": ("relationships", "group_faction"),
    "held_up": ("action", "holding"),
    "hufflepuff": ("relationships", "group_faction"),
    "product_girl": ("people", "role_focus"),
    "tryzub": ("symbols", "emblem"),
    "broken_condom": ("adult_kink", "adult_toys"),
    "cinnamon_stick": ("food_drink", "seasoning"),
    "fingerprint": ("body_detail", "tattoo_mark"),
    "h&k_mp5k": ("weapons", "firearm"),
    "hacksaw": ("household_objects", "tools"),
    "reverse_prayer": ("pose", "hand_gesture"),
    "silver_circlet": ("head_accessories", "headpiece"),
    "stielhandgranate": ("weapons", "explosive"),
    "bulges_touching": ("adult", "adult_suggestive"),
    "euphemism": ("text_meta", "text"),
    "holoforce": ("relationships", "group_faction"),
    "narehate": ("creatures", "fantasy_creature"),
    "oppai_challenge": ("adult", "adult_suggestive"),
    "pantograph": ("transport_play", "land_vehicle"),
    "sotoba": ("symbols", "religious_symbol"),
    "telnyashka": ("uniform_costume", "military_uniform"),
    "capsule_corp": ("text_meta", "brand"),
    "claw_mark": ("body_detail", "scar_wound"),
    "electrostimulation": ("adult_kink", "adult_toys"),
    "marriage_certificate_(object)": ("culture_objects", "books_paper"),
    "padlocked_chastity_cage": ("adult_kink", "adult_toys"),
    "poem": ("text_meta", "text"),
    "pokemon_center": ("urban_architecture", "public_building"),
    "purikura": ("digital_media", "camera_video"),
    "runway": ("outdoor_scene", "terrain_surface"),
    "skunk_girl": ("people", "fantasy_person"),
    "cruiser": ("transport_play", "water_vehicle"),
    "fetus": ("adult_body", "reproductive"),
    "racism": ("themes", "narrative_situation"),
    "shiroshouzoku": ("traditional_clothes", "traditional_japan"),
    "slit_throat": ("sensitive", "injury_death"),
    "cat_paw": ("animal_traits", "claw_scale"),
    "chamomile": ("nature", "flower_species"),
    "marlboro": ("text_meta", "brand"),
    "mg_mg": ("text_meta", "comic"),
    "sharing": ("action", "interaction"),
    "bonk": ("action", "interaction"),
    "cantaloupe": ("food_drink", "fruit_vegetable"),
    "mamianqun": ("traditional_clothes", "traditional_china"),
    "^q^": ("expression", "neutral_expression"),
    "agejo_gyaru": ("clothing_appearance", "fashion_style"),
    "command_input": ("text_meta", "screen_ui"),
    "hell": ("outdoor_scene", "other_scene"),
    "human_village_(touhou)": ("urban_architecture", "urban"),
    "scallop": ("creatures", "aquatic"),
    "sternum": ("body", "torso_back"),
    "alternate_element": ("themes", "persona_variant"),
    "gon-san": ("themes", "persona_variant"),
    "ohitsu": ("household_objects", "container"),
    "toyota_sprinter_trueno": ("transport_play", "land_vehicle"),
    "armpit_stubble": ("body_detail", "body_hair"),
    "american_football": ("recreation", "sports"),
    "gallente_federation_(eve_online)": ("relationships", "group_faction"),
    "himekaji": ("clothing_appearance", "fashion_style"),
    "hostess": ("people", "occupation"),
    "mora_(genshin_impact)": ("recreation", "games"),
    "obsidian_slasher": ("weapons", "blade"),
    "sapling": ("nature", "tree"),
    "scoreboard": ("recreation", "sports"),
    "watermelon_beachball": ("recreation", "sports"),
    "fiat": ("transport_play", "land_vehicle"),
    "honda_super_cub": ("transport_play", "land_vehicle"),
    "jaw": ("face", "face_shape"),
    "title_page": ("culture_objects", "books_paper"),
    "cereal": ("food_drink", "staple_food"),
    "gerwalk": ("mech_scifi", "mecha"),
    "penguins_performance_project_(kemono_friends)": ("relationships", "group_faction"),
    "price_list": ("text_meta", "text"),
    "surgeonfish": ("creatures", "aquatic"),
    "chinese_wedding": ("themes", "narrative_situation"),
    "lamia_boy": ("people", "fantasy_person"),
    "manhole": ("urban_architecture", "urban"),
    "sprain": ("body_detail", "scar_wound"),
    "calculator": ("digital_media", "computer_device"),
    "x-ray_film": ("culture_objects", "books_paper"),
    "akihabara_(tokyo)": ("urban_architecture", "urban"),
    "chinese_peony": ("nature", "flower_species"),
    "cocoon": ("creatures", "insect"),
    "bear_position": ("pose", "body_pose"),
    "bladder": ("body", "internal_organs"),
    "panther_boy": ("people", "fantasy_person"),
    "red-crowned_crane": ("creatures", "bird"),
    "roasting": ("action", "daily_action"),
    "splat_dualies_(splatoon)": ("weapons", "firearm"),
    "veiny_neck": ("body_detail", "body_state"),
    "zebra": ("creatures", "mammal"),
    "cubicle": ("indoor_scene", "public_indoor"),
    "genius_invokation_tcg": ("recreation", "games"),
    "laundry_pole": ("household_objects", "tools"),
    "serval": ("creatures", "mammal"),
    "yuzu_bath": ("indoor_scene", "public_indoor"),
    "bagel": ("food_drink", "bakery"),
    "smoothie": ("food_drink", "drink"),
    "tadpole": ("creatures", "aquatic"),
    "balancing_on_head": ("pose", "body_pose"),
    "carabiner": ("household_objects", "rope_lock"),
    "howling": ("action", "daily_action"),
    "pushing_face": ("action", "interaction"),
    "red_carnation": ("nature", "flower_species"),
    "construction": ("urban_architecture", "public_building"),
    "drawing_on_self": ("action", "daily_action"),
    "making_faces": ("expression", "neutral_expression"),
    "printer": ("digital_media", "computer_device"),
    "black_negligee": ("underwear_swim", "bra_lingerie"),
    "jammers": ("underwear_swim", "male_swim"),
    "luchador": ("people", "occupation"),
    "pip_boy": ("mech_scifi", "scifi_device"),
    "rabbit_earmuffs": ("head_accessories", "headpiece"),
    "single_loose_sock": ("clothing_appearance", "unworn_missing"),
    "tnt_block_(minecraft)": ("weapons", "explosive"),
    "chain_around_neck": ("accessories", "neckwear"),
    "geisha": ("people", "occupation"),
    "mori_kei": ("clothing_appearance", "fashion_style"),
    "oarfish": ("creatures", "aquatic"),
    "patriotism": ("themes", "narrative_situation"),
    "ski_pole": ("recreation", "sports"),
    "supreme_(brand)": ("text_meta", "brand"),
    "countdown_timer": ("text_meta", "screen_ui"),
})

# v15 exhaustive tag-by-tag audit, pass 3: residual strong-head conflicts.
EXACT_OVERRIDES.update({
    "pug": ("creatures", "mammal"),
    "cat_loaf": ("pose", "stationary_pose"),
    **dict.fromkeys(("cat_on_person", "dog_on_head", "cats_love_being_spanked"), ("action", "interaction")),
    "camel_girl": ("people", "fantasy_person"),
    "fish_head": ("food_drink", "meat_seafood"),
    "fish_grill": ("household_objects", "appliance"),
    "insect_pin": ("household_objects", "tools"),
    "chain_blades": ("weapons", "blade"),
})

def parts(name: str) -> set[str]:
    return {token for token in re.split(r"[_()\-/' ]+", name.lower()) if token}


def any_fragment(name: str, values) -> bool:
    return any(value in name for value in values)


def any_suffix(name: str, values) -> bool:
    return any(name.endswith(value) for value in values)


def any_prefix(name: str, values) -> bool:
    return any(name.startswith(value) for value in values)


def initial_category(name: str) -> str:
    first = name[:1].upper()
    return f"letter_{first.lower()}" if first in string.ascii_uppercase else "letter_other"


def other_category(name: str) -> str:
    first = name[:1].lower()
    if "a" <= first <= "e": return "other_a_e"
    if "f" <= first <= "j": return "other_f_j"
    if "k" <= first <= "o": return "other_k_o"
    if "p" <= first <= "t": return "other_p_t"
    if "u" <= first <= "z": return "other_u_z"
    return "other_symbol"


# The bundled database supplies a curated Chinese display name for every row.
# It is used only as a conservative last pass after all English rules, never as
# a replacement for the auditable source-category and tag-name rules above.
CN_FALLBACK_RULES = [
    # Explicit content and censorship.
    (r"性交|性行为|口交|肛交|乳交|足交|手交|群交|乱交|兽交|强奸", ("adult", "adult_sex")),
    (r"自慰|手淫|指交", ("adult", "adult_self")),
    (r"射精|精液|爱液|乳汁分泌|颜射|潮吹", ("adult", "adult_fluid")),
    (r"阴茎|龟头|阴囊|睾丸|外阴|阴道|阴蒂|阴唇|子宫|肛门|会阴|包皮", ("adult", "adult_anatomy")),
    (r"性玩具|假阳具|跳蛋|振动棒|束缚|捆绑|调教|恋物癖|露出癖|口塞|口嚼", ("adult", "adult_fetish")),
    (r"^(色情|成人内容|公共场合猥亵|裸体|全裸|露点)$|色情内容", ("adult", "adult_other")),
    (r"肢解|斩首|断肢|内脏|尸体|血腥", ("adult", "adult_gore")),
    (r"打码|马赛克|审查|遮盖|遮挡|无修正|内容分级", ("text_meta", "censorship")),

    # Text, symbols, publishing and screen grammar.
    (r"文字|文本|字幕|标题|页码|标语|语言|字体|书写|台词", ("text_meta", "text")),
    (r"符号|标志|徽标|问号|感叹号|音符|五角星|三角形|菱形|十字|二维码", ("text_meta", "symbol")),
    (r"漫画格|分镜|对话框|气泡|拟声|效果音", ("text_meta", "comic")),
    (r"截图|界面|光标|屏幕|游戏画面|录制中", ("text_meta", "screen_ui")),
    (r"迷因|网络梗|玩梗|恶搞|戏仿|双关", ("text_meta", "meme")),
    (r"封面|水印|签名|用户名|公司名称|创作错误|作画错误", ("text_meta", "meta")),

    # Relations, character variants and narrative situations.
    (r"性别转换|性转|拟人化|人类化|动物化|女仆化|身份互换", ("themes", "identity_change")),
    (r"人格|克隆|角色变体|黑暗版本|堕落", ("themes", "persona_variant")),
    (r"^(兄妹|姐弟|姐妹|兄弟|夫妻|母女|父女|母子|父子|亲子|家庭关系)$", ("themes", "family_relation")),
    (r"异性|百合|耽美|蔷薇|跨种族|异种|配对", ("themes", "romance_orientation")),
    (r"声优梗|名字梗|特征关联|公司关联", ("themes", "character_connection")),
    (r"日常生活|战斗场景|战败|^死亡$|^濒死|暗示死亡|时间悖论|进化链", ("themes", "narrative_situation")),

    # Facial expression and pose/action.
    (r"微笑|笑脸|坏笑|大笑|开心|快乐", ("expression", "positive")),
    (r"哭|含泪|泪滴|悲伤|落泪", ("expression", "sad_cry")),
    (r"怒视|愤怒|生气|不满|撇嘴|皱眉", ("expression", "anger")),
    (r"惊讶|震惊|害怕|恐惧|慌张|困惑", ("expression", "fear_surprise")),
    (r"脸红|害羞|尴尬", ("expression", "shy_blush")),
    (r"表情|颜文字|无语|豆豆眼|歪嘴|闭眼", ("expression", "neutral_expression")),
    (r"斜视|凝视|看向|回头|转头|视线", ("pose", "gaze")),
    (r"站立|坐姿|跪姿|躺|斜倚|正坐|侧身坐", ("pose", "stationary_pose")),
    (r"姿势|跨坐|劈叉|踮脚|倒立|悬空|交叉双腿|踝部交叉", ("pose", "body_pose")),
    (r"手势|剪刀手|摇滚手势|竖中指|指向|敬礼|嘘", ("pose", "hand_gesture")),
    (r"手持|拿着|举起|抓住|握持|拔剑|入鞘", ("action", "holding")),
    (r"行走|奔跑|跳跃|飞行|漂浮|游泳|舞蹈|摇尾巴", ("action", "movement")),
    (r"开火|射击|攻击|战斗动作|挥剑|格挡", ("action", "combat_action")),
    (r"接吻|亲吻|拥抱|摸头|喂食|^戳(?:人|脸|身体)?$|肩上的动物|头上的动物", ("action", "interaction")),
    (r"说话|喊叫|拍照|玩游戏|睡醒|倒水|抽烟|阅读|写作", ("action", "daily_action")),

    # Hair, face and body.
    (r"发色$|头发颜色|挑染|发梢染色|多色头发", ("hair", "hair_color")),
    (r"长发|短发|中长发", ("hair", "hair_length")),
    (r"马尾|双马尾|辫子|发髻|卷发|波波头|寸头|秃头|呆毛|飞机头|发型", ("hair", "hair_style")),
    (r"刘海|鬓发|鬓角|发际", ("hair", "bangs")),
    (r"发饰|发带|发夹|发簪|发髻罩", ("accessories", "hair_accessory")),
    (r"瞳孔|虹膜|巩膜|异色瞳|第三只眼|独眼|眼球|睫毛|眼型", ("face", "eye_shape")),
    (r"眉毛", ("face", "eyebrows")),
    (r"鼻子|鼻孔", ("face", "nose")),
    (r"卧蚕", ("face", "eye_shape")),
    (r"嘴|嘴唇|舌头|牙齿|尖牙|口鼻部", ("face", "mouth")),
    (r"胡须|胡子|山羊胡|胡茬", ("face", "facial_hair")),
    (r"妆容|眼影|眼线|口红|面部彩绘", ("face", "makeup")),
    (r"胸肌|乳房|胸部|乳沟|露脐|腹部|背部|肩胛|锁骨", ("body", "chest")),
    (r"腰部|臀部|大腿|小腿|膝盖|脚掌|腹股沟|鼠蹊", ("body", "waist_legs")),
    (r"手臂|手掌|手指|指甲|脚趾|腋下|腋窝", ("body", "arms_hands_feet")),
    (r"体型|身材|肌肉|肥胖|苗条|高个|矮小|巨人", ("body", "build")),
    (r"肤色|皮肤颜色|晒黑", ("body", "skin")),
    (r"纹身|伤疤|痣|咬痕|身体标记|病灶|缝合线", ("body", "body_marks")),
    (r"受伤|流血|鼻血|义肢|湿身|肮脏|抽搐|身体变化", ("body", "body_state")),

    # Clothing and wearable items.
    (r"衬衫|上衣|毛衣|背心|吊带衫|高领衫|束腰外衣|马甲", ("clothes_main", "tops")),
    (r"短裤|长裤|牛仔裤|灯笼裤", ("clothes_main", "bottoms")),
    (r"半身裙|短裙|超短裙|裙甲", ("clothes_main", "skirt")),
    (r"连衣裙|礼服|长裙", ("clothes_main", "dress")),
    (r"外套|披风|披肩|斗篷|夹克|罩衫|燕尾服|雨衣", ("clothes_main", "outerwear")),
    (r"校服|水手服|学兰|体操服", ("clothes_special", "school_uniform")),
    (r"制服|女仆装|护士服|警服|军服|道服|赛车女郎", ("clothes_special", "occupation_uniform")),
    (r"和服|浴衣|汉服|韩服|旗袍|袴|狩衣|振袖", ("clothes_special", "traditional_east")),
    (r"睡衣|家居服|纱笼|民族服饰", ("clothes_special", "sleep_casual")),
    (r"胸罩|内衣|乳贴|娃娃装睡衣", ("underwear_swim", "bra_lingerie")),
    (r"内裤|兜裆布|裈|粘贴式内裤", ("underwear_swim", "panties_underwear")),
    (r"泳装|泳衣|比基尼", ("underwear_swim", "swimsuit")),
    (r"紧身衣|连体衣|全身袜", ("underwear_swim", "bodysuit_leotard")),
    (r"过膝袜|长筒袜|丝袜|裤袜|网袜|腿袜", ("legwear_footwear", "stockings")),
    (r"袜子|短袜|足袋|单只袜", ("legwear_footwear", "socks")),
    (r"靴子|长靴|短靴", ("legwear_footwear", "boots")),
    (r"鞋|凉鞋|木屐|高跟鞋|人字拖", ("legwear_footwear", "shoes")),
    (r"盔甲|护甲|护腕|护腿|肩甲|胸甲", ("legwear_footwear", "armor")),
    (r"头盔|防护服", ("legwear_footwear", "helmet_protective")),
    (r"领口|袖口|无肩带|肩带|双排扣|拉绳|纽扣|拉链|开衩|开口", ("clothing_detail", "clothing_structure")),
    (r"面料|布料|蕾丝|皮革|乳胶|针织|透明材质", ("clothing_detail", "clothing_material")),
    (r"破损衣物|衣衫不整|解开扣子|拉链拉开|脱衣|穿衣", ("clothing_detail", "clothing_state")),
    (r"帽|头巾|头饰|头冠|圆箍|面纱|兜帽", ("accessories", "headwear")),
    (r"(?!眼镜蛇)眼镜|护目镜|眼罩|面具|面罩", ("accessories", "eyewear")),
    (r"项链|耳环|耳夹|手镯|戒指|珠宝|宝石|首饰", ("accessories", "jewelry")),
    (r"领巾|领带|围巾|颈圈|阿斯科特", ("accessories", "neckwear")),
    (r"手套|腕带|袖扣|臂章", ("accessories", "handwear")),
    (r"手提包|背包|书包|腰带|皮带|背带", ("accessories", "bags_belts")),

    # Things, creatures, places and rendering.
    (r"匕首|刀鞘|剑鞘|(?:刀|剑)$", ("weapons", "blade")),
    (r"手枪|步枪|火器|枪械|左轮", ("weapons", "firearm")),
    (r"弓箭|弩|箭袋", ("weapons", "bow")),
    (r"长矛|镰刀|锤|长柄武器", ("weapons", "polearm")),
    (r"蛋糕|饼干|糖果|巧克力|冰淇淋|甜点|零食|马卡龙|棒冰", ("food_drink", "dessert_snack")),
    (r"水果|蔬菜|南瓜|大葱", ("food_drink", "fruit_vegetable")),
    (r"饭团|团子|汉堡|料理|主食", ("food_drink", "staple_food")),
    (r"^(?:饮料|清酒|咖啡|茶|奶茶|红茶|绿茶|果汁|啤酒|葡萄酒|鸡尾酒)$|饮品$", ("food_drink", "drink")),
    (r"茶壶|茶托|茶杯|酒杯|茶匙|餐具|盘子|碗|勺|筷子|杯子", ("food_drink", "tableware")),
    (r"手机|电脑|键盘|游戏机|任天堂Switch", ("culture_objects", "phone_computer")),
    (r"相机|耳机|麦克风|电视|录音", ("culture_objects", "camera_media")),
    (r"书|杂志|信封|纸张|写字板", ("culture_objects", "books_paper")),
    (r"乐器|吉他|钢琴|小提琴|哨子", ("culture_objects", "music")),
    (r"椅|桌子|床|沙发|王座|被炉|靠垫|布团", ("household_objects", "seating_table")),
    (r"书架|储物柜|柜子|镜子|窗帘", ("household_objects", "storage_furniture")),
    (r"灯柱|灯具|蜡烛|时钟|家电", ("household_objects", "lighting_clock")),
    (r"绳子|链条|胶带|雨伞|阳伞|手杖|针筒|工具", ("household_objects", "tools")),
    (r"花瓶|袋子|容器|盒子|罐子", ("household_objects", "container")),
    (r"汽车|火车|自行车|摩托车|陆地载具", ("transport_play", "land_vehicle")),
    (r"飞机|直升机|飞行器|宇宙飞船|航天器", ("transport_play", "air_vehicle")),
    (r"^(船|锚)$|船舶|帆船|轮船|游艇|水上交通工具|潜艇", ("transport_play", "water_vehicle")),
    (r"运动器材|游泳圈|滑板|球拍", ("transport_play", "sports")),
    (r"玩具|玩偶|毛绒|人偶", ("transport_play", "toys")),
    (r"兽耳|尾巴|翅膀|羽毛|鹿角|兽角|独角|双角|触角|鳞片|爪子|肉垫|鸟喙", ("creatures", "animal_feature")),
    (r"^(猫|狗|狼|狐狸|兔子|熊|老虎|狮子|浣熊)$|猫娘|狗娘|狼娘|狐娘|兔娘|熊娘|虎娘|豹娘", ("creatures", "mammal")),
    (r"^(鸟|小鸡|鹰|乌鸦|企鹅|鸽子)$|鸟类", ("creatures", "bird")),
    (r"^(鱼|鲨鱼|鲸|海豚|章鱼|海星)$|水生生物", ("creatures", "aquatic")),
    (r"^(昆虫|蜘蛛|蝴蝶|蜜蜂)$|节肢动物", ("creatures", "insect")),
    (r"^(妖怪|幽灵|怪物|僵尸|人鱼|九尾|猫又)$|幻想生物", ("creatures", "fantasy_creature")),
    (r"^(花|树枝|树木|灌木|藤蔓|三叶草|植物|苔藓)$|花卉|植物叶片", ("creatures", "plant")),
    (r"机器人|仿生人", ("mech_scifi", "robot_android")),
    (r"机甲|高达|大型机械", ("mech_scifi", "mecha")),
    (r"机械臂|机械腿|义体|赛博改造", ("mech_scifi", "cybernetic")),
    (r"电缆|机器|机械零件", ("mech_scifi", "machine")),
    (r"卧室|浴室|客厅|厨房|浴缸|马桶", ("indoor_scene", "home_room")),
    (r"学校|教室|办公室|医院|实验室", ("indoor_scene", "public_indoor")),
    (r"道路|街道|城市|车站|灯柱", ("indoor_scene", "urban")),
    (r"^(?:门|柱子|栏杆|栅栏|鸟居|建筑)$|(?:大门|木门|玻璃门|门廊|门框|门扉|舱门|柱子|栏杆|栅栏|鸟居|建筑物)$", ("indoor_scene", "architecture")),
    (r"^(森林|田野|草地|公园)$|森林场景|田野场景", ("outdoor_scene", "forest_field")),
    (r"^(山|沙漠|沙子|悬崖|洞穴)$|山地|沙漠场景", ("outdoor_scene", "mountain_desert")),
    (r"^(海|海洋|河|河流|湖|湖泊|水池|水洼|温泉|波浪)$|海边|河岸|湖边|水域", ("outdoor_scene", "water_scene")),
    (r"^(天空|云|宇宙|月亮|星空)$|天空背景|宇宙空间", ("outdoor_scene", "sky_space")),
    (r"风景|景观|地平线|户外", ("outdoor_scene", "other_scene")),
    (r"^(雨|雪|风|雾|闪电|天气)$|下雨|下雪|刮风|暴风雨|暴雪|浓雾|雷雨|天气现象", ("time_weather", "weather")),
    (r"白天|夜晚|早晨|黄昏|日落|黎明", ("time_weather", "time_day")),
    (r"镜头|视角|透视|俯视|仰视|倒置", ("composition", "camera_angle")),
    (r"边框|裁切|留黑|画框", ("composition", "framing")),
    (r"光线|照明|阴影|黑暗|逆光", ("light_effect", "lighting")),
    (r"配色|色调|低饱和|单色|彩虹", ("light_effect", "palette")),
    (r"气泡|粒子|闪光|花瓣", ("light_effect", "particles")),
    (r"魔法|能量|光环|特效", ("light_effect", "magic_effect")),
    (r"水彩|油画|铅笔|传统媒介", ("style", "medium")),
    (r"线稿|上色|半色调|绘画技法|剪影", ("style", "technique")),
    (r"画风|绘画风格|艺术风格|静物", ("style", "art_style")),
    (r"作画错误|高分辨率|低分辨率|画质", ("style", "quality")),
]


# v16 exhaustive semantic audit.  Every bundled definition was compared with
# all 335 semantic categories, then checked against exact nearest neighbours.
# Only the highest-consensus previously-unclassified results are fixed here;
# three homonyms were manually corrected after reading their wiki definitions.
EXACT_OVERRIDES.update({
    '9a-91': ('weapons', 'firearm'),
    'aa-12': ('weapons', 'firearm'),
    'acog': ('weapons', 'firearm'),
    'ak-15': ('weapons', 'firearm'),
    'aks-74': ('weapons', 'firearm'),
    'as_val': ('weapons', 'firearm'),
    'b&t_mp9': ('weapons', 'firearm'),
    'bell_pepper_slice': ('food_drink', 'fruit_vegetable'),
    'benelli_m4': ('weapons', 'firearm'),
    'beretta_ar70/90': ('weapons', 'firearm'),
    'bibi_(love_live!)': ('relationships', 'group_faction'),
    'border_collie': ('creatures', 'mammal'),
    'brown_streaks': ('hair', 'hair_color'),
    'browning_m1919': ('weapons', 'firearm'),
    'burmecian': ('people', 'fantasy_person'),
    'capybara_girl': ('people', 'fantasy_person'),
    'carcano': ('weapons', 'firearm'),
    'cataracts': ('face', 'eye_shape'),
    'chariot': ('transport_play', 'land_vehicle'),
    'chinchilla_girl': ('people', 'fantasy_person'),
    'coelacanth': ('creatures', 'aquatic'),
    'colt_1851_navy': ('weapons', 'firearm'),
    'colt_9mm_smg': ('weapons', 'firearm'),
    'colt_commando': ('weapons', 'firearm'),
    'colt_python': ('weapons', 'firearm'),
    'crayfish': ('creatures', 'aquatic'),
    'cz_75': ('weapons', 'firearm'),
    'daewoo_k2': ('weapons', 'firearm'),
    'de_lisle_carbine': ('weapons', 'firearm'),
    'diesel_locomotive': ('transport_play', 'land_vehicle'),
    'donburi': ('food_drink', 'staple_food'),
    'donkey_girl': ('people', 'fantasy_person'),
    'dragon_horn': ('animal_traits', 'horns'),
    'ebony_&_ivory': ('weapons', 'firearm'),
    'eel_girl': ('people', 'fantasy_person'),
    'elcan_scope': ('weapons', 'firearm'),
    'eremite_(faction)': ('relationships', 'group_faction'),
    'fabarm_fp6': ('weapons', 'firearm'),
    'fabarm_fp6/sdass': ('weapons', 'firearm'),
    'famicom_gamepad': ('digital_media', 'game_device'),
    'fn_f2000': ('weapons', 'firearm'),
    'fn_fnc': ('weapons', 'firearm'),
    'footstool': ('household_objects', 'seating_table'),
    'futou': ('head_accessories', 'hats_caps'),
    'game_boy_advance_sp': ('digital_media', 'game_device'),
    'goal': ('recreation', 'sports'),
    'grizzly_win_mag': ('weapons', 'firearm'),
    'guqin': ('culture_objects', 'music'),
    'guzheng': ('culture_objects', 'music'),
    'gyarugasaki': ('franchise_clothes', 'school_variant'),
    'h&k_g36c': ('weapons', 'firearm'),
    'h&k_g41': ('weapons', 'firearm'),
    'h&k_mark_23': ('weapons', 'firearm'),
    'half-track': ('transport_play', 'land_vehicle'),
    'haregi': ('traditional_clothes', 'traditional_japan'),
    'hitchhiking': ('action', 'movement'),
    'humvee': ('transport_play', 'land_vehicle'),
    'imi_negev': ('weapons', 'firearm'),
    'jack_of_hearts': ('recreation', 'games'),
    'jagdpanzer_38(t)': ('transport_play', 'land_vehicle'),
    'jirou_(ramen)': ('food_drink', 'staple_food'),
    'karuta_(card_game)': ('recreation', 'games'),
    'king_of_hearts_(playing_card)': ('recreation', 'games'),
    'lahti-saloranta_m/26': ('weapons', 'firearm'),
    'le_mans_prototype': ('transport_play', 'land_vehicle'),
    'locked_slide': ('weapons', 'firearm'),
    'lotus_root_slice': ('food_drink', 'fruit_vegetable'),
    'lychee': ('food_drink', 'fruit_vegetable'),
    'm134_minigun': ('weapons', 'firearm'),
    'm16a2': ('weapons', 'firearm'),
    'm16a4': ('weapons', 'firearm'),
    'm249_saw': ('weapons', 'firearm'),
    'm60_(machine_gun)': ('weapons', 'firearm'),
    'mailbag': ('accessories', 'bags_belts'),
    'marshall_amplification': ('culture_objects', 'music'),
    'melodica': ('culture_objects', 'music'),
    'melon_slice': ('food_drink', 'fruit_vegetable'),
    'mg34': ('weapons', 'firearm'),
    'micro_uzi': ('weapons', 'firearm'),
    'minecart': ('transport_play', 'land_vehicle'),
    'moose_girl': ('people', 'fantasy_person'),
    'mossberg_590': ('weapons', 'firearm'),
    'mousse_(food)': ('food_drink', 'dessert_snack'),
    'mvp': ('recreation', 'sports'),
    'nagant_m1895': ('weapons', 'firearm'),
    'nine_of_hearts': ('recreation', 'games'),
    'nintendo_64': ('digital_media', 'game_device'),
    'nintendo_switch_lite': ('digital_media', 'game_device'),
    'no_neckwear': ('clothing_appearance', 'unworn_missing'),
    'ntw-20': ('weapons', 'firearm'),
    'oboe': ('culture_objects', 'music'),
    'organ_(instrument)': ('culture_objects', 'music'),
    'ots-14_groza': ('weapons', 'firearm'),
    'ottoman_(furniture)': ('household_objects', 'seating_table'),
    'p-chan_(p90)': ('weapons', 'firearm'),
    'partially_opaque_sunglasses': ('head_accessories', 'eyewear'),
    'peas': ('food_drink', 'fruit_vegetable'),
    'photokinesis': ('light_effect', 'magic_energy'),
    'pkm': ('weapons', 'firearm'),
    'pkp_pecheneg': ('weapons', 'firearm'),
    'playstation_3': ('digital_media', 'game_device'),
    'powdered_sugar': ('food_drink', 'dessert_snack'),
    'pushcart': ('transport_play', 'land_vehicle'),
    'r-301_carbine': ('weapons', 'firearm'),
    'r-99_smg': ('weapons', 'firearm'),
    'regloss_(hololive)': ('relationships', 'group_faction'),
    'rickenbacker': ('culture_objects', 'music'),
    'rickshaw': ('transport_play', 'land_vehicle'),
    'royal_flush': ('recreation', 'games'),
    'rpk': ('weapons', 'firearm'),
    'rpk-16': ('weapons', 'firearm'),
    'saddlebags': ('body', 'waist_hips'),
    'samue': ('traditional_clothes', 'traditional_japan'),
    'sega_mega_drive': ('digital_media', 'game_device'),
    'sega_saturn': ('digital_media', 'game_device'),
    'segway': ('transport_play', 'land_vehicle'),
    'seminar_(blue_archive)': ('relationships', 'group_faction'),
    'seven_of_hearts': ('recreation', 'games'),
    'sidecar': ('transport_play', 'land_vehicle'),
    'sig_sauer_p320': ('weapons', 'firearm'),
    'skinsuit': ('underwear_swim', 'bodysuit_leotard'),
    'skorpion_vz._61': ('weapons', 'firearm'),
    'skousers': ('clothes_main', 'bottoms'),
    'smith_&_wesson_360': ('weapons', 'firearm'),
    'snail_girl': ('people', 'fantasy_person'),
    'soul_patch': ('face', 'facial_hair'),
    'sports_sunglasses': ('head_accessories', 'eyewear'),
    'st._bernard': ('creatures', 'mammal'),
    'standard_manufacturing_dp-12': ('weapons', 'firearm'),
    'stechkin_aps': ('weapons', 'firearm'),
    'steyr_aug': ('weapons', 'firearm'),
    'stoat_girl': ('people', 'fantasy_person'),
    'strangulation_mark': ('body_detail', 'scar_wound'),
    'strappado': ('adult_kink', 'adult_bondage'),
    'sumimi_(bang_dream!)': ('relationships', 'group_faction'),
    'super_famicom_gamepad': ('digital_media', 'game_device'),
    'sv-98': ('weapons', 'firearm'),
    'sybian': ('adult_kink', 'adult_toys'),
    'tail_removed': ('animal_traits', 'tails'),
    'tail_tuft': ('animal_traits', 'tails'),
    'ten_of_hearts': ('recreation', 'games'),
    'three-wheeler': ('transport_play', 'land_vehicle'),
    'three_of_hearts': ('recreation', 'games'),
    'tractor': ('transport_play', 'land_vehicle'),
    'tumbler_glass': ('food_drink', 'tableware'),
    'type_100_smg': ('weapons', 'firearm'),
    'type_97_chi-ha': ('transport_play', 'land_vehicle'),
    'umbrella_stand': ('household_objects', 'storage_furniture'),
    'volkswagen_type_2': ('transport_play', 'land_vehicle'),
    'vsk-94': ('weapons', 'firearm'),
    'vss_vintorez': ('weapons', 'firearm'),
    'waking_another': ('action', 'interaction'),
    'walther_p38': ('weapons', 'firearm'),
    'welrod': ('weapons', 'firearm'),
    'wii_u': ('digital_media', 'game_device'),
    'winchester_model_1897': ('weapons', 'firearm'),
    'xylophone': ('culture_objects', 'music'),
    'yellow_shrug': ('outerwear_suits', 'cardigan_shawl'),
    'zanscare': ('relationships', 'group_faction'),
})

# v17 screenshot audit: definitions were read individually.  These entries also
# cover categories that lexical similarity consistently confused (a country is
# not scenery; a medical catheter is not an adult preference; a named character
# remains a character even when the source CSV marks it as a general tag).
EXACT_OVERRIDES.update({
    "ardor_blossom_star_(e.g.o)": ("franchise_clothes", "franchise_armor"),
    "argentina": ("outdoor_scene", "country_region"),
    "chloroform": ("household_objects", "other_object"),
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
})

# Seed categories introduced after the unmatched-definition clustering pass.
EXACT_OVERRIDES.update({
    "chemicals": ("household_objects", "chemical_liquid"),
    "chloroform": ("household_objects", "chemical_liquid"),
    "acid": ("household_objects", "chemical_liquid"),
    "oil": ("household_objects", "chemical_liquid"),
    "petroleum": ("household_objects", "chemical_liquid"),
    "ferrofluid": ("household_objects", "chemical_liquid"),
    "shaped_liquid": ("household_objects", "chemical_liquid"),
    "green_liquid": ("household_objects", "chemical_liquid"),
    "blue_liquid": ("household_objects", "chemical_liquid"),
    "purple_liquid": ("household_objects", "chemical_liquid"),
    "pink_liquid": ("household_objects", "chemical_liquid"),
    "top_of_moe_2014": ("meta_info", "work_event"),
    "top_of_moe_2015": ("meta_info", "work_event"),
    "top_of_moe_2016": ("meta_info", "work_event"),
    "top_of_moe_2018": ("meta_info", "work_event"),
    "top_of_moe_2021": ("meta_info", "work_event"),
    "top_of_moe_2022": ("meta_info", "work_event"),
    "touhou_16th_popularity_poll": ("meta_info", "work_event"),
    "touhou_17th_popularity_poll": ("meta_info", "work_event"),
    "touhou_18th_popularity_poll": ("meta_info", "work_event"),
    "united_nations": ("relationships", "group_faction"),
    "liquid_clothes": ("clothing_appearance", "clothing_material"),
    "liquid_dress": ("clothing_appearance", "clothing_material"),
    "spilled_milk": ("food_drink", "dairy_ingredient"),
    "nectar": ("food_drink", "drink"),
    "on_liquid": ("pose", "body_pose"),
    "liquid-in-glass_thermometer": ("household_objects", "tools"),
    "overflowing": ("light_effect", "other_effect"),
    "leaking": ("light_effect", "other_effect"),
    "moe_(phrase)": ("text_meta", "text"),
})

# v19 Wiki-definition review. These tags formed a low-confidence semantic
# cluster that the embedding pass had incorrectly collapsed into "cosplay".
# Each destination below was chosen from the bundled Wiki definition, not from
# the English spelling alone.
EXACT_OVERRIDES.update({
    "night_battle_idiot": ("meta_info", "meme"),
    "negai_wa_itsuka_asa_wo_koete_(project_sekai)": ("meta_info", "work_event"),
    "pokestar_studios": ("recreation", "games"),
    "asacoco": ("household_objects", "chemical_liquid"),
    "horosho": ("meta_info", "meme"),
    "kotori_photobomb": ("meta_info", "meme"),
    "reality_arc_(sinoalice)": ("themes", "narrative_situation"),
    "make_a_contract": ("meta_info", "meme"),
    "wryyyyyyyyyyyyyyyyyyyy": ("meta_info", "meme"),
    "zui_zui_dance": ("action", "daily_action"),
    "shinjuku_(fate/grand_order)": ("outdoor_scene", "other_scene"),
    "lasso_of_truth": ("weapons", "magic_weapon"),
    "feature_scout_1_(ensemble_stars!)": ("meta_info", "work_event"),
    "bousouzoku": ("relationships", "group_faction"),
    "are_you_my_master": ("meta_info", "meme"),
    "kimi_no_kokoro_wa_kagayaiteru_kai?": ("culture_objects", "music"),
    "lat_model_(mikumikudance)": ("style", "photo_3d"),
    "may": ("time_weather", "calendar"),
    "pactio": ("household_objects", "other_object"),
    "freezer": ("character", "letter_f"),
    "bad_apple!!": ("culture_objects", "music"),
    "f6_(osomatsu-san)": ("themes", "persona_variant"),
    "prelati's_spellbook": ("weapons", "magic_weapon"),
    "shikairo_days": ("culture_objects", "music"),
    "hoshino_ruby_dance": ("action", "daily_action"),
    "ethyria": ("relationships", "group_faction"),
    "shimousa_(fate/grand_order)": ("outdoor_scene", "other_scene"),
    "starter_five_(kancolle)": ("relationships", "group_faction"),
    "dromas_(honkai:_star_rail)": ("character", "letter_d"),
    "okawaii_koto": ("meta_info", "meme"),
    "tsukuyomi_kurage": ("culture_objects", "music"),
    "caved_(touhou)": ("meta_info", "meme"),
    "eientei": ("urban_architecture", "residential"),
    "mutsuki_face_(blue_archive)": ("meta_info", "meme"),
    "chaldea_boys_collection": ("meta_info", "work_event"),
    "monolith_(stella_sora)": ("character", "letter_m"),
    "hakka_no_togame_(bankai)": ("themes", "persona_variant"),
    "kirino_ranmaru_(mixi_max_jeanne_d'arc)": ("themes", "persona_variant"),
    "little_devil_(love_live!)": ("franchise_clothes", "franchise_outfit"),
    "big_onis_of_gensokyo_(touhou)": ("people", "fantasy_person"),
    "international_precure": ("relationships", "group_faction"),
    "brynhild_romantia": ("weapons", "magic_weapon"),
    "yubi_yubi_(inugami_korone)": ("meta_info", "meme"),
    "it's_just_not_right!": ("meta_info", "meme"),
    "ganbaruzoi": ("meta_info", "meme"),
    "harpe_(fate/grand_order)": ("weapons", "magic_weapon"),
    "tracen_ondo_(song)": ("culture_objects", "music"),
    "ags_(last_origin)": ("mech_scifi", "robot_android"),
    "2_fuel_4_ammo_11_steel": ("meta_info", "meme"),
    "genkai_made_pom_pon!!": ("copyright", "letter_g"),
    "tokimeki_poporon": ("culture_objects", "music"),
    "frolicking_fairies_of_gensokyo_(touhou)": ("copyright", "letter_f"),
    "aigis_(fate)": ("weapons", "shield"),
    "camelot_(fate/grand_order)": ("outdoor_scene", "other_scene"),
    "hagane_vocaloid": ("themes", "persona_variant"),
    "animal_realm_yakuza_(touhou)": ("relationships", "group_faction"),
    "kenmyouren_(fate)": ("weapons", "magic_weapon"),
    "tsukkomi": ("people", "occupation"),
    "hajimari_wa_kimi_no_sora": ("culture_objects", "music"),
    "olympus_(fate/grand_order)": ("outdoor_scene", "other_scene"),
    "secret_of_pedigree_(fate)": ("light_effect", "magic_energy"),
    "nahui_mictlan_(fate/grand_order)": ("outdoor_scene", "other_scene"),
    "tasukete_eirin": ("meta_info", "meme"),
    "grand_servant_(fate/grand_order)": ("people", "role_focus"),
    "atlantis_(fate/grand_order)": ("outdoor_scene", "other_scene"),
    "zukyuun": ("text_meta", "comic"),
    "arima_kinen": ("recreation", "sports"),
    "x-drive_(symphogear)": ("themes", "persona_variant"),
    "dream_world_(touhou)": ("outdoor_scene", "other_scene"),
    "lilistia": ("character", "letter_l"),
    "hannya_(arknights)": ("weapons", "shield"),
    "shiritori": ("recreation", "games"),
    "mime": ("people", "occupation"),
    "bloody_stream": ("culture_objects", "music"),
    "amazons_quartet": ("relationships", "group_faction"),
    "koyukkuri": ("creatures", "fantasy_creature"),
    "balmung_kriemhild_(fate)": ("weapons", "magic_weapon"),
    "kitsune_dance": ("action", "daily_action"),
    "carat_(umamusume)": ("character", "letter_c"),
    "hyakkaryouran_(blue_archive)": ("relationships", "group_faction"),
    "ampere_(love_live!)": ("character", "letter_a"),
    "anon_tokyo_(bang_dream!)": ("franchise_clothes", "franchise_outfit"),
    "g'ie_(hundred_line)": ("character", "letter_g"),
    "bond_level_(fate/grand_order)": ("text_meta", "screen_ui"),
    "hula": ("action", "daily_action"),
    "feature_scout_2_(ensemble_stars!)": ("meta_info", "work_event"),
    "dazzling_pearl_(nikke)": ("relationships", "group_faction"),
    "moai_(koseki_bijou)": ("themes", "persona_variant"),
    "wonderful_pact": ("household_objects", "other_object"),
    "chidori_(naruto)": ("light_effect", "magic_energy"),
    "cutie_(umamusume)": ("recreation", "toys"),
})

# v19 Wiki-definition review, batch 2. Every item below was read in the five
# largest unresolved semantic groups plus the idol-outfit boundary group.
EXACT_OVERRIDES.update({
    # Group/faction false positives: songs, work events, roles and themes.
    "bokutachi_wa_hitotsu_no_hikari": ("culture_objects", "music"),
    "octarian_(enemy)": ("people", "fantasy_person"),
    "link_to_the_future_(love_live!)": ("culture_objects", "music"),
    "gangster": ("people", "occupation"),
    "communism": ("themes", "social_theme"),
    "united_states_medal_of_honor": ("accessories", "badges_ornaments"),
    "korekara_no_someday": ("culture_objects", "music"),
    "seizon_honnou_valkyria_(idolmaster)": ("culture_objects", "music"),
    "whip_the_wimp_girl!!_(project_sekai)": ("meta_info", "work_event"),
    "fuwafuwa_time": ("culture_objects", "music"),
    "cold_war": ("themes", "social_theme"),
    "proof_(love_live!)": ("culture_objects", "music"),
    "space_marine": ("people", "occupation"),
    "natsumeki_pain": ("culture_objects", "music"),
    "battle_chatelaine": ("people", "occupation"),
    "deepness_(love_live!)": ("culture_objects", "music"),
    "shocking_party": ("culture_objects", "music"),
    "bokutachi_no_seizon_tousou_(project_sekai)": ("meta_info", "work_event"),
    "chase_my_ideal_idol!_(project_sekai)": ("meta_info", "work_event"),
    "ichigo_ichie_na_hyakki_yagyou!?_(project_sekai)": ("meta_info", "work_event"),
    "sugar_song_and_bitter_step": ("culture_objects", "music"),
    "kono_matsuri_ni_yuuyami_iro_mo_(project_sekai)": ("meta_info", "work_event"),
    "senpai_kinshi!_(love_live!)": ("meta_info", "meme"),
    "aoku_haruka": ("culture_objects", "music"),
    "2nd_live_tour_~blooming_with_ooo~": ("meta_info", "work_event"),

    # A vehicle is not its window, tyre or fuel nozzle; motion tags are actions.
    "windshield": ("transport_play", "vehicle_parts"),
    "akira_slide": ("action", "movement"),
    "goshoguruma": ("symbols", "general_symbol"),
    "tank_cupola": ("transport_play", "vehicle_parts"),
    "mclaren": ("text_meta", "brand"),
    "car_keys": ("transport_play", "vehicle_parts"),
    "spare_tire": ("transport_play", "vehicle_parts"),
    "genjiguruma": ("symbols", "general_symbol"),
    "catwalk_(walkway)": ("building_parts", "bridge_walkway"),
    "renault": ("text_meta", "brand"),
    "ducati": ("text_meta", "brand"),
    "gas_pump": ("mech_scifi", "machine"),
    "wheelie": ("action", "movement"),
    "the_chariot_(tarot)": ("recreation", "games"),
    "in_trunk": ("pose", "body_pose"),
    "drive-thru": ("indoor_scene", "commercial"),
    "pirelli": ("text_meta", "brand"),
    "portable_barricade": ("building_parts", "fence_gate"),
    "pulley": ("mech_scifi", "machine"),
    "vehicle_chase": ("action", "movement"),
    "convoy": ("action", "movement"),
    "towing": ("action", "movement"),

    # Fantasy-weapon false positives: abilities, locations, props and bodies.
    "spicebush_(e.g.o)": ("themes", "persona_variant"),
    "delusion_(genshin_impact)": ("household_objects", "other_object"),
    "noble_phantasm_(fate)": ("light_effect", "magic_energy"),
    "paladin": ("people", "occupation"),
    "amphoreus_(honkai:_star_rail)": ("outdoor_scene", "other_scene"),
    "void_(guilty_crown)": ("light_effect", "magic_energy"),
    "remnant_cube_(wuthering_waves)": ("household_objects", "other_object"),
    "hezi": ("body", "anatomy_anomaly"),
    "star_rail_special_pass_(honkai:_star_rail)": ("household_objects", "other_object"),
    "sekai_wo_kakumei_suru_chikara_wo": ("themes", "narrative_situation"),
    "star_bit": ("household_objects", "other_object"),
    "haraegushi": ("household_objects", "other_object"),
    "death_guard": ("relationships", "group_faction"),
    "red_sheet_(e.g.o)": ("themes", "persona_variant"),
    "gunbai": ("household_objects", "umbrella_fan"),
    "shroud_of_martin": ("accessories", "other_accessory"),
    "o_medal": ("household_objects", "other_object"),
    "devil_bringer": ("body", "anatomy_anomaly"),
    "d20_(die)": ("recreation", "games"),
    "lor_starcutter": ("transport_play", "air_vehicle"),

    # Firearm false positives: vehicles, brands, accessories and other weapons.
    "tri-stringer_(splatoon)": ("weapons", "bow"),
    "bt-42": ("transport_play", "land_vehicle"),
    "smith_&_wesson": ("text_meta", "brand"),
    "staccato_2011": ("meta_info", "meta"),
    "stug_iii": ("transport_play", "land_vehicle"),
    "aim-9_sidewinder": ("weapons", "explosive"),
    "octobrush_(splatoon)": ("weapons", "other_weapon"),
    "splatana_stamper_(splatoon)": ("weapons", "blade"),
    "gas_pump_nozzle": ("transport_play", "vehicle_parts"),
    "carbon_roller_(splatoon)": ("weapons", "other_weapon"),
    "plasma_cutter": ("weapons", "other_weapon"),
    "cannonball": ("weapons", "explosive"),
    "artillery_shell": ("weapons", "explosive"),
    "wire_manipulation": ("weapons", "magic_weapon"),

    # Game false positives: UI, consumables, props, an event and a symbol.
    "hitbox": ("text_meta", "screen_ui"),
    "potion_(pokemon)": ("household_objects", "chemical_liquid"),
    "intertwined_fate": ("household_objects", "other_object"),
    "scorecard": ("text_meta", "screen_ui"),
    "rave_party": ("action", "daily_action"),
    "nyan_nyan_nyan_fair_in_gamers": ("meta_info", "work_event"),
    "phonecard_(medium)": ("culture_objects", "books_paper"),
    "rider_gashat": ("mech_scifi", "scifi_device"),
    "tetromino": ("symbols", "shape_math"),

    # Idol-outfit false positives: groups, songs, brands and tour events.
    "illumination_stars_(idolmaster)": ("relationships", "group_faction"),
    "bokura_no_live_kimi_to_no_life": ("culture_objects", "music"),
    "more_more_jump!_(project_sekai)": ("relationships", "group_faction"),
    "pikapikapop_(idolmaster)": ("text_meta", "brand"),
    "star!!_(idolmaster)": ("culture_objects", "music"),
    "koukei_(idolmaster)": ("culture_objects", "music"),
    "sunny_day_song": ("culture_objects", "music"),
    "individuals_(idolmaster)": ("relationships", "group_faction"),
    "jupiter_(idolmaster)": ("relationships", "group_faction"),
    "concept_gyarus_(idolmaster)": ("franchise_clothes", "franchise_outfit"),
    "5th_live_tour_~4pair_power_spread!!!!~": ("meta_info", "work_event"),
    "ryuuguu_komachi_(idolmaster)": ("relationships", "group_faction"),
    "cometik_(idolmaster)": ("relationships", "group_faction"),
    "hajime_(idolmaster)": ("culture_objects", "music"),
    "sexy_guilty_(idolmaster)": ("relationships", "group_faction"),
    "love_live!_series_asia_tour_2024": ("meta_info", "work_event"),
    "project_krone_(idolmaster)": ("relationships", "group_faction"),
    "mofumofuen_(idolmaster)": ("relationships", "group_faction"),
    "tristar_vision_(idolmaster)": ("relationships", "group_faction"),
    "what_is_my_life?_(love_live!)": ("culture_objects", "music"),
})

# v19 Wiki-definition review, batch 3. Food, blade, mammal, combat,
# dessert, fantasy-creature/person and interaction groups were read in full.
EXACT_OVERRIDES.update({
    # Food and written recipes.
    "umeboshi": ("food_drink", "seasoning"),
    "takuan": ("food_drink", "seasoning"),
    "cookbook": ("culture_objects", "books_paper"),
    "eat_me": ("text_meta", "text"),
    "recipe": ("culture_objects", "books_paper"),
    "nantaimori": ("adult", "adult_theme"),
    "fukujinzuke": ("food_drink", "seasoning"),
    "sandwich_board": ("household_objects", "other_object"),
    "deer_cracker": ("food_drink", "bakery"),
    "grilled_corn": ("food_drink", "fruit_vegetable"),
    "caloriemate": ("food_drink", "dessert_snack"),
    "noodle_stopper": ("recreation", "toys"),
    "benishouga": ("food_drink", "seasoning"),
    "menma": ("food_drink", "seasoning"),
    "recipe_(object)": ("culture_objects", "books_paper"),
    "red_bean_paste": ("food_drink", "seasoning"),
    "konnyaku_(food)": ("food_drink", "staple_food"),
    "decorating_baked_goods": ("action", "daily_action"),
    "granulated_sugar": ("food_drink", "seasoning"),
    "hakuchu_a_la_mode": ("culture_objects", "music"),
    "potato_wedges": ("food_drink", "staple_food"),
    "ice_block": ("food_drink", "drink"),
    "ice_cream_stand": ("indoor_scene", "commercial"),

    # Weapon components, transformations and non-blade objects/actions.
    "hilt": ("weapons", "weapon_parts"),
    "shikai": ("themes", "persona_variant"),
    "japanese_saw": ("household_objects", "tools"),
    "tsuka_(handle)": ("weapons", "weapon_parts"),
    "excalibolg": ("weapons", "blunt_chain"),
    "resurreccion": ("themes", "persona_variant"),
    "too_many_knives": ("action", "holding"),
    "justice_(tarot)": ("recreation", "games"),
    "slicing": ("action", "combat_action"),
    "swept_hilt": ("weapons", "weapon_parts"),
    "cup_hilt": ("weapons", "weapon_parts"),
    "reflex_sight": ("weapons", "weapon_parts"),
    "angled_foregrip": ("weapons", "weapon_parts"),
    "aimpoint": ("weapons", "weapon_parts"),
    "red_dot_sight": ("weapons", "weapon_parts"),

    # Real mammals versus songs and fictional creatures.
    "cutie_panther": ("culture_objects", "music"),
    "cabbit": ("creatures", "fantasy_creature"),
    "metabole_piglets": ("creatures", "fantasy_creature"),
    "star_guardian_pet": ("creatures", "fantasy_creature"),

    # Combat false positives.
    "multiple_wielding": ("action", "holding"),
    "denki_anma": ("adult_kink", "adult_power"),
    "booby_trap": ("weapons", "other_weapon"),
    "boxer": ("people", "occupation"),
    "collision": ("action", "movement"),
    "k.o.": ("text_meta", "text"),
    "beating": ("body_detail", "body_function"),
    "carrot_on_stick": ("household_objects", "other_object"),
    "paratrooper": ("people", "occupation"),
    "banging": ("adult", "adult_sex"),
    "implied_after_fight": ("themes", "narrative_situation"),

    # Fantasy-creature/person boundary corrections.
    "shouryouuma": ("household_objects", "other_object"),
    "cherub": ("people", "fantasy_person"),
    "the_devil_(tarot)": ("recreation", "games"),
    "rex_genome": ("background", "background_pattern"),
    "golem_(d.gray-man)": ("mech_scifi", "robot_android"),
    "himedanshi": ("people", "role_focus"),
    "cavewoman": ("people", "role_focus"),
    "omegaverse": ("adult", "adult_theme"),
    "mamono_with_mamono": ("adult", "adult_theme"),

    # Interaction false positives.
    "forced_to_watch": ("adult_kink", "adult_power"),
    "rapping": ("action", "daily_action"),
    "clutching_head": ("pose", "arm_pose"),
    "other_with_other": ("adult", "adult_sex"),
    "imminent_spanking": ("adult_kink", "adult_power"),
    "the_hanged_man_(tarot)": ("recreation", "games"),
    "webclap": ("text_meta", "screen_ui"),
    "cradling": ("action", "holding"),
    "shared_sense": ("themes", "character_connection"),
    "chin_on_palm_challenge": ("meta_info", "meme"),
    "yobai": ("adult", "adult_theme"),
})

# v19 Wiki-definition review, batch 4. Toy, occupation, container,
# aircraft, sci-fi device, brand, produce and aquatic groups were read in full.
EXACT_OVERRIDES.update({
    # Toys, display fixtures, playground equipment and tools.
    "hinadan": ("household_objects", "storage_furniture"),
    "sandbox": ("recreation", "playground"),
    "seesaw": ("recreation", "playground"),
    "guardian_chara": ("creatures", "fantasy_creature"),
    "dummy": ("household_objects", "tools"),
    "pop-up_pirate": ("recreation", "games"),
    "figure_stage": ("household_objects", "storage_furniture"),
    "air_pump": ("household_objects", "tools"),

    # Occupation homonyms.
    "the_high_priestess_(tarot)": ("recreation", "games"),
    "server": ("digital_media", "computer_device"),

    # Containers versus actions, poses, liquids, signs and adult themes.
    "wrapping": ("action", "daily_action"),
    "in_pot": ("pose", "body_pose"),
    "komaniya_express_(genshin_impact)": ("text_meta", "brand"),
    "box_on_head": ("head_accessories", "headpiece"),
    "perfume_(cosmetics)": ("household_objects", "chemical_liquid"),
    "in_cauldron": ("pose", "body_pose"),
    "temperance_(tarot)": ("recreation", "games"),
    "your_present_is_me": ("adult", "adult_theme"),
    "herbarium": ("household_objects", "storage_furniture"),

    # Aircraft false positives and vehicle openings.
    "open_cockpit": ("transport_play", "vehicle_parts"),
    "open_hatch": ("transport_play", "vehicle_parts"),
    "nasa": ("relationships", "group_faction"),

    # Sci-fi-device false positives.
    "breathing_tube": ("household_objects", "tools"),
    "motion_slit": ("franchise_clothes", "franchise_outfit"),
    "safeguard_(blame!)": ("mech_scifi", "robot_android"),
    "maclone": ("people", "fantasy_person"),
    "matrix_of_leadership": ("household_objects", "other_object"),
    "space_elevator": ("urban_architecture", "tower_landmark"),

    # Vehicle models are vehicles, not logos; a finish line is sports scenery.
    "nissan_fairlady_z": ("transport_play", "land_vehicle"),
    "finish_line": ("recreation", "sports"),
    "nissan_gt-r": ("transport_play", "land_vehicle"),
    "nissan_skyline_r32": ("transport_play", "land_vehicle"),

    # Produce and aquatic boundary corrections.
    "sliced": ("action", "combat_action"),
    "orangette": ("food_drink", "dessert_snack"),
    "snail_shell": ("animal_traits", "claw_scale"),
    "back_fin": ("animal_traits", "claw_scale"),
    "beaver": ("creatures", "mammal"),
    "narwhal": ("creatures", "mammal"),
    "kraken": ("creatures", "fantasy_creature"),
    "walrus": ("creatures", "mammal"),
    "crab_on_shoulder": ("action", "interaction"),
    "buri_hamachi": ("meta_info", "meme"),
    "illicium": ("animal_traits", "claw_scale"),
})

# v19 Wiki-definition review, batch 5. Ornament, franchise armor, music,
# persona, tools, effects, memes, sports, pose/movement, traditional clothing,
# narrative, holiday/sky/mineral/urban, flowers, bondage, objects and UI groups.
EXACT_OVERRIDES.update({
    "ornate": ("clothing_detail", "trim_detail"),
    "supportasse": ("clothing_detail", "collar_detail"),
    "pommel_tassel": ("weapons", "weapon_parts"),
    "love_wing_bell": ("culture_objects", "music"),
    "studded": ("clothing_detail", "trim_detail"),
    "tapestry": ("household_objects", "storage_furniture"),
    "nameplate": ("text_meta", "text"),
    "plain_epaulettes": ("clothing_detail", "trim_detail"),
    "flourish_(design)": ("background", "background_pattern"),
    "bobbles": ("clothing_detail", "trim_detail"),
    "decoden": ("style", "technique"),
    "shimekazari": ("household_objects", "storage_furniture"),
    "ornamental_weight": ("clothing_detail", "trim_detail"),
    "mandalorian": ("people", "fantasy_person"),
    "witcher_medallion": ("jewelry_accessories", "necklace_choker"),
    "typhoon_(kamen_rider)": ("themes", "persona_variant"),
    "arcle_(kuuga)": ("mech_scifi", "scifi_device"),
    "goddess_of_war_(fate)": ("accessories", "bags_belts"),
    "vistamp": ("mech_scifi", "scifi_device"),
    "character_single": ("culture_objects", "music"),
    "carving": ("action", "daily_action"),
    "fishing_lure": ("recreation", "sports"),
    "magic_circuit": ("body", "internal_organs"),
    "enkephalin_(project_moon)": ("household_objects", "chemical_liquid"),
    "telepathy": ("themes", "character_connection"),
    "level_5_(toaru)": ("people", "role_focus"),
    "contract": ("culture_objects", "books_paper"),
    "affection_meter": ("text_meta", "screen_ui"),
    "adrenaline!!!": ("culture_objects", "music"),
    "buried_in_sculpted_sand": ("pose", "body_pose"),
    "music_s.t.a.r.t!!": ("culture_objects", "music"),
    "sprite_sheet": ("composition", "layout"),
    "insulting_viewer": ("action", "interaction"),
    "sparkling_daydream": ("culture_objects", "music"),
    "i_do_me!_(love_live!)": ("culture_objects", "music"),
    "satire": ("style", "genre"),
    "let's_make_touhou_kids": ("meta_info", "work_event"),
    "ball_pit": ("recreation", "playground"),
    "tachihanabishi": ("adult", "adult_sex"),
    "mid-stride": ("action", "movement"),
    "rabbit_on_shoulder": ("action", "interaction"),
    "tied_to_stake": ("sensitive", "restraint"),
    "kirara_jump": ("action", "movement"),
    "back_pain": ("body_detail", "body_state"),
    "rise_up_high!_(love_live!)": ("franchise_clothes", "franchise_outfit"),
    "figure_stand": ("household_objects", "storage_furniture"),
    "jockey": ("people", "occupation"),
    "cavalry": ("people", "occupation"),
    "collapsed": ("pose", "stationary_pose"),
    "streaking": ("adult_body", "adult_nudity"),
    "ice_fishing": ("action", "daily_action"),
    "hiroshimaben": ("text_meta", "text"),
    "shima_(pattern)": ("background", "background_pattern"),
    "tsuka-ito": ("weapons", "weapon_parts"),
    "jojifuku": ("uniform_costume", "themed_costume"),
    "akabeko": ("recreation", "toys"),
    "sashimono": ("symbols", "flag"),
    "kagome_(pattern)": ("background", "background_pattern"),
    "kintsugi": ("style", "technique"),
    "gari_gari-kun": ("food_drink", "dessert_snack"),
    "ojigi_(bowing)": ("pose", "body_pose"),
    "blue_jingasa": ("protective_clothes", "combat_helmet"),
    "okinawa": ("outdoor_scene", "country_region"),
    "vietnam_war": ("themes", "social_theme"),
    "keikyoku_no_machi_wa_doko_e_(project_sekai)": ("meta_info", "work_event"),
    "multiple_fusions": ("themes", "identity_change"),
    "in_hourglass": ("pose", "body_pose"),
    "interrogation": ("sensitive", "restraint"),
    "freudian_slip": ("text_meta", "text"),
    "hostage": ("sensitive", "restraint"),
    "charisma_establishment": ("themes", "persona_variant"),
    "candle_no_kaori_wa_omoide_to_tomo_ni_(project_sekai)": ("meta_info", "work_event"),
    "relax_teatime_(project_sekai)": ("meta_info", "work_event"),
    "napoleonic_wars": ("themes", "social_theme"),
    "take_the_best_shot!_(project_sekai)": ("meta_info", "work_event"),
    "stand-up_comedy": ("action", "daily_action"),
    "ragfes": ("meta_info", "work_event"),
    "playable_character_celebration": ("action", "daily_action"),
    "post_guild_war_celebration": ("meta_info", "work_event"),
    "servant_summer_festival!_2018": ("meta_info", "work_event"),
    "fai_chun": ("household_objects", "other_object"),
    "solar_term": ("time_weather", "calendar"),
    "holiday_holiday_(tenko)_(love_live!)": ("culture_objects", "music"),
    "space_habitat": ("urban_architecture", "tower_landmark"),
    "celestial_globe": ("household_objects", "other_object"),
    "sky_mirage": ("household_objects", "other_object"),
    "o'neill_cylinder": ("urban_architecture", "tower_landmark"),
    "the_moon_(tarot)": ("recreation", "games"),
    "the_sun_(tarot)": ("recreation", "games"),
    "orbited": ("light_effect", "other_effect"),
    "cyberspace": ("indoor_scene", "virtual_space"),
    "observatory": ("urban_architecture", "public_building"),
    "praise_the_sun": ("pose", "arm_pose"),
    "philosopher's_stone": ("household_objects", "other_object"),
    "pyroxene_(blue_archive)": ("household_objects", "other_object"),
    "secret_stone": ("household_objects", "other_object"),
    "ice_pick": ("household_objects", "tools"),
    "monolith_(object)": ("household_objects", "other_object"),
    "sarcophagus": ("household_objects", "container"),
    "thunder_stone": ("household_objects", "other_object"),
    "z-crystal": ("household_objects", "other_object"),
    "mining": ("action", "daily_action"),
    "inkstone": ("culture_objects", "stationery"),
    "ishikawa_prefecture": ("outdoor_scene", "country_region"),
    "hokkaido": ("outdoor_scene", "country_region"),
    "kanagawa": ("outdoor_scene", "country_region"),
    "shibuya_109": ("urban_architecture", "public_building"),
    "raised_curb": ("outdoor_scene", "terrain_surface"),
    "ranunculus": ("nature", "flower_species"),
    "qinghua_(porcelain)": ("household_objects", "container"),
    "purple_pansy": ("nature", "flower_species"),
    "yellow_pansy": ("nature", "flower_species"),
    "hollyhock": ("nature", "flower_species"),
    "sweet_pea": ("nature", "flower_species"),
    "gracidea": ("nature", "flower_species"),
    "bouquet_toss": ("action", "daily_action"),
    "dianthus": ("nature", "flower_species"),
    "organic": ("style", "art_style"),
    "tweedia": ("nature", "flower_species"),
    "egret_orchid": ("nature", "flower_species"),
    "herb_bundle": ("nature", "grass_crop"),
    "bindle": ("accessories", "bags_belts"),
    "glue": ("household_objects", "chemical_liquid"),
    "love_potion": ("household_objects", "chemical_liquid"),
    "impossible_storage": ("adult_kink", "adult_insertion"),
    "engraved": ("style", "technique"),
    "too_many_stickers": ("accessories", "badges_ornaments"),
    "guide": ("text_meta", "text"),
    "interactive_media": ("meta_info", "meta"),
    "ipod_ad": ("meta_info", "meme"),
})

# v19 Wiki-definition review, batch 6. Remaining effect, insect, tableware,
# explicit action, metadata and water-vehicle boundary groups were read in full.
EXACT_OVERRIDES.update({
    "lubrication": ("action", "daily_action"),
    "slimy": ("body_detail", "surface_stain"),
    "relief": ("style", "medium"),
    "whirlpool": ("outdoor_scene", "water_scene"),
    "smudge": ("style", "technique"),
    "lsd": ("household_objects", "other_object"),
    "flyswatter": ("household_objects", "tools"),
    "butterfly_on_face": ("action", "interaction"),
    "butterfly_on_shoulder": ("action", "interaction"),
    "chitin": ("animal_traits", "claw_scale"),
    "insect_on_head": ("action", "interaction"),
    "beehive": ("household_objects", "other_object"),
    "griddle": ("household_objects", "appliance"),
    "porcelain": ("household_objects", "container"),
    "bong": ("household_objects", "other_object"),
    "saucepan": ("household_objects", "appliance"),
    "nuka-cola": ("food_drink", "drink"),
    "fullbottle": ("mech_scifi", "scifi_device"),
    "strainer": ("household_objects", "tools"),
    "grater": ("household_objects", "tools"),
    "bottle_opener": ("household_objects", "tools"),
    "youtube_creator_award": ("household_objects", "other_object"),
    "stickam": ("text_meta", "brand"),
    "information_sheet": ("text_meta", "text"),
    "niconico_id": ("text_meta", "text"),
    "colophon": ("text_meta", "text"),
    "character_chart": ("composition", "layout"),
    "production_note": ("text_meta", "text"),
    "gold_creator_award": ("household_objects", "other_object"),
    "true_crime": ("sensitive", "injury_death"),
    "master_up": ("meta_info", "work_event"),
    "sailing": ("action", "movement"),
    "ship_deck": ("transport_play", "vehicle_parts"),
    "shroud_(sailing)": ("transport_play", "vehicle_parts"),
    "tetrapod": ("building_parts", "frame_structure"),
    "ratline": ("transport_play", "vehicle_parts"),
    "dazzle_paint": ("background", "background_pattern"),
    "orel_cruise": ("action", "movement"),
    "buoy": ("household_objects", "other_object"),
    "landship": ("transport_play", "land_vehicle"),
})

# v19 Wiki cross-check, batch 7. Definition keywords (song, event, tarot,
# group, country and vehicle) were checked across every unresolved category.
EXACT_OVERRIDES.update({
    "shikai_no_sumi_kuchiru_oto": ("culture_objects", "music"),
    "kira-kira_sensation!": ("culture_objects", "music"),
    "trust_me_(durarara!!)": ("culture_objects", "music"),
    "hare_hare_yukai": ("culture_objects", "music"),
    "sekaiichi_kawaii_watashi_(idolmaster)": ("culture_objects", "music"),
    "otomad": ("culture_objects", "music"),
    "miracreation": ("culture_objects", "music"),
    "close_game/offline_(project_sekai)": ("meta_info", "work_event"),
    "the_lovers_(tarot)": ("recreation", "games"),
    "the_star_(tarot)": ("recreation", "games"),
    "the_empress_(tarot)": ("recreation", "games"),
    "death_(tarot)": ("recreation", "games"),
    "the_emperor_(tarot)": ("recreation", "games"),
    "the_hierophant_(tarot)": ("recreation", "games"),
    "heart_tail_duo": ("relationships", "romance_orientation"),
    "novum_chaldea": ("relationships", "group_faction"),
    "s.w.a.t.": ("relationships", "group_faction"),
    "leo/need_(project_sekai)": ("relationships", "group_faction"),
    "crossbone_vanguard": ("relationships", "group_faction"),
    "maximal": ("relationships", "group_faction"),
    "vspo!_showdown": ("meta_info", "work_event"),
    "religious_offering": ("household_objects", "other_object"),
    "predacon": ("relationships", "group_faction"),
    "loud": ("culture_objects", "music"),
    "death_star": ("transport_play", "air_vehicle"),
    "range_finder": ("weapons", "weapon_parts"),
    "itano_circus": ("light_effect", "particles"),
    "sv001_(metal_slug)": ("transport_play", "land_vehicle"),
    "wisdom_cube_(azur_lane)": ("household_objects", "other_object"),
    "augma": ("mech_scifi", "scifi_device"),
    "pharaoh": ("people", "role_focus"),
    "russian_empire": ("outdoor_scene", "country_region"),
    "korea": ("outdoor_scene", "country_region"),
    "israel": ("outdoor_scene", "country_region"),
    "ooarai_(ibaraki)": ("outdoor_scene", "country_region"),
    "moose": ("creatures", "mammal"),
})

# v19 Wiki review, batch 8: lowest-confidence unresolved candidates.
EXACT_OVERRIDES.update({
    "mitsuketa_keshiki_tazusaete": ("meta_info", "work_event"),
    "tango": ("action", "daily_action"),
    "sefirot": ("symbols", "religious_symbol"),
    "coronation": ("meta_info", "work_event"),
    "hay_bale": ("nature", "grass_crop"),
    "unequal_popsicle_division": ("relationships", "comparison"),
    "trench": ("outdoor_scene", "terrain_surface"),
    "suiten_nikkou_amaterasu_yanoshisu_ishi": ("household_objects", "other_object"),
    "rotisserie": ("household_objects", "appliance"),
    "egosearching": ("action", "daily_action"),
    "sighting": ("style", "technique"),
    "protocol_omega": ("relationships", "group_faction"),
    "hokage": ("people", "occupation"),
    "leaving": ("action", "movement"),
    "taking_cover": ("action", "combat_action"),
    "shachihoko": ("creatures", "fantasy_creature"),
    "hakuren": ("relationships", "group_faction"),
    "calavera": ("household_objects", "other_object"),
    "caduceus": ("symbols", "science_sign"),
    "sewer": ("urban_architecture", "urban"),
    "plaque": ("text_meta", "text"),
    "rivets": ("clothing_detail", "fastener"),
    "lifestream": ("light_effect", "magic_energy"),
    "abacus": ("household_objects", "tools"),
    "pet_cone": ("household_objects", "care_cleaning"),
    "umpire": ("people", "occupation"),
    "powder_puff": ("household_objects", "care_cleaning"),
    "hazard_stripes": ("background", "background_pattern"),
    "morse_code": ("text_meta", "text"),
})


def classify_from_chinese(tag: dict) -> tuple[str, str] | None:
    cn = str(tag.get("cn") or "").strip()
    for pattern, location in CN_FALLBACK_RULES:
        if re.search(pattern, cn):
            return location
    return None


def classify_adult(name: str) -> tuple[str, str] | None:
    token = parts(name)
    # Use explicit words/stems here.  Loose fragments such as ``bra``, ``oral``
    # and ``cum`` would otherwise misclassify bracelet, floral and cumulus.
    explicit_fluid_word = bool(re.search(r"(^|_)(semen|sperm|spermatozoa)($|_)", name))
    if any_fragment(name, ("ejaculat", "precum", "pussy_juice", "bukkake", "lactation", "female_ejaculation")) or explicit_fluid_word or re.search(r"(^|_)cum($|_|shot|drip|dump|flation)", name):
        return "adult", "adult_fluid"
    anatomy_target = bool(re.search(r"(^|_)(penis|vulva|pussy|testicles?|scrotum|nipples?|areolae?|genitals?|clitoris|anus|urethra)($|_)", name))
    if anatomy_target and re.search(r"(^|_)(licking|kissing|sucking|biting)($|_)", name):
        return "adult", "adult_oral"
    if anatomy_target and ("own" in token or any_prefix(name, ("self_", "grabbing_own_", "spreading_own_", "tweaking_own_"))):
        return "adult", "adult_self"
    fetish_object = bool(token & {"piercing", "jewelry", "clamp", "clamps", "chain", "bells", "tag", "tassel", "tassels", "vibrator", "torture", "beads", "hook", "toy", "machine", "doll", "controller"})
    if (anatomy_target and fetish_object) or any_fragment(name, ("sex_toy", "sex_machine", "sex_doll", "anal_beads", "anal_hook", "object_insertion", "ball_insertion")):
        return "adult", "adult_fetish"
    if anatomy_target and re.search(r"(^|_)(grabbing|spreading|presenting|looking|smelling|tweaking)($|_)", name):
        return "adult", "adult_suggestive"
    if any_fragment(name, ("fellatio", "cunnilingus", "deepthroat", "blowjob", "irrumatio", "licking_penis", "licking_vulva")) or "oral" in token:
        return "adult", "adult_oral"
    if any_fragment(name, ("masturbat", "self_finger", "self_fondle", "self_grab", "auto_", "handjob", "fingering")):
        return "adult", "adult_self"
    explicit_sex_word = name == "sex" or name.startswith("sex_") or name.endswith("_sex") or "_sex_" in name
    if any_fragment(name, ("penetrat", "paizuri", "tribadism", "humping", "vaginal", "intercrural", "impregnation", "cowgirl_position", "missionary", "doggystyle", "threesome", "foursome", "gangbang", "footjob")) or explicit_sex_word or "anal" in token:
        return "adult", "adult_sex"
    if anatomy_target or "pubic_hair" in name:
        return "adult", "adult_anatomy"
    explicit_gag = name == "gag" or any_fragment(name, ("ball_gag", "ring_gag", "bit_gag", "tape_gag", "improvised_gag", "cleave_gag"))
    if any_fragment(name, ("bondage", "shibari", "bdsm", "femdom", "foot_fetish", "breast_fetish", "vore", "erotic_hypnosis")) or explicit_gag or "submission" in token:
        return "adult", "adult_fetish"
    if any_fragment(name, ("pantyshot", "panty_pull", "clothing_aside", "clothes_aside", "downblouse", "upskirt", "open_fly", "wardrobe_malfunction")):
        return "adult", "adult_clothes"
    if any_fragment(name, ("nude", "naked", "topless", "bottomless", "exposed_genital", "exposed_breast", "public_indecency", "covering_breasts", "covering_crotch")):
        return "adult", "adult_nudity"
    if any_fragment(name, ("fondling", "groping", "seductive", "suggestive", "imminent_sex", "breast_grab", "ass_grab", "presenting_")):
        return "adult", "adult_suggestive"
    if any_fragment(name, ("gore", "decapitat", "dismember", "severed_head", "severed_limb", "corpse", "entrails", "eviscerat", "internal_organs")) or "guro" in token:
        return "adult", "adult_gore"
    explicit_rape = name == "rape" or name.startswith("rape_") or name.endswith("_rape") or "_rape_" in name
    if any_fragment(name, ("explicit", "porn", "hentai", "nsfw", "sexualized", "bestiality", "incest", "orgasm", "peeing", "defecat")) or explicit_rape:
        return "adult", "adult_other"
    return None


def classify_general(tag: dict) -> tuple[str, str]:
    name = tag["name"].lower()
    # A trailing Danbooru qualifier identifies a franchise or disambiguates a
    # word; it is not normally the semantic head.  Treating ``_(fire_emblem)``
    # or ``_(stellar_blade)`` as ordinary tokens used to turn unrelated outfits
    # and props into symbols or swords.
    base_name = re.sub(r"_\([^)]*\)$", "", name)
    token = parts(base_name)
    ordered_tokens = [item for item in re.split(r"[_()\-/' ]+", base_name) if item]
    head = ordered_tokens[-1] if ordered_tokens else base_name
    if name in EXACT_OVERRIDES:
        return EXACT_OVERRIDES[name]
    adult_location = classify_adult(name)
    if adult_location:
        return adult_location
    if re.match(r"^\d+\+?(girls|boys|others?)$", name):
        return "people", "count_gender"

    # Audited semantic families that are safer as closed sets than as broad
    # substring rules.
    if re.fullmatch(r"[a-z]+_type_theme_\(pokemon\)", name):
        return "style", "genre"
    constellation_names = {
        "cancer", "cassiopeia", "capricorn", "aries", "aquarius", "cygnus", "aquila", "gemini",
        "leo", "orion", "lyra", "taurus", "scorpius", "sagittarius", "pisces", "pegasus", "virgo",
        "ursa_minor", "ursa_major",
    }
    if base_name in constellation_names and (name == base_name or name.endswith("_(constellation)")):
        return "outdoor_scene", "sky_space"
    celestial_names = {
        "black_hole", "m87_black_hole", "comet", "asteroid", "milky_way", "meteor", "meteor_shower",
        "eclipse", "solar_eclipse", "solar_system", "in_orbit", "orbital_path", "moon_phases",
        "moon_reflection", "moon_in_daylight", "on_moon", "starry_moon", "new_moon", "half_moon",
        "gibbous_moon", "multiple_moons", "blue_moon", "orange_moon", "pink_moon", "purple_moon",
        "yellow_moon", "huge_moon", "broken_moon",
    }
    if base_name in celestial_names or name.endswith("_(planet)"):
        return "outdoor_scene", "sky_space"
    commemorative_days = {
        "cirno_day", "digimon_day", "gardevoir_day", "flandre_day", "miku_day", "koishi_day",
        "marine_day", "marisa_day", "pokemon_day", "satori_day", "parsee_day", "patchouli_day",
        "sekibanki_day", "reimu_day", "remilia_day", "youmu_day", "cat_day", "bunny_day",
        "children's_day", "good_meat_day", "meat_day", "hinamatsuri",
    }
    if base_name in commemorative_days:
        return "time_weather", "holiday"
    ui_software = {
        "adobe_photoshop", "clip_studio_paint", "ibispaint", "microsoft_paint", "painttool_sai",
        "procreate", "mikumikudance", "dialogue_options", "character_select", "attribute_slider",
        "heads-up_display", "options", "minimap", "search_bar", "taskbar", "error_message",
        "hypnosis_app", "social_network", "desktop", "fake_transparency", "facial_recognition",
        "gameplay_ability", "level_up", "strawpage", "google_maps", "signal_bar", "chat_log",
        "fake_video", "choice", "snapchat", "video_call", "recycle_bin", "tweet", "news",
        "clockshow", "segment_display", "super_chat", "momotalk", "no_image",
    }
    if base_name in ui_software:
        return "text_meta", "screen_ui"
    if name.endswith(("_(symbol)", "_(emblem)", "_(coat_of_arms)", "_(zodiac)")):
        return "text_meta", "symbol"
    audited_symbols = {
        "crest", "ankh", "runes", "sakuramon", "roundel", "bass_clef", "star_of_david",
        "jolly_roger", "swastika", "trigram", "triquetra", "zodiac", "zodiac_wheel", "ss_insignia",
        "imperial_aquila", "digital_hazard", "quarter_rest", "eighth_rest", "no_smoking", "ouroboros",
        "bagua", "checkmark", "mandala", "wheel_of_dharma", "hanamaru", "omanko_mark", "digimon_crest",
        "mark_of_the_doom_slayer", "emergency_exit", "siegrunen", "white_ensign", "mitsu_uroko",
        "signet_of_ego", "rod_of_asclepius", "endless_knot", "o_x", "+_-",
    }
    if base_name in audited_symbols:
        return "text_meta", "symbol"
    text_names = {
        "lyrics", "math", "credits", "afterword", "equation", "cyrillic", "kunreishiki",
        "unownglyphics", "alphabet", "blackletter", "source_quote", "bad_math",
    }
    if base_name in text_names or any_suffix(base_name, ("_name", "_number")) or name.endswith(("_(phrase)", "_(language)", "_(letter)", "_(kanji)", "_(equation)", "_(math)", "_(asl)", "_(profanity)")):
        return "text_meta", "text"
    audited_styles = {
        "ligne_claire": "art_style", "cartoonized": "art_style", "egyptian_art": "art_style",
        "acid_graphics": "art_style", "character_sticker": "art_style", "cyber_sigilism": "art_style",
        "realified": "art_style", "nanatsu-yoru": "art_style", "zeknova": "art_style",
        "mold_camelot": "art_style", "woren": "art_style", "gurokawa": "art_style",
        "frutiger_aero": "genre", "frutiger_metro": "genre", "weirdcore": "genre",
        "liminal_space": "genre", "biopunk": "genre", "solarpunk": "genre",
        "tenshi_kaiwai": "genre", "yami_kawaii": "genre", "victorian": "era_style",
        "medieval": "era_style", "heian": "era_style", "ben-day_dots": "technique",
        "dithering": "technique", "canvas_texture": "technique", "speedpaint": "technique",
        "symbolism": "art_style", "smear_frame": "technique", "color_trace": "technique",
        "pixelated": "technique", "ttgl_eyecatch": "technique", "low_poly": "photo_3d",
        "wireframe": "photo_3d", "time_lapse": "photo_3d", "mugshot": "photo_3d",
        "id_photo": "photo_3d", "polaroid_photo": "photo_3d", "marble_sculpture": "photo_3d",
        "sumi-e": "medium", "zhongguo_hua": "medium",
    }
    if base_name in audited_styles:
        return "style", audited_styles[base_name]
    composition_sets = {
        "layout": {"grid_lineup", "negative_space", "projected_inset", "inset", "doodle_inset", "before_and_after", "symmetry", "comparison", "age_comparison", "odd_one_out", "opposing_sides", "front_and_back", "pile", "variations"},
        "framing": {"round_image", "floral_border", "gold_border", "irregular_border", "fading_border", "red_border", "green_border", "stepping_on_frame", "art_tools_in_frame"},
        "viewpoint": {"under_shot", "pov_doorway", "mirror_selfie", "viewer_self-insert", "camera_feed", "back_view_in_reflection", "peephole", "from_outside", "from_inside"},
        "focus": {"blending", "zooming_in"},
    }
    for category_id, names in composition_sets.items():
        if base_name in names:
            return "composition", category_id
    weather_names = {"blizzard", "after_rain", "haze", "frost", "sun_shower", "sandstorm", "smog", "whirlwind", "dark_cloud", "flood", "earthquake", "aurora"}
    if base_name in weather_names:
        return "time_weather", "weather"
    if base_name in {"seasons", "changing_seasons"}:
        return "time_weather", "season"
    if base_name in {"january", "february", "march", "april", "june", "july", "august", "september", "october", "november", "december"}:
        return "time_weather", "calendar"
    lighting_names = {"tree_shade", "crack_of_light", "blue_light", "green_light", "red_light", "pink_light", "purple_light", "orange_light", "yellow_light", "colored_lights", "lights", "headlight_beam", "flashlight_beam", "overlighting", "underlighting", "ray_of_grace"}
    if base_name in lighting_names:
        return "light_effect", "lighting"
    optical_names = {"refraction", "dispersion", "subsurface_scattering", "star_trail", "gradient_filter", "double_exposure", "sun_glare", "face_filter"}
    if base_name in optical_names:
        return "light_effect", "optical"
    audited_places = {
        "home_room": {"apartment"},
        "public_indoor": {"aquarium_tunnel", "archery_dojo", "ballroom", "clubroom", "courtroom", "dojo", "dungeon", "garage", "hangar", "infirmary", "parking_garage", "public_restroom", "sauna", "studio", "warehouse", "workshop", "stairwell"},
        "commercial": {"mall", "nightclub", "planetarium", "tavern", "waterpark", "bowling_alley", "market_stall"},
        "architecture": {"gazebo", "chimney", "colonnade", "pagoda", "pavilion", "pyramid", "spiral_staircase", "spire", "steeple", "thatched_roof", "treehouse", "tunnel", "windmill", "windowsill", "wooden_stairs", "overpass", "walkway", "transom_window", "broken_door", "moon_gate", "wire_fence", "padded_walls", "wooden_porch", "stairs", "deck", "boardwalk", "boarded_windows", "courtyard"},
        "urban": {"town_square"},
    }
    for category_id, names in audited_places.items():
        if base_name in names:
            return "indoor_scene", category_id
    outdoor_places = {
        "water_scene": {"stream", "island", "pier", "dock", "canal", "coral_reef", "seafloor", "seaside", "seascape", "port"},
        "other_scene": {"floating_island", "floating_rock", "boulder", "crater", "underground", "valley", "glacier", "mountaintop", "oasis", "gravel", "snowscape", "wetland", "farm", "rural", "battlefield"},
    }
    for category_id, names in outdoor_places.items():
        if base_name in names:
            return "outdoor_scene", category_id
    palette_names = {"gradient", "analogous_colors", "color_contrast", "contrast", "color_coordination", "saturated", "multiple_theme_colors", "color_drain", "inverted_colors", "pastels", "negative"}
    if base_name in palette_names:
        return "light_effect", "palette"
    fire_effect_names = {"campfire", "mushroom_cloud", "afterburner", "eruption", "missile_trail"}
    if base_name in fire_effect_names:
        return "light_effect", "fire_smoke"
    magic_effect_names = {"laser", "laser_pointer_projection", "master_spark", "pillar_of_light", "will-o'-the-wisp", "umbrakinesis", "purple_lightning"}
    if base_name in magic_effect_names:
        return "light_effect", "magic_effect"

    # Strong compound nouns are resolved before their modifiers.  Without this
    # small priority layer, tags such as ``rabbit_hair_ornament``,
    # ``birthday_cake`` and ``energy_gun`` are stolen by rabbit/birthday/energy.
    # Copyright and character tags have already been separated in classify_tag.
    if "holding_hands" in name:
        return "action", "interaction"
    if any_prefix(name, ("holding_", "carrying_", "grabbing_", "gripping_", "wielding_")):
        return "action", "holding"

    if any_fragment(name, ("hair_ornament", "hairband", "hairpin", "hairclip", "hair_ribbon", "hair_bow", "hair_flower", "hair_tie", "hair_bobbles", "hair_tubes", "hair_rings")):
        return "accessories", "hair_accessory"

    garment_words = {
        "clothes", "clothing", "shirt", "blouse", "sweater", "hoodie", "top", "dress", "gown",
        "skirt", "pants", "shorts", "trousers", "jeans", "bra", "bikini", "swimsuit", "panties",
        "underwear", "jacket", "coat", "cape", "cloak", "kimono", "apron", "uniform", "sleeve",
        "sleeves", "stocking", "stockings", "thighhighs", "kneehighs", "pantyhose", "leggings",
        "hat", "headwear", "eyewear", "mask", "helmet", "glove", "gloves", "sock", "socks",
        "legwear", "shoes", "boots", "camisole", "vest", "leotard", "bodysuit", "unitard",
        "buruma", "bloomers", "bandeau", "fundoshi", "loincloth", "pajamas", "nightgown", "robe",
        "hakama", "yukata", "tabard", "sarong", "visor", "blindfold", "eyepatch", "necktie",
        "scarf", "choker", "necklace", "collar", "strap", "suspenders", "veil", "cardigan",
        "overalls", "babydoll", "pajama", "waistcoat", "tights", "jumpsuit", "romper",
    }
    if name == "see-through" or (name.startswith("see-through_") and token & garment_words):
        return "clothing_detail", "clothing_material"
    garment_state = base_name.startswith("no_") or bool(re.search(
        r"(^|_)(lift|lifted|lifting|pull|pulled|pulling|open|opened|torn|wet|unworn|removed|removing|adjusting|putting|aside|lowered|raised|rolled|slip|down|undressing)($|_)",
        base_name,
    ))
    if token & garment_words and garment_state and not any_fragment(name, ("open_toe", "open_heel", "open-back")):
        return "clothing_detail", "clothing_state"

    # Predicate-first rules.  A semantic object such as hand, skirt or tail
    # must not hide the fact that the tag describes an interaction.
    interaction_targets = {
        "ankle", "arm", "ass", "belly", "body", "breast", "cheek", "chest", "crotch", "ear",
        "eyelid", "face", "finger", "foot", "hand", "head", "hip", "horn", "leg", "legs", "mouth",
        "neck", "nipple", "pectoral", "shoulder", "tail", "tentacle", "thigh", "throat", "toe",
        "tongue", "torso", "waist",
    }
    if base_name.endswith("_kiss"):
        return "action", "interaction"
    if base_name.endswith(("_grab", "_hold")):
        return ("action", "interaction") if token & interaction_targets else ("action", "holding")
    if base_name.endswith("_pull"):
        return ("action", "interaction") if token & interaction_targets else ("action", "holding")
    if base_name.endswith("_carry"):
        return "action", "holding"

    # Cross-folder compound heads that must win before generic body/face/color
    # rules.  These cover marks, injuries, prosthetics and makeup regardless of
    # which body part appears elsewhere in the tag.
    if re.search(r"(^|_)(tattoo|scar|scars|birthmark|bandaid|bandage|bruise|bite_mark|markings|stitches|stitched)($|_)", base_name):
        return "body", "body_marks"
    if re.search(r"(^|_)(severed|detached)_(arm|arms|hand|hands|finger|fingers|leg|legs|foot|feet|head)($|_)", base_name):
        return "adult", "adult_gore"
    if re.search(r"(^|_)(broken|injured|bleeding|blood_on)_(arm|arms|hand|hands|finger|fingers|leg|legs|foot|feet|face|head|chest|body)($|_)", base_name):
        return "body", "body_state"
    if re.search(r"(^|_)(mechanical|robotic|cybernetic)_(eye|eyes|arm|arms|hand|hands|leg|legs|foot|feet|spine|tail|tentacle|tentacles)($|_)", base_name):
        return "mech_scifi", "cybernetic"
    if base_name.endswith("_eyeshadow") or token & {"eyeshadow", "eyeliner", "mascara"}:
        return "face", "makeup"
    if re.search(r"(^|_)(bad_hands|bad_feet|wrong_hand|bad_anatomy)($|_)", base_name):
        return "style", "quality"

    if "uniform" in token:
        school_markers = ("school", "academy", "gakuen", "kindergarten", "elementary", "middle_school", "high_school", "schoolgirl")
        if any(marker in name for marker in school_markers):
            return "clothes_special", "school_uniform"
        return "clothes_special", "occupation_uniform"
    if name == "apron" or name.endswith("_apron"):
        return "clothes_special", "occupation_uniform"
    if any_suffix(base_name, ("_costume", "_themed_outfit")) or head == "costume":
        return "clothes_special", "themed_costume"

    # Underwear and protective wear precede ordinary tops so compounds such as
    # ``front-tie_bikini_top`` retain their actual garment family.
    if any_suffix(name, ("_swimsuit", "_bikini", "_swimwear")) or name in {"swimsuit", "bikini", "swimwear"} or ("bikini" in token and name.endswith("_top")):
        return "underwear_swim", "swimsuit"
    if any_suffix(name, ("_bra", "_lingerie", "_bandeau")) or name in {"bra", "lingerie", "bralette", "bandeau"}:
        return "underwear_swim", "bra_lingerie"
    if any_suffix(name, ("_panties", "_underwear", "_thong")) or name in {"panties", "underwear", "thong", "loincloth"}:
        return "underwear_swim", "panties_underwear"
    if any_suffix(name, ("_leotard", "_bodysuit", "_unitard")) or name in {"leotard", "bodysuit", "unitard", "catsuit"}:
        return "underwear_swim", "bodysuit_leotard"
    if any_suffix(name, ("_thighhighs", "_kneehighs", "_pantyhose", "_stockings", "_stocking", "_leggings", "_legwear")):
        return "legwear_footwear", "stockings"
    if any_suffix(name, ("_socks",)) or name == "socks":
        return "legwear_footwear", "socks"
    if any_suffix(name, ("_boots",)) or name in {"boots", "boot", "waders", "sweatboots"}:
        return "legwear_footwear", "boots"
    if any_suffix(name, ("_shoes", "_sandals", "_heels", "_loafers", "_sneakers", "_slippers", "_footwear")):
        return "legwear_footwear", "shoes"
    if any_suffix(name, ("_armor", "_armour")) or name in {"armor", "armour", "chainmail", "breastplate"}:
        return "legwear_footwear", "armor"
    if any_suffix(name, ("_helmet", "_wetsuit", "_hazmat_suit")):
        return "legwear_footwear", "helmet_protective"

    if (name.startswith("hat_") or "_hat_" in name or name.endswith(("_hat", "_cap"))) and not any_prefix(name, ("hand_", "no_", "missing_")):
        return "accessories", "headwear"
    if any_suffix(name, ("_mask", "_glasses", "_eyewear", "_goggles", "_eyepatch", "_blindfold")):
        return "accessories", "eyewear"
    if any_suffix(name, ("_gloves", "_mittens", "_gauntlets")):
        return "accessories", "handwear"
    if any_suffix(name, ("_earrings", "_necklace", "_bracelet", "_choker", "_brooch", "_anklet")):
        return "accessories", "jewelry"

    if any_suffix(name, ("_shirt", "_blouse", "_sweater", "_hoodie", "_camisole", "_vest", "_jersey")):
        return "clothes_main", "tops"
    if any_suffix(name, ("_shorts", "_pants", "_trousers", "_jeans", "_culottes")) or name == "sweatpants":
        return "clothes_main", "bottoms"
    if any_suffix(name, ("_skirt",)):
        return "clothes_main", "skirt"
    if any_suffix(name, ("_dress", "_gown")):
        return "clothes_main", "dress"
    if any_suffix(name, ("_coat", "_jacket", "_cloak", "_cape", "_cardigan", "_blazer", "_poncho")):
        return "clothes_main", "outerwear"
    if any_suffix(name, ("_suit", "_jumpsuit", "_romper", "_overalls")):
        return "clothes_main", "suit"

    if name.endswith("_bun"):
        return "hair", "hair_style"

    if name.startswith("stuffed_") or token & {"plush", "plushie", "stuffed_toy", "figurine", "action_figure"}:
        return "transport_play", "toys"

    # Food nouns, weapon nouns and device nouns likewise outrank decorative or
    # calendar modifiers that happen to occur earlier in a compound.
    if name.endswith("_(food)") and token & {"meat", "beef", "pork", "chicken", "egg", "fish", "seafood"}:
        return "food_drink", "meat_seafood"
    if head in {"cake", "shortcake", "cookie", "candy", "chocolate", "ice", "dessert", "pudding", "parfait", "donut", "doughnut", "lollipop", "pancake", "gingerbread"}:
        return "food_drink", "dessert_snack"
    if base_name in {"pineapple", "apple", "banana", "orange", "strawberry", "cherry", "grape", "watermelon", "peach", "lemon", "tomato", "carrot"} or name.endswith("_(fruit)"):
        return "food_drink", "fruit_vegetable"
    if head in {"steak", "meat", "beef", "pork", "sausage", "bacon"}:
        return "food_drink", "meat_seafood"
    if head in {"bread", "rice", "noodles", "ramen", "soup", "pizza", "sandwich", "pasta", "curry", "bento"}:
        return "food_drink", "staple_food"

    if "finger" in token and "gun" in token:
        return "pose", "hand_gesture"
    if head in {"gun", "rifle", "pistol", "revolver", "shotgun", "firearm", "machinegun", "cannon"}:
        return "weapons", "firearm"
    if head in {"sword", "katana", "knife", "dagger", "blade", "saber", "rapier", "scimitar", "machete", "axe"}:
        return "weapons", "blade"
    if name in {"arrow", "bow_(weapon)", "bow_and_arrow"} or token & {"crossbow", "longbow", "yumi", "quiver"}:
        return "weapons", "bow"

    if head in {"computer", "laptop", "smartphone", "cellphone", "keyboard", "monitor", "console", "controller", "3ds"}:
        return "culture_objects", "phone_computer"
    if head in {"volleyball", "basketball", "baseball", "soccer", "tennis", "racket", "surfboard", "skateboard"}:
        return "transport_play", "sports"
    animal_person = token & {"cat", "dog", "wolf", "fox", "rabbit", "bunny", "bear", "horse", "cow", "sheep", "goat", "mouse", "rat", "squirrel", "deer", "lion", "tiger", "leopard", "jaguar", "hyena", "zebra", "monkey", "ape", "pig", "elephant", "giraffe", "shark", "fish", "whale", "dolphin", "octopus", "squid", "jellyfish", "crab", "bird", "owl", "penguin", "duck", "chicken", "parrot", "snake", "lizard", "turtle", "tortoise", "crocodile", "alligator", "frog", "reptile", "spider", "scorpion", "centipede", "arthropod", "moth", "butterfly", "bee", "ant", "insect", "plant", "mushroom", "dragon", "monster", "demon", "angel", "fairy", "mermaid", "vampire", "werewolf", "slime", "zombie", "undead", "ghost", "centaur", "harpy", "griffin", "phoenix", "unicorn", "jackalope", "alien"}
    if animal_person and re.search(r"_(girl|boy|woman|man)$", name):
        return "people", "fantasy_person"

    if re.fullmatch(r"(18|19|20)\d0s_\(style\)", name):
        return "style", "era_style"

    # Meta, screen and textual concepts are checked early to prevent words such
    # as "shot" in screenshot or "character" in character_name from leaking.
    if any_fragment(name, ("cosplay", "costume_swap", "clothes_swap", "outfit_swap", "role_reversal", "crossover", "alternate_costume", "alternate_hairstyle", "personification")):
        return "text_meta", "cosplay"
    if any_fragment(name, ("meme", "parody", "reference", "spoof", "reaction_image", "image_macro", "what_if", "4koma", "yonkoma")):
        return "text_meta", "meme"
    if any_fragment(base_name, ("screenshot", "interface", "hud", "cursor", "webpage", "browser", "video_player", "gameplay_mechanics")) or token & {"screen", "ui"}:
        return "text_meta", "screen_ui"
    if any_fragment(name, ("speech_bubble", "thought_bubble", "narration", "comic", "panel", "sound_effects", "onomatopoeia")) or name.startswith("spoken_"):
        return "text_meta", "comic"
    if any_suffix(name, ("_text", "_language", "_caption", "_subtitle", "_writing")) or token & {"text", "letter", "word", "typography", "kanji", "hiragana", "katakana"}:
        return "text_meta", "text"
    if any_suffix(base_name, ("_symbol", "_logo", "_flag", "_emblem", "_sign")) or token & {"symbol", "logo", "flag", "emblem", "watermark", "barcode", "qr", "icon"}:
        return "text_meta", "symbol"
    if any_fragment(name, ("official_art", "artist_name", "character_name", "copyright_name", "commission", "revision", "bad_id", "commentary", "sample_watermark", "third-party_edit", "tagme", "translation_request", "source_request", "paid_reward", "variant_set", "drawing_challenge")) or name.endswith("_username"):
        return "text_meta", "meta"

    # Camera and composition.
    if name in {"close-up", "portrait", "bust", "upper_body", "cowboy_shot", "full_body", "wide_shot", "very_wide_shot", "from_afar", "extreme_close-up"}:
        return "composition", "shot"
    if name in {"from_above", "from_below", "from_side", "from_behind", "from_front", "dutch_angle", "fisheye", "wide_angle", "aerial_view", "bird's_eye_view", "worm's_eye_view", "over_shoulder", "low_angle", "high_angle"} or any_fragment(name, ("camera_angle", "perspective_view")):
        return "composition", "camera_angle"
    if name in {"symmetrical", "asymmetrical", "centered", "off-center", "diagonal", "split_screen", "multiple_views", "panorama"} or any_fragment(name, ("composition", "rule_of_thirds", "visual_balance", "vanishing_point")):
        return "composition", "layout"
    if any_fragment(name, ("depth_of_field", "focus", "focused", "blurry", "blur", "bokeh", "zoom_layer")):
        return "composition", "focus"
    if name in {"cropped", "framed", "frame", "border", "foreground", "obscured", "partially_visible", "cut_off"} or any_fragment(name, ("out_of_frame", "image_border", "decorative_border")):
        return "composition", "framing"
    if name in {"pov", "viewfinder", "security_camera", "surveillance", "drone_view", "selfie"} or any_fragment(name, ("first-person_view", "first_person_view")):
        return "composition", "viewpoint"

    # Art medium, style and rendering.
    if any_fragment(name, ("watercolor", "oil_paint", "colored_pencil", "traditional_media", "digital_art", "pixel_art", "paper_cut")) or token & {"gouache", "acrylic", "graphite", "charcoal", "ink", "marker", "pastel", "crayon", "chalk", "woodcut", "linocut"}:
        return "style", "medium"
    if any_fragment(name, ("lineart", "sketch", "shading", "hatching", "crosshatching", "stippling", "flat_color", "cel_shading", "impasto", "brushstroke", "coloring", "outline", "unfinished")):
        return "style", "technique"
    if any_fragment(name, ("artstyle", "art_style", "impressionism", "expressionism", "surreal", "minimalis", "art_nouveau", "art_deco", "pop_art", "ukiyo-e", "cubism", "baroque", "rococo", "realistic", "oekaki")) or name.endswith("_style"):
        return "style", "art_style"
    if any_fragment(name, ("cyberpunk", "steampunk", "dieselpunk", "gothic", "fantasy", "sci-fi", "science_fiction", "noir", "horror", "western", "vaporwave", "synthwave")):
        return "style", "genre"
    if any_fragment(name, ("retro", "vintage", "1980s", "1990s", "2000s", "old_school", "modern", "historical")):
        return "style", "era_style"
    if name.endswith("_(style)"):
        return "style", "art_style"
    if any_fragment(name, ("highres", "absurdres", "lowres", "resolution", "highly_detailed", "detailed", "intricate", "sharp_focus", "quality", "wallpaper", "key_visual")):
        return "style", "quality"
    if any_fragment(name, ("3d", "cgi", "render", "photograph", "photo_", "photoreal", "animation", "animated", "stop_motion", "claymation", "live_action")):
        return "style", "photo_3d"

    # Light, palette and visual effects.
    if any_fragment(name, ("backlight", "rim_light", "neon_light", "light_rays", "sunbeam", "chiaroscuro")) or token & {"lighting", "sunlight", "moonlight", "candlelight", "spotlight", "shadow", "shadows"}:
        return "light_effect", "lighting"
    if any_fragment(name, ("palette", "monochrome", "greyscale", "sepia", "colorful", "pastel_colors", "vibrant_colors", "muted_colors", "warm_colors", "cool_colors")) or name.endswith("_theme"):
        return "light_effect", "palette"
    if any_fragment(name, ("explosion",)) or token & {"fire", "flame", "flames", "smoke", "steam", "burning", "embers", "ash", "ashes"}:
        return "light_effect", "fire_smoke"
    if any_fragment(name, ("sparkle", "particle", "floating_dust", "glitter", "confetti", "petals", "snowflakes", "light_particles", "lens_dust")):
        return "light_effect", "particles"
    if any_fragment(name, ("lens_flare", "chromatic_aberration", "film_grain", "vignet", "motion_blur", "afterimage", "glitch", "scanlines", "distortion")):
        return "light_effect", "optical"
    magic_tokens = {"aura", "electricity", "glowing", "glow", "halo", "summoning"}
    energy_effect = bool(re.search(r"(^|_)energy_(aura|ball|beam|blast|burst|field|glow|light|particles|wave)($|_)", base_name))
    power_effect = bool(re.search(r"(^|_)power_(aura|beam|blast|effect|glow|light|wave)($|_)", base_name))
    if any_fragment(base_name, ("magic_circle", "lightning_effect", "magic_effect")) or token & magic_tokens or energy_effect or power_effect:
        return "light_effect", "magic_effect"
    if any_suffix(name, ("_effect", "_effects")):
        return "light_effect", "other_effect"

    # Weather, time and calendar.
    if name in {"rain", "raining", "snow", "snowing", "wind", "windy", "storm", "fog", "mist", "hail", "cloudy", "sunny", "overcast", "thunder", "tornado", "hurricane"} or name.endswith("_weather"):
        return "time_weather", "weather"
    if name in {"day", "night", "morning", "afternoon", "evening", "dawn", "dusk", "sunrise", "sunset", "twilight", "midnight", "noon", "daytime", "nighttime"}:
        return "time_weather", "time_day"
    if name in {"spring_(season)", "summer", "autumn", "fall_(season)", "winter", "season"}:
        return "time_weather", "season"
    if token & {"christmas", "halloween", "valentine", "easter", "festival", "birthday", "anniversary", "tanabata", "thanksgiving"} or "new_year" in name or "white_day" in name:
        return "time_weather", "holiday"
    if re.fullmatch(r"(18|19|20)\d{2}", name) or re.search(r"(^|_)(18|19|20)\d0s?($|_)", name) or token & {"century", "era", "calendar", "date"}:
        return "time_weather", "calendar"

    if base_name.startswith(("robot_", "robotic_", "mechanical_")) and head in {
        "cat", "dog", "wolf", "fox", "rabbit", "bear", "tiger", "lion", "bird", "fish", "shark",
        "dragon", "dinosaur", "spider", "scorpion", "snake",
    }:
        return "mech_scifi", "robot_android"
    if base_name.startswith(("inflatable_", "rubber_", "toy_", "model_", "rocking_", "wooden_")) and head in {
        "cat", "dog", "wolf", "fox", "rabbit", "bear", "tiger", "lion", "bird", "fish", "shark",
        "dragon", "dinosaur", "horse", "duck", "chicken", "frog", "snake",
    }:
        return "transport_play", "toys"

    # Strong creature heads precede environment modifiers (sea, garden,
    # mountain).  Conversely a creature word used as a modifier in cat_costume,
    # tiger_print or robot_dog must not turn the object into an animal.
    mammal_heads = {"cat", "dog", "wolf", "fox", "rabbit", "bunny", "bear", "horse", "cow", "sheep", "goat", "pig", "mouse", "rat", "deer", "lion", "tiger", "leopard", "monkey", "ape", "elephant", "giraffe", "squirrel", "otter", "seal"}
    bird_heads = {"bird", "eagle", "hawk", "owl", "crow", "raven", "sparrow", "pigeon", "duck", "goose", "swan", "chicken", "penguin", "parrot", "heron"}
    aquatic_heads = {"fish", "shark", "whale", "dolphin", "octopus", "squid", "jellyfish", "crab", "lobster", "shrimp", "seahorse", "eel", "urchin", "anemone", "slug", "sunfish"}
    insect_heads = {"butterfly", "moth", "bee", "wasp", "ant", "beetle", "spider", "scorpion", "dragonfly", "insect", "bug", "centipede"}
    reptile_heads = {"snake", "lizard", "turtle", "tortoise", "crocodile", "alligator", "frog", "toad", "salamander", "reptile", "dinosaur"}
    fantasy_heads = {"dragon", "demon", "angel", "fairy", "mermaid", "vampire", "werewolf", "monster", "ghost", "spirit", "slime", "zombie", "undead", "centaur", "harpy", "griffin", "phoenix", "alien", "elemental"}
    plant_heads = {"flower", "flowers", "rose", "lily", "sunflower", "tree", "grass", "leaf", "leaves", "plant", "vine", "bamboo", "cactus", "mushroom", "blossom", "blossoms", "camellia"}
    if head in mammal_heads or name.endswith("_(mammal)"):
        return "creatures", "mammal"
    if head in bird_heads or name.endswith("_(bird)"):
        return "creatures", "bird"
    if head in aquatic_heads or name.endswith("_(fish)"):
        return "creatures", "aquatic"
    if head in insect_heads or name.endswith("_(insect)"):
        return "creatures", "insect"
    if head in reptile_heads or name.endswith("_(reptile)"):
        return "creatures", "reptile"
    if head in fantasy_heads:
        return "creatures", "fantasy_creature"
    if head in plant_heads or name.endswith(("_(flower)", "_(plant)", "_(tree)")):
        return "creatures", "plant"

    # Environments and backgrounds.
    if any_fragment(name, ("bedroom", "bathroom", "living_room", "kitchen", "dining_room", "hallway", "attic", "basement", "home_interior")):
        return "indoor_scene", "home_room"
    if name in {"classroom", "library", "office", "hospital", "laboratory", "gym", "indoors", "interior"} or name.endswith(("_interior", "_room")):
        return "indoor_scene", "public_indoor"
    if name == "bar_(place)" or "shopping_mall" in name or token & {"restaurant", "cafe", "shop", "store", "hotel", "theater", "cinema", "arcade"}:
        return "indoor_scene", "commercial"
    if any_fragment(name, ("shopping_mall", "parking_lot")) or token & {"city", "street", "alley", "crosswalk", "sidewalk", "market", "station", "airport", "harbor", "urban"}:
        return "indoor_scene", "urban"
    if token & {"building", "castle", "palace", "temple", "shrine", "church", "tower", "bridge", "ruins", "monument", "skyscraper", "house", "architecture"}:
        return "indoor_scene", "architecture"
    if token & {"forest", "woods", "field", "meadow", "grassland", "jungle", "garden", "park", "orchard", "outdoors"}:
        return "outdoor_scene", "forest_field"
    if token & {"mountain", "hill", "desert", "canyon", "cave", "cliff", "rocky", "volcano", "dune"}:
        return "outdoor_scene", "mountain_desert"
    if token & {"ocean", "sea", "beach", "river", "lake", "pond", "waterfall", "shore", "underwater", "waterside", "pool"}:
        return "outdoor_scene", "water_scene"
    if name in {"sky", "cloud", "clouds", "space", "outer_space", "universe", "galaxy", "planet", "moon", "sun", "stars", "nebula"} or any_suffix(name, ("_sky", "_clouds", "_galaxy", "_planet")):
        return "outdoor_scene", "sky_space"
    if any_fragment(name, ("simple_background", "plain_background", "white_background", "black_background", "transparent_background", "gradient_background")):
        return "outdoor_scene", "background_plain"
    if name.endswith("_background") or token & {"background", "backdrop"}:
        return "outdoor_scene", "background_pattern"
    if token & {"floor", "ground", "wall", "ceiling", "pavement", "tiles", "surface", "tabletop"} and not token & {"hair", "dress", "skirt", "coat"}:
        return "indoor_scene", "surface"
    if any_suffix(name, ("_place", "_location", "_park", "_garden")):
        return "outdoor_scene", "other_scene"

    # Creatures and plants.
    if any_suffix(base_name, ("_ears", "_tail", "_tails", "_wings", "_horns", "_antlers", "_antennae", "_claws", "_fins", "_whiskers", "_feather", "_feathers", "_fur", "_scales")) or any_fragment(base_name, ("animal_ears", "kemonomimi", "paw_pose", "animal_hands", "animal_feet")):
        return "creatures", "animal_feature"
    if head in mammal_heads:
        return "creatures", "mammal"
    if head in bird_heads:
        return "creatures", "bird"
    if head in aquatic_heads:
        return "creatures", "aquatic"
    if head in insect_heads:
        return "creatures", "insect"
    if head in reptile_heads:
        return "creatures", "reptile"
    if head in fantasy_heads:
        return "creatures", "fantasy_creature"
    if head in plant_heads or any_suffix(base_name, ("_flower", "_plant", "_tree")):
        return "creatures", "plant"
    if any_suffix(name, ("_animal", "_creature")):
        return "creatures", "other_creature"

    # Holding is an action even when the held object has a strong noun.
    if any_prefix(name, ("holding_", "carrying_", "grabbing_", "gripping_", "wielding_")):
        return "action", "holding"
    if any_prefix(base_name, ("looking_", "facing_")) or base_name in {"head_tilt", "head_back", "head_down", "head_up", "head_turn", "head_turned", "head_turned_away"} or any_fragment(base_name, ("eye_contact",)) or token & {"gaze", "staring"}:
        return "pose", "gaze"
    if token & {"standing", "sitting", "kneeling", "lying", "squatting", "crouching", "seiza"}:
        return "pose", "stationary_pose"
    if any_fragment(name, ("hand_on_", "hands_on_", "finger_", "peace_sign", "thumbs_up", "waving", "salute", "heart_hands", "pointing", "arms_crossed", "arms_up", "clenched_hand", "covering_privates")):
        return "pose", "hand_gesture"
    if token & {"walking", "running", "jumping", "falling", "flying", "swimming", "climbing", "dancing", "spinning", "skating", "skiing", "riding"}:
        return "action", "movement"
    if any_fragment(name, ("fighting", "punch", "kick", "attack", "aiming", "shooting", "sword_fighting", "combat", "dodging", "blocking", "parrying")):
        return "action", "combat_action"
    if token & {"hug", "hugs"} or any_fragment(name, ("holding_hands", "handshake", "head_pat", "piggyback", "princess_carry", "facing_another", "back-to-back", "high_five", "whispering", "talking_to", "restrained")):
        return "action", "interaction"
    if token & {"eating", "drinking", "cooking", "reading", "writing", "sleeping", "yawning", "stretching", "singing", "shopping", "cleaning", "studying", "working", "bathing"}:
        return "action", "daily_action"
    if any_suffix(name, ("_pose", "_stance", "_posture")) or any_fragment(name, ("leaning", "bent_over", "arched_back", "contrapposto", "spread_legs", "crossed_legs")):
        return "pose", "body_pose"

    # Hair before face/body avoids tags such as hair_over_one_eye.
    if name.endswith("_hair") and (token & COLORS or any_fragment(name, ("two-tone_hair", "multicolored_hair", "colored_inner_hair", "split-color_hair", "gradient_hair", "streaked_hair", "colored_tips"))):
        return "hair", "hair_color"
    if any_fragment(name, ("very_short_hair", "short_hair", "medium_hair", "long_hair", "very_long_hair", "absurdly_long_hair", "shoulder-length_hair")):
        return "hair", "hair_length"
    if any_fragment(name, ("bangs", "sidelocks", "hair_between_eyes", "hairline", "widow's_peak", "forehead")):
        return "hair", "bangs"
    if any_fragment(name, ("hair_ribbon", "hair_bow", "hairclip", "hair_ornament", "hair_flower", "hairpin", "hairband", "scrunchie", "hair_tubes", "hair_bobbles", "hair_rings", "hair_beads", "hair_tie")):
        return "accessories", "hair_accessory"
    if any_fragment(name, ("ponytail", "twintails", "braid", "hair_bun", "side_bun", "updo", "drill_hair", "drills", "bob_cut", "hime_cut", "pixie_cut", "wavy_hair", "curly_hair", "straight_hair", "spiked_hair", "dreadlocks", "mohawk", "afro")):
        return "hair", "hair_style"
    hair_state_words = {
        "floating", "messy", "wet", "adjusting", "tying", "tied", "tucking", "twirling", "brushing",
        "drying", "cutting", "washing", "ruffling", "flowing", "windblown", "disheveled", "combing",
        "pulling", "grabbing", "holding", "hairdressing", "loose", "untied",
    }
    if "hair" in token and token & hair_state_words:
        return "hair", "hair_action"

    # Facial features and expression.
    if name.endswith("_eyes") and token & COLORS:
        return "face", "eye_color"
    if any_fragment(name, ("eyes", "eye_", "pupil", "iris", "sclera", "eyelash", "eyelid", "heterochromia", "tareme", "tsurime", "jitome", "sanpaku")):
        return "face", "eye_shape"
    if token & {"eyebrows", "eyebrow"}:
        return "face", "eyebrows"
    if token & {"nose", "nostril"}:
        return "face", "nose"
    if token & {"mouth", "lips", "lip", "tongue", "teeth", "tooth", "fang", "saliva"} or any_suffix(name, ("_mouth", "_lips", "_teeth")):
        return "face", "mouth"
    if "ear" in token or "ears" in token or name.endswith("_ear"):
        return "face", "ears"
    if any_fragment(name, ("makeup", "eyeshadow", "eyeliner", "mascara", "lipstick", "facepaint", "facial_mark", "beauty_mark", "freckles", "mole_on_face", "rouge")):
        return "face", "makeup"
    if token & {"smile", "smiles", "smiling", "grin", "grinning", "laugh", "laughing", "happiness", "excited", "excitement", "playful", "smug"} or name in {"happy", "happy_tears"}:
        return "expression", "positive"
    if token & {"cry", "cries", "crying", "tears", "tearful", "sad", "sadness", "sorrow", "sorrowful", "depressed", "depression", "lonely", "loneliness", "gloom", "gloomy", "unhappy"}:
        return "expression", "sad_cry"
    if token & {"angry", "anger", "annoyed", "annoyance", "frown", "frowning", "disgust", "disgusted", "scowl", "scowling", "pout", "pouting", "frustrated", "frustration"}:
        return "expression", "anger"
    if token & {"scared", "fear", "fearful", "afraid", "surprised", "surprise", "shocked", "nervous", "worried", "worry", "panic", "panicked", "confused", "confusion"} or name in {"shock", "in_shock"}:
        return "expression", "fear_surprise"
    if token & {"blush", "blushing", "shy", "shyness", "embarrassed", "embarrassment", "flustered"}:
        return "expression", "shy_blush"
    if name.endswith("_expression") or token & {"expressionless", "serious", "sleepy", "drunk", "crazy", "ahegao"}:
        return "expression", "neutral_expression"

    # Clothing and accessories use endings because Danbooru color/pattern
    # variants retain the garment as their final token.
    if any_fragment(name, ("school_uniform", "serafuku", "sailor_uniform", "gym_uniform", "student_uniform")):
        return "clothes_special", "school_uniform"
    if any_suffix(name, ("_uniform",)) or name in {"uniform", "maid", "nurse", "waitress", "cheerleader", "police", "military", "chef", "pilot"}:
        return "clothes_special", "occupation_uniform"
    if any_suffix(name, ("_kimono", "_yukata", "_hanfu", "_hanbok", "_cheongsam", "_hakama")) or token & {"kimono", "yukata", "hanfu", "hanbok", "cheongsam", "hakama", "haori", "obi", "miko"}:
        return "clothes_special", "traditional_east"
    if any_suffix(name, ("_sari", "_dirndl", "_kilt", "_toga", "_kaftan")) or token & {"sari", "dirndl", "kilt", "toga", "kaftan", "ethnic_clothes", "historical_clothes"}:
        return "clothes_special", "traditional_world"
    if token & {"pajamas", "pyjamas", "nightgown", "sleepwear", "loungewear", "casual", "robe", "bathrobe"}:
        return "clothes_special", "sleep_casual"
    if token & {"magical_girl", "stage_clothes", "idol_clothes", "fantasy_clothes", "lolita_fashion", "gothic_lolita", "costume"}:
        return "clothes_special", "themed_costume"
    garment_top = name.endswith("_top") and not name.endswith("_on_top")
    if garment_top or any_suffix(name, ("_shirt", "_blouse", "_sweater", "_hoodie", "_camisole", "_vest", "_jersey")) or token & {"shirt", "blouse", "sweater", "hoodie", "camisole"}:
        return "clothes_main", "tops"
    if any_suffix(name, ("_shorts", "_pants", "_trousers", "_jeans", "_culottes")) or token & {"shorts", "pants", "trousers", "jeans", "culottes", "bloomers"}:
        return "clothes_main", "bottoms"
    if any_suffix(name, ("_skirt",)) or token & {"skirt", "miniskirt", "overskirt", "petticoat"}:
        return "clothes_main", "skirt"
    if any_suffix(name, ("_dress", "_gown")) or token & {"dress", "gown", "sundress"}:
        return "clothes_main", "dress"
    if any_suffix(name, ("_coat", "_jacket", "_cloak", "_cape", "_cardigan", "_blazer", "_poncho")) or token & {"coat", "jacket", "cloak", "cape", "cardigan", "blazer"}:
        return "clothes_main", "outerwear"
    if any_suffix(name, ("_suit", "_jumpsuit", "_romper", "_overalls")) or token & {"suit", "jumpsuit", "romper", "overalls"}:
        return "clothes_main", "suit"
    if any_suffix(name, ("_bra", "_lingerie", "_bandeau")) or token & {"bra", "lingerie", "bralette", "bandeau"}:
        return "underwear_swim", "bra_lingerie"
    if any_suffix(name, ("_panties", "_underwear", "_thong")) or token & {"panties", "underwear", "thong", "loincloth"}:
        return "underwear_swim", "panties_underwear"
    if any_suffix(name, ("_swimsuit", "_bikini", "_swimwear")) or token & {"swimsuit", "bikini", "swimwear"}:
        return "underwear_swim", "swimsuit"
    if any_suffix(name, ("_leotard", "_bodysuit", "_unitard")) or token & {"leotard", "bodysuit", "unitard", "catsuit"}:
        return "underwear_swim", "bodysuit_leotard"
    if re.search(r"(^|_)(bra|panties|bikini|swimsuit|underwear|lingerie)_", name):
        return "underwear_swim", "underwear_design"
    if any_suffix(name, ("_socks",)) or token & {"socks", "ankle_socks", "crew_socks"}:
        return "legwear_footwear", "socks"
    if any_suffix(name, ("_thighhighs", "_kneehighs", "_pantyhose", "_stockings", "_leggings", "_legwear")) or token & {"thighhighs", "kneehighs", "pantyhose", "stockings", "leggings", "legwear"}:
        return "legwear_footwear", "stockings"
    if any_suffix(name, ("_boots",)) or token & {"boots", "boot", "waders"}:
        return "legwear_footwear", "boots"
    if any_suffix(name, ("_shoes", "_sandals", "_heels", "_loafers", "_sneakers", "_slippers", "_footwear")) or token & {"shoes", "sandals", "heels", "loafers", "sneakers", "footwear", "barefoot", "slippers"}:
        return "legwear_footwear", "shoes"
    if any_suffix(name, ("_armor", "_armour")) or token & {"armor", "armour", "chainmail", "breastplate", "pauldrons", "gauntlets"}:
        return "legwear_footwear", "armor"
    if any_suffix(name, ("_helmet", "_wetsuit", "_hazmat_suit")) or token & {"helmet", "wetsuit", "hazmat", "protective_suit"}:
        return "legwear_footwear", "helmet_protective"
    if any_fragment(name, ("torn_clothes", "wet_clothes", "open_clothes", "clothes_pull", "clothes_lift", "clothes_aside", "undressing", "dressing", "unworn_", "partially_unbuttoned", "wardrobe_")):
        return "clothing_detail", "clothing_state"
    if token & COLORS and token & {"clothes", "clothing", "sleeves", "trim", "collar", "outfit"}:
        return "clothing_detail", "clothing_color"
    pattern_words = {"striped", "plaid", "checkered", "polka", "floral", "print", "pattern", "camouflage"}
    if token & pattern_words and (token & garment_words or base_name in pattern_words or head in {"print", "pattern", "camouflage", "fabric", "clothes", "clothing", "outfit", "trim"}):
        return "clothing_detail", "clothing_pattern"
    material_words = {"lace", "silk", "satin", "leather", "denim", "latex", "fur", "transparent", "velvet", "cotton", "wool", "spandex"}
    if token & material_words and (token & garment_words or base_name in material_words or head in {"fabric", "clothes", "clothing", "outfit", "trim", "material"}):
        return "clothing_detail", "clothing_material"
    if token & {"sleeves", "sleeve", "collar", "buttons", "button", "zipper", "pocket", "lapels", "straps", "strap", "frills", "frilled", "hem", "seams", "cutout"}:
        return "clothing_detail", "clothing_structure"
    if any_suffix(name, ("_clothes", "_clothing", "_outfit", "_costume", "_suit", "_sleeves")):
        return "clothing_detail", "other_clothes"

    if any_suffix(name, ("_hat", "_cap", "_crown", "_tiara", "_hood", "_headdress", "_headwear", "_helmet")) or token & {"hat", "cap", "crown", "tiara", "headwear"}:
        return "accessories", "headwear"
    if any_suffix(name, ("_glasses", "_eyewear", "_goggles", "_mask", "_eyepatch", "_blindfold")) or token & {"glasses", "eyewear", "goggles", "monocle", "eyepatch", "mask", "blindfold"}:
        return "accessories", "eyewear"
    if any_suffix(name, ("_earrings", "_necklace", "_bracelet", "_anklet", "_ring", "_piercing", "_jewelry", "_brooch")) or token & {"earrings", "necklace", "bracelet", "anklet", "jewelry", "piercing", "brooch"}:
        return "accessories", "jewelry"
    if any_suffix(name, ("_tie", "_necktie", "_bowtie", "_scarf", "_choker", "_collar")) or token & {"necktie", "bowtie", "scarf", "choker"}:
        return "accessories", "neckwear"
    if any_suffix(name, ("_gloves", "_mittens", "_wristband", "_cuff", "_armband")) or token & {"gloves", "mittens", "wristband", "cuff", "armband"}:
        return "accessories", "handwear"
    if any_suffix(name, ("_bag", "_purse", "_backpack", "_belt", "_pouch", "_holster")) or token & {"bag", "purse", "backpack", "belt", "pouch", "holster"}:
        return "accessories", "bags_belts"
    if any_suffix(name, ("_ribbon", "_bow", "_badge", "_ornament", "_decoration")) or token & {"ribbon", "badge", "ornament"}:
        return "accessories", "badges_ornaments"
    if any_suffix(name, ("_accessory", "_accessories")):
        return "accessories", "other_accessory"

    # Mechanical and science-fiction concepts.
    if token & {"robot", "android", "automaton", "humanoid_robot", "robot_girl", "robot_boy"}:
        return "mech_scifi", "robot_android"
    if token & {"mecha", "mech", "mobile_suit", "power_armor", "giant_robot"}:
        return "mech_scifi", "mecha"
    if any_fragment(name, ("cyborg", "cybernetic", "prosthetic", "mechanical_arm", "mechanical_leg", "artificial_limb", "bionic")):
        return "mech_scifi", "cybernetic"
    if token & {"machine", "machinery", "gear", "gears", "engine", "motor", "industrial", "factory", "mechanism", "mechanical"}:
        return "mech_scifi", "machine"
    if any_fragment(name, ("hologram", "sci-fi_device", "futuristic_device", "teleporter", "cryopod", "energy_core", "force_field")):
        return "mech_scifi", "scifi_device"

    # Weapons before generic objects.
    if head in {"sword", "katana", "knife", "dagger", "blade", "saber", "rapier", "scimitar", "machete", "axe"}:
        return "weapons", "blade"
    if head in {"gun", "rifle", "pistol", "revolver", "shotgun", "firearm", "machinegun", "cannon"}:
        return "weapons", "firearm"
    if name in {"arrow", "bow_(weapon)", "bow_and_arrow"} or token & {"crossbow", "longbow", "yumi", "quiver"}:
        return "weapons", "bow"
    if head in {"spear", "lance", "halberd", "staff", "club", "hammer", "mace", "flail", "whip", "polearm"}:
        return "weapons", "polearm"
    if any_fragment(name, ("magic_weapon", "energy_sword", "lightsaber", "wand", "magic_staff", "holy_sword", "demon_weapon")):
        return "weapons", "magic_weapon"
    if head in {"bomb", "grenade", "missile", "rocket", "torpedo", "explosive", "mine"}:
        return "weapons", "explosive"
    if head in {"shield", "buckler", "barrier"}:
        return "weapons", "shield"
    if name.endswith("_weapon") or "weapon" in token:
        return "weapons", "other_weapon"

    # Food and drinks.
    if head in {"meat", "beef", "pork", "chicken", "egg", "eggs", "fish", "seafood", "sausage", "bacon"}:
        return "food_drink", "meat_seafood"
    if head in {"cake", "cookie", "candy", "chocolate", "dessert", "pudding", "donut", "doughnut", "lollipop", "snack"}:
        return "food_drink", "dessert_snack"
    if head in {"fruit", "vegetable", "apple", "banana", "orange", "strawberry", "cherry", "grape", "watermelon", "peach", "lemon", "tomato", "carrot"}:
        return "food_drink", "fruit_vegetable"
    if head in {"food", "bread", "rice", "noodles", "ramen", "soup", "pizza", "sandwich", "pasta", "curry", "meal", "bento"} or base_name.endswith("_food"):
        return "food_drink", "staple_food"
    if head in {"drink", "water", "tea", "coffee", "juice", "soda", "beer", "wine", "milk", "alcohol", "cocktail"}:
        return "food_drink", "drink"
    if head in {"cup", "mug", "bottle", "plate", "bowl", "fork", "spoon", "chopsticks", "tableware", "teacup", "teapot"} or base_name in {"glass", "drinking_glass", "wine_glass", "cocktail_glass", "shot_glass", "champagne_glass"}:
        return "food_drink", "tableware"

    # Electronic, printed and musical objects.
    if head in {"phone", "smartphone", "cellphone", "computer", "laptop", "tablet", "controller", "console", "keyboard", "monitor"}:
        return "culture_objects", "phone_computer"
    if head in {"camera", "television", "tv", "radio", "headphones", "headset", "microphone", "projector", "speaker", "video_camera"}:
        return "culture_objects", "camera_media"
    if head in {"book", "magazine", "newspaper", "paper", "notebook", "letter", "scroll", "poster", "pamphlet"}:
        return "culture_objects", "books_paper"
    if head in {"pen", "pencil", "brush", "eraser", "stationery", "ruler", "crayon", "marker", "paintbrush", "inkwell"}:
        return "culture_objects", "stationery"
    if head in {"guitar", "piano", "violin", "drum", "flute", "trumpet", "saxophone", "harp", "instrument", "music", "turntable"}:
        return "culture_objects", "music"

    # Household objects.
    if head in {"chair", "table", "desk", "bed", "sofa", "couch", "bench", "stool"}:
        return "household_objects", "seating_table"
    if head in {"shelf", "cabinet", "furniture", "mirror", "wardrobe", "dresser", "bookcase", "curtains", "pillow", "blanket"}:
        return "household_objects", "storage_furniture"
    if head in {"lamp", "lantern", "clock", "fan", "heater", "conditioner", "refrigerator", "oven", "television"}:
        return "household_objects", "lighting_clock"
    if head in {"tool", "screwdriver", "scissors", "rope", "towel", "soap", "toothbrush", "comb", "key", "lock", "umbrella", "broom", "mop", "tray"}:
        return "household_objects", "tools"
    if head in {"box", "jar", "can", "basket", "bucket", "container", "package", "bag", "bowl", "plate"}:
        return "household_objects", "container"
    if name.endswith("_object") or "object" in token:
        return "household_objects", "other_object"

    # Vehicles, sports, games and toys.
    if head in {"car", "truck", "bus", "train", "bicycle", "motorcycle", "vehicle", "tank", "tram", "scooter"}:
        return "transport_play", "land_vehicle"
    if head in {"airplane", "aircraft", "helicopter", "jet", "rocket", "spaceship", "glider"}:
        return "transport_play", "air_vehicle"
    if head in {"ship", "boat", "submarine", "yacht", "canoe", "kayak", "sailboat"}:
        return "transport_play", "water_vehicle"
    if head in {"ball", "racket", "bat", "skateboard", "surfboard", "sports", "sport", "soccer", "baseball", "basketball", "tennis"}:
        return "transport_play", "sports"
    if head in {"game", "card", "cards", "dice", "chess", "mahjong", "controller", "board_game"}:
        return "transport_play", "games"
    if head in {"toy", "doll", "plush", "plushie", "figurine", "figure"}:
        return "transport_play", "toys"

    # Body and people. These are later so clothing/pose compounds win.
    if any_fragment(name, ("1girl", "1boy", "2girls", "2boys", "3girls", "3boys", "multiple_girls", "multiple_boys", "solo", "group", "crowd", "male_focus", "female_focus", "androgynous")):
        return "people", "count_gender"
    age_words = {"baby", "child", "children", "teenage", "young", "adult", "mature", "elderly", "old", "shota", "loli"}
    person_words = {"girl", "girls", "boy", "boys", "woman", "women", "man", "men", "lady", "ladies", "person", "people", "male", "female"}
    if base_name in age_words or (token & age_words and token & person_words):
        return "people", "age"
    if token & {"couple", "family", "siblings", "sisters", "brothers", "twins", "mother", "father", "daughter", "son", "friends", "rivals"}:
        return "people", "relationship"
    if token & {"teacher", "student", "doctor", "nurse", "police", "soldier", "knight", "maid", "waitress", "idol", "singer", "musician", "artist", "athlete", "chef", "scientist", "office_lady", "priest", "nun", "witch", "magician"}:
        return "people", "occupation"
    if any_fragment(base_name, ("protagonist", "antagonist", "player_character", "original_character", "faceless", "silhouette_person", "chibi_character")) or token & {"villain", "hero", "superhero", "heroine"}:
        return "people", "role_focus"
    if token & {"elf", "dwarf", "orc", "goblin", "android", "cyborg", "robot_girl", "demon_girl", "angel", "fairy", "mermaid", "vampire"}:
        return "people", "fantasy_person"

    if token & {"petite", "slender", "skinny", "athletic", "muscular", "curvy", "plump", "fat", "tall", "short", "giant", "dwarf", "body"}:
        return "body", "build"
    if token & {"breasts", "breast", "chest", "torso", "cleavage", "navel", "stomach", "abdomen", "ribs"}:
        return "body", "chest"
    if token & {"waist", "hips", "hip", "ass", "buttocks", "thighs", "thigh", "legs", "leg", "knees", "knee", "calves"}:
        return "body", "waist_legs"
    if token & {"arms", "arm", "elbows", "elbow", "hands", "hand", "fingers", "finger", "feet", "foot", "toes", "toe", "nails"}:
        return "body", "arms_hands_feet"
    if token & {"skin", "tan", "dark_skin", "pale", "albino", "sunburn", "skin_color"} or name.endswith("_skin"):
        return "body", "skin"
    if token & {"tattoo", "scar", "scars", "birthmark", "bandaid", "bruise", "wound", "markings", "bodypaint", "mole"}:
        return "body", "body_marks"
    if any_fragment(base_name, ("wet_body", "injured", "bleeding", "pregnant", "inflated", "prosthetic", "amputee", "missing_limb", "extra_arms", "multiple_arms")) or token & {"sweat", "sweating"}:
        return "body", "body_state"

    chinese_location = classify_from_chinese(tag)
    if chinese_location:
        return chinese_location
    return "other", other_category(name)


def classify_tag(tag: dict) -> tuple[str, str]:
    kind = str(tag.get("category", "0"))
    if kind == "3":
        return "copyright", initial_category(tag["name"])
    if kind == "4":
        return "character", initial_category(tag["name"])
    return normalize_location(classify_general(tag), tag["name"])


def validate_taxonomy():
    assert len(FOLDER_BY_ID) == len(TAXONOMY)
    for item in TAXONOMY:
        ids = [cat["id"] for cat in item["categories"]]
        assert len(ids) == len(set(ids)), f"Duplicate category id in {item['id']}"
    for tag_name, (folder_id, category_id) in EXACT_OVERRIDES.items():
        folder_id, category_id = normalize_location((folder_id, category_id), tag_name)
        assert folder_id in CATEGORY_IDS, f"Unknown folder for {tag_name}: {folder_id}"
        assert category_id in CATEGORY_IDS[folder_id], f"Unknown category for {tag_name}: {folder_id}/{category_id}"
    for pattern, (folder_id, category_id) in CN_FALLBACK_RULES:
        folder_id, category_id = normalize_location((folder_id, category_id))
        assert folder_id in CATEGORY_IDS, f"Unknown Chinese-rule folder for {pattern}: {folder_id}"
        assert category_id in CATEGORY_IDS[folder_id], f"Unknown Chinese-rule category for {pattern}: {folder_id}/{category_id}"


validate_taxonomy()
