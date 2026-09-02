const assert = require('assert');
const fs = require('fs');
const path = require('path');

const source = fs.readFileSync(path.join(__dirname, 'app.js'), 'utf8');
const migrationSource = source.slice(source.indexOf('function tagKey'), source.indexOf('function formatCount'));
const editsSource = source.slice(source.indexOf('function defaultLibraryEdits'), source.indexOf('function cloneData'));
const api = new Function(`${migrationSource}\n${editsSource}\nreturn { migrateLegacyLocation, migrateLegacyCategoryLocations, migrateV8Location, migrateV8CategoryLocations, migrateV10Location, migrateV10CategoryLocations, migrateV11Location, migrateV11CategoryLocations, migrateV12Location, migrateV12CategoryLocations, migrateV13Location, migrateV13CategoryLocations, migrateV14Location, migrateV14CategoryLocations, normalizeLibraryEdits, tupleKey, rowKey };`)();

function catalogFrom(rows) {
  const folders = new Map();
  rows.forEach(([folderId, categoryId, tagName]) => {
    if (!folders.has(folderId)) folders.set(folderId, new Map());
    const categories = folders.get(folderId);
    if (!categories.has(categoryId)) categories.set(categoryId, []);
    if (tagName) categories.get(categoryId).push({ name: tagName });
  });
  return {
    version: 17,
    folders: [...folders].map(([folderId, categories]) => ({
      id: folderId,
      categories: [...categories].map(([categoryId, tags]) => ({ id: categoryId, tags }))
    }))
  };
}

const catalog = catalogFrom([
  ['digital_media', 'phone_device', 'smartphone'],
  ['clothing_detail', 'other_structure', 'crinoline'],
  ['animal_traits', 'animal_ears', 'fox_ears'],
  ['clothes_main', 'sweater_hoodie', 'hoodie'],
  ['body', 'torso_back', 'navel'],
  ['sensitive', 'injury_death', 'corpse'],
  ['action', 'clothing_action', 'removing_shirt'],
  ['culture_objects', 'books_paper', 'note'],
  ['head_accessories', 'hairband_ribbon', 'hair_ribbon'],
  ['traditional_clothes', 'traditional_china', 'hanfu'],
  ['protective_clothes', 'shoulder_armor', 'shoulder_spikes'],
  ['underwear_swim', 'school_swim', 'school_swimsuit'],
  ['legwear_footwear', 'heels', 'high_heels'],
  ['legwear_footwear', 'short_boots', 'thigh_boots'],
  ['legwear_footwear', 'short_boots', 'knee_boots'],
  ['legwear_footwear', 'stockings', 'thighhighs_under_boots'],
  ['legwear_footwear', 'short_boots', 'single_thigh_boot'],
  ['legwear_footwear', 'short_boots', 'single_knee_boot'],
  ['nature', 'flower_species', 'rose'],
  ['urban_architecture', 'tower_landmark', 'lighthouse'],
  ['adult_body', 'penis', 'penis'],
  ['franchise_clothes', 'school_variant', 'tracen_school_uniform'],
  ['franchise_clothes', 'franchise_outfit', 'unofficial_precure_costume'],
  ['nature', 'flower_species', 'lotus'],
  ['nature', 'grass_crop', 'mushroom'],
  ['urban_architecture', 'tower_landmark', 'ruins'],
  ['clothing_appearance', 'damaged_dirty', 'torn_clothes'],
  ['clothing_appearance', 'unworn_missing', 'no_shirt'],
  ['clothing_appearance', 'open_wear', 'open_shirt'],
  ['body_detail', 'surface_stain', 'paint_on_body'],
  ['building_parts', 'surface', 'tiles'],
  ['traditional_clothes', 'traditional_other', 'sari'],
  ['traditional_clothes', 'traditional_other', 'keffiyeh'],
  ['protective_clothes', 'full_armor', 'armor'],
  ['protective_clothes', 'full_armor', 'black_armor'],
  ['protective_clothes', 'torso_armor', 'breastplate'],
  ['protective_clothes', 'torso_armor', 'chest_guard'],
  ['protective_clothes', 'protective_suit', 'flak_jacket'],
  ['protective_clothes', 'protective_suit', 'power_suit'],
  ['people', 'fantasy_person', 'living_armor'],
  ['adult', 'adult_sex', 'bootjob'],
  ['protective_clothes', 'leg_armor', 'knee_pads'],
  ['body_detail', 'bandage_patch', 'arm_sling'],
  ['protective_clothes', 'civilian_helmet', 'respirator'],
  ['face', 'eyebrows'], ['face', 'nose'], ['face', 'face_shape'],
  ['clothing_detail', 'sleeve_detail'], ['clothing_detail', 'collar_detail'],
  ['clothing_detail', 'strap_detail'], ['clothing_detail', 'cutout_slit'],
  ['clothing_detail', 'fastener'], ['clothing_detail', 'trim_detail'],
  ['clothing_detail', 'pocket_detail'],
  ['symbols', 'general_symbol'], ['symbols', 'shape_math'], ['symbols', 'music_symbol'],
  ['symbols', 'religious_symbol'], ['symbols', 'zodiac_symbol'], ['symbols', 'flag'],
  ['symbols', 'emblem'], ['symbols', 'science_sign']
]);

