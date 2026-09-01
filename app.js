const $ = (selector) => document.querySelector(selector);
const SESSION_KEY = 'prompt-atelier-state';
const LIBRARY_KEY = 'prompt-atelier-library-v1';

const state = {
  baseCatalog: null,
  catalog: null,
  edits: null,
  folderId: null,
  categoryId: null,
  selected: [],
  showNsfw: false,
  dragging: null,
  manageMode: false,
  editorContext: null,
  tagIndex: new Map(),
  tagMemberships: new Map(),
  searchEntries: [],
  databaseTagChoices: [],
  searchScope: 'global',
  searchResults: [],
  searchActiveIndex: -1,
  manageDrag: null,
  manageDragArmed: false
};

const els = {
  tabs: $('#category-tabs'),
  cloud: $('#tag-cloud'),
  libraries: $('#library-list'),
  folderTitle: $('#folder-title'),
  categoryName: $('#category-name'),
  visibleCount: $('#visible-count'),
  selectedList: $('#selected-list'),
  editor: $('#prompt-editor'),
  promptCount: $('#prompt-count'),
  previewTotal: $('#preview-total'),
  previewGroups: $('#preview-groups'),
  finalPrompt: $('#final-prompt'),
  dbStat: $('#database-stat'),
  libraryCount: $('#library-count'),
  nsfw: $('#nsfw-toggle'),
  toast: $('#toast'),
  addFolder: $('#add-folder'),
  addCategory: $('#add-category'),
  addTag: $('#add-tag'),
  toggleManage: $('#toggle-manage'),
  libraryEditor: $('#library-editor'),
  libraryEditorForm: $('#library-editor-form'),
  libraryEditorTitle: $('#library-editor-title'),
  libraryEditorSubtitle: $('#library-editor-subtitle'),
  libraryNameField: $('#library-name-field'),
  libraryNameLabel: $('#library-name-label'),
  libraryName: $('#library-name'),
  libraryDescription: $('#library-description'),
  libraryIcon: $('#library-icon'),
  libraryAccent: $('#library-accent'),
  libraryCn: $('#library-cn'),
  libraryNsfw: $('#library-nsfw'),
  libraryEditorError: $('#library-editor-error'),
  libraryEditorSubmit: $('#library-editor-submit'),
  tagSourceField: $('#tag-source-field'),
  tagSourceDatabase: $('#tag-source-database'),
  tagSourceManual: $('#tag-source-manual'),
  databaseTagPanel: $('#tag-database-panel'),
  databaseTagSearch: $('#database-tag-search'),
  databaseTagResults: $('#database-tag-results'),
  databaseTagResultCount: $('#database-tag-result-count'),
  databaseTagSelectedCount: $('#database-tag-selected-count'),
  tagSearch: $('#tag-search'),
  searchInput: $('#tag-search-input'),
  searchResults: $('#tag-search-results'),
  searchGlobal: $('#search-scope-global'),
  searchLibrary: $('#search-scope-library'),
  searchLocal: $('#search-scope-local'),
  clearSearch: $('#clear-search')
};

function currentFolder() {
  return state.catalog?.folders.find(folder => folder.id === state.folderId) || null;
}

function currentCategory() {
  return currentFolder()?.categories.find(category => category.id === state.categoryId) || null;
}

function tagKey(name) {
  return String(name || '').toLowerCase().trim();
}

function labelKey(name) {
  return String(name || '').trim().toLocaleLowerCase('zh-CN');
}

function tupleKey(...parts) {
  return JSON.stringify(parts.map(part => String(part)));
}

function rowKey(row) {
  return Array.isArray(row) ? tupleKey(...row) : '';
}