const raw = {
  schemaVersion: 1,
  baseCatalogVersion: 6,
  updatedAt: '2026-07-18T00:00:00.000Z',
  added: {
    folders: [{ id: 'custom-folder', name: '自建库' }],
    categories: [{ id: 'custom-category', folderId: 'custom-folder', name: '自建类' }],
    tags: [
      { id: 'a', folderId: 'culture_objects', categoryId: 'phone_computer', name: 'smartphone' },
      { id: 'b', folderId: 'underwear_swim', categoryId: 'underwear_design', name: 'crinoline' },
      { id: 'c', folderId: 'creatures', categoryId: 'animal_feature', name: 'fox_ears' },
      { id: 'd', folderId: 'clothes_main', categoryId: 'tops', name: 'hoodie' },
      { id: 'e', folderId: 'body', categoryId: 'chest', name: 'navel' },
      { id: 'f', folderId: 'adult', categoryId: 'adult_gore', name: 'corpse' },
      { id: 'g', folderId: 'clothing_detail', categoryId: 'clothing_state', name: 'removing_shirt' },
      { id: 'h', folderId: 'text_meta', categoryId: 'symbol', name: 'note' },
      { id: 'i', folderId: 'custom-folder', categoryId: 'custom-category', name: 'smartphone' }
    ]
  },
  overrides: {
    folders: {},
    categories: { '["hair","hair_accessory"]': { name: '我的发饰' } }
  },
  removed: {
    folders: [],
    categories: [['face', 'brows_nose'], ['clothing_detail', 'clothing_structure'], ['text_meta', 'symbol']],
    tags: [['culture_objects', 'phone_computer', 'smartphone'], ['adult', 'adult_gore', 'corpse']]
  }
};

const migrated = api.normalizeLibraryEdits(raw, catalog);
const locations = new Map(migrated.added.tags.map(tag => [tag.id, [tag.folderId, tag.categoryId]]));
assert.deepStrictEqual(locations.get('a'), ['digital_media', 'phone_device']);
assert.deepStrictEqual(locations.get('b'), ['clothing_detail', 'other_structure']);
assert.deepStrictEqual(locations.get('c'), ['animal_traits', 'animal_ears']);
assert.deepStrictEqual(locations.get('d'), ['clothes_main', 'sweater_hoodie']);
assert.deepStrictEqual(locations.get('e'), ['body', 'torso_back']);
assert.deepStrictEqual(locations.get('f'), ['sensitive', 'injury_death']);
assert.deepStrictEqual(locations.get('g'), ['action', 'clothing_action']);
assert.deepStrictEqual(locations.get('h'), ['culture_objects', 'books_paper']);
assert.deepStrictEqual(locations.get('i'), ['custom-folder', 'custom-category']);
assert.deepStrictEqual(migrated.removed.tags, [
  ['digital_media', 'phone_device', 'smartphone'],
  ['sensitive', 'injury_death', 'corpse']
]);

const removedCategories = new Set(migrated.removed.categories.map(api.rowKey));
['eyebrows', 'nose', 'face_shape'].forEach(id => assert(removedCategories.has(api.tupleKey('face', id))));
['sleeve_detail', 'collar_detail', 'strap_detail', 'cutout_slit', 'fastener', 'trim_detail', 'pocket_detail', 'other_structure']
  .forEach(id => assert(removedCategories.has(api.tupleKey('clothing_detail', id))));
['general_symbol', 'shape_math', 'music_symbol', 'religious_symbol', 'zodiac_symbol', 'flag', 'emblem', 'science_sign']
  .forEach(id => assert(removedCategories.has(api.tupleKey('symbols', id))));
['hairband_ribbon', 'hairclip_pin', 'hairtie_ring', 'wig_hairpiece', 'themed_hair_ornament']
  .forEach(id => assert.deepStrictEqual(migrated.overrides.categories[api.tupleKey('head_accessories', id)], { name: '我的发饰' }));
assert.strictEqual(migrated.baseCatalogVersion, 17);
assert.deepStrictEqual(api.normalizeLibraryEdits(migrated, catalog), migrated);

const v7Raw = {
  schemaVersion: 1,
  baseCatalogVersion: 7,
  added: { folders: [], categories: [{ id: 'my-category', folderId: 'clothes_special', name: '自建服装' }], tags: [
    { id: 'j', folderId: 'accessories', categoryId: 'jewelry', name: 'bridge_piercing' },
    { id: 'k', folderId: 'face', categoryId: 'mouth', name: 'tongue' },
    { id: 'l', folderId: 'clothes_special', categoryId: 'my-category', name: 'my_custom_outfit' }
  ] },
  overrides: { folders: {}, categories: { '["accessories","headwear"]': { name: '我的头饰' } }, tags: {} },
  removed: { folders: [], categories: [['pose', 'hand_gesture']], tags: [] },
  order: { folders: ['accessories'], categories: { accessories: ['headwear'] }, tags: {} }
};
const migratedV8 = api.normalizeLibraryEdits(v7Raw, catalog);
assert.deepStrictEqual(migratedV8.added.tags.map(tag => [tag.folderId, tag.categoryId]), [
  ['jewelry_accessories', 'piercing'], ['face', 'oral_detail'], ['uniform_costume', 'my-category']
]);
assert.deepStrictEqual([migratedV8.added.categories[0].folderId, migratedV8.added.categories[0].id], ['uniform_costume', 'my-category']);
assert.deepStrictEqual(migratedV8.order, { folders: [], categories: {}, tags: {} });
assert(migratedV8.removed.categories.some(row => api.rowKey(row) === api.tupleKey('pose', 'arm_pose')));
assert(migratedV8.removed.categories.some(row => api.rowKey(row) === api.tupleKey('pose', 'hand_gesture')));
assert.deepStrictEqual(migratedV8.overrides.categories['["head_accessories","hats_caps"]'], { name: '我的头饰' });
assert.strictEqual(migratedV8.baseCatalogVersion, 17);

const v8OrderRaw = {
  schemaVersion: 1,
  baseCatalogVersion: 8,
  added: { folders: [], categories: [], tags: [] },
  overrides: { folders: {}, categories: {}, tags: {} },
  removed: { folders: [], categories: [], tags: [] },
  order: { folders: ['other', 'people'], categories: { people: ['age'] }, tags: { '["people","age"]': ['adult'] } }
};
const migratedV9 = api.normalizeLibraryEdits(v8OrderRaw, catalog);
assert.deepStrictEqual(migratedV9.order.folders, []);
assert.deepStrictEqual(migratedV9.order.categories, {});
assert.deepStrictEqual(migratedV9.order.tags, {});
assert.strictEqual(migratedV9.baseCatalogVersion, 17);

const v9Raw = {
  schemaVersion: 1,
  baseCatalogVersion: 9,
  added: { folders: [], categories: [], tags: [
    { id: 'm1', folderId: 'head_accessories', categoryId: 'hair_accessory', name: 'hair_ribbon' },
    { id: 'm2', folderId: 'head_accessories', categoryId: 'hair_accessory', name: 'my_hair_charm' },
    { id: 'm3', folderId: 'traditional_clothes', categoryId: 'traditional_east', name: 'hanfu' },
    { id: 'm4', folderId: 'protective_clothes', categoryId: 'armor', name: 'shoulder_spikes' },
    { id: 'm5', folderId: 'underwear_swim', categoryId: 'swimsuit', name: 'my_swimsuit' },
    { id: 'm6', folderId: 'legwear_footwear', categoryId: 'shoes', name: 'high_heels' },
    { id: 'm7', folderId: 'nature', categoryId: 'plant', name: 'rose' },
    { id: 'm8', folderId: 'urban_architecture', categoryId: 'architecture', name: 'lighthouse' },
    { id: 'm9', folderId: 'adult_body', categoryId: 'adult_anatomy', name: 'penis' },
    { id: 'm10', folderId: 'uniform_costume', categoryId: 'school_variant', name: 'tracen_school_uniform' }
  ] },
  overrides: { folders: {}, categories: { '["nature","plant"]': { name: '我的植物' } }, tags: {} },
  removed: { folders: ['urban_architecture'], categories: [['legwear_footwear', 'boots']], tags: [] },
  order: { folders: ['nature'], categories: { nature: ['plant'] }, tags: {} }
};
const migratedV10 = api.normalizeLibraryEdits(v9Raw, catalog);
const v10Locations = new Map(migratedV10.added.tags.map(tag => [tag.id, [tag.folderId, tag.categoryId]]));
assert.deepStrictEqual(v10Locations.get('m1'), ['head_accessories', 'hairband_ribbon']);
assert.deepStrictEqual(v10Locations.get('m2'), ['head_accessories', 'themed_hair_ornament']);
assert.deepStrictEqual(v10Locations.get('m3'), ['traditional_clothes', 'traditional_china']);
assert.deepStrictEqual(v10Locations.get('m4'), ['protective_clothes', 'shoulder_armor']);
assert.deepStrictEqual(v10Locations.get('m5'), ['underwear_swim', 'other_swim']);
assert.deepStrictEqual(v10Locations.get('m6'), ['legwear_footwear', 'heels']);
assert.deepStrictEqual(v10Locations.get('m7'), ['nature', 'flower_species']);
assert.deepStrictEqual(v10Locations.get('m8'), ['urban_architecture', 'tower_landmark']);
assert.deepStrictEqual(v10Locations.get('m9'), ['adult_body', 'penis']);
assert.deepStrictEqual(v10Locations.get('m10'), ['franchise_clothes', 'school_variant']);
assert(migratedV10.removed.folders.includes('building_parts'));
assert(migratedV10.removed.folders.includes('urban_architecture'));
['short_boots', 'work_special_shoes']
  .forEach(id => assert(migratedV10.removed.categories.some(row => api.rowKey(row) === api.tupleKey('legwear_footwear', id))));