function migrateLegacyLocation(folderId, categoryId, tagName = '') {
  const fullName = tagKey(tagName);
  const name = fullName.replace(/_\([^)]*\)$/, '');
  const tokens = new Set(name.split(/[_()\-/' ]+/).filter(Boolean));
  const hasToken = (...values) => values.some(value => tokens.has(value));
  if (folderId === 'text_meta' && categoryId === 'symbol') {
    if (hasToken('flag', 'banner', 'pennant', 'ensign')) return ['text_meta', 'flag'];
    if (hasToken('note', 'notes', 'clef', 'rest', 'staff') || name.includes('musical')) return ['text_meta', 'music_symbol'];
    if (hasToken('zodiac', 'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces')) return ['text_meta', 'zodiac_symbol'];
    if (hasToken('shape', 'circle', 'triangle', 'square', 'rectangle', 'hexagon', 'cube', 'pyramid') || name.includes('geometry')) return ['text_meta', 'shape_math'];
    if (hasToken('cross', 'ankh', 'mandala', 'pentagram', 'trigram', 'triquetra') || name.includes('dharma')) return ['text_meta', 'religious_symbol'];
    if (hasToken('radiation', 'biohazard', 'dna', 'atom') || name.includes('chemical')) return ['text_meta', 'science_sign'];
    if (hasToken('emblem', 'crest') || name.endsWith('_logo')) return ['text_meta', 'emblem'];
    return ['text_meta', 'general_symbol'];
  }
  if (folderId === 'body' && categoryId === 'body_marks') {
    if (['blood_stain', 'blood_on_breasts', 'blood_on_neck', 'blood_on_stomach'].includes(name)) return ['sensitive', 'blood'];
    if (['self-harm_scar', 'deep_wound', 'gunshot_wound'].includes(name)) return ['sensitive', 'injury_death'];
    if (name === 'glasgow_smile') return ['sensitive', 'gore'];
    if (name === 'bindi') return ['face', 'makeup'];
    if (name === 'w_over_eye') return ['pose', 'hand_gesture'];
    if (name === 'armpit_hair_peek') return ['body', 'body_hair'];
    if (name === 'tan_tattoo') return ['body', 'skin'];
    if (name === 'bridge_piercing') return ['accessories', 'jewelry'];
    if (name.includes('tattoo') || hasToken('mark', 'marking', 'markings')) return ['body', 'tattoo_mark'];
    if (['mole', 'freckle', 'birthmark'].some(fragment => name.includes(fragment))) return ['body', 'mole_freckle'];
    if (['scar', 'bruise', 'wound', 'cuts', 'scratches', 'hickey', 'bite', 'bitten', 'stitch', 'scrape'].some(fragment => name.includes(fragment))) return ['body', 'scar_wound'];
    if (['bandaid', 'bandage', 'gauze'].some(fragment => name.includes(fragment))) return ['body', 'bandage_patch'];
    if (['paint', 'sticker', 'ink'].some(fragment => name.includes(fragment))) return ['body', 'surface_decor'];
    if (hasToken('food', 'cream', 'rice', 'chocolate', 'stain')) return ['body', 'surface_stain'];
    return ['body', 'tattoo_mark'];
  }
  if (folderId === 'hair' && categoryId === 'hair_accessory') {
    const exceptions = new Map([
      ['feather_hair', ['creatures', 'wing_feather']],
      ['hair_rollers', ['household_objects', 'tools']],
      ['wrist_scrunchie', ['accessories', 'handwear']],
      ['arm_scrunchie', ['accessories', 'handwear']],
      ['ear_scrunchie', ['accessories', 'other_accessory']],
      ['ankle_scrunchie', ['accessories', 'other_accessory']],
      ['thigh_scrunchie', ['accessories', 'other_accessory']]
    ]);
    return exceptions.get(name) || ['accessories', 'hair_accessory'];
  }
  if (folderId === 'face' && categoryId === 'brows_nose') {
    const exceptions = new Map([
      ['aegyo_sal', ['face', 'eye_shape']],
      ['forehead', ['face', 'face_shape']],
      ['cheekbones', ['face', 'face_shape']],
      ['large_forehead', ['face', 'face_shape']],
      ['shiny_forehead', ['face', 'face_shape']],
      ['sunken_cheeks', ['face', 'face_shape']],
      ['snot', ['body', 'body_state']],
      ['nose_bubble', ['body', 'body_state']],
      ['runny_nose', ['body', 'body_state']],
      ['nose_ring', ['accessories', 'jewelry']],
      ['red_nose', ['accessories', 'other_accessory']],
      ['clown_nose', ['accessories', 'other_accessory']],
      ['fake_nose', ['accessories', 'other_accessory']],
      ['nose_tape', ['accessories', 'other_accessory']],
      ['nose_hook', ['adult', 'adult_fetish']],
      ['butterfly_on_nose', ['creatures', 'insect']],
      ['nose_picking', ['action', 'daily_action']],
      ['wiping_nose', ['action', 'daily_action']],
      ['blowing_nose', ['action', 'daily_action']],
      ['rubbing_nose', ['pose', 'hand_gesture']],
      ['nose_pinch', ['action', 'interaction']],
      ['poking_nose', ['action', 'interaction']]
    ]);
    if (exceptions.has(name)) return exceptions.get(name);
    if (!name || name.includes('eyebrow')) return ['face', 'eyebrows'];
    return ['face', 'nose'];
  }
  if (folderId === 'clothes_special' && categoryId === 'sleep_casual') {
    if (name.includes('sarong')) return ['clothes_special', 'traditional_world'];
    if (['business_casual', 'casual', 'streetwear'].includes(name)) return ['clothes_special', 'casualwear'];
    if (name === 'bathrobe' || name.split('_').includes('robe')) return ['clothes_special', 'robe'];
    return ['clothes_special', 'sleepwear'];
  }
  if (folderId === 'underwear_swim' && categoryId === 'underwear_design') {
    return name === 'crinoline' ? ['clothing_detail', 'other_structure'] : ['underwear_swim', 'swimsuit'];
  }
  if (folderId === 'creatures' && categoryId === 'animal_feature') {
    const exceptions = new Map([
      ['fake_animal_ears', ['accessories', 'headwear']],
      ['mickey_mouse_ears', ['accessories', 'headwear']],
      ['minnie_mouse_ears', ['accessories', 'headwear']],
      ['fake_horns', ['accessories', 'headwear']],
      ['fake_antlers', ['accessories', 'headwear']],
      ['hair_ears', ['hair', 'hair_style']],
      ['raccoon_tails_(hairstyle)', ['hair', 'hair_style']],
      ['headphones_for_animal_ears', ['digital_media', 'audio_device']],
      ['earphones_on_animal_ears', ['digital_media', 'audio_device']],
      ["playing_with_another's_ears", ['action', 'interaction']],
      ['flapping_ears', ['action', 'movement']],
      ['flapping', ['action', 'movement']],
      ['innertube_with_ears', ['recreation', 'sports']],
      ['tail_insertion', ['adult', 'adult_sex']],
      ['implied_tail_plug', ['adult', 'adult_toys']],
      ['tail_bell', ['accessories', 'badges_ornaments']],
      ['bandaged_tail', ['body', 'body_marks']],
      ['foxtail', ['creatures', 'tails']],
      ['dock_(tail)', ['creatures', 'tails']],
      ['talons', ['creatures', 'claw_scale']],
      ['suction_cups', ['creatures', 'claw_scale']],
      ['hirschgeweih_antennas', ['mech_scifi', 'machine']]
    ]);
    if (exceptions.has(fullName)) return exceptions.get(fullName);
    if (hasToken('wing', 'wings', 'feather', 'feathers', 'plumage')) return ['creatures', 'wing_feather'];
    if (hasToken('claw', 'claws', 'scale', 'scales', 'tentacle', 'tentacles', 'fin', 'fins', 'paw', 'paws', 'antenna', 'antennae')) return ['creatures', 'claw_scale'];
    if (hasToken('ear', 'ears') || name.endsWith('_ear') || name.endsWith('_ears')) return ['creatures', 'animal_ears'];
    if (hasToken('horn', 'horns', 'antler', 'antlers')) return ['creatures', 'horns'];
    if (hasToken('tail', 'tails')) return ['creatures', 'tails'];
    return ['creatures', 'fur_feature'];
  }
  if (folderId === 'light_effect' && categoryId === 'magic_effect') {
    if (hasToken('halo', 'halos') || name.endsWith('_halo')) return ['light_effect', 'halo_effect'];
    if (hasToken('aura', 'glowing', 'glow') || name.startsWith('glowing_')) return ['light_effect', 'glow_aura'];
    return ['light_effect', 'magic_energy'];
  }
  if (folderId === 'clothing_detail' && categoryId === 'clothing_state') {
    const actionNames = new Set([
      'clothes_lift', 'clothes_pull', 'dressing', 'dressing_another', 'undressing',
      'undressing_another', 'untying', 'tying', 'unbuttoning', 'clothes_on_and_off',
      'imminent_forced_dressing', 'skirt_flip', 'clothes_tug', 'removing_bra_under_shirt'
    ]);
    if (['adjusting_', 'removing_', 'putting_on_', 'lifting_', 'pulling_'].some(prefix => name.startsWith(prefix))
      || ['_lift', '_pull', '_aside'].some(fragment => name.includes(fragment)) || actionNames.has(name)) {
      return ['action', 'clothing_action'];
    }
    if (name === 'lactation_through_clothes' || name === 'torn' || name === 'rags' || name === 'burning_clothes'
      || ['torn_', 'wet_', 'blood_on_'].some(prefix => name.startsWith(prefix))) return ['clothing_detail', 'damaged_dirty'];
    if (name === 'clothes_on_floor' || ['unworn_', 'no_', 'missing_'].some(prefix => name.startsWith(prefix))
      || name.includes('_unworn_')) return ['clothing_detail', 'unworn_missing'];
    return ['clothing_detail', 'open_wear'];
  }
  if (folderId === 'clothing_detail' && categoryId === 'clothing_structure') {
    const exceptions = new Map([
      ['zipping', ['action', 'clothing_action']], ['unzipping', ['action', 'clothing_action']],
      ['pressing_button', ['action', 'daily_action']], ['hands_in_pocket', ['pose', 'hand_gesture']],
      ['thumb_in_pocket', ['pose', 'hand_gesture']], ["hand_in_another's_pocket", ['action', 'interaction']],
      ['in_pocket', ['pose', 'body_pose']], ['safety_pin', ['household_objects', 'tools']],
      ['frilled_umbrella', ['household_objects', 'tools']], ['frilled_innertube', ['recreation', 'sports']],
      ['frilled_headwear', ['accessories', 'headwear']], ['frilled_bonnet', ['accessories', 'headwear']],
      ['wide_brim', ['accessories', 'headwear']], ['eyewear_strap', ['accessories', 'eyewear']],
      ['frilled_ascot', ['accessories', 'neckwear']], ['frilled_necktie', ['accessories', 'neckwear']],
      ['frilled_bowtie', ['accessories', 'neckwear']], ['frilled_armband', ['accessories', 'handwear']],
      ['frilled_wristband', ['accessories', 'handwear']], ['glove_cuffs', ['accessories', 'handwear']],
      ['frilled_armlet', ['accessories', 'jewelry']], ['cellphone_strap', ['accessories', 'other_accessory']],
      ['shoulder_sash', ['accessories', 'bags_belts']], ['dress_flower', ['accessories', 'badges_ornaments']],
      ['pom_pom', ['accessories', 'badges_ornaments']], ['single_epaulette', ['accessories', 'badges_ornaments']],
      ['weapon_strap', ['weapons', 'other_weapon']], ['shoe_strap', ['legwear_footwear', 'shoes']],
      ['shirt_tucked_in', ['clothing_detail', 'open_wear']], ['hem_peeking_out', ['clothing_detail', 'open_wear']]
    ]);
    if (exceptions.has(name)) return exceptions.get(name);
    if (['pocket', 'breast_pocket', 'exposed_pocket', 'object_in_pocket', 'pen_in_pocket', 'pocket_square', 'phone_in_pocket', 'carrot_in_pocket'].includes(name)) return ['clothing_detail', 'pocket_detail'];
    if (hasToken('sleeve', 'sleeves', 'cuff', 'cuffs')) return ['clothing_detail', 'sleeve_detail'];
    if (hasToken('collar', 'neckline', 'lapel')) return ['clothing_detail', 'collar_detail'];
    if (hasToken('strap', 'straps', 'suspender', 'suspenders')) return ['clothing_detail', 'strap_detail'];
    if (hasToken('cutout', 'cutouts', 'slit', 'slits')) return ['clothing_detail', 'cutout_slit'];
    if (hasToken('button', 'buttons', 'zipper', 'zippers', 'buckle', 'buckles')
      || ['lace-up', 'cross-laced', 'o-ring'].some(fragment => name.includes(fragment))
      || ['drawstring', 'pankou', 'toggles', 'pull_cord'].includes(name)) return ['clothing_detail', 'fastener'];
    if (hasToken('frill', 'frills', 'frilled', 'trim', 'trimmed', 'feather', 'fringe')) return ['clothing_detail', 'trim_detail'];
    return ['clothing_detail', 'other_structure'];
  }
  if (folderId === 'clothes_main' && categoryId === 'tops') {
    if (hasToken('shirt', 'blouse', 'tunic', 'jersey', 'chemise', 'guimpe')) return ['clothes_main', 'shirt_top'];
    if (hasToken('sweater', 'hoodie') || ['turtleneck', 'sleeveless_turtleneck'].includes(name)) return ['clothes_main', 'sweater_hoodie'];
    return ['clothes_main', 'vest_top'];
  }
  if (folderId === 'clothes_main' && categoryId === 'outerwear') {
    if (hasToken('jacket', 'coat', 'blazer', 'raincoat', 'parka', 'windbreaker', 'duster', 'smock') || name === 'sukajan') return ['clothes_main', 'jacket_coat'];
    if (hasToken('cape', 'cloak', 'poncho', 'tabard', 'surcoat')) return ['clothes_main', 'cape_cloak'];
    return ['clothes_main', 'cardigan_shawl'];
  }
  if ((folderId === 'digital_media' || folderId === 'culture_objects') && categoryId === 'phone_computer') {
    const phones = new Set(['phone', 'cellphone', 'smartphone', 'flip_phone', 'corded_phone', 'antique_phone', 'iphone', 'rotary_phone', 'payphone', 'feature_phone', 'bar_phone', 'string_phone', 'camera_phone', 'phone_with_ears', 'cordless_phone', 'phone_on_wall', 'slide_phone', 'cracked_phone', 'x-ray_phone']);
    const games = new Set(['controller', 'game_controller', 'handheld_game_console', 'nintendo_switch', 'game_console', 'd-pad', 'playstation_controller', 'playstation_portable', 'nintendo_ds', 'game_boy', 'joy-con', 'nintendo_3ds', 'dualshock', 'game_boy_(original)', 'game_boy_advance', 'famicom', 'playstation_vita', 'playstation_5', 'nintendo_switch_2', 'super_famicom_controller', 'gamecube_controller', 'nintendo_64_controller', 'xbox_controller', 'famicom_controller', 'nintendo_switch_pro_controller', 'flight_stick']);
    if (phones.has(fullName)) return ['digital_media', 'phone_device'];
    if (games.has(fullName)) return ['digital_media', 'game_device'];
    if (name === 'cellphone_photo') return ['digital_media', 'camera_video'];
    return ['digital_media', 'computer_device'];
  }
  if ((folderId === 'digital_media' || folderId === 'culture_objects') && categoryId === 'camera_media') {
    const audio = new Set(['headphones', 'microphone', 'headset', 'headphones_around_neck', 'animal_ear_headphones', 'earphones', 'cat_ear_headphones', 'radio_antenna', 'microphone_stand', 'earpiece', 'megaphone', 'speaker', 'mp3_player', 'earbuds', 'walkie-talkie', 'radio', 'cd', 'ipod', 'boombox', 'ipod_nano', 'cassette_player', 'cassette_tape', 'digital_walkman', 'walkman', 'stereo']);
    return audio.has(fullName) ? ['digital_media', 'audio_device'] : ['digital_media', 'camera_video'];
  }
  if (folderId === 'body' && categoryId === 'chest') {
    if (fullName === 'heart_(organ)' || fullName === 'stomach_(organ)' || name === 'brain') return ['body', 'internal_organs'];
    if (hasToken('breast', 'breasts', 'pectoral', 'pectorals', 'cleavage', 'chest', 'boob', 'boobs', 'bust', 'sidepec', 'underpec', 'underbust') || name.includes('cup_size')) return ['body', 'breast_chest'];
    return ['body', 'torso_back'];
  }
  if (folderId === 'body' && categoryId === 'waist_legs') {
    if (hasToken('leg', 'legs', 'thigh', 'thighs', 'knee', 'knees', 'calf', 'calves')) return ['body', 'legs_knees'];
    if (hasToken('waist', 'hip', 'hips', 'ass', 'butt', 'buttocks', 'groin', 'crotch', 'lap', 'lower', 'body')) return ['body', 'waist_hips'];
    return ['body', 'body_state'];
  }
  if (folderId === 'body' && categoryId === 'arms_hands_feet') {
    if (hasToken('foot', 'feet', 'toe', 'toes', 'sole', 'soles', 'heel', 'heels', 'toenail', 'toenails')) return ['body', 'feet_toes'];
    if (hasToken('arm', 'arms', 'hand', 'hands', 'finger', 'fingers', 'nail', 'nails', 'elbow', 'elbows', 'armpit', 'armpits', 'palm', 'palms', 'triceps', 'joint', 'joints')) return ['body', 'arms_hands'];
    return ['body', 'body_state'];
  }
  if (folderId === 'adult' && categoryId === 'adult_gore') {
    if (['blood_on_ground', 'pool_of_blood', 'blood_on_wall', 'blood_spray', 'blood_trail'].includes(name)) return ['sensitive', 'blood'];
    if (['corpse', 'impaled', 'stab', 'self-harm', 'torture', 'wrist_cutting', 'suicide', 'crucifixion', 'cannibalism', 'hanged', 'implied_murder', 'imminent_suicide', 'execution', 'knife_in_head', 'pile_of_corpses'].includes(name)) return ['sensitive', 'injury_death'];
    if (['ryona', 'ero_guro', 'reverse_ryona'].includes(name)) return ['sensitive', 'sexual_violence'];
    return ['sensitive', 'gore'];
  }
  const moves = new Map([
    [tupleKey('people', 'relationship'), ['relationships', 'social_relation']],
    [tupleKey('themes', 'romance_orientation'), ['relationships', 'romance_orientation']],
    [tupleKey('themes', 'family_relation'), ['relationships', 'family_relation']],
    [tupleKey('themes', 'social_relation'), ['relationships', 'social_relation']],
    [tupleKey('legwear_footwear', 'armor'), ['clothes_special', 'armor']],
    [tupleKey('legwear_footwear', 'helmet_protective'), ['clothes_special', 'helmet_protective']],
    [tupleKey('clothes_main', 'suit'), ['clothes_main', 'formal_suit']],
    [tupleKey('culture_objects', 'phone_computer'), ['digital_media', 'phone_computer']],
    [tupleKey('culture_objects', 'camera_media'), ['digital_media', 'camera_media']],
    [tupleKey('transport_play', 'sports'), ['recreation', 'sports']],
    [tupleKey('transport_play', 'games'), ['recreation', 'games']],
    [tupleKey('transport_play', 'toys'), ['recreation', 'toys']],
    [tupleKey('creatures', 'plant'), ['nature', 'plant']],
    [tupleKey('creatures', 'mineral'), ['nature', 'mineral']],
    [tupleKey('text_meta', 'meme'), ['meta_info', 'meme']],
    [tupleKey('text_meta', 'cosplay'), ['meta_info', 'cosplay']],
    [tupleKey('text_meta', 'censorship'), ['meta_info', 'censorship']],
    [tupleKey('text_meta', 'meta'), ['meta_info', 'meta']]
  ]);
  return moves.get(tupleKey(folderId, categoryId)) || [String(folderId), String(categoryId)];
}

function migrateLegacyCategoryLocations(folderId, categoryId) {
  const expansions = new Map([
    [tupleKey('face', 'brows_nose'), [['face', 'eyebrows'], ['face', 'nose'], ['face', 'face_shape']]],
    [tupleKey('clothes_special', 'sleep_casual'), [['clothes_special', 'sleepwear'], ['clothes_special', 'robe'], ['clothes_special', 'casualwear']]],
    [tupleKey('underwear_swim', 'underwear_design'), [['underwear_swim', 'swimsuit'], ['clothing_detail', 'other_structure']]],
    [tupleKey('creatures', 'animal_feature'), [['creatures', 'animal_ears'], ['creatures', 'horns'], ['creatures', 'tails'], ['creatures', 'fur_feature']]],
    [tupleKey('light_effect', 'magic_effect'), [['light_effect', 'halo_effect'], ['light_effect', 'glow_aura'], ['light_effect', 'magic_energy']]],
    [tupleKey('clothing_detail', 'clothing_state'), [['clothing_detail', 'damaged_dirty'], ['clothing_detail', 'unworn_missing'], ['clothing_detail', 'open_wear']]],
    [tupleKey('clothing_detail', 'clothing_structure'), [
      ['clothing_detail', 'sleeve_detail'], ['clothing_detail', 'collar_detail'],
      ['clothing_detail', 'strap_detail'], ['clothing_detail', 'cutout_slit'],
      ['clothing_detail', 'fastener'], ['clothing_detail', 'trim_detail'],
      ['clothing_detail', 'pocket_detail'], ['clothing_detail', 'other_structure']
    ]],
    [tupleKey('clothes_main', 'tops'), [['clothes_main', 'shirt_top'], ['clothes_main', 'sweater_hoodie'], ['clothes_main', 'vest_top']]],
    [tupleKey('clothes_main', 'outerwear'), [['clothes_main', 'jacket_coat'], ['clothes_main', 'cape_cloak'], ['clothes_main', 'cardigan_shawl']]],
    [tupleKey('digital_media', 'phone_computer'), [['digital_media', 'phone_device'], ['digital_media', 'game_device'], ['digital_media', 'computer_device']]],
    [tupleKey('culture_objects', 'phone_computer'), [['digital_media', 'phone_device'], ['digital_media', 'game_device'], ['digital_media', 'computer_device']]],
    [tupleKey('digital_media', 'camera_media'), [['digital_media', 'audio_device'], ['digital_media', 'camera_video']]],
    [tupleKey('culture_objects', 'camera_media'), [['digital_media', 'audio_device'], ['digital_media', 'camera_video']]],
    [tupleKey('body', 'chest'), [['body', 'breast_chest'], ['body', 'torso_back'], ['body', 'internal_organs']]],
    [tupleKey('body', 'waist_legs'), [['body', 'waist_hips'], ['body', 'legs_knees']]],
    [tupleKey('body', 'arms_hands_feet'), [['body', 'arms_hands'], ['body', 'feet_toes']]],
    [tupleKey('adult', 'adult_gore'), [
      ['sensitive', 'blood'], ['sensitive', 'injury_death'],
      ['sensitive', 'gore'], ['sensitive', 'sexual_violence']
    ]],
    [tupleKey('body', 'body_marks'), [
      ['body', 'tattoo_mark'], ['body', 'mole_freckle'], ['body', 'scar_wound'],
      ['body', 'bandage_patch'], ['body', 'surface_stain'], ['body', 'surface_decor']
    ]],
    [tupleKey('text_meta', 'symbol'), [
      ['text_meta', 'general_symbol'], ['text_meta', 'shape_math'], ['text_meta', 'music_symbol'],
      ['text_meta', 'religious_symbol'], ['text_meta', 'zodiac_symbol'], ['text_meta', 'flag'],
      ['text_meta', 'emblem'], ['text_meta', 'science_sign']
    ]]
  ]);
  return expansions.get(tupleKey(folderId, categoryId)) || [migrateLegacyLocation(folderId, categoryId)];
}

const V8_CHANGED_CATEGORY_KEYS = new Set([
  ['body', 'skin'], ['body', 'tattoo_mark'], ['body', 'mole_freckle'], ['body', 'scar_wound'],
  ['body', 'bandage_patch'], ['body', 'surface_stain'], ['body', 'surface_decor'], ['body', 'body_hair'],
  ['body', 'body_function'], ['body', 'body_state'],
  ['clothes_main', 'jacket_coat'], ['clothes_main', 'cape_cloak'], ['clothes_main', 'cardigan_shawl'],
  ['clothes_main', 'formal_suit'], ['clothes_main', 'jumpsuit'],
  ['clothes_special', 'school_uniform'], ['clothes_special', 'occupation_uniform'],
  ['clothes_special', 'sports_uniform'], ['clothes_special', 'themed_costume'],
  ['clothes_special', 'traditional_east'], ['clothes_special', 'traditional_world'],
  ['clothes_special', 'armor'], ['clothes_special', 'helmet'], ['clothes_special', 'helmet_protective'],
  ['clothes_special', 'sleepwear'], ['clothes_special', 'robe'], ['clothes_special', 'casualwear'],
  ['clothing_detail', 'clothing_color'], ['clothing_detail', 'clothing_pattern'],
  ['clothing_detail', 'clothing_material'], ['clothing_detail', 'damaged_dirty'],
  ['clothing_detail', 'unworn_missing'], ['clothing_detail', 'open_wear'],
  ['accessories', 'hair_accessory'], ['accessories', 'headwear'], ['accessories', 'eyewear'],
  ['accessories', 'jewelry'], ['accessories', 'badges_ornaments'],
  ['creatures', 'animal_ears'], ['creatures', 'horns'], ['creatures', 'tails'],
  ['creatures', 'fur_feature'], ['creatures', 'wing_feather'], ['creatures', 'claw_scale'],
  ['indoor_scene', 'urban'], ['indoor_scene', 'architecture'], ['indoor_scene', 'surface'],
  ['outdoor_scene', 'background_plain'], ['outdoor_scene', 'background_pattern'],
  ['text_meta', 'general_symbol'], ['text_meta', 'shape_math'], ['text_meta', 'music_symbol'],
  ['text_meta', 'religious_symbol'], ['text_meta', 'zodiac_symbol'], ['text_meta', 'flag'],
  ['text_meta', 'emblem'], ['text_meta', 'science_sign'],
  ['adult', 'adult_nudity'], ['adult', 'adult_anatomy'], ['adult', 'adult_clothes'],
  ['adult', 'adult_suggestive'], ['adult', 'adult_bondage'], ['adult', 'adult_toys'],
  ['adult', 'adult_fetish'], ['adult', 'adult_taboo'], ['adult', 'adult_other'],
  ['face', 'mouth'], ['pose', 'body_pose'], ['pose', 'hand_gesture'],
  ['household_objects', 'tools']
].map(row => rowKey(row)));

function migrateV8Location(folderId, categoryId, tagName = '') {
  const name = String(tagName || '').toLowerCase().replace(/_\([^)]*\)$/, '');
  const tokens = new Set(name.split(/[_()\-/' ]+/).filter(Boolean));
  const direct = new Map([
    ...['skin', 'tattoo_mark', 'mole_freckle', 'scar_wound', 'bandage_patch', 'surface_stain', 'surface_decor', 'body_hair', 'body_function', 'body_state']
      .map(id => [tupleKey('body', id), ['body_detail', id]]),
    ...['jacket_coat', 'cape_cloak', 'cardigan_shawl', 'formal_suit', 'jumpsuit']
      .map(id => [tupleKey('clothes_main', id), ['outerwear_suits', id]]),
    ...['school_uniform', 'occupation_uniform', 'sports_uniform', 'themed_costume']
      .map(id => [tupleKey('clothes_special', id), ['uniform_costume', id]]),
    ...['traditional_east', 'traditional_world'].map(id => [tupleKey('clothes_special', id), ['traditional_clothes', id]]),
    ...['armor', 'helmet', 'helmet_protective'].map(id => [tupleKey('clothes_special', id), ['protective_clothes', id]]),
    ...['sleepwear', 'robe'].map(id => [tupleKey('clothes_special', id), ['clothes_main', id]]),
    ...['clothing_color', 'clothing_pattern', 'clothing_material'].map(id => [tupleKey('clothing_detail', id), ['clothing_appearance', id]]),
    ...['damaged_dirty', 'unworn_missing', 'open_wear'].map(id => [tupleKey('clothing_detail', id), ['clothing_state', id]]),
    ...['animal_ears', 'horns', 'tails', 'fur_feature', 'wing_feather', 'claw_scale'].map(id => [tupleKey('creatures', id), ['animal_traits', id]]),
    ...['urban', 'architecture', 'surface'].map(id => [tupleKey('indoor_scene', id), ['urban_architecture', id]]),
    ...['background_plain', 'background_pattern'].map(id => [tupleKey('outdoor_scene', id), ['background', id]]),
    ...['general_symbol', 'shape_math', 'music_symbol', 'religious_symbol', 'zodiac_symbol', 'flag', 'emblem', 'science_sign']
      .map(id => [tupleKey('text_meta', id), ['symbols', id]]),
    ...['adult_nudity', 'adult_anatomy', 'adult_clothes', 'adult_suggestive'].map(id => [tupleKey('adult', id), ['adult_body', id]]),
    ...['adult_bondage', 'adult_toys', 'adult_fetish', 'adult_taboo'].map(id => [tupleKey('adult', id), ['adult_kink', id]])
  ]);
  const key = tupleKey(folderId, categoryId);
  if (direct.has(key)) return direct.get(key);
  if (folderId === 'clothes_special' && categoryId === 'casualwear') return ['clothing_appearance', 'fashion_style'];
  if (folderId === 'adult' && categoryId === 'adult_other') return ['adult', 'adult_theme'];
  if (folderId === 'accessories' && categoryId === 'hair_accessory') return ['head_accessories', 'hair_accessory'];
  if (folderId === 'accessories' && categoryId === 'headwear') return ['head_accessories', 'hats_caps'];
  if (folderId === 'accessories' && categoryId === 'eyewear') return ['head_accessories', name.includes('mask') ? 'face_mask' : 'eyewear'];
  if (folderId === 'accessories' && categoryId === 'jewelry') {
    if (name.includes('piercing')) return ['jewelry_accessories', 'piercing'];
    if (name.includes('earring')) return ['jewelry_accessories', 'earrings'];
    if (name.includes('necklace') || name.includes('choker')) return ['jewelry_accessories', 'necklace_choker'];
    if (tokens.has('ring')) return ['jewelry_accessories', 'rings'];
    if (['bracelet', 'anklet', 'armlet', 'bangle'].some(word => tokens.has(word))) return ['jewelry_accessories', 'bracelet_anklet'];
    return ['jewelry_accessories', 'gem_brooch'];
  }
  if (folderId === 'accessories' && categoryId === 'badges_ornaments' && (tokens.has('bow') || tokens.has('ribbon'))) {
    return ['accessories', 'bows_ribbons'];
  }
  if (folderId === 'face' && categoryId === 'mouth' && ['tongue', 'teeth', 'tooth', 'fang', 'saliva', 'drool'].some(word => name.includes(word))) {
    return ['face', 'oral_detail'];
  }
  if (folderId === 'pose' && categoryId === 'body_pose' && ['leg', 'foot', 'feet', 'knee', 'toe'].some(word => tokens.has(word))) {
    return ['pose', 'leg_pose'];
  }
  if (folderId === 'pose' && categoryId === 'hand_gesture') return ['pose', 'arm_pose'];
  if (folderId === 'household_objects' && categoryId === 'tools') return ['household_objects', 'tools'];
  // clothes_special was the only v7 parent removed outright.  Preserve
  // user-created categories inside it by moving the custom category intact.
  if (folderId === 'clothes_special') return ['uniform_costume', String(categoryId)];
  return [String(folderId), String(categoryId)];
}

function migrateV8CategoryLocations(folderId, categoryId) {
  const expansions = new Map([
    [tupleKey('accessories', 'headwear'), [['head_accessories', 'hats_caps'], ['head_accessories', 'headwrap_veil'], ['head_accessories', 'headpiece']]],
    [tupleKey('accessories', 'eyewear'), [['head_accessories', 'eyewear'], ['head_accessories', 'face_mask']]],
    [tupleKey('accessories', 'jewelry'), [['jewelry_accessories', 'earrings'], ['jewelry_accessories', 'necklace_choker'], ['jewelry_accessories', 'rings'], ['jewelry_accessories', 'bracelet_anklet'], ['jewelry_accessories', 'piercing'], ['jewelry_accessories', 'gem_brooch']]],
    [tupleKey('accessories', 'badges_ornaments'), [['accessories', 'bows_ribbons'], ['accessories', 'badges_ornaments']]],
    [tupleKey('face', 'mouth'), [['face', 'mouth'], ['face', 'oral_detail']]],
    [tupleKey('pose', 'body_pose'), [['pose', 'body_pose'], ['pose', 'leg_pose']]],
    [tupleKey('pose', 'hand_gesture'), [['pose', 'arm_pose'], ['pose', 'hand_gesture']]],
    [tupleKey('clothes_special', 'school_uniform'), [['uniform_costume', 'school_uniform'], ['uniform_costume', 'school_variant'], ['uniform_costume', 'sailor_uniform']]],
    [tupleKey('clothes_special', 'occupation_uniform'), [['uniform_costume', 'service_uniform'], ['uniform_costume', 'occupation_uniform'], ['uniform_costume', 'military_uniform'], ['uniform_costume', 'sports_uniform'], ['uniform_costume', 'franchise_uniform']]],
    [tupleKey('adult', 'adult_fetish'), [['adult_kink', 'adult_bondage'], ['adult_kink', 'adult_toys'], ['adult_kink', 'adult_power'], ['adult_kink', 'adult_piercing'], ['adult_kink', 'adult_insertion'], ['adult_kink', 'adult_excretion'], ['adult_kink', 'adult_fetish']]],
    [tupleKey('adult', 'adult_other'), [['adult', 'adult_response'], ['adult', 'adult_theme'], ['sensitive', 'sexual_violence'], ['adult_kink', 'adult_taboo']]],
    [tupleKey('household_objects', 'tools'), [['household_objects', 'umbrella_fan'], ['household_objects', 'rope_lock'], ['household_objects', 'care_cleaning'], ['household_objects', 'tools']]]
  ]);
  return expansions.get(tupleKey(folderId, categoryId)) || [migrateV8Location(folderId, categoryId)];
}

const V10_CHANGED_CATEGORY_KEYS = new Set([
  ['head_accessories', 'hair_accessory'],
  ['uniform_costume', 'school_variant'], ['uniform_costume', 'franchise_uniform'],
  ['traditional_clothes', 'traditional_east'], ['traditional_clothes', 'traditional_world'],
  ['protective_clothes', 'armor'], ['protective_clothes', 'helmet'], ['protective_clothes', 'helmet_protective'],
  ['underwear_swim', 'swimsuit'],
  ['legwear_footwear', 'shoes'], ['legwear_footwear', 'boots'],
  ['nature', 'plant'], ['urban_architecture', 'architecture'],
  ['adult_body', 'adult_anatomy'], ['adult_body', 'adult_suggestive']
].map(row => rowKey(row)));

function migrateV10Location(folderId, categoryId) {
  const direct = new Map([
    [tupleKey('head_accessories', 'hair_accessory'), ['head_accessories', 'themed_hair_ornament']],
    [tupleKey('uniform_costume', 'school_variant'), ['franchise_clothes', 'school_variant']],
    [tupleKey('uniform_costume', 'franchise_uniform'), ['franchise_clothes', 'franchise_uniform']],
    [tupleKey('traditional_clothes', 'traditional_east'), ['traditional_clothes', 'traditional_other']],
    [tupleKey('traditional_clothes', 'traditional_world'), ['traditional_clothes', 'traditional_other']],
    [tupleKey('protective_clothes', 'armor'), ['protective_clothes', 'torso_armor']],
    [tupleKey('protective_clothes', 'helmet'), ['protective_clothes', 'combat_helmet']],
    [tupleKey('protective_clothes', 'helmet_protective'), ['protective_clothes', 'protective_suit']],
    [tupleKey('underwear_swim', 'swimsuit'), ['underwear_swim', 'other_swim']],
    [tupleKey('legwear_footwear', 'shoes'), ['legwear_footwear', 'casual_shoes']],
    [tupleKey('legwear_footwear', 'boots'), ['legwear_footwear', 'short_boots']],
    [tupleKey('nature', 'plant'), ['nature', 'flower_general']],
    [tupleKey('urban_architecture', 'architecture'), ['urban_architecture', 'public_building']],
    [tupleKey('adult_body', 'adult_anatomy'), ['adult_body', 'genital_variation']],
    [tupleKey('adult_body', 'adult_suggestive'), ['adult', 'adult_suggestive']]
  ]);
  return direct.get(tupleKey(folderId, categoryId)) || [String(folderId), String(categoryId)];
}

function migrateV10CategoryLocations(folderId, categoryId) {
  const expansions = new Map([
    [tupleKey('head_accessories', 'hair_accessory'), ['hairband_ribbon', 'hairclip_pin', 'hairtie_ring', 'wig_hairpiece', 'themed_hair_ornament'].map(id => ['head_accessories', id])],
    [tupleKey('traditional_clothes', 'traditional_east'), ['traditional_japan', 'traditional_china', 'traditional_korea', 'traditional_other'].map(id => ['traditional_clothes', id])],
    [tupleKey('traditional_clothes', 'traditional_world'), ['traditional_india', 'traditional_se_asia', 'traditional_central_west', 'traditional_europe', 'traditional_americas', 'traditional_africa', 'traditional_other'].map(id => ['traditional_clothes', id])],
    [tupleKey('protective_clothes', 'armor'), ['torso_armor', 'shoulder_armor', 'arm_armor', 'leg_armor', 'flexible_armor', 'powered_armor'].map(id => ['protective_clothes', id])],
    [tupleKey('protective_clothes', 'helmet'), ['combat_helmet', 'civilian_helmet'].map(id => ['protective_clothes', id])],
    [tupleKey('protective_clothes', 'helmet_protective'), ['pads_support', 'protective_suit'].map(id => ['protective_clothes', id])],
    [tupleKey('underwear_swim', 'swimsuit'), ['bikini', 'onepiece_swim', 'school_swim', 'male_swim', 'highleg_swim', 'other_swim'].map(id => ['underwear_swim', id])],
    [tupleKey('legwear_footwear', 'shoes'), ['heels', 'casual_shoes', 'sandals_slippers', 'traditional_shoes', 'sports_shoes'].map(id => ['legwear_footwear', id])],
    [tupleKey('legwear_footwear', 'boots'), ['short_boots', 'tall_boots', 'work_special_shoes'].map(id => ['legwear_footwear', id])],
    [tupleKey('nature', 'plant'), ['flower_general', 'rose', 'flower_species', 'aquatic_flower', 'tree', 'foliage_vine', 'grass_crop', 'potted_shrub', 'fungus_fantasy'].map(id => ['nature', id])],
    [tupleKey('urban_architecture', 'architecture'), [
      ...['door_window', 'stairs_railing', 'fence_gate', 'bridge_walkway', 'roof_exterior', 'frame_structure'].map(id => ['building_parts', id]),
      ...['residential', 'public_building', 'religious_building', 'tower_landmark', 'ruin_structure', 'architecture_style'].map(id => ['urban_architecture', id])
    ]],
    [tupleKey('adult_body', 'adult_anatomy'), ['penis', 'testicles', 'vulva', 'clitoris', 'anus', 'pubic_hair', 'reproductive', 'genital_variation'].map(id => ['adult_body', id])]
  ]);
  return expansions.get(tupleKey(folderId, categoryId)) || [migrateV10Location(folderId, categoryId)];
}

const V11_CHANGED_CATEGORY_KEYS = new Set([
  ['franchise_clothes', 'character_costume'],
  ['nature', 'aquatic_flower'], ['nature', 'fungus_fantasy'],
  ['urban_architecture', 'ruin_structure']
].map(row => rowKey(row)));

function migrateV11Location(folderId, categoryId, tagName = '') {
  const name = String(tagName || '').toLowerCase();
  const key = tupleKey(folderId, categoryId);
  if (key === tupleKey('franchise_clothes', 'character_costume')) {
    return name.includes('precure')
      ? ['franchise_clothes', 'franchise_outfit']
      : ['uniform_costume', 'themed_costume'];
  }
  if (key === tupleKey('nature', 'aquatic_flower')) {
    return ['nature', ['seaweed', 'algae', 'aquatic_plant'].some(word => name.includes(word)) ? 'grass_crop' : 'flower_species'];
  }
  if (key === tupleKey('nature', 'fungus_fantasy')) {
    return ['nature', ['mushroom', 'fungus', 'toadstool', 'mycelium', 'agaric'].some(word => name.includes(word)) ? 'grass_crop' : 'unusual_plant'];
  }
  if (key === tupleKey('urban_architecture', 'ruin_structure')) {
    return ['urban_architecture', 'tower_landmark'];
  }
  return [String(folderId), String(categoryId)];
}

function migrateV11CategoryLocations(folderId, categoryId) {
  const expansions = new Map([
    [tupleKey('franchise_clothes', 'character_costume'), [
      ['uniform_costume', 'themed_costume'], ['franchise_clothes', 'franchise_outfit']
    ]],
    [tupleKey('nature', 'aquatic_flower'), [
      ['nature', 'flower_species'], ['nature', 'grass_crop']
    ]],
    [tupleKey('nature', 'fungus_fantasy'), [
      ['nature', 'grass_crop'], ['nature', 'unusual_plant']
    ]],
    [tupleKey('urban_architecture', 'ruin_structure'), [
      ['urban_architecture', 'tower_landmark'], ['building_parts', 'frame_structure']
    ]]
  ]);
  return expansions.get(tupleKey(folderId, categoryId)) || [migrateV11Location(folderId, categoryId)];
}

const V12_CHANGED_CATEGORY_KEYS = new Set([
  ['clothing_state', 'damaged_dirty'],
  ['clothing_state', 'unworn_missing'],
  ['clothing_state', 'open_wear'],
  ['body_detail', 'surface_decor'], ['body', 'surface_decor'],
  ['nature', 'rose'],
  ['urban_architecture', 'surface']
].map(row => rowKey(row)));

function migrateV12Location(folderId, categoryId) {
  const folder = String(folderId);
  const category = String(categoryId);
  if (folder === 'clothing_state') return ['clothing_appearance', category];
  if ((folder === 'body_detail' || folder === 'body') && category === 'surface_decor') {
    return ['body_detail', 'surface_stain'];
  }
  if (folder === 'nature' && category === 'rose') return ['nature', 'flower_species'];
  if (folder === 'urban_architecture' && category === 'surface') return ['building_parts', 'surface'];
  return [folder, category];
}

function migrateV12CategoryLocations(folderId, categoryId) {
  return [migrateV12Location(folderId, categoryId)];
}

const V13_CHANGED_CATEGORY_KEYS = new Set([
  ['traditional_clothes', 'traditional_india'],
  ['traditional_clothes', 'traditional_central_west'],
  ['traditional_clothes', 'traditional_africa'],
  ['protective_clothes', 'torso_armor'],
  ['protective_clothes', 'powered_armor'],
  ['protective_clothes', 'pads_support'],
  ['protective_clothes', 'protective_suit']
].map(row => rowKey(row)));

const V13_PAD_SUPPORT_TAGS = [
  'knee_pads', 'arm_guards', 'shoulder_pads', 'elbow_pads',
  'wrist_guards', 'shin_guards', 'chest_guard', 'single_knee_pad',
  'cast', 'single_elbow_pad', 'arm_sling', 'knee_guards',
  'single_arm_guard', 'chest_protector', 'knee_brace', 'leg_cast'
];

function migrateV13Location(folderId, categoryId, tagName = '') {
  const folder = String(folderId);
  const category = String(categoryId);
  const name = String(tagName || '').toLowerCase();
  const key = tupleKey(folder, category);

  if (folder === 'traditional_clothes' && [
    'traditional_india', 'traditional_central_west', 'traditional_africa'
  ].includes(category)) {
    return ['traditional_clothes', 'traditional_other'];
  }
  if (key === tupleKey('protective_clothes', 'powered_armor')) {
    return ['protective_clothes', 'protective_suit'];
  }
  if (key === tupleKey('protective_clothes', 'pads_support')) {
    if (['cast', 'arm_sling', 'leg_cast'].includes(name) || /(medical_sling|splint)/.test(name)) {
      return ['body_detail', 'bandage_patch'];
    }
    if (name.includes('shoulder')) return ['protective_clothes', 'shoulder_armor'];
    if (/(arm_|elbow|wrist|forearm)/.test(name)) return ['protective_clothes', 'arm_armor'];
    if (/(knee|shin|leg_|thigh|ankle)/.test(name)) return ['protective_clothes', 'leg_armor'];
    if (/(chest_|torso_)/.test(name)) return ['protective_clothes', 'torso_armor'];
    return ['protective_clothes', 'protective_suit'];
  }
  if (key === tupleKey('protective_clothes', 'torso_armor')) {
    if (/(power|powered|exosuit|bulletproof|flak|ballistic)/.test(name) || name === 'body_armor') {
      return ['protective_clothes', 'protective_suit'];
    }
    if (/(chain|mail|leather|scale|gambeson|lamellar)/.test(name)) {
      return ['protective_clothes', 'flexible_armor'];
    }
    if (/(arm_|elbow|wrist|gauntlet|rondel)/.test(name)) {
      return ['protective_clothes', 'arm_armor'];
    }
    if (/(leg_|knee|shin|greave|codpiece|tasset)/.test(name)) {
      return ['protective_clothes', 'leg_armor'];
    }
    if (/(chest|breast|cuirass|torso|muneate|gorget|boobplate|plackart|armored_corset)/.test(name)) {
      return ['protective_clothes', 'torso_armor'];
    }
    return ['protective_clothes', 'full_armor'];
  }
  return [folder, category];
}

function migrateV13CategoryLocations(folderId, categoryId) {
  const key = tupleKey(folderId, categoryId);
  const expansions = new Map([
    [tupleKey('protective_clothes', 'torso_armor'), [
      ['protective_clothes', 'full_armor'],
      ['protective_clothes', 'torso_armor'],
      ['protective_clothes', 'arm_armor'],
      ['protective_clothes', 'leg_armor'],
      ['protective_clothes', 'flexible_armor'],
      ['protective_clothes', 'protective_suit']
    ]],
    [tupleKey('protective_clothes', 'pads_support'), [
      ['protective_clothes', 'torso_armor'],
      ['protective_clothes', 'shoulder_armor'],
      ['protective_clothes', 'arm_armor'],
      ['protective_clothes', 'leg_armor'],
      ['body_detail', 'bandage_patch']
    ]]
  ]);
  return expansions.get(key) || [migrateV13Location(folderId, categoryId)];
}

function migrateV13OverrideCategoryLocations(folderId, categoryId) {
  const key = tupleKey(folderId, categoryId);
  if (key === tupleKey('protective_clothes', 'pads_support')) return [];
  // These two categories still exist.  Their labels or colors should remain
  // attached to that same user-facing category rather than being copied onto
  // every new semantic destination.
  if (key === tupleKey('protective_clothes', 'torso_armor')
      || key === tupleKey('protective_clothes', 'protective_suit')) {
    return [[String(folderId), String(categoryId)]];
  }
  return [migrateV13Location(folderId, categoryId)];
}

const V14_CHANGED_CATEGORY_KEYS = new Set([
  tupleKey('legwear_footwear', 'tall_boots'),
  tupleKey('other', 'other_a_e')
]);

const V14_TALL_BOOT_TAGS = [
  'thigh_boots', 'knee_boots', 'thighhighs_under_boots',
  'single_thigh_boot', 'single_knee_boot'
];

function migrateV14Location(folderId, categoryId, tagName = '') {
  const folder = String(folderId);
  const category = String(categoryId);
  const name = String(tagName || '').toLowerCase();
  if (name === 'bootjob' && folder === 'other' && category === 'other_a_e') {
    return ['adult', 'adult_sex'];
  }
  if (folder === 'legwear_footwear' && category === 'tall_boots') {
    if (name === 'thighhighs_under_boots') return ['legwear_footwear', 'stockings'];
    return ['legwear_footwear', 'short_boots'];
  }
  return [folder, category];
}

function migrateV14CategoryLocations(folderId, categoryId) {
  return [migrateV14Location(folderId, categoryId)];
}

function catalogTagLocationIndex(catalog) {
  const index = new Map();
  (catalog?.folders || []).forEach(folder => (folder.categories || []).forEach(category => {
    (category.tags || []).forEach(tag => index.set(tagKey(tag.name), [folder.id, category.id]));
  }));
  return index;
}

const LEGACY_REMOVED_CATEGORY_KEYS = new Set([
  ['hair', 'hair_accessory'], ['face', 'brows_nose'], ['clothes_special', 'sleep_casual'],
  ['underwear_swim', 'underwear_design'], ['creatures', 'animal_feature'],
  ['light_effect', 'magic_effect'], ['clothing_detail', 'clothing_state'],
  ['clothing_detail', 'clothing_structure'], ['clothes_main', 'tops'],
  ['clothes_main', 'outerwear'], ['digital_media', 'phone_computer'],
  ['digital_media', 'camera_media'], ['culture_objects', 'phone_computer'],
  ['culture_objects', 'camera_media'], ['body', 'chest'], ['body', 'waist_legs'],
  ['body', 'arms_hands_feet'], ['adult', 'adult_gore'], ['people', 'relationship'],
  ['body', 'body_marks'], ['text_meta', 'symbol'],
  ['legwear_footwear', 'armor'], ['legwear_footwear', 'helmet_protective'],
  ['clothes_main', 'suit'], ['transport_play', 'sports'], ['transport_play', 'games'],
  ['transport_play', 'toys'], ['creatures', 'plant'], ['creatures', 'mineral'],
  ['text_meta', 'meme'], ['text_meta', 'cosplay'], ['text_meta', 'censorship'],
  ['text_meta', 'meta']
].map(row => rowKey(row)));

function formatCount(value) {
  return value >= 1000000 ? `${(value / 1000000).toFixed(1)}m` : value >= 1000 ? `${Math.round(value / 1000)}k` : String(value);
}

function clampWeight(value) {
  return Math.max(.1, Math.min(2, Math.round((Number(value) || 1) * 10) / 10));
}

function promptToken(item) {
  return Math.abs(item.weight - 1) < .01 ? item.name : `(${item.name}:${item.weight.toFixed(1)})`;
}

function promptText() {
  return state.selected.map(promptToken).join(', ');
}

function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"]/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[char]));
}

function safeAccent(value) {
  return /^#[0-9a-f]{6}$/i.test(String(value || '')) ? value : '#78a7ff';
}

function showToast(text, duration = 1800) {
  els.toast.textContent = text;
  els.toast.classList.add('show');
  clearTimeout(showToast.timer);
  showToast.timer = setTimeout(() => els.toast.classList.remove('show'), duration);
}

function save() {
  try {
    localStorage.setItem(SESSION_KEY, JSON.stringify({
      schemaVersion: 2,
      selected: state.selected,
      folderId: state.folderId,
      categoryId: state.categoryId,
      showNsfw: state.showNsfw
    }));
  } catch {
    showToast('当前选择保存失败');
  }
}

function restore() {
  try {
    return JSON.parse(localStorage.getItem(SESSION_KEY)) || {};
  } catch {
    return {};
  }
}

function applyUiScale(value, persist = false) {
  const scale = Math.max(100, Math.min(140, Number(value) || 100));
  document.documentElement.style.removeProperty('--user-font-scale');
  document.documentElement.style.zoom = String(scale / 100);
  document.body.style.overflow = scale > 100 ? 'auto' : '';
  $('#font-scale').value = scale;
  $('#font-scale-value').textContent = `${scale}%`;
  if (persist) localStorage.setItem('prompt-atelier-ui-scale', String(scale));
}

function openSettings() {
  const saved = Number(localStorage.getItem('prompt-atelier-ui-scale') || 100);
  applyUiScale(saved);
  $('#settings-backdrop').hidden = false;
  $('#settings-panel').hidden = false;
}

function closeSettings() {
  $('#settings-backdrop').hidden = true;
  $('#settings-panel').hidden = true;
}

function defaultLibraryEdits(baseCatalogVersion = 0) {
  return {
    schemaVersion: 1,
    baseCatalogVersion,
    updatedAt: null,
    added: { folders: [], categories: [], tags: [] },
    overrides: { folders: {}, categories: {}, tags: {} },
    removed: { folders: [], categories: [], tags: [] },
    order: { folders: [], categories: {}, tags: {} }
  };
}

function objectOrEmpty(value) {
  return value && typeof value === 'object' && !Array.isArray(value) ? value : {};
}

function normalizeLibraryEdits(raw, baseCatalog) {
  const baseCatalogVersion = Number(baseCatalog?.version) || 0;
  const currentTagLocations = catalogTagLocationIndex(baseCatalog);
  const clean = defaultLibraryEdits(baseCatalogVersion);
  if (!raw || raw.schemaVersion !== 1) return clean;
  const previousCatalogVersion = Number(raw.baseCatalogVersion) || 0;
  const added = objectOrEmpty(raw.added);
  const overrides = objectOrEmpty(raw.overrides);
  const removed = objectOrEmpty(raw.removed);
  const order = objectOrEmpty(raw.order);
  clean.baseCatalogVersion = previousCatalogVersion || baseCatalogVersion;
  clean.updatedAt = typeof raw.updatedAt === 'string' ? raw.updatedAt : null;
  clean.added.folders = Array.isArray(added.folders) ? added.folders.filter(item => item && item.id && item.name) : [];
  clean.added.categories = Array.isArray(added.categories) ? added.categories.filter(item => item && item.id && item.folderId && item.name) : [];
  clean.added.tags = Array.isArray(added.tags) ? added.tags.filter(item => item && item.id && item.folderId && item.categoryId && item.name) : [];
  clean.overrides.folders = objectOrEmpty(overrides.folders);
  clean.overrides.categories = objectOrEmpty(overrides.categories);
  clean.overrides.tags = objectOrEmpty(overrides.tags);
  clean.removed.folders = Array.isArray(removed.folders) ? removed.folders.filter(Boolean).map(String) : [];
  clean.removed.categories = Array.isArray(removed.categories) ? removed.categories.filter(row => Array.isArray(row) && row.length === 2) : [];
  clean.removed.tags = Array.isArray(removed.tags) ? removed.tags.filter(row => Array.isArray(row) && row.length === 3) : [];
  clean.order.folders = Array.isArray(order.folders) ? order.folders.filter(Boolean).map(String) : [];
  clean.order.categories = objectOrEmpty(order.categories);
  clean.order.tags = objectOrEmpty(order.tags);

  if (previousCatalogVersion < 7) {
    clean.added.tags = clean.added.tags.map(tag => {
      const oldCategoryWasRemoved = LEGACY_REMOVED_CATEGORY_KEYS.has(tupleKey(tag.folderId, tag.categoryId));
      const [folderId, categoryId] = (oldCategoryWasRemoved && currentTagLocations.get(tagKey(tag.name)))
        || migrateLegacyLocation(tag.folderId, tag.categoryId, tag.name);
      return { ...tag, folderId, categoryId };
    });
    clean.removed.categories = clean.removed.categories
      .flatMap(([folderId, categoryId]) => migrateLegacyCategoryLocations(folderId, categoryId))
      .filter((row, index, rows) => rows.findIndex(candidate => rowKey(candidate) === rowKey(row)) === index);
    clean.removed.tags = clean.removed.tags.map(([folderId, categoryId, name]) => {
      const migrated = currentTagLocations.get(tagKey(name)) || migrateLegacyLocation(folderId, categoryId, name);
      return [migrated[0], migrated[1], name];
    });
    const migratedOverrides = {};
    Object.entries(clean.overrides.categories).forEach(([key, value]) => {
      try {
        const row = JSON.parse(key);
        if (!Array.isArray(row) || row.length !== 2) return;
        const migrated = migrateLegacyLocation(row[0], row[1]);
        const migratedKey = tupleKey(...migrated);
        migratedOverrides[migratedKey] = { ...objectOrEmpty(migratedOverrides[migratedKey]), ...objectOrEmpty(value) };
      } catch { /* Ignore malformed legacy keys. */ }
    });
    clean.overrides.categories = migratedOverrides;
    clean.baseCatalogVersion = baseCatalogVersion;
  }
  if (previousCatalogVersion < 8) {
    clean.added.categories = clean.added.categories.map(category => {
      const [folderId] = migrateV8Location(category.folderId, category.id);
      return { ...category, folderId };
    });
    clean.added.tags = clean.added.tags.map(tag => {
      const oldCategoryChanged = V8_CHANGED_CATEGORY_KEYS.has(tupleKey(tag.folderId, tag.categoryId));
      const [folderId, categoryId] = (oldCategoryChanged && currentTagLocations.get(tagKey(tag.name)))
        || migrateV8Location(tag.folderId, tag.categoryId, tag.name);
      return { ...tag, folderId, categoryId };
    });
    clean.removed.categories = clean.removed.categories
      .flatMap(([folderId, categoryId]) => migrateV8CategoryLocations(folderId, categoryId))
      .filter((row, index, rows) => rows.findIndex(candidate => rowKey(candidate) === rowKey(row)) === index);
    clean.removed.tags = clean.removed.tags.map(([folderId, categoryId, name]) => {
      const migrated = currentTagLocations.get(tagKey(name)) || migrateV8Location(folderId, categoryId, name);
      return [migrated[0], migrated[1], name];
    });
    const folderExpansions = new Map([
      ['body', ['body', 'body_detail']],
      ['clothes_main', ['clothes_main', 'outerwear_suits']],
      ['clothes_special', ['uniform_costume', 'traditional_clothes', 'protective_clothes']],
      ['clothing_detail', ['clothing_appearance', 'clothing_detail', 'clothing_state']],
      ['accessories', ['head_accessories', 'jewelry_accessories', 'accessories']],
      ['creatures', ['animal_traits', 'creatures']],
      ['indoor_scene', ['indoor_scene', 'urban_architecture']],
      ['outdoor_scene', ['outdoor_scene', 'background']],
      ['text_meta', ['text_meta', 'symbols']],
      ['adult', ['adult_body', 'adult', 'adult_kink', 'sensitive']]
    ]);
    clean.removed.folders = clean.removed.folders
      .flatMap(folderId => folderExpansions.get(folderId) || [folderId])
      .filter((folderId, index, rows) => rows.indexOf(folderId) === index);
    const migratedOverrides = {};
    Object.entries(clean.overrides.categories).forEach(([key, value]) => {
      try {
        const row = JSON.parse(key);
        if (!Array.isArray(row) || row.length !== 2) return;
        migrateV8CategoryLocations(row[0], row[1]).forEach(migrated => {
          const migratedKey = tupleKey(...migrated);
          migratedOverrides[migratedKey] = { ...objectOrEmpty(migratedOverrides[migratedKey]), ...objectOrEmpty(value) };
        });
      } catch { /* Ignore malformed legacy keys. */ }
    });
    clean.overrides.categories = migratedOverrides;
    // The built-in hierarchy changed substantially in v8.  Old drag orders
    // cannot describe the new folders/categories reliably, so use the audited
    // default order while preserving all user content and edits above.
    clean.order = { folders: [], categories: {}, tags: {} };
    clean.baseCatalogVersion = baseCatalogVersion;
  }
  if (previousCatalogVersion < 9) {
    // v9 changes only the audited top-level library sequence.  Keep category
    // and tag drag orders, but let every user receive the new folder order.
    clean.order.folders = [];
    clean.baseCatalogVersion = baseCatalogVersion;
  }
  if (previousCatalogVersion < 10) {
    clean.added.tags = clean.added.tags.map(tag => {
      const oldCategoryChanged = V10_CHANGED_CATEGORY_KEYS.has(tupleKey(tag.folderId, tag.categoryId));
      const [folderId, categoryId] = (oldCategoryChanged && currentTagLocations.get(tagKey(tag.name)))
        || migrateV10Location(tag.folderId, tag.categoryId);
      return { ...tag, folderId, categoryId };
    });
    clean.removed.categories = clean.removed.categories
      .flatMap(([folderId, categoryId]) => migrateV10CategoryLocations(folderId, categoryId))
      .filter((row, index, rows) => rows.findIndex(candidate => rowKey(candidate) === rowKey(row)) === index);
    clean.removed.tags = clean.removed.tags.map(([folderId, categoryId, name]) => {
      const migrated = currentTagLocations.get(tagKey(name)) || migrateV10Location(folderId, categoryId);
      return [migrated[0], migrated[1], name];
    });
    const folderExpansions = new Map([
      ['uniform_costume', ['uniform_costume', 'franchise_clothes']],
      ['urban_architecture', ['building_parts', 'urban_architecture']]
    ]);
    clean.removed.folders = clean.removed.folders
      .flatMap(folderId => folderExpansions.get(folderId) || [folderId])
      .filter((folderId, index, rows) => rows.indexOf(folderId) === index);
    if (clean.removed.folders.includes('adult_body')) {
      clean.removed.categories.push(['adult', 'adult_suggestive']);
    }
    const migratedOverrides = {};
    Object.entries(clean.overrides.categories).forEach(([key, value]) => {
      try {
        const row = JSON.parse(key);
        if (!Array.isArray(row) || row.length !== 2) return;
        migrateV10CategoryLocations(row[0], row[1]).forEach(migrated => {
          const migratedKey = tupleKey(...migrated);
          migratedOverrides[migratedKey] = { ...objectOrEmpty(migratedOverrides[migratedKey]), ...objectOrEmpty(value) };
        });
      } catch { /* Ignore malformed legacy keys. */ }
    });
    clean.overrides.categories = migratedOverrides;
    // Several v9 categories were split or moved.  Reset only drag order; all
    // custom content, deletions and edits above remain preserved.
    clean.order = { folders: [], categories: {}, tags: {} };
    clean.baseCatalogVersion = baseCatalogVersion;
  }
  if (previousCatalogVersion < 11) {
    clean.added.tags = clean.added.tags.map(tag => {
      const oldCategoryChanged = V11_CHANGED_CATEGORY_KEYS.has(tupleKey(tag.folderId, tag.categoryId));
      const [folderId, categoryId] = (oldCategoryChanged && currentTagLocations.get(tagKey(tag.name)))
        || migrateV11Location(tag.folderId, tag.categoryId, tag.name);
      return { ...tag, folderId, categoryId };
    });
    clean.removed.categories = clean.removed.categories
      .flatMap(([folderId, categoryId]) => migrateV11CategoryLocations(folderId, categoryId))
      .filter((row, index, rows) => rows.findIndex(candidate => rowKey(candidate) === rowKey(row)) === index);
    clean.removed.tags = clean.removed.tags.map(([folderId, categoryId, name]) => {
      const migrated = currentTagLocations.get(tagKey(name)) || migrateV11Location(folderId, categoryId, name);
      return [migrated[0], migrated[1], name];
    });
    const migratedOverrides = {};
    Object.entries(clean.overrides.categories).forEach(([key, value]) => {
      try {
        const row = JSON.parse(key);
        if (!Array.isArray(row) || row.length !== 2) return;
        migrateV11CategoryLocations(row[0], row[1]).forEach(migrated => {
          const migratedKey = tupleKey(...migrated);
          migratedOverrides[migratedKey] = { ...objectOrEmpty(migratedOverrides[migratedKey]), ...objectOrEmpty(value) };
        });
      } catch { /* Ignore malformed legacy keys. */ }
    });
    clean.overrides.categories = migratedOverrides;
    // Removed and merged built-in categories invalidate old drag order.  User
    // content and edits remain intact, while the audited default order wins.
    clean.order = { folders: [], categories: {}, tags: {} };
    clean.baseCatalogVersion = baseCatalogVersion;
  }
  if (previousCatalogVersion < 12) {
    clean.added.categories = clean.added.categories.map(category => {
      const [folderId, id] = migrateV12Location(category.folderId, category.id);
      return { ...category, folderId, id };
    });
    clean.added.tags = clean.added.tags.map(tag => {
      const oldCategoryChanged = V12_CHANGED_CATEGORY_KEYS.has(tupleKey(tag.folderId, tag.categoryId));
      const [folderId, categoryId] = (oldCategoryChanged && currentTagLocations.get(tagKey(tag.name)))
        || migrateV12Location(tag.folderId, tag.categoryId);
      return { ...tag, folderId, categoryId };
    });
    clean.removed.categories = clean.removed.categories
      .flatMap(([folderId, categoryId]) => migrateV12CategoryLocations(folderId, categoryId));
    clean.removed.tags = clean.removed.tags.map(([folderId, categoryId, name]) => {
      const oldCategoryChanged = V12_CHANGED_CATEGORY_KEYS.has(tupleKey(folderId, categoryId));
      const migrated = (oldCategoryChanged && currentTagLocations.get(tagKey(name)))
        || migrateV12Location(folderId, categoryId);
      return [migrated[0], migrated[1], name];
    });

    // The removed clothing-state folder was merged into clothing_appearance.
    // Preserve the user's intent by removing only its three former built-in
    // categories; removing the destination folder would also hide unrelated
    // appearance categories and user-created content.
    if (clean.removed.folders.includes('clothing_state')) {
      clean.removed.folders = clean.removed.folders.filter(folderId => folderId !== 'clothing_state');
      ['damaged_dirty', 'unworn_missing', 'open_wear'].forEach(categoryId => {
        clean.removed.categories.push(['clothing_appearance', categoryId]);
      });
    }
    clean.removed.folders = clean.removed.folders
      .filter((folderId, index, rows) => rows.indexOf(folderId) === index);
    clean.removed.categories = clean.removed.categories
      .filter((row, index, rows) => rows.findIndex(candidate => rowKey(candidate) === rowKey(row)) === index);

    if (Object.prototype.hasOwnProperty.call(clean.overrides.folders, 'clothing_state')) {
      const stateOverride = objectOrEmpty(clean.overrides.folders.clothing_state);
      const appearanceOverride = objectOrEmpty(clean.overrides.folders.clothing_appearance);
      clean.overrides.folders = { ...clean.overrides.folders };
      clean.overrides.folders.clothing_appearance = { ...stateOverride, ...appearanceOverride };
      delete clean.overrides.folders.clothing_state;
    }
    const migratedCategoryOverrides = {};
    Object.entries(clean.overrides.categories).forEach(([key, value]) => {
      try {
        const row = JSON.parse(key);
        if (!Array.isArray(row) || row.length !== 2) return;
        migrateV12CategoryLocations(row[0], row[1]).forEach(migrated => {
          const migratedKey = tupleKey(...migrated);
          migratedCategoryOverrides[migratedKey] = {
            ...objectOrEmpty(migratedCategoryOverrides[migratedKey]),
            ...objectOrEmpty(value)
          };
        });
      } catch { /* Ignore malformed legacy keys. */ }
    });
    clean.overrides.categories = migratedCategoryOverrides;

    const migratedTagOverrides = {};
    Object.entries(clean.overrides.tags).forEach(([key, value]) => {
      try {
        const row = JSON.parse(key);
        if (!Array.isArray(row) || row.length !== 3) return;
        const oldCategoryChanged = V12_CHANGED_CATEGORY_KEYS.has(tupleKey(row[0], row[1]));
        const migrated = (oldCategoryChanged && currentTagLocations.get(tagKey(row[2])))
          || migrateV12Location(row[0], row[1]);
        const migratedKey = tupleKey(migrated[0], migrated[1], row[2]);
        migratedTagOverrides[migratedKey] = {
          ...objectOrEmpty(migratedTagOverrides[migratedKey]),
          ...objectOrEmpty(value)
        };
      } catch { /* Ignore malformed legacy keys. */ }
    });
    clean.overrides.tags = migratedTagOverrides;

    // Merged and moved categories make legacy drag-order keys ambiguous.
    // Reset only ordering while retaining all content, removals and overrides.
    clean.order = { folders: [], categories: {}, tags: {} };
    clean.baseCatalogVersion = baseCatalogVersion;
  }
  if (previousCatalogVersion < 13) {
    clean.added.tags = clean.added.tags.map(tag => {
      const oldCategoryChanged = V13_CHANGED_CATEGORY_KEYS.has(tupleKey(tag.folderId, tag.categoryId));
      const [folderId, categoryId] = (oldCategoryChanged && currentTagLocations.get(tagKey(tag.name)))
        || migrateV13Location(tag.folderId, tag.categoryId, tag.name);
      return { ...tag, folderId, categoryId };
    });

    const removedPadSupport = clean.removed.categories.some(
      ([folderId, categoryId]) => tupleKey(folderId, categoryId) === tupleKey('protective_clothes', 'pads_support')
    );
    if (removedPadSupport) {
      V13_PAD_SUPPORT_TAGS.forEach(name => {
        const migrated = currentTagLocations.get(tagKey(name))
          || migrateV13Location('protective_clothes', 'pads_support', name);
        clean.removed.tags.push([migrated[0], migrated[1], name]);
      });
    }
    clean.removed.categories = clean.removed.categories
      .filter(([folderId, categoryId]) => (
        tupleKey(folderId, categoryId) !== tupleKey('protective_clothes', 'pads_support')
      ))
      .flatMap(([folderId, categoryId]) => migrateV13CategoryLocations(folderId, categoryId))
      .filter((row, index, rows) => rows.findIndex(candidate => rowKey(candidate) === rowKey(row)) === index);

    clean.removed.tags = clean.removed.tags
      .map(([folderId, categoryId, name]) => {
        const oldCategoryChanged = V13_CHANGED_CATEGORY_KEYS.has(tupleKey(folderId, categoryId));
        const migrated = (oldCategoryChanged && currentTagLocations.get(tagKey(name)))
          || migrateV13Location(folderId, categoryId, name);
        return [migrated[0], migrated[1], name];
      })
      .filter((row, index, rows) => rows.findIndex(candidate => rowKey(candidate) === rowKey(row)) === index);

    const categoryOverrideEntries = Object.entries(clean.overrides.categories)
      .map(entry => {
        try {
          const row = JSON.parse(entry[0]);
          return { entry, row, changed: Array.isArray(row) && V13_CHANGED_CATEGORY_KEYS.has(tupleKey(row[0], row[1])) };
        } catch {
          return { entry, row: null, changed: false };
        }
      })
      .sort((a, b) => Number(b.changed) - Number(a.changed));
    const migratedCategoryOverrides = {};
    categoryOverrideEntries.forEach(({ entry: [key, value], row }) => {
      if (!Array.isArray(row) || row.length !== 2) return;
      migrateV13OverrideCategoryLocations(row[0], row[1]).forEach(migrated => {
        const migratedKey = tupleKey(...migrated);
        migratedCategoryOverrides[migratedKey] = {
          ...objectOrEmpty(migratedCategoryOverrides[migratedKey]),
          ...objectOrEmpty(value)
        };
      });
    });
    clean.overrides.categories = migratedCategoryOverrides;

    const tagOverrideEntries = Object.entries(clean.overrides.tags)
      .map(entry => {
        try {
          const row = JSON.parse(entry[0]);
          return { entry, row, changed: Array.isArray(row) && V13_CHANGED_CATEGORY_KEYS.has(tupleKey(row[0], row[1])) };
        } catch {
          return { entry, row: null, changed: false };
        }
      })
      .sort((a, b) => Number(b.changed) - Number(a.changed));
    const migratedTagOverrides = {};
    tagOverrideEntries.forEach(({ entry: [key, value], row, changed }) => {
      if (!Array.isArray(row) || row.length !== 3) return;
      const migrated = (changed && currentTagLocations.get(tagKey(row[2])))
        || migrateV13Location(row[0], row[1], row[2]);
      const migratedKey = tupleKey(migrated[0], migrated[1], row[2]);
      migratedTagOverrides[migratedKey] = {
        ...objectOrEmpty(migratedTagOverrides[migratedKey]),
        ...objectOrEmpty(value)
      };
    });
    clean.overrides.tags = migratedTagOverrides;

    // Category merges and tag redistribution invalidate all three stored drag
    // order levels.  Restore the audited built-in order while preserving edits.
    clean.order = { folders: [], categories: {}, tags: {} };
    clean.baseCatalogVersion = baseCatalogVersion;
  }
  if (previousCatalogVersion < 14) {
    const addedTallBootTagNames = clean.added.tags
      .filter(tag => tupleKey(tag.folderId, tag.categoryId) === tupleKey('legwear_footwear', 'tall_boots'))
      .map(tag => tag.name);
    clean.added.tags = clean.added.tags.map(tag => {
      const [folderId, categoryId] = migrateV14Location(tag.folderId, tag.categoryId, tag.name);
      return { ...tag, folderId, categoryId };
    });

    const removedTallBoots = clean.removed.categories.some(
      ([folderId, categoryId]) => tupleKey(folderId, categoryId) === tupleKey('legwear_footwear', 'tall_boots')
    );
    if (removedTallBoots) {
      [...V14_TALL_BOOT_TAGS, ...addedTallBootTagNames].forEach(name => {
        const migrated = currentTagLocations.get(tagKey(name))
          || migrateV14Location('legwear_footwear', 'tall_boots', name);
        clean.removed.tags.push([migrated[0], migrated[1], name]);
      });
    }
    const removedOtherAe = clean.removed.categories.some(
      ([folderId, categoryId]) => tupleKey(folderId, categoryId) === tupleKey('other', 'other_a_e')
    );
    if (removedOtherAe) clean.removed.tags.push(['adult', 'adult_sex', 'bootjob']);
    clean.removed.categories = clean.removed.categories
      .filter(([folderId, categoryId]) => (
        tupleKey(folderId, categoryId) !== tupleKey('legwear_footwear', 'tall_boots')
      ))
      .flatMap(([folderId, categoryId]) => migrateV14CategoryLocations(folderId, categoryId))
      .filter((row, index, rows) => rows.findIndex(candidate => rowKey(candidate) === rowKey(row)) === index);
    clean.removed.tags = clean.removed.tags
      .map(([folderId, categoryId, name]) => {
        const migrated = migrateV14Location(folderId, categoryId, name);
        return [migrated[0], migrated[1], name];
      })
      .filter((row, index, rows) => rows.findIndex(candidate => rowKey(candidate) === rowKey(row)) === index);

    const categoryOverrideEntries = Object.entries(clean.overrides.categories)
      .map(entry => {
        try {
          const row = JSON.parse(entry[0]);
          return { entry, row, changed: Array.isArray(row) && V14_CHANGED_CATEGORY_KEYS.has(tupleKey(row[0], row[1])) };
        } catch {
          return { entry, row: null, changed: false };
        }
      })
      .sort((a, b) => Number(b.changed) - Number(a.changed));
    const migratedCategoryOverrides = {};
    categoryOverrideEntries.forEach(({ entry: [, value], row }) => {
      if (!Array.isArray(row) || row.length !== 2) return;
      const migrated = migrateV14Location(row[0], row[1]);
      const migratedKey = tupleKey(...migrated);
      migratedCategoryOverrides[migratedKey] = {
        ...objectOrEmpty(migratedCategoryOverrides[migratedKey]),
        ...objectOrEmpty(value)
      };
    });
    clean.overrides.categories = migratedCategoryOverrides;

    const tagOverrideEntries = Object.entries(clean.overrides.tags)
      .map(entry => {
        try {
          const row = JSON.parse(entry[0]);
          return { entry, row, changed: Array.isArray(row) && V14_CHANGED_CATEGORY_KEYS.has(tupleKey(row[0], row[1])) };
        } catch {
          return { entry, row: null, changed: false };
        }
      })
      .sort((a, b) => Number(b.changed) - Number(a.changed));
    const migratedTagOverrides = {};
    tagOverrideEntries.forEach(({ entry: [, value], row }) => {
      if (!Array.isArray(row) || row.length !== 3) return;
      const migrated = migrateV14Location(row[0], row[1], row[2]);
      const migratedKey = tupleKey(migrated[0], migrated[1], row[2]);
      migratedTagOverrides[migratedKey] = {
        ...objectOrEmpty(migratedTagOverrides[migratedKey]),
        ...objectOrEmpty(value)
      };
    });
    clean.overrides.tags = migratedTagOverrides;

    // Only the footwear category sequence changed.  Preserve unrelated drag
    // ordering while restoring the merged boot category and its tag order.
    clean.order.categories = { ...clean.order.categories };
    delete clean.order.categories.legwear_footwear;
    clean.order.tags = { ...clean.order.tags };
    delete clean.order.tags[tupleKey('legwear_footwear', 'short_boots')];
    delete clean.order.tags[tupleKey('legwear_footwear', 'tall_boots')];
    clean.baseCatalogVersion = baseCatalogVersion;
  }
  return clean;
}

function loadLibraryEdits(baseCatalog) {
  try {
    const raw = JSON.parse(localStorage.getItem(LIBRARY_KEY));
    const normalized = normalizeLibraryEdits(raw, baseCatalog);
    if (raw?.baseCatalogVersion !== normalized.baseCatalogVersion) {
      localStorage.setItem(LIBRARY_KEY, JSON.stringify(normalized));
    }
    return normalized;
  } catch {
    return defaultLibraryEdits(Number(baseCatalog?.version) || 0);
  }
}

function cloneData(value) {
  return typeof structuredClone === 'function' ? structuredClone(value) : JSON.parse(JSON.stringify(value));
}

function applyExplicitOrder(items, order, keyOf) {
  if (!Array.isArray(order) || !order.length) return items;
  const positions = new Map(order.map((key, index) => [String(key), index]));
  return items.map((item, index) => ({ item, index }))
    .sort((a, b) => {
      const aPosition = positions.get(String(keyOf(a.item)));
      const bPosition = positions.get(String(keyOf(b.item)));
      if (aPosition === undefined && bPosition === undefined) return a.index - b.index;
      if (aPosition === undefined) return 1;
      if (bPosition === undefined) return -1;
      return aPosition - bPosition;
    })
    .map(entry => entry.item);
}

function stableTagId(tag) {
  return String(tag?.id || tag?._sourceName || tag?.name || '');
}

function applyLibraryEdits(baseCatalog, edits) {
  const removedFolders = new Set(edits.removed.folders.map(String));
  const removedCategories = new Set(edits.removed.categories.map(rowKey));
  const removedTags = new Set(edits.removed.tags.map(rowKey));
  const uniqueTags = new Set();

  const folderSources = applyExplicitOrder([
    ...baseCatalog.folders.map(folder => ({ value: folder, builtin: true })),
    ...edits.added.folders.map(folder => ({ value: { ...folder, categories: [] }, builtin: false }))
  ], edits.order?.folders, source => source.value.id);

  const folders = folderSources
    .filter(source => !removedFolders.has(String(source.value.id)))
    .map(source => {
      const originalFolder = source.value;
      const folderOverride = source.builtin ? objectOrEmpty(edits.overrides.folders[originalFolder.id]) : {};
      const folder = { ...originalFolder, ...folderOverride };
      const categorySources = applyExplicitOrder([
        ...(Array.isArray(originalFolder.categories) ? originalFolder.categories : []).map(category => ({ value: category, builtin: source.builtin })),
        ...edits.added.categories
          .filter(category => category.folderId === folder.id)
          .map(category => ({ value: { ...category, tags: [] }, builtin: false }))
      ], edits.order?.categories?.[folder.id], categorySource => categorySource.value.id);

      folder.categories = categorySources
        .filter(categorySource => !removedCategories.has(tupleKey(folder.id, categorySource.value.id)))
        .map(categorySource => {
          const originalCategory = categorySource.value;
          const categoryOverride = categorySource.builtin
            ? objectOrEmpty(edits.overrides.categories[tupleKey(folder.id, originalCategory.id)])
            : {};
          const category = { ...originalCategory, ...categoryOverride };
          const tags = (Array.isArray(originalCategory.tags) ? originalCategory.tags : [])
            .filter(tag => !removedTags.has(tupleKey(folder.id, category.id, tag.name)))
            .map(tag => {
              const override = objectOrEmpty(edits.overrides?.tags?.[tupleKey(folder.id, category.id, tag.name)]);
              return { ...tag, ...override, _sourceName: tag.name };
            });
          const addedTags = edits.added.tags
            .filter(tag => tag.folderId === folder.id && tag.categoryId === category.id)
            .map(tag => ({ ...tag, _sourceName: tag.name }));
          category.tags = applyExplicitOrder(
            [...tags, ...addedTags],
            edits.order?.tags?.[tupleKey(folder.id, category.id)],
            stableTagId
          );
          category.tags.forEach(tag => uniqueTags.add(tagKey(tag.name)));
          return category;
        });

      const folderTags = new Set();
      folder.categories.forEach(category => category.tags.forEach(tag => folderTags.add(tagKey(tag.name))));
      folder.tagCount = folderTags.size;
      return folder;
    });

  return {
    ...baseCatalog,
    folders,
    tagCount: uniqueTags.size,
    customTagCount: edits.added.tags.length
  };
}

function baseFolder(folderId) {
  return state.baseCatalog?.folders.find(folder => folder.id === folderId) || null;
}

function baseCategory(folderId, categoryId) {
  return baseFolder(folderId)?.categories.find(category => category.id === categoryId) || null;
}

function baseTag(folderId, categoryId, name) {
  const key = tagKey(name);
  return baseCategory(folderId, categoryId)?.tags.find(tag => tagKey(tag.name) === key) || null;
}

function normalizeActiveLocation() {
  const folder = state.catalog?.folders.find(item => item.id === state.folderId) || state.catalog?.folders[0] || null;
  state.folderId = folder?.id || null;
  const category = folder?.categories.find(item => item.id === state.categoryId) || folder?.categories[0] || null;
  state.categoryId = category?.id || null;
}

function rebuildCatalog() {
  state.catalog = applyLibraryEdits(state.baseCatalog, state.edits);
  normalizeActiveLocation();
}

function buildTagIndex() {
  const index = new Map();
  const memberships = new Map();
  const searchEntries = [];
  state.catalog.folders.forEach(folder => folder.categories.forEach(category => category.tags.forEach(tag => {
    const key = tagKey(tag.name);
    const membership = { tag, folderId: folder.id, categoryId: category.id };
    if (!index.has(key)) index.set(key, membership);
    if (!memberships.has(key)) memberships.set(key, []);
    memberships.get(key).push(membership);
    const aliases = Array.isArray(tag.aliases) ? tag.aliases.join(' ') : '';
    searchEntries.push({
      ...membership,
      folderName: folder.name,
      categoryName: category.name,
      searchable: `${tag.name} ${tag.cn || ''} ${aliases} ${tag.wiki || ''}`.toLocaleLowerCase('zh-CN')
    });
  })));
  state.tagIndex = index;
  state.tagMemberships = memberships;
  state.searchEntries = searchEntries;
}

function databaseTagDescription(tag) {
  const wiki = String(tag?.wiki || '').trim();
  if (wiki) return wiki;
  const aliases = Array.isArray(tag?.aliases) ? tag.aliases.filter(Boolean).slice(0, 4) : [];
  const details = [];
  if (tag?.cn) details.push(`中文说明：${tag.cn}`);
  if (aliases.length) details.push(`别名：${aliases.join('、')}`);
  return `暂无数据库释义${details.length ? `；${details.join('；')}` : ''}`;
}

function buildDatabaseTagChoices() {
  const choices = new Map();
  state.baseCatalog?.folders.forEach(folder => folder.categories.forEach(category => category.tags.forEach(tag => {
    const key = tagKey(tag.name);
    if (!key) return;
    const location = { folderId: folder.id, categoryId: category.id, folderName: folder.name, categoryName: category.name };
    const richness = String(tag.wiki || '').trim().length * 10
      + String(tag.cn || '').trim().length
      + (Array.isArray(tag.aliases) ? tag.aliases.length : 0);
    const existing = choices.get(key);
    if (existing) {
      existing.locations.push(location);
      if (richness > existing.richness) {
        existing.tag = tag;
        existing.folderId = folder.id;
        existing.categoryId = category.id;
        existing.folderName = folder.name;
        existing.categoryName = category.name;
        existing.richness = richness;
      }
      return;
    }
    choices.set(key, {
      key,
      tag,
      folderId: folder.id,
      categoryId: category.id,
      folderName: folder.name,
      categoryName: category.name,
      locations: [location],
      richness
    });
  })));
  state.databaseTagChoices = Array.from(choices.values()).map(entry => {
    const aliases = Array.isArray(entry.tag.aliases) ? entry.tag.aliases.join(' ') : '';
    const description = databaseTagDescription(entry.tag);
    const pathLabel = `${entry.folderName} › ${entry.categoryName}${entry.locations.length > 1 ? `（另 ${entry.locations.length - 1} 处）` : ''}`;
    return {
      ...entry,
      description,
      pathLabel,
      searchable: `${entry.tag.name} ${entry.tag.cn || ''} ${aliases} ${entry.tag.wiki || ''} ${entry.locations.map(location => `${location.folderName} ${location.categoryName}`).join(' ')}`
        .toLocaleLowerCase('zh-CN')
    };
  }).sort((a, b) => Number(b.tag.count || 0) - Number(a.tag.count || 0)
    || a.tag.name.localeCompare(b.tag.name));
}

function reconcileSelectedOrigins() {
  state.selected = state.selected.filter(item => item && item.name).map(item => {
    const memberships = state.tagMemberships.get(tagKey(item.name)) || [];
    const exact = memberships.find(entry => entry.folderId === item.folderId && entry.categoryId === item.categoryId);
    const sameFolder = memberships.find(entry => entry.folderId === item.folderId);
    const match = exact || sameFolder || memberships[0];
    if (!match) {
      return { ...item, folderId: 'custom', categoryId: null, custom: true };
    }
    return {
      ...item,
      name: match.tag.name,
      cn: item.cn || match.tag.cn,
      folderId: match.folderId,
      categoryId: match.categoryId,
      custom: false
    };
  });
}

function updateDatabaseStat() {
  if (!state.baseCatalog || !state.catalog) return;
  const custom = state.edits.added.tags.length;
  els.dbStat.textContent = `数据库 ${Number(state.baseCatalog.sourceCount || 0).toLocaleString()} 条 · 当前可选 ${Number(state.catalog.tagCount || 0).toLocaleString()} 条${custom ? ` · 自定义 ${custom.toLocaleString()}` : ''}`;
}

function renderLibraries() {
  els.libraryCount.textContent = state.catalog.folders.length;
  els.libraries.classList.toggle('manage-mode', state.manageMode);
  els.toggleManage.classList.toggle('active', state.manageMode);
  els.toggleManage.textContent = state.manageMode ? '完成' : '管理';
  els.libraries.innerHTML = state.catalog.folders.length ? state.catalog.folders.map(folder => `
    <div class="library-card-shell ${state.manageMode ? 'manage-shell' : ''} ${state.manageMode && folder.id === state.folderId ? 'active' : ''}" style="--folder-accent:${safeAccent(folder.accent)}" ${state.manageMode ? `draggable="true" data-manage-type="folder" data-manage-id="${escapeHtml(folder.id)}"` : ''}>
      ${state.manageMode ? '<span class="manage-drag" title="拖动排序" aria-hidden="true">⠿</span>' : ''}
      <button class="library-card ${folder.id === state.folderId ? 'active' : ''}" data-action="open-folder" data-folder="${escapeHtml(folder.id)}" style="--folder-accent:${safeAccent(folder.accent)}">
        <span class="library-icon">${escapeHtml(folder.icon || '◇')}</span>
        <span class="library-copy"><strong>${escapeHtml(folder.name)}</strong><small>${escapeHtml(folder.description || '自定义提示词库')}</small></span>
        <span class="library-meta"><b>${folder.categories.length} 类</b><span>${formatCount(folder.tagCount)} 标签</span></span>
      </button>
      ${state.manageMode ? `<div class="item-manage-actions"><button data-action="edit-folder" data-folder="${escapeHtml(folder.id)}" title="编辑词库" aria-label="编辑词库">✎</button><button class="danger" data-action="delete-folder" data-folder="${escapeHtml(folder.id)}" title="删除词库" aria-label="删除词库">×</button></div>` : ''}
    </div>`).join('') : '<div class="empty-library">还没有提示词库。点击右上角“＋”新建一个。</div>';
}

function keepActiveCategoryVisible() {
  requestAnimationFrame(() => {
    const active = els.tabs.querySelector('.category-tab.active');
    if (!active) return;
    const scrollsVertically = els.tabs.scrollHeight > els.tabs.clientHeight;
    const scrollsHorizontally = els.tabs.scrollWidth > els.tabs.clientWidth;
    if (!scrollsVertically && !scrollsHorizontally) return;
    const container = els.tabs.getBoundingClientRect();
    const item = active.closest('.category-tab-wrap').getBoundingClientRect();
    if (scrollsVertically && item.top < container.top) {
      els.tabs.scrollTop += item.top - container.top - 4;
    } else if (scrollsVertically && item.bottom > container.bottom) {
      els.tabs.scrollTop += item.bottom - container.bottom + 4;
    }
    if (scrollsHorizontally && item.left < container.left) {
      els.tabs.scrollLeft += item.left - container.left - 4;
    } else if (scrollsHorizontally && item.right > container.right) {
      els.tabs.scrollLeft += item.right - container.right + 4;
    }
  });
}

function renderTabs() {
  const folder = currentFolder();
  els.addCategory.disabled = !folder;
  updateSearchScopeUi();
  if (!folder) {
    document.documentElement.style.setProperty('--accent', '#78a7ff');
    els.folderTitle.textContent = '尚未创建词库';
    els.tabs.innerHTML = '<div class="empty-inline">请先从右侧新建提示词库</div>';
    return;
  }
  document.documentElement.style.setProperty('--accent', safeAccent(folder.accent));
  els.folderTitle.textContent = folder.name;
  els.tabs.classList.toggle('manage-mode', state.manageMode);
  els.tabs.innerHTML = folder.categories.length ? folder.categories.map(category => `
    <span class="category-tab-wrap ${state.manageMode ? 'manage-shell' : ''} ${state.manageMode && category.id === state.categoryId ? 'active' : ''}" ${state.manageMode ? `draggable="true" data-manage-type="category" data-manage-id="${escapeHtml(category.id)}"` : ''}>
      ${state.manageMode ? '<span class="manage-drag" title="拖动排序" aria-hidden="true">⠿</span>' : ''}
      <button class="category-tab ${category.id === state.categoryId ? 'active' : ''}" data-action="open-category" data-category="${escapeHtml(category.id)}">${escapeHtml(category.name)}</button>
      ${state.manageMode ? `<span class="category-manage"><button data-action="edit-category" data-category="${escapeHtml(category.id)}" title="重命名分类">✎</button><button class="danger" data-action="delete-category" data-category="${escapeHtml(category.id)}" title="删除分类">×</button></span>` : ''}
    </span>`).join('') : '<div class="empty-inline">此词库暂无分类，点击“＋”新建</div>';
  keepActiveCategoryVisible();
}

function renderCloud() {
  const category = currentCategory();
  els.addTag.disabled = !category;
  els.cloud.classList.toggle('manage-mode', state.manageMode);
  if (!category) {
    els.categoryName.textContent = currentFolder() ? '尚未创建分类' : '暂无词库';
    els.visibleCount.textContent = '';
    els.cloud.innerHTML = '<div class="empty-inline">新建细分类后即可添加标签</div>';
    return;
  }
  const tags = category.tags.filter(tag => state.showNsfw || !tag.nsfw);
  const selectedNames = new Set(state.selected.map(item => tagKey(item.name)));
  els.categoryName.textContent = category.name;
  els.visibleCount.textContent = `共 ${tags.length} 项`;
  els.cloud.innerHTML = tags.length ? tags.map(tag => {
    const aliases = Array.isArray(tag.aliases) ? tag.aliases : [];
    const title = tag.wiki || aliases.join(' / ');
    return `
      <span class="tag-chip-wrap ${state.manageMode ? 'manage-shell' : ''} ${state.manageMode && selectedNames.has(tagKey(tag.name)) ? 'active' : ''}" ${state.manageMode ? `draggable="true" data-manage-type="tag" data-manage-id="${escapeHtml(stableTagId(tag))}"` : ''}>
        ${state.manageMode ? '<span class="manage-drag" title="拖动排序" aria-hidden="true">⠿</span>' : ''}
        <button class="tag-chip ${selectedNames.has(tagKey(tag.name)) ? 'active' : ''}" data-action="toggle-tag" data-tag="${escapeHtml(tag.name)}" title="${escapeHtml(title)}">
          <span class="en">${escapeHtml(tag.name)}</span><span class="cn">${escapeHtml(tag.cn || tag.name.replaceAll('_', ' '))}</span>${tag.nsfw ? '<span class="sensitive">NSFW</span>' : ''}
        </button>
        ${state.manageMode ? `<span class="tag-manage"><button data-action="edit-tag" data-tag="${escapeHtml(tag.name)}" title="编辑标签" aria-label="编辑标签">✎</button><button class="danger" data-action="delete-tag" data-tag="${escapeHtml(tag.name)}" title="从此分类删除" aria-label="删除标签">×</button></span>` : ''}
      </span>`;
  }).join('') : '<div class="empty-inline">此分类暂无可显示标签</div>';
}

function updateSearchScopeUi() {
  if (!els.searchLibrary || !els.searchLocal) return;
  const folder = currentFolder();
  const category = currentCategory();
  if (!folder && state.searchScope === 'library') state.searchScope = 'global';
  if (!category && state.searchScope === 'local') state.searchScope = folder ? 'library' : 'global';
  els.searchGlobal.classList.toggle('active', state.searchScope === 'global');
  els.searchLibrary.classList.toggle('active', state.searchScope === 'library');
  els.searchLocal.classList.toggle('active', state.searchScope === 'local');
  els.searchLibrary.disabled = !folder;
  els.searchLocal.disabled = !category;
  els.searchLibrary.title = folder ? `只搜索“${folder.name}”词库` : '当前没有可搜索的词库';
  els.searchLocal.title = category ? `只搜索“${category.name}”` : '当前没有可搜索的分类';
  if (state.searchScope === 'local' && category) {
    els.searchInput.placeholder = `在“${category.name}”中搜索标签…`;
  } else if (state.searchScope === 'library' && folder) {
    els.searchInput.placeholder = `在“${folder.name}”词库中搜索标签…`;
  } else {
    els.searchInput.placeholder = '搜索标签、中文说明…';
  }
}

function searchEntryScore(entry, query) {
  const name = tagKey(entry.tag.name);
  const cn = String(entry.tag.cn || '').toLocaleLowerCase('zh-CN');
  if (name === query || cn === query) return 0;
  if (name.startsWith(query) || cn.startsWith(query)) return 1;
  if (name.split(/[_\-\s]+/).some(word => word.startsWith(query))) return 2;
  if (name.includes(query) || cn.includes(query)) return 3;
  return entry.searchable.includes(query) ? 4 : 99;
}

function performTagSearch() {
  if (!state.catalog) return;
  const query = els.searchInput.value.trim().toLocaleLowerCase('zh-CN');
  els.clearSearch.classList.toggle('visible', Boolean(query));
  if (!query) {
    state.searchResults = [];
    state.searchActiveIndex = -1;
    els.searchResults.hidden = true;
    els.searchInput.setAttribute('aria-expanded', 'false');
    return;
  }
  state.searchResults = state.searchEntries
    .filter(entry => (state.searchScope === 'global'
      || (state.searchScope === 'library' && entry.folderId === state.folderId)
      || (state.searchScope === 'local' && entry.folderId === state.folderId && entry.categoryId === state.categoryId))
      && (state.showNsfw || !entry.tag.nsfw)
      && entry.searchable.includes(query))
    .map(entry => ({ entry, score: searchEntryScore(entry, query) }))
    .sort((a, b) => a.score - b.score || Number(b.entry.tag.count || 0) - Number(a.entry.tag.count || 0)
      || a.entry.tag.name.localeCompare(b.entry.tag.name))
    .slice(0, 30)
    .map(result => result.entry);
  state.searchActiveIndex = state.searchResults.length ? 0 : -1;
  renderSearchResults(query);
}

function renderSearchResults(query) {
  const scopeText = state.searchScope === 'local'
    ? `当前分类 · ${currentCategory()?.name || ''}`
    : state.searchScope === 'library'
      ? `当前词库 · ${currentFolder()?.name || ''}`
      : '全部提示词库';
  if (!state.searchResults.length) {
    els.searchResults.innerHTML = `<div class="search-empty"><strong>没有找到“${escapeHtml(query)}”</strong><span>${escapeHtml(scopeText)}中暂无匹配标签</span></div>`;
  } else {
    els.searchResults.innerHTML = `
      <div class="search-results-head"><span>${escapeHtml(scopeText)}</span><b>${state.searchResults.length} 个结果</b></div>
      <div class="search-result-list">${state.searchResults.map((entry, index) => {
        const aliases = Array.isArray(entry.tag.aliases) ? entry.tag.aliases.filter(Boolean) : [];
        const description = entry.tag.wiki || aliases.slice(0, 4).join(' · ') || entry.tag.cn || '暂无详细说明';
        return `<button class="search-result ${index === state.searchActiveIndex ? 'active' : ''}" type="button" role="option" aria-selected="${index === state.searchActiveIndex}" data-search-index="${index}" title="点击定位、选中并复制提示词">
          <span class="search-result-main"><strong>${escapeHtml(entry.tag.name)}</strong><em>${escapeHtml(entry.tag.cn || entry.tag.name.replaceAll('_', ' '))}</em>${entry.tag.nsfw ? '<i>NSFW</i>' : ''}</span>
          <span class="search-result-description">${escapeHtml(description)}</span>
          <span class="search-result-path"><b>${escapeHtml(entry.folderName)}</b><span>›</span><b>${escapeHtml(entry.categoryName)}</b></span>
        </button>`;
      }).join('')}</div>`;
  }
  els.searchResults.hidden = false;
  els.searchInput.setAttribute('aria-expanded', 'true');
}

function closeSearchResults(clear = false) {
  if (clear) {
    els.searchInput.value = '';
    els.clearSearch.classList.remove('visible');
  }
  state.searchResults = [];
  state.searchActiveIndex = -1;
  els.searchResults.hidden = true;
  els.searchInput.setAttribute('aria-expanded', 'false');
}

async function writeClipboardText(text) {
  const value = String(text || '');
  try {
    if (!navigator.clipboard?.writeText) throw new Error('Clipboard API unavailable');
    await navigator.clipboard.writeText(value);
    return true;
  } catch {
    const fallback = document.createElement('textarea');
    fallback.value = value;
    fallback.readOnly = true;
    fallback.style.position = 'fixed';
    fallback.style.opacity = '0';
    fallback.style.pointerEvents = 'none';
    document.body.appendChild(fallback);
    fallback.select();
    let copied = false;
    try {
      copied = document.execCommand('copy');
    } catch { /* Browser denied the legacy clipboard fallback. */ }
    fallback.remove();
    return copied;
  }
}

function chooseSearchResult(index) {
  const entry = state.searchResults[index];
  if (!entry) return;
  const copyPromise = writeClipboardText(entry.tag.name);
  state.folderId = entry.folderId;
  state.categoryId = entry.categoryId;
  if (!state.selected.some(item => tagKey(item.name) === tagKey(entry.tag.name))) {
    state.selected.push({
      name: entry.tag.name,
      cn: entry.tag.cn,
      weight: 1,
      folderId: entry.folderId,
      categoryId: entry.categoryId,
      custom: false
    });
  }
  closeSearchResults(false);
  save();
  renderWorkspace();
  copyPromise.then(copied => {
    showToast(copied ? `已复制 · ${entry.tag.name}` : '复制失败，请重试', copied ? 1050 : 1800);
  });
  requestAnimationFrame(() => requestAnimationFrame(() => {
    const chip = Array.from(els.cloud.querySelectorAll('[data-action="toggle-tag"]'))
      .find(button => tagKey(button.dataset.tag) === tagKey(entry.tag.name));
    if (!chip) return;
    chip.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'nearest' });
    chip.classList.add('search-flash');
    setTimeout(() => chip.classList.remove('search-flash'), 1600);
  }));
}

function selectFolder(folderId) {
  state.folderId = folderId;
  state.categoryId = currentFolder()?.categories[0]?.id || null;
  save();
  renderLibraries();
  renderTabs();
  renderCloud();
  if (state.searchScope !== 'global' && els.searchInput.value.trim()) performTagSearch();
}

function selectCategory(categoryId) {
  state.categoryId = categoryId;
  save();
  renderTabs();
  renderCloud();
  if (state.searchScope === 'local' && els.searchInput.value.trim()) performTagSearch();
}

function toggleTag(name) {
  const category = currentCategory();
  if (!category) return;
  const key = tagKey(name);
  const tag = category.tags.find(item => tagKey(item.name) === key);
  if (!tag) return;
  const copyPromise = writeClipboardText(tag.name);
  const existing = state.selected.findIndex(item => tagKey(item.name) === key);
  if (existing >= 0) {
    state.selected.splice(existing, 1);
  } else {
    state.selected.push({
      name: tag.name,
      cn: tag.cn,
      weight: 1,
      folderId: state.folderId,
      categoryId: state.categoryId,
      custom: false
    });
  }
  syncAll();
  copyPromise.then(copied => {
    showToast(copied ? `已复制 · ${tag.name}` : '复制失败，请重试', copied ? 1050 : 1800);
  });
}

function adjustWeight(index, delta) {
  state.selected[index].weight = clampWeight(state.selected[index].weight + delta);
  syncAll();
}

function removeSelected(index) {
  state.selected.splice(index, 1);
  syncAll();
}

function renderSelected() {
  els.selectedList.innerHTML = state.selected.length ? state.selected.map((item, index) => `
    <div class="selected-item" draggable="true" data-index="${index}">
      <span class="drag">⠿</span><span>${escapeHtml(item.name)}</span><span class="selected-cn">${escapeHtml(item.cn || '自定义')}</span>
      <button class="weight-btn" data-action="down" title="降低权重">−</button><span class="weight-value">${item.weight.toFixed(1)}</span><button class="weight-btn" data-action="up" title="提高权重">＋</button>
      <button class="remove-btn" data-action="remove" title="移除">×</button>
    </div>`).join('') : '<div class="empty-inline">还没有选择标签</div>';
  els.selectedList.querySelectorAll('.selected-item').forEach(item => {
    const index = Number(item.dataset.index);
    item.querySelector('[data-action="down"]').onclick = () => adjustWeight(index, -.1);
    item.querySelector('[data-action="up"]').onclick = () => adjustWeight(index, .1);
    item.querySelector('[data-action="remove"]').onclick = () => removeSelected(index);
    item.addEventListener('dragstart', () => {
      state.dragging = index;
      item.classList.add('dragging');
    });
    item.addEventListener('dragend', () => {
      state.dragging = null;
      item.classList.remove('dragging');
    });
    item.addEventListener('dragover', event => {
      event.preventDefault();
      if (state.dragging === null || state.dragging === index) return;
      const moved = state.selected.splice(state.dragging, 1)[0];
      state.selected.splice(index, 0, moved);
      state.dragging = index;
      syncAll();
    });
  });
}

function renderPreview() {
  els.previewTotal.textContent = state.selected.length;
  els.finalPrompt.textContent = promptText() || '等待选择…';
  const visibleFolderIds = new Set(state.catalog.folders.map(folder => folder.id));
  const groups = state.catalog.folders
    .map(folder => ({ folder, items: state.selected.filter(item => item.folderId === folder.id) }))
    .filter(group => group.items.length);
  const custom = state.selected.filter(item => !visibleFolderIds.has(item.folderId));
  if (custom.length) groups.push({ folder: { name: '自定义 / 来源已删除', accent: '#aab0bd' }, items: custom });
  els.previewGroups.innerHTML = groups.length ? groups.map(group => `
    <div class="preview-group" style="--group-accent:${safeAccent(group.folder.accent)}">
      <div class="preview-group-title"><span><i class="folder-dot"></i>${escapeHtml(group.folder.name)}</span><em>${group.items.length}</em></div>
      <div>${group.items.map(item => `<span class="preview-token">${escapeHtml(promptToken(item))}</span>`).join('')}</div>
    </div>`).join('') : '<div class="empty-preview">从右侧选择一个词库，然后在左侧点选标签。</div>';
}

function renderWorkspace(updateEditor = true) {
  renderLibraries();
  renderTabs();
  renderCloud();
  renderSelected();
  renderPreview();
  updateDatabaseStat();
  if (updateEditor) els.editor.value = promptText();
  els.promptCount.textContent = `${state.selected.length} 个提示词`;
}

function syncAll(updateEditor = true) {
  save();
  renderCloud();
  renderSelected();
  renderPreview();
  if (updateEditor) els.editor.value = promptText();
  els.promptCount.textContent = `${state.selected.length} 个提示词`;
}

function parseEditor() {
  const pieces = els.editor.value.split(/[,，\n]+/).map(item => item.trim()).filter(Boolean);
  state.selected = pieces.map(raw => {
    const weighted = raw.match(/^\((.+):([0-9.]+)\)$/);
    const name = weighted ? weighted[1].trim() : raw;
    const weight = clampWeight(weighted ? weighted[2] : 1);
    const known = state.tagIndex.get(tagKey(name));
    return known ? {
      name: known.tag.name,
      cn: known.tag.cn,
      weight,
      folderId: known.folderId,
      categoryId: known.categoryId,
      custom: false
    } : {
      name,
      cn: '自定义',
      weight,
      folderId: 'custom',
      categoryId: null,
      custom: true
    };
  });
  save();
  renderCloud();
  renderSelected();
  renderPreview();
  els.promptCount.textContent = `${state.selected.length} 个提示词`;
}

async function copyPrompt() {
  if (!state.selected.length) {
    showToast('还没有提示词');
    return;
  }
  try {
    await navigator.clipboard.writeText(promptText());
    showToast('提示词已复制');
  } catch {
    els.editor.select();
    document.execCommand('copy');
    showToast('提示词已复制');
  }
}

function commitLibraryEdit(mutator, options = {}) {
  if (!state.baseCatalog || !state.edits) return false;
  const next = cloneData(state.edits);
  try {
    mutator(next);
    next.baseCatalogVersion = Number(state.baseCatalog.version) || 0;
    next.updatedAt = new Date().toISOString();
    localStorage.setItem(LIBRARY_KEY, JSON.stringify(next));
  } catch (error) {
    showToast(error?.name === 'QuotaExceededError' ? '保存失败：本地存储空间不足' : '词库修改保存失败');
    return false;
  }
  state.edits = next;
  rebuildCatalog();
  if (Object.prototype.hasOwnProperty.call(options, 'folderId')) state.folderId = options.folderId;
  if (Object.prototype.hasOwnProperty.call(options, 'categoryId')) state.categoryId = options.categoryId;
  normalizeActiveLocation();
  buildTagIndex();
  if (options.renameTag) {
    state.selected.forEach(item => {
      if (tagKey(item.name) === tagKey(options.renameTag.from)) {
        item.name = options.renameTag.to;
        item.cn = options.renameTag.cn || item.cn;
      }
    });
  }
  reconcileSelectedOrigins();
  save();
  renderWorkspace();
  if (options.message) showToast(options.message);
  return true;
}

function newId(prefix) {
  const value = typeof crypto.randomUUID === 'function' ? crypto.randomUUID() : `${Date.now()}_${Math.random().toString(16).slice(2)}`;
  return `u_${prefix}_${value}`;
}

function folderNameTaken(name, exceptId = null) {
  const key = labelKey(name);
  return state.catalog.folders.some(folder => folder.id !== exceptId && labelKey(folder.name) === key);
}

function categoryNameTaken(folderId, name, exceptId = null) {
  const folder = state.catalog.folders.find(item => item.id === folderId);
  const key = labelKey(name);
  return Boolean(folder?.categories.some(category => category.id !== exceptId && labelKey(category.name) === key));
}

function editorTargetCategory(context = state.editorContext) {
  const folder = state.catalog?.folders.find(item => item.id === context?.folderId);
  return folder?.categories.find(item => item.id === context?.categoryId) || null;
}

function updateDatabaseTagSelectionUi() {
  const context = state.editorContext;
  if (!context || context.kind !== 'tag' || context.action !== 'add') return;
  const selected = context.databaseSelections || new Map();
  els.databaseTagSelectedCount.textContent = `已选择 ${selected.size} 个`;
  els.libraryEditorSubmit.disabled = context.tagSource === 'database' && !selected.size;
  els.libraryEditorSubmit.textContent = context.tagSource === 'database'
    ? (selected.size ? `复制 ${selected.size} 个标签` : '请选择标签')
    : '保存';
  els.databaseTagResults.querySelectorAll('[data-database-tag]').forEach(option => {
    const key = option.dataset.databaseTag;
    const active = selected.has(key);
    const alreadyPresent = option.dataset.alreadyPresent === 'true';
    option.classList.toggle('selected', active);
    option.setAttribute('aria-selected', String(active));
    option.querySelector('.database-tag-check').textContent = active ? '✓' : '';
    option.querySelector('.database-tag-state').textContent = alreadyPresent ? '当前分类已有' : active ? '已选择' : '选择';
  });
}

function renderDatabaseTagPicker() {
  const context = state.editorContext;
  if (!context || context.kind !== 'tag' || context.action !== 'add') return;
  if (!state.databaseTagChoices.length) buildDatabaseTagChoices();
  const query = els.databaseTagSearch.value.trim().toLocaleLowerCase('zh-CN');
  const target = editorTargetCategory(context);
  const existingNames = new Set((target?.tags || []).map(tag => tagKey(tag.name)));
  const queryMatches = state.databaseTagChoices.filter(entry => !query || entry.searchable.includes(query));
  const hiddenSensitiveCount = state.showNsfw ? 0 : queryMatches.filter(entry => entry.tag.nsfw).length;
  let matches = queryMatches.filter(entry => state.showNsfw || !entry.tag.nsfw);
  if (query) {
    matches = matches.map(entry => ({ entry, score: searchEntryScore(entry, query) }))
      .sort((a, b) => a.score - b.score
        || Number(b.entry.tag.count || 0) - Number(a.entry.tag.count || 0)
        || a.entry.tag.name.localeCompare(b.entry.tag.name))
      .map(result => result.entry);
  }
  const total = matches.length;
  const visible = matches.slice(0, 60);
  context.visibleDatabaseTags = visible;
  const hiddenText = hiddenSensitiveCount ? ` · 已隐藏 ${hiddenSensitiveCount.toLocaleString()} 个敏感标签` : '';
  els.databaseTagResultCount.textContent = query
    ? `${total.toLocaleString()} 个匹配${total > visible.length ? ` · 显示前 ${visible.length} 个` : ''}${hiddenText}`
    : `数据库 ${total.toLocaleString()} 个标签 · 显示常用的前 ${visible.length} 个${hiddenText}`;

  if (!visible.length) {
    els.databaseTagResults.innerHTML = `<div class="database-tag-empty"><strong>没有找到匹配标签</strong><span>${hiddenSensitiveCount ? '部分敏感标签已隐藏，可在顶部开启显示' : '请尝试英文 Tag、中文说明或描述中的关键词'}</span></div>`;
    updateDatabaseTagSelectionUi();
    return;
  }

  const selected = context.databaseSelections || new Map();
  els.databaseTagResults.innerHTML = visible.map(entry => {
    const alreadyPresent = existingNames.has(entry.key);
    const active = selected.has(entry.key);
    return `<button class="database-tag-option ${active ? 'selected' : ''} ${alreadyPresent ? 'already-present' : ''}" type="button"
      role="option" aria-selected="${active}" data-database-tag="${escapeHtml(entry.key)}" data-already-present="${alreadyPresent}"
      title="${escapeHtml(entry.description)}" ${alreadyPresent ? 'disabled' : ''}>
      <span class="database-tag-check" aria-hidden="true">${active ? '✓' : ''}</span>
      <span class="database-tag-copy">
        <span class="database-tag-name"><strong>${escapeHtml(entry.tag.name)}</strong><em>${escapeHtml(entry.tag.cn || entry.tag.name.replaceAll('_', ' '))}</em>${entry.tag.nsfw ? '<i>NSFW</i>' : ''}</span>
        <span class="database-tag-description"><b>说明</b>${escapeHtml(entry.description)}</span>
        <span class="database-tag-path"><b>来源</b>${escapeHtml(entry.pathLabel)}</span>
      </span>
      <span class="database-tag-state">${alreadyPresent ? '当前分类已有' : active ? '已选择' : '选择'}</span>
    </button>`;
  }).join('');
  updateDatabaseTagSelectionUi();
}

function setTagSourceMode(mode) {
  const context = state.editorContext;
  if (!context || context.kind !== 'tag' || context.action !== 'add') return;
  context.tagSource = mode === 'manual' ? 'manual' : 'database';
  const databaseMode = context.tagSource === 'database';
  els.tagSourceDatabase.classList.toggle('active', databaseMode);
  els.tagSourceManual.classList.toggle('active', !databaseMode);
  els.tagSourceDatabase.setAttribute('aria-pressed', String(databaseMode));
  els.tagSourceManual.setAttribute('aria-pressed', String(!databaseMode));
  els.databaseTagPanel.hidden = !databaseMode;
  els.libraryNameField.hidden = databaseMode;
  document.querySelectorAll('.tag-field').forEach(element => { element.hidden = databaseMode; });
  els.libraryName.disabled = databaseMode;
  els.libraryName.required = !databaseMode;
  els.libraryCn.disabled = databaseMode;
  els.libraryNsfw.disabled = databaseMode;
  els.libraryEditor.classList.toggle('database-tag-mode', databaseMode);
  if (databaseMode) renderDatabaseTagPicker();
  else {
    els.libraryEditorSubmit.disabled = false;
    els.libraryEditorSubmit.textContent = '保存';
  }
}

function showEditorError(message) {
  els.libraryEditorError.textContent = message;
  if (state.editorContext?.tagSource === 'database') els.databaseTagSearch.focus();
  else els.libraryName.focus();
}

function setEditorFields(kind) {
  document.querySelectorAll('.folder-field').forEach(element => { element.hidden = kind !== 'folder'; });
  document.querySelectorAll('.tag-field').forEach(element => { element.hidden = kind !== 'tag'; });
  els.tagSourceField.hidden = true;
  els.databaseTagPanel.hidden = true;
  els.libraryNameField.hidden = false;
  els.libraryName.disabled = false;
  els.libraryName.required = true;
  els.libraryCn.disabled = false;
  els.libraryNsfw.disabled = false;
  els.libraryEditorSubmit.disabled = false;
  els.libraryEditorSubmit.textContent = '保存';
  els.libraryEditor.classList.remove('database-tag-mode');
}

function openLibraryEditor(kind, action, identifiers = {}) {
  if (!state.catalog) return;
  const folder = identifiers.folderId ? state.catalog.folders.find(item => item.id === identifiers.folderId) : null;
  const category = folder && identifiers.categoryId ? folder.categories.find(item => item.id === identifiers.categoryId) : null;
  const tag = category && identifiers.tagName
    ? category.tags.find(item => tagKey(item.name) === tagKey(identifiers.tagName))
    : null;
  if (kind === 'category' && !folder) {
    showToast('请先新建提示词库');
    return;
  }
  if (kind === 'tag' && !category) {
    showToast('请先新建细分类');
    return;
  }
  state.editorContext = {
    kind,
    action,
    folderId: identifiers.folderId || null,
    categoryId: identifiers.categoryId || null,
    tagId: tag ? stableTagId(tag) : null,
    tagName: tag?.name || null,
    sourceName: tag?._sourceName || tag?.name || null,
    tagSource: 'manual',
    databaseSelections: new Map(),
    visibleDatabaseTags: []
  };
  setEditorFields(kind);
  els.libraryEditorError.textContent = '';
  els.libraryEditorSubtitle.textContent = '';
  els.libraryDescription.value = '';
  els.libraryIcon.value = '◇';
  els.libraryAccent.value = '#78a7ff';
  els.libraryCn.value = '';
  els.libraryNsfw.checked = false;
  els.databaseTagSearch.value = '';

  if (kind === 'folder') {
    els.libraryEditorTitle.textContent = action === 'add' ? '新建提示词库' : '编辑提示词库';
    els.libraryNameLabel.textContent = '词库名称';
    els.libraryName.maxLength = 40;
    els.libraryName.value = folder?.name || '';
    els.libraryDescription.value = folder?.description || '';
    els.libraryIcon.value = folder?.icon || '◇';
    els.libraryAccent.value = safeAccent(folder?.accent);
  } else if (kind === 'category') {
    els.libraryEditorTitle.textContent = action === 'add' ? '新建细分类' : '重命名细分类';
    els.libraryEditorSubtitle.textContent = folder.name;
    els.libraryNameLabel.textContent = '分类名称';
    els.libraryName.maxLength = 40;
    els.libraryName.value = category?.name || '';
  } else {
    els.libraryEditorTitle.textContent = action === 'add' ? '添加标签' : '编辑标签';
    els.libraryEditorSubtitle.textContent = `${folder.name} / ${category.name}`;
    els.libraryNameLabel.textContent = '提示词 Tag';
    els.libraryName.maxLength = 200;
    els.libraryName.value = tag?.name || '';
    els.libraryCn.value = tag?.cn || '';
    els.libraryNsfw.checked = Boolean(tag?.nsfw);
    if (action === 'add') {
      els.tagSourceField.hidden = false;
      setTagSourceMode('database');
    }
  }

  if (els.libraryEditor.open) els.libraryEditor.close();
  els.libraryEditor.showModal();
  setTimeout(() => {
    if (state.editorContext?.tagSource === 'database') els.databaseTagSearch.focus();
    else els.libraryName.focus();
  }, 0);
}

function closeLibraryEditor() {
  if (els.libraryEditor.open) els.libraryEditor.close();
  state.editorContext = null;
  els.libraryEditorError.textContent = '';
}

function copySelectedDatabaseTags(context) {
  const selected = Array.from(context.databaseSelections?.values() || []);
  if (!selected.length) {
    showEditorError('请至少选择一个数据库标签');
    return false;
  }
  const target = editorTargetCategory(context);
  if (!target) {
    showEditorError('目标分类不存在，请关闭弹窗后重试');
    return false;
  }
  const existingNames = new Set(target.tags.map(tag => tagKey(tag.name)));
  const operations = selected.filter(entry => !existingNames.has(entry.key)).map(entry => {
    const hiddenBuiltin = baseTag(context.folderId, context.categoryId, entry.tag.name);
    const hiddenKey = hiddenBuiltin ? tupleKey(context.folderId, context.categoryId, hiddenBuiltin.name) : null;
    const restore = Boolean(hiddenKey && state.edits.removed.tags.some(row => rowKey(row) === hiddenKey));
    return { entry, restore, hiddenKey };
  });
  if (!operations.length) {
    showEditorError('所选标签已全部存在于当前分类');
    return false;
  }
  const restoredCount = operations.filter(operation => operation.restore).length;
  const copiedCount = operations.length - restoredCount;
  return commitLibraryEdit(next => {
    operations.forEach(({ entry, restore, hiddenKey }) => {
      if (restore) {
        next.removed.tags = next.removed.tags.filter(row => rowKey(row) !== hiddenKey);
        return;
      }
      next.added.tags.push({
        id: newId('t'),
        folderId: context.folderId,
        categoryId: context.categoryId,
        name: entry.tag.name,
        cn: entry.tag.cn || entry.tag.name.replaceAll('_', ' '),
        aliases: Array.isArray(entry.tag.aliases) ? [...entry.tag.aliases] : [],
        wiki: String(entry.tag.wiki || ''),
        count: Number(entry.tag.count || 0),
        nsfw: Boolean(entry.tag.nsfw),
        createdAt: Date.now()
      });
    });
  }, {
    message: copiedCount && restoredCount
      ? `已复制 ${copiedCount} 个标签，并恢复 ${restoredCount} 个内置标签`
      : copiedCount
        ? `已复制 ${copiedCount} 个数据库标签`
        : `已恢复 ${restoredCount} 个内置标签`
  });
}

function handleLibraryEditorSubmit(event) {
  event.preventDefault();
  const context = state.editorContext;
  if (!context) return;
  if (context.kind === 'tag' && context.action === 'add' && context.tagSource === 'database') {
    if (copySelectedDatabaseTags(context)) closeLibraryEditor();
    return;
  }
  const name = els.libraryName.value.trim();
  if (!name) {
    showEditorError('名称不能为空');
    return;
  }

  let committed = false;
  if (context.kind === 'folder') {
    if (folderNameTaken(name, context.action === 'edit' ? context.folderId : null)) {
      showEditorError('已经存在同名提示词库');
      return;
    }
    const values = {
      name,
      description: els.libraryDescription.value.trim() || '自定义提示词库',
      icon: Array.from(els.libraryIcon.value.trim()).slice(0, 2).join('') || '◇',
      accent: safeAccent(els.libraryAccent.value)
    };
    if (context.action === 'add') {
      const folderId = newId('f');
      committed = commitLibraryEdit(next => {
        next.added.folders.push({ id: folderId, ...values, createdAt: Date.now() });
      }, { folderId, categoryId: null, message: '提示词库已创建' });
    } else {
      committed = commitLibraryEdit(next => {
        const custom = next.added.folders.find(folder => folder.id === context.folderId);
        if (custom) Object.assign(custom, values);
        else next.overrides.folders[context.folderId] = { ...objectOrEmpty(next.overrides.folders[context.folderId]), ...values };
      }, { message: '提示词库已保存' });
    }
  } else if (context.kind === 'category') {
    if (categoryNameTaken(context.folderId, name, context.action === 'edit' ? context.categoryId : null)) {
      showEditorError('当前词库中已经存在同名分类');
      return;
    }
    if (context.action === 'add') {
      const categoryId = newId('c');
      committed = commitLibraryEdit(next => {
        next.added.categories.push({ id: categoryId, folderId: context.folderId, name, createdAt: Date.now() });
      }, { folderId: context.folderId, categoryId, message: '细分类已创建' });
    } else {
      committed = commitLibraryEdit(next => {
        const custom = next.added.categories.find(category => category.folderId === context.folderId && category.id === context.categoryId);
        if (custom) custom.name = name;
        else {
          const key = tupleKey(context.folderId, context.categoryId);
          next.overrides.categories[key] = { ...objectOrEmpty(next.overrides.categories[key]), name };
        }
      }, { message: '分类名称已保存' });
    }
  } else {
    if (/[,，\r\n]/.test(name)) {
      showEditorError('Tag 不能包含逗号或换行');
      return;
    }
    if (/^\(.+:[0-9.]+\)$/.test(name)) {
      showEditorError('Tag 不能使用权重表达式作为名称');
      return;
    }
    const category = state.catalog.folders.find(folder => folder.id === context.folderId)?.categories.find(item => item.id === context.categoryId);
    if (category?.tags.some(tag => stableTagId(tag) !== context.tagId && tagKey(tag.name) === tagKey(name))) {
      showEditorError('当前分类中已经存在这个 Tag');
      return;
    }
    if (context.action === 'edit') {
      const cn = els.libraryCn.value.trim() || name.replaceAll('_', ' ');
      const values = { name, cn, nsfw: els.libraryNsfw.checked };
      committed = commitLibraryEdit(next => {
        const custom = next.added.tags.find(item => item.id === context.tagId);
        if (custom) {
          Object.assign(custom, values);
        } else {
          const key = tupleKey(context.folderId, context.categoryId, context.sourceName);
          next.overrides.tags[key] = { ...objectOrEmpty(next.overrides.tags[key]), ...values };
        }
      }, {
        message: '标签已保存',
        renameTag: { from: context.tagName, to: name, cn }
      });
      if (committed) closeLibraryEditor();
      return;
    }
    const hiddenBuiltin = baseTag(context.folderId, context.categoryId, name);
    if (hiddenBuiltin) {
      const hiddenKey = tupleKey(context.folderId, context.categoryId, hiddenBuiltin.name);
      if (state.edits.removed.tags.some(row => rowKey(row) === hiddenKey)) {
        committed = commitLibraryEdit(next => {
          next.removed.tags = next.removed.tags.filter(row => rowKey(row) !== hiddenKey);
        }, { message: '内置标签已恢复' });
      }
    }
    if (!committed) {
      const tagId = newId('t');
      const cn = els.libraryCn.value.trim() || name.replaceAll('_', ' ');
      committed = commitLibraryEdit(next => {
        next.added.tags.push({
          id: tagId,
          folderId: context.folderId,
          categoryId: context.categoryId,
          name,
          cn,
          aliases: els.libraryCn.value.trim() ? [els.libraryCn.value.trim()] : [],
          wiki: '',
          count: 0,
          nsfw: els.libraryNsfw.checked,
          createdAt: Date.now()
        });
      }, { message: '标签已添加' });
    }
  }

  if (committed) closeLibraryEditor();
}

function editFolder(folderId) {
  openLibraryEditor('folder', 'edit', { folderId });
}

function deleteFolder(folderId) {
  const folder = state.catalog.folders.find(item => item.id === folderId);
  if (!folder) return;
  const tagMembershipCount = folder.categories.reduce((total, category) => total + category.tags.length, 0);
  if (!confirm(`删除“${folder.name}”？\n\n将隐藏 ${folder.categories.length} 个分类和 ${tagMembershipCount} 个标签。内置内容可以在设置中恢复；其中的自建内容会被永久删除。`)) return;
  commitLibraryEdit(next => {
    if (baseFolder(folderId)) {
      if (!next.removed.folders.includes(folderId)) next.removed.folders.push(folderId);
    } else {
      next.added.folders = next.added.folders.filter(item => item.id !== folderId);
    }
    next.added.categories = next.added.categories.filter(item => item.folderId !== folderId);
    next.added.tags = next.added.tags.filter(item => item.folderId !== folderId);
  }, { message: '提示词库已删除' });
}

function editCategory(categoryId) {
  openLibraryEditor('category', 'edit', { folderId: state.folderId, categoryId });
}

function editTag(name) {
  openLibraryEditor('tag', 'edit', { folderId: state.folderId, categoryId: state.categoryId, tagName: name });
}

function deleteCategory(categoryId) {
  const folder = currentFolder();
  const category = folder?.categories.find(item => item.id === categoryId);
  if (!folder || !category) return;
  if (!confirm(`删除“${category.name}”？\n\n将隐藏 ${category.tags.length} 个标签。内置内容可以在设置中恢复；此分类中的自建标签会被永久删除。`)) return;
  commitLibraryEdit(next => {
    if (baseCategory(folder.id, categoryId)) {
      const key = tupleKey(folder.id, categoryId);
      if (!next.removed.categories.some(row => rowKey(row) === key)) next.removed.categories.push([folder.id, categoryId]);
    } else {
      next.added.categories = next.added.categories.filter(item => !(item.folderId === folder.id && item.id === categoryId));
    }
    next.added.tags = next.added.tags.filter(item => !(item.folderId === folder.id && item.categoryId === categoryId));
  }, { message: '细分类已删除' });
}

function deleteTag(name) {
  const folder = currentFolder();
  const category = currentCategory();
  const tag = category?.tags.find(item => tagKey(item.name) === tagKey(name));
  if (!folder || !category || !tag) return;
  if (!confirm(`从“${category.name}”中删除标签“${tag.name}”？`)) return;
  commitLibraryEdit(next => {
    const custom = next.added.tags.find(item => item.folderId === folder.id && item.categoryId === category.id && tagKey(item.name) === tagKey(tag.name));
    if (custom) {
      next.added.tags = next.added.tags.filter(item => item.id !== custom.id);
    } else {
      const builtin = baseTag(folder.id, category.id, tag._sourceName || tag.name);
      if (!builtin) return;
      const key = tupleKey(folder.id, category.id, builtin.name);
      if (!next.removed.tags.some(row => rowKey(row) === key)) next.removed.tags.push([folder.id, category.id, builtin.name]);
    }
  }, { message: '标签已删除' });
}

function restoreBuiltinContent() {
  const reordered = state.edits.order.folders.length
    + Object.values(state.edits.order.categories).reduce((total, items) => total + (Array.isArray(items) ? items.length : 0), 0)
    + Object.values(state.edits.order.tags).reduce((total, items) => total + (Array.isArray(items) ? items.length : 0), 0);
  const changed = state.edits.removed.folders.length
    + state.edits.removed.categories.length
    + state.edits.removed.tags.length
    + Object.keys(state.edits.overrides.folders).length
    + Object.keys(state.edits.overrides.categories).length
    + Object.keys(state.edits.overrides.tags).length
    + reordered;
  if (!changed) {
    showToast('内置内容已经是原始状态');
    return;
  }
  if (!confirm('恢复所有内置词库、分类、标签、原始名称和默认顺序？\n\n你自己新增的内容会保留。')) return;
  commitLibraryEdit(next => {
    next.overrides = { folders: {}, categories: {}, tags: {} };
    next.removed = { folders: [], categories: [], tags: [] };
    next.order = { folders: [], categories: {}, tags: {} };
  }, { message: '内置内容已恢复' });
}

function clearCustomContent() {
  const count = state.edits.added.folders.length + state.edits.added.categories.length + state.edits.added.tags.length;
  if (!count) {
    showToast('没有自建内容');
    return;
  }
  if (!confirm(`永久清除 ${count} 项自建词库数据？\n\n内置内容的隐藏和重命名状态不会改变。此操作无法撤销。`)) return;
  commitLibraryEdit(next => {
    next.added = { folders: [], categories: [], tags: [] };
  }, { message: '全部自建内容已清除' });
}

function moveOrderItem(ids, fromId, toId) {
  const next = [...ids].map(String);
  const from = next.indexOf(String(fromId));
  const to = next.indexOf(String(toId));
  if (from < 0 || to < 0 || from === to) return null;
  const [item] = next.splice(from, 1);
  next.splice(to, 0, item);
  return next;
}

function reorderManagedItems(type, fromId, toId) {
  let ids;
  if (type === 'folder') ids = state.catalog.folders.map(folder => folder.id);
  if (type === 'category') ids = currentFolder()?.categories.map(category => category.id);
  if (type === 'tag') ids = currentCategory()?.tags.map(stableTagId);
  const ordered = moveOrderItem(ids || [], fromId, toId);
  if (!ordered) return;
  commitLibraryEdit(next => {
    next.order ||= { folders: [], categories: {}, tags: {} };
    next.order.categories ||= {};
    next.order.tags ||= {};
    if (type === 'folder') next.order.folders = ordered;
    if (type === 'category') next.order.categories[state.folderId] = ordered;
    if (type === 'tag') next.order.tags[tupleKey(state.folderId, state.categoryId)] = ordered;
  }, { message: '顺序已保存' });
}

function bindManagedSorting(container) {
  container.addEventListener('pointerdown', event => {
    state.manageDragArmed = Boolean(event.target.closest('.manage-drag'));
  });
  container.addEventListener('dragstart', event => {
    const item = event.target.closest('[data-manage-type]');
    if (!item || !state.manageMode || !state.manageDragArmed) {
      event.preventDefault();
      return;
    }
    state.manageDrag = { type: item.dataset.manageType, id: item.dataset.manageId };
    item.classList.add('dragging-managed');
    event.dataTransfer.effectAllowed = 'move';
    event.dataTransfer.setData('text/plain', item.dataset.manageId);
  });
  container.addEventListener('dragover', event => {
    const item = event.target.closest('[data-manage-type]');
    if (!item || !state.manageDrag || item.dataset.manageType !== state.manageDrag.type) return;
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
    container.querySelectorAll('.drag-over').forEach(node => node.classList.remove('drag-over'));
    if (item.dataset.manageId !== state.manageDrag.id) item.classList.add('drag-over');
  });
  container.addEventListener('drop', event => {
    const item = event.target.closest('[data-manage-type]');
    if (!item || !state.manageDrag || item.dataset.manageType !== state.manageDrag.type) return;
    event.preventDefault();
    const drag = state.manageDrag;
    state.manageDrag = null;
    reorderManagedItems(drag.type, drag.id, item.dataset.manageId);
  });
  container.addEventListener('dragend', () => {
    state.manageDrag = null;
    state.manageDragArmed = false;
    container.querySelectorAll('.dragging-managed,.drag-over').forEach(node => node.classList.remove('dragging-managed', 'drag-over'));
  });
}

function bindActions() {
  $('#copy-all').onclick = copyPrompt;
  $('#copy-preview').onclick = copyPrompt;
  $('#clear-all').onclick = () => {
    if (!state.selected.length) return;
    state.selected = [];
    syncAll();
    showToast('已清空');
  };
  $('#reverse-order').onclick = () => {
    state.selected.reverse();
    syncAll();
  };
  $('#weight-up').onclick = () => {
    state.selected.forEach(item => { item.weight = clampWeight(item.weight + .1); });
    syncAll();
  };
  $('#weight-down').onclick = () => {
    state.selected.forEach(item => { item.weight = clampWeight(item.weight - .1); });
    syncAll();
  };
  els.nsfw.onchange = () => {
    state.showNsfw = els.nsfw.checked;
    save();
    renderCloud();
    if (els.searchInput.value.trim()) performTagSearch();
  };
  els.editor.addEventListener('input', parseEditor);

  els.libraries.addEventListener('click', event => {
    const button = event.target.closest('[data-action]');
    if (!button) return;
    const action = button.dataset.action;
    if (action === 'open-folder') selectFolder(button.dataset.folder);
    if (action === 'edit-folder') editFolder(button.dataset.folder);
    if (action === 'delete-folder') deleteFolder(button.dataset.folder);
  });
  els.tabs.addEventListener('click', event => {
    const button = event.target.closest('[data-action]');
    if (!button) return;
    const action = button.dataset.action;
    if (action === 'open-category') selectCategory(button.dataset.category);
    if (action === 'edit-category') editCategory(button.dataset.category);
    if (action === 'delete-category') deleteCategory(button.dataset.category);
  });
  els.tabs.addEventListener('wheel', event => {
    if (els.tabs.scrollWidth <= els.tabs.clientWidth || Math.abs(event.deltaX) >= Math.abs(event.deltaY)) return;
    event.preventDefault();
    els.tabs.scrollLeft += event.deltaY;
  }, { passive: false });
  els.cloud.addEventListener('click', event => {
    const button = event.target.closest('[data-action]');
    if (!button) return;
    if (button.dataset.action === 'toggle-tag') toggleTag(button.dataset.tag);
    if (button.dataset.action === 'edit-tag') editTag(button.dataset.tag);
    if (button.dataset.action === 'delete-tag') deleteTag(button.dataset.tag);
  });
  bindManagedSorting(els.libraries);
  bindManagedSorting(els.tabs);
  bindManagedSorting(els.cloud);

  els.searchInput.addEventListener('input', performTagSearch);
  els.searchInput.addEventListener('focus', () => {
    if (els.searchInput.value.trim()) performTagSearch();
  });
  els.searchInput.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      closeSearchResults(false);
      els.searchInput.blur();
      return;
    }
    if (!state.searchResults.length) return;
    if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
      event.preventDefault();
      const direction = event.key === 'ArrowDown' ? 1 : -1;
      state.searchActiveIndex = (state.searchActiveIndex + direction + state.searchResults.length) % state.searchResults.length;
      renderSearchResults(els.searchInput.value.trim());
      els.searchResults.querySelector('.search-result.active')?.scrollIntoView({ block: 'nearest' });
    }
    if (event.key === 'Enter') {
      event.preventDefault();
      chooseSearchResult(Math.max(0, state.searchActiveIndex));
    }
  });
  els.searchResults.addEventListener('mousemove', event => {
    const result = event.target.closest('[data-search-index]');
    if (!result) return;
    const index = Number(result.dataset.searchIndex);
    if (index === state.searchActiveIndex) return;
    state.searchActiveIndex = index;
    els.searchResults.querySelectorAll('.search-result').forEach((node, nodeIndex) => {
      node.classList.toggle('active', nodeIndex === index);
      node.setAttribute('aria-selected', String(nodeIndex === index));
    });
  });
  els.searchResults.addEventListener('click', event => {
    const result = event.target.closest('[data-search-index]');
    if (result) chooseSearchResult(Number(result.dataset.searchIndex));
  });
  [els.searchGlobal, els.searchLibrary, els.searchLocal].forEach(button => {
    button.addEventListener('click', () => {
      if (button.disabled) return;
      state.searchScope = button.dataset.scope;
      updateSearchScopeUi();
      if (els.searchInput.value.trim()) performTagSearch();
      els.searchInput.focus();
    });
  });
  els.clearSearch.onclick = () => {
    closeSearchResults(true);
    els.searchInput.focus();
  };
  document.addEventListener('pointerdown', event => {
    if (!els.tagSearch.contains(event.target)) closeSearchResults(false);
  });

  els.addFolder.onclick = () => openLibraryEditor('folder', 'add');
  els.addCategory.onclick = () => openLibraryEditor('category', 'add', { folderId: state.folderId });
  els.addTag.onclick = () => openLibraryEditor('tag', 'add', { folderId: state.folderId, categoryId: state.categoryId });
  els.toggleManage.onclick = () => {
    state.manageMode = !state.manageMode;
    renderLibraries();
    renderTabs();
    renderCloud();
  };

  els.libraryEditorForm.addEventListener('submit', handleLibraryEditorSubmit);
  [els.tagSourceDatabase, els.tagSourceManual].forEach(button => {
    button.addEventListener('click', () => {
      setTagSourceMode(button.dataset.tagSource);
      if (state.editorContext?.tagSource === 'database') els.databaseTagSearch.focus();
      else els.libraryName.focus();
    });
  });
  els.databaseTagSearch.addEventListener('input', renderDatabaseTagPicker);
  els.databaseTagResults.addEventListener('click', event => {
    const option = event.target.closest('[data-database-tag]');
    const context = state.editorContext;
    if (!option || option.disabled || !context?.databaseSelections) return;
    const key = option.dataset.databaseTag;
    if (context.databaseSelections.has(key)) {
      context.databaseSelections.delete(key);
    } else {
      const entry = context.visibleDatabaseTags.find(candidate => candidate.key === key);
      if (entry) context.databaseSelections.set(key, entry);
    }
    updateDatabaseTagSelectionUi();
  });
  $('#close-library-editor').onclick = closeLibraryEditor;
  $('#cancel-library-editor').onclick = closeLibraryEditor;
  els.libraryEditor.addEventListener('cancel', event => {
    event.preventDefault();
    closeLibraryEditor();
  });

  $('#open-settings').onclick = openSettings;
  $('#close-settings').onclick = closeSettings;
  $('#settings-backdrop').onclick = closeSettings;
  $('#font-scale').oninput = event => applyUiScale(event.target.value);
  $('#save-settings').onclick = () => {
    applyUiScale($('#font-scale').value, true);
    closeSettings();
    showToast('界面大小已保存');
  };
  $('#reset-settings').onclick = () => {
    applyUiScale(100, true);
    showToast('已恢复默认界面大小');
  };
  $('#restore-builtin').onclick = restoreBuiltinContent;
  $('#clear-custom').onclick = clearCustomContent;
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && !els.libraryEditor.open) closeSettings();
  });
}