['thigh_boots', 'knee_boots', 'single_thigh_boot', 'single_knee_boot']
  .forEach(name => assert(migratedV10.removed.tags.some(row => api.rowKey(row) === api.tupleKey('legwear_footwear', 'short_boots', name))));
assert(migratedV10.removed.tags.some(
  row => api.rowKey(row) === api.tupleKey('legwear_footwear', 'stockings', 'thighhighs_under_boots')
));
['flower_general', 'flower_species', 'tree', 'foliage_vine', 'grass_crop', 'potted_shrub', 'unusual_plant']
  .forEach(id => assert.deepStrictEqual(migratedV10.overrides.categories[api.tupleKey('nature', id)], { name: '我的植物' }));
assert.deepStrictEqual(migratedV10.order, { folders: [], categories: {}, tags: {} });
assert.strictEqual(migratedV10.baseCatalogVersion, 17);

const v10Raw = {
  schemaVersion: 1,
  baseCatalogVersion: 10,
  added: { folders: [], categories: [], tags: [
    { id: 'n1', folderId: 'franchise_clothes', categoryId: 'character_costume', name: 'unofficial_precure_costume' },
    { id: 'n2', folderId: 'franchise_clothes', categoryId: 'character_costume', name: 'my_character_costume' },
    { id: 'n3', folderId: 'nature', categoryId: 'aquatic_flower', name: 'lotus' },
    { id: 'n4', folderId: 'nature', categoryId: 'fungus_fantasy', name: 'mushroom' },
    { id: 'n5', folderId: 'urban_architecture', categoryId: 'ruin_structure', name: 'ruins' }
  ] },
  overrides: { folders: {}, categories: { '["nature","aquatic_flower"]': { name: '水生植物' } }, tags: {} },
  removed: { folders: [], categories: [['franchise_clothes', 'character_costume'], ['nature', 'fungus_fantasy']], tags: [] },
  order: { folders: ['nature'], categories: { nature: ['aquatic_flower'] }, tags: {} }
};
const migratedV11 = api.normalizeLibraryEdits(v10Raw, catalog);
const v11Locations = new Map(migratedV11.added.tags.map(tag => [tag.id, [tag.folderId, tag.categoryId]]));
assert.deepStrictEqual(v11Locations.get('n1'), ['franchise_clothes', 'franchise_outfit']);
assert.deepStrictEqual(v11Locations.get('n2'), ['uniform_costume', 'themed_costume']);
assert.deepStrictEqual(v11Locations.get('n3'), ['nature', 'flower_species']);
assert.deepStrictEqual(v11Locations.get('n4'), ['nature', 'grass_crop']);
assert.deepStrictEqual(v11Locations.get('n5'), ['urban_architecture', 'tower_landmark']);
assert(migratedV11.removed.categories.some(row => api.rowKey(row) === api.tupleKey('uniform_costume', 'themed_costume')));
assert(migratedV11.removed.categories.some(row => api.rowKey(row) === api.tupleKey('franchise_clothes', 'franchise_outfit')));
assert(migratedV11.removed.categories.some(row => api.rowKey(row) === api.tupleKey('nature', 'grass_crop')));
assert.deepStrictEqual(migratedV11.overrides.categories[api.tupleKey('nature', 'flower_species')], { name: '水生植物' });
assert.deepStrictEqual(migratedV11.overrides.categories[api.tupleKey('nature', 'grass_crop')], { name: '水生植物' });
assert.deepStrictEqual(migratedV11.order, { folders: [], categories: {}, tags: {} });
assert.strictEqual(migratedV11.baseCatalogVersion, 17);

const v11StructuralRaw = {
  schemaVersion: 1,
  baseCatalogVersion: 11,
  added: {
    folders: [{ id: 'custom-folder-v12', name: '自建词库' }],
    categories: [
      { id: 'my-clothing-state', folderId: 'clothing_state', name: '自建服装状态' },
      { id: 'surface_decor', folderId: 'body_detail', name: '体表装饰' },
      { id: 'rose', folderId: 'nature', name: '玫瑰' },
      { id: 'surface', folderId: 'urban_architecture', name: '建筑表面' }
    ],
    tags: [
      { id: 'p1', folderId: 'clothing_state', categoryId: 'open_wear', name: 'open_shirt' },
      { id: 'p2', folderId: 'body_detail', categoryId: 'surface_decor', name: 'paint_on_body' },
      { id: 'p3', folderId: 'nature', categoryId: 'rose', name: 'rose' },
      { id: 'p4', folderId: 'urban_architecture', categoryId: 'surface', name: 'tiles' }
    ]
  },
  overrides: {
    folders: {
      clothing_state: { name: '服装状态', icon: 'S' },
      clothing_appearance: { name: '服装属性' }
    },
    categories: {
      '["clothing_state","damaged_dirty"]': { name: '旧状态名', icon: 'D' },
      '["clothing_appearance","damaged_dirty"]': { name: '新属性名' },
      '["body_detail","surface_decor"]': { name: '体表附着' },
      '["nature","rose"]': { name: '花卉品种' },
      '["urban_architecture","surface"]': { name: '建筑表面' }
    },
    tags: {
      '["clothing_state","open_wear","open_shirt"]': { cn: '敞开衬衫' },
      '["body_detail","surface_decor","paint_on_body"]': { cn: '身体颜料' },
      '["nature","rose","rose"]': { cn: '玫瑰花' },
      '["urban_architecture","surface","tiles"]': { cn: '瓷砖' }
    }
  },
  removed: {
    folders: ['clothing_state', 'custom-folder-v12'],
    categories: [
      ['clothing_state', 'damaged_dirty'],
      ['body_detail', 'surface_decor'],
      ['nature', 'rose'],
      ['urban_architecture', 'surface']
    ],
    tags: [
      ['clothing_state', 'unworn_missing', 'no_shirt'],
      ['body', 'surface_decor', 'paint_on_body'],
      ['nature', 'rose', 'rose'],
      ['urban_architecture', 'surface', 'tiles']
    ]
  },
  order: {
    folders: ['clothing_state', 'nature'],
    categories: { clothing_state: ['open_wear'], nature: ['rose'] },
    tags: { '["nature","rose"]': ['rose'] }
  }
};

const migratedV12 = api.normalizeLibraryEdits(v11StructuralRaw, catalog);
assert.deepStrictEqual(api.migrateV12Location('clothing_state', 'open_wear'), ['clothing_appearance', 'open_wear']);
assert.deepStrictEqual(api.migrateV12Location('body', 'surface_decor'), ['body_detail', 'surface_stain']);
assert.deepStrictEqual(api.migrateV12Location('nature', 'rose'), ['nature', 'flower_species']);
assert.deepStrictEqual(api.migrateV12Location('urban_architecture', 'surface'), ['building_parts', 'surface']);
assert.deepStrictEqual(migratedV12.added.categories.map(item => [item.folderId, item.id]), [
  ['clothing_appearance', 'my-clothing-state'],
  ['body_detail', 'surface_stain'],
  ['nature', 'flower_species'],
  ['building_parts', 'surface']
]);
assert.deepStrictEqual(migratedV12.added.tags.map(tag => [tag.folderId, tag.categoryId]), [
  ['clothing_appearance', 'open_wear'],
  ['body_detail', 'surface_stain'],
  ['nature', 'flower_species'],
  ['building_parts', 'surface']
]);
assert(!migratedV12.removed.folders.includes('clothing_state'));
assert(!migratedV12.removed.folders.includes('clothing_appearance'));
assert(migratedV12.removed.folders.includes('custom-folder-v12'));
const v12RemovedCategories = new Set(migratedV12.removed.categories.map(api.rowKey));
['damaged_dirty', 'unworn_missing', 'open_wear'].forEach(id => {
  assert(v12RemovedCategories.has(api.tupleKey('clothing_appearance', id)));
});
assert(v12RemovedCategories.has(api.tupleKey('body_detail', 'surface_stain')));
assert(v12RemovedCategories.has(api.tupleKey('nature', 'flower_species')));
assert(v12RemovedCategories.has(api.tupleKey('building_parts', 'surface')));
assert.deepStrictEqual(migratedV12.removed.tags, [
  ['clothing_appearance', 'unworn_missing', 'no_shirt'],
  ['body_detail', 'surface_stain', 'paint_on_body'],
  ['nature', 'flower_species', 'rose'],
  ['building_parts', 'surface', 'tiles']
]);
assert.deepStrictEqual(migratedV12.overrides.folders.clothing_appearance, { name: '服装属性', icon: 'S' });
assert.strictEqual(migratedV12.overrides.folders.clothing_state, undefined);
assert.deepStrictEqual(
  migratedV12.overrides.categories[api.tupleKey('clothing_appearance', 'damaged_dirty')],
  { name: '新属性名', icon: 'D' }
);
assert.deepStrictEqual(migratedV12.overrides.categories[api.tupleKey('body_detail', 'surface_stain')], { name: '体表附着' });
assert.deepStrictEqual(migratedV12.overrides.categories[api.tupleKey('nature', 'flower_species')], { name: '花卉品种' });
assert.deepStrictEqual(migratedV12.overrides.categories[api.tupleKey('building_parts', 'surface')], { name: '建筑表面' });
assert.deepStrictEqual(migratedV12.overrides.tags[api.tupleKey('clothing_appearance', 'open_wear', 'open_shirt')], { cn: '敞开衬衫' });
assert.deepStrictEqual(migratedV12.overrides.tags[api.tupleKey('body_detail', 'surface_stain', 'paint_on_body')], { cn: '身体颜料' });
assert.deepStrictEqual(migratedV12.overrides.tags[api.tupleKey('nature', 'flower_species', 'rose')], { cn: '玫瑰花' });
assert.deepStrictEqual(migratedV12.overrides.tags[api.tupleKey('building_parts', 'surface', 'tiles')], { cn: '瓷砖' });
assert.deepStrictEqual(migratedV12.order, { folders: [], categories: {}, tags: {} });
assert.strictEqual(migratedV12.baseCatalogVersion, 17);
assert.deepStrictEqual(api.normalizeLibraryEdits(migratedV12, catalog), migratedV12);