async function init() {
  applyUiScale(localStorage.getItem('prompt-atelier-ui-scale') || 100);
  localStorage.removeItem('prompt-atelier-logo-style');
  bindActions();
  try {
    const response = await fetch('/api/catalog');
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || '读取失败');

    state.baseCatalog = data;
    state.edits = loadLibraryEdits(data);
    state.catalog = applyLibraryEdits(data, state.edits);

    const saved = restore();
    state.folderId = saved.folderId || null;
    state.categoryId = saved.categoryId || null;
    normalizeActiveLocation();
    buildTagIndex();

    state.showNsfw = Boolean(saved.showNsfw);
    els.nsfw.checked = state.showNsfw;
    state.selected = Array.isArray(saved.selected) ? saved.selected.filter(item => item && item.name).map(item => {
      const known = state.tagIndex.get(tagKey(item.name));
      return {
        name: String(item.name),
        cn: String(item.cn || known?.tag.cn || '自定义'),
        weight: clampWeight(item.weight),
        folderId: item.folderId || known?.folderId || 'custom',
        categoryId: item.categoryId || known?.categoryId || null,
        custom: Boolean(item.custom)
      };
    }) : [];
    reconcileSelectedOrigins();
    renderWorkspace();
    save();
  } catch (error) {
    els.cloud.innerHTML = `<div class="loading-card">数据库读取失败：${escapeHtml(error.message)}</div>`;
    els.dbStat.textContent = '数据库不可用';
    els.addFolder.disabled = true;
    els.addCategory.disabled = true;
    els.addTag.disabled = true;
  }
}

init();