const v12ArmorRaw = {
  schemaVersion: 1,
  baseCatalogVersion: 12,
  added: {
    folders: [],
    categories: [],
    tags: [
      { id: 'q1', folderId: 'traditional_clothes', categoryId: 'traditional_india', name: 'sari' },
      { id: 'q2', folderId: 'protective_clothes', categoryId: 'torso_armor', name: 'armor' },
      { id: 'q3', folderId: 'protective_clothes', categoryId: 'powered_armor', name: 'power_suit' },
      { id: 'q4', folderId: 'protective_clothes', categoryId: 'pads_support', name: 'knee_pads' },
      { id: 'q5', folderId: 'protective_clothes', categoryId: 'pads_support', name: 'arm_sling' },
      { id: 'q6', folderId: 'protective_clothes', categoryId: 'protective_suit', name: 'respirator' },
      { id: 'q7', folderId: 'protective_clothes', categoryId: 'torso_armor', name: 'custom_chest_plate' },
      { id: 'q8', folderId: 'protective_clothes', categoryId: 'pads_support', name: 'custom_elbow_guard' },
      { id: 'q9', folderId: 'protective_clothes', categoryId: 'powered_armor', name: 'living_armor' }
    ]
  },
  overrides: {
    folders: {},
    categories: {
      '["traditional_clothes","traditional_india"]': { name: 'My regional clothes' },
      '["traditional_clothes","traditional_other"]': { icon: 'T' },
      '["protective_clothes","pads_support"]': { name: 'Old pads' },
      '["protective_clothes","torso_armor"]': { name: 'My chest armor' },
      '["protective_clothes","protective_suit"]': { color: '#123456' }
    },
    tags: {
      '["protective_clothes","torso_armor","armor"]': { cn: 'old armor' },
      '["protective_clothes","full_armor","armor"]': { wiki: 'destination wins' },
      '["protective_clothes","protective_suit","respirator"]': { cn: 'respirator edit' },
      '["protective_clothes","pads_support","knee_pads"]': { cn: 'knee edit' }
    }
  },
  removed: {
    folders: [],
    categories: [
      ['traditional_clothes', 'traditional_africa'],
      ['protective_clothes', 'powered_armor'],
      ['protective_clothes', 'pads_support'],
      ['protective_clothes', 'torso_armor']
    ],
    tags: [
      ['traditional_clothes', 'traditional_india', 'sari'],
      ['protective_clothes', 'torso_armor', 'black_armor'],
      ['protective_clothes', 'protective_suit', 'respirator'],
      ['protective_clothes', 'pads_support', 'knee_pads']
    ]
  },
  order: {
    folders: ['protective_clothes'],
    categories: { protective_clothes: ['powered_armor', 'pads_support'] },
    tags: { '["protective_clothes","pads_support"]': ['knee_pads'] }
  }
};

const migratedV13 = api.normalizeLibraryEdits(v12ArmorRaw, catalog);
const v13Locations = new Map(migratedV13.added.tags.map(tag => [tag.id, [tag.folderId, tag.categoryId]]));
assert.deepStrictEqual(v13Locations.get('q1'), ['traditional_clothes', 'traditional_other']);
assert.deepStrictEqual(v13Locations.get('q2'), ['protective_clothes', 'full_armor']);
assert.deepStrictEqual(v13Locations.get('q3'), ['protective_clothes', 'protective_suit']);
assert.deepStrictEqual(v13Locations.get('q4'), ['protective_clothes', 'leg_armor']);
assert.deepStrictEqual(v13Locations.get('q5'), ['body_detail', 'bandage_patch']);
assert.deepStrictEqual(v13Locations.get('q6'), ['protective_clothes', 'civilian_helmet']);
assert.deepStrictEqual(v13Locations.get('q7'), ['protective_clothes', 'torso_armor']);
assert.deepStrictEqual(v13Locations.get('q8'), ['protective_clothes', 'arm_armor']);
assert.deepStrictEqual(v13Locations.get('q9'), ['people', 'fantasy_person']);

assert.deepStrictEqual(api.migrateV13Location('traditional_clothes', 'traditional_india', 'custom'), ['traditional_clothes', 'traditional_other']);
assert.deepStrictEqual(api.migrateV13Location('protective_clothes', 'powered_armor', 'custom'), ['protective_clothes', 'protective_suit']);
assert.deepStrictEqual(api.migrateV13Location('protective_clothes', 'pads_support', 'custom_shin_guard'), ['protective_clothes', 'leg_armor']);
assert.deepStrictEqual(api.migrateV13Location('protective_clothes', 'torso_armor', 'custom_chainmail'), ['protective_clothes', 'flexible_armor']);
assert.strictEqual(api.migrateV13CategoryLocations('protective_clothes', 'pads_support').length, 5);
assert.strictEqual(api.migrateV13CategoryLocations('protective_clothes', 'torso_armor').length, 6);

const v13RemovedCategories = new Set(migratedV13.removed.categories.map(api.rowKey));
assert(v13RemovedCategories.has(api.tupleKey('traditional_clothes', 'traditional_other')));
assert(v13RemovedCategories.has(api.tupleKey('protective_clothes', 'protective_suit')));
['full_armor', 'torso_armor', 'arm_armor', 'leg_armor', 'flexible_armor'].forEach(categoryId => {
  assert(v13RemovedCategories.has(api.tupleKey('protective_clothes', categoryId)));
});
assert(!v13RemovedCategories.has(api.tupleKey('protective_clothes', 'pads_support')));

const v13RemovedTags = new Set(migratedV13.removed.tags.map(api.rowKey));
assert(v13RemovedTags.has(api.tupleKey('traditional_clothes', 'traditional_other', 'sari')));
assert(v13RemovedTags.has(api.tupleKey('protective_clothes', 'full_armor', 'black_armor')));
assert(v13RemovedTags.has(api.tupleKey('protective_clothes', 'civilian_helmet', 'respirator')));
assert(v13RemovedTags.has(api.tupleKey('protective_clothes', 'leg_armor', 'knee_pads')));
assert(v13RemovedTags.has(api.tupleKey('protective_clothes', 'arm_armor', 'elbow_pads')));
assert(v13RemovedTags.has(api.tupleKey('body_detail', 'bandage_patch', 'arm_sling')));

assert.deepStrictEqual(
  migratedV13.overrides.categories[api.tupleKey('traditional_clothes', 'traditional_other')],
  { name: 'My regional clothes', icon: 'T' }
);
assert.deepStrictEqual(
  migratedV13.overrides.categories[api.tupleKey('protective_clothes', 'torso_armor')],
  { name: 'My chest armor' }
);
assert.strictEqual(migratedV13.overrides.categories[api.tupleKey('protective_clothes', 'pads_support')], undefined);
assert.deepStrictEqual(
  migratedV13.overrides.tags[api.tupleKey('protective_clothes', 'full_armor', 'armor')],
  { cn: 'old armor', wiki: 'destination wins' }
);
assert.deepStrictEqual(
  migratedV13.overrides.tags[api.tupleKey('protective_clothes', 'civilian_helmet', 'respirator')],
  { cn: 'respirator edit' }
);
assert.deepStrictEqual(
  migratedV13.overrides.tags[api.tupleKey('protective_clothes', 'leg_armor', 'knee_pads')],
  { cn: 'knee edit' }
);
assert.deepStrictEqual(migratedV13.order, { folders: [], categories: {}, tags: {} });
assert.strictEqual(migratedV13.baseCatalogVersion, 17);
assert.deepStrictEqual(api.normalizeLibraryEdits(migratedV13, catalog), migratedV13);

const v13BootRaw = {
  schemaVersion: 1,
  baseCatalogVersion: 13,
  added: {
    folders: [],
    categories: [],
    tags: [
      { id: 'r1', folderId: 'legwear_footwear', categoryId: 'tall_boots', name: 'thigh_boots' },
      { id: 'r2', folderId: 'legwear_footwear', categoryId: 'tall_boots', name: 'thighhighs_under_boots' },
      { id: 'r3', folderId: 'legwear_footwear', categoryId: 'tall_boots', name: 'custom_tall_boot' },
      { id: 'r4', folderId: 'other', categoryId: 'other_a_e', name: 'bootjob' }
    ]
  },
  overrides: {
    folders: {},
    categories: {
      '["legwear_footwear","tall_boots"]': { name: 'My tall boots' },
      '["legwear_footwear","short_boots"]': { icon: 'B' },
      '["other","other_a_e"]': { name: 'Other A-E' }
    },
    tags: {
      '["legwear_footwear","tall_boots","thigh_boots"]': { cn: 'old edit' },
      '["legwear_footwear","short_boots","thigh_boots"]': { wiki: 'destination edit' },
      '["other","other_a_e","bootjob"]': { cn: 'adult edit' }
    }
  },
  removed: {
    folders: [],
    categories: [
      ['legwear_footwear', 'tall_boots'],
      ['other', 'other_a_e']
    ],
    tags: [
      ['legwear_footwear', 'tall_boots', 'knee_boots']
    ]
  },
  order: {
    folders: ['people', 'legwear_footwear'],
    categories: {
      legwear_footwear: ['tall_boots', 'short_boots'],
      people: ['age']
    },
    tags: {
      '["legwear_footwear","tall_boots"]': ['thigh_boots'],
      '["legwear_footwear","short_boots"]': ['boots'],
      '["people","age"]': ['adult']
    }
  }
};

const migratedV14 = api.normalizeLibraryEdits(v13BootRaw, catalog);
const v14Locations = new Map(migratedV14.added.tags.map(tag => [tag.id, [tag.folderId, tag.categoryId]]));
assert.deepStrictEqual(v14Locations.get('r1'), ['legwear_footwear', 'short_boots']);
assert.deepStrictEqual(v14Locations.get('r2'), ['legwear_footwear', 'stockings']);
assert.deepStrictEqual(v14Locations.get('r3'), ['legwear_footwear', 'short_boots']);
assert.deepStrictEqual(v14Locations.get('r4'), ['adult', 'adult_sex']);
assert.deepStrictEqual(api.migrateV14Location('legwear_footwear', 'tall_boots', 'knee_boots'), ['legwear_footwear', 'short_boots']);
assert.deepStrictEqual(api.migrateV14Location('legwear_footwear', 'tall_boots', 'thighhighs_under_boots'), ['legwear_footwear', 'stockings']);
assert.deepStrictEqual(api.migrateV14Location('other', 'other_a_e', 'bootjob'), ['adult', 'adult_sex']);

const v14RemovedCategories = new Set(migratedV14.removed.categories.map(api.rowKey));
assert(!v14RemovedCategories.has(api.tupleKey('legwear_footwear', 'tall_boots')));
assert(!v14RemovedCategories.has(api.tupleKey('legwear_footwear', 'short_boots')));
assert(v14RemovedCategories.has(api.tupleKey('other', 'other_a_e')));
const v14RemovedTags = new Set(migratedV14.removed.tags.map(api.rowKey));
['thigh_boots', 'knee_boots', 'single_thigh_boot', 'single_knee_boot', 'custom_tall_boot'].forEach(name => {
  assert(v14RemovedTags.has(api.tupleKey('legwear_footwear', 'short_boots', name)));
});
assert(v14RemovedTags.has(api.tupleKey('legwear_footwear', 'stockings', 'thighhighs_under_boots')));
assert(v14RemovedTags.has(api.tupleKey('adult', 'adult_sex', 'bootjob')));

assert.deepStrictEqual(
  migratedV14.overrides.categories[api.tupleKey('legwear_footwear', 'short_boots')],
  { name: 'My tall boots', icon: 'B' }
);
assert.deepStrictEqual(
  migratedV14.overrides.tags[api.tupleKey('legwear_footwear', 'short_boots', 'thigh_boots')],
  { cn: 'old edit', wiki: 'destination edit' }
);
assert.deepStrictEqual(
  migratedV14.overrides.tags[api.tupleKey('adult', 'adult_sex', 'bootjob')],
  { cn: 'adult edit' }
);
assert.deepStrictEqual(migratedV14.order.folders, ['people', 'legwear_footwear']);
assert.deepStrictEqual(migratedV14.order.categories, { people: ['age'] });
assert.deepStrictEqual(migratedV14.order.tags, { '["people","age"]': ['adult'] });
assert.strictEqual(migratedV14.baseCatalogVersion, 17);
assert.deepStrictEqual(api.normalizeLibraryEdits(migratedV14, catalog), migratedV14);

console.log('v6/v7/v8/v9/v10/v11/v12/v13/v14/v15/v16 -> v17 library migration: ok');
