const assert = require('assert');
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const root = __dirname;
const catalog = {
  version: 9,
  sourceCount: 8,
  sourceRowCount: 8,
  fallbackCount: 0,
  tagCount: 8,
  folders: [
    { id: 'digital_media', name: '数码影音', icon: '▣', accent: '#d29a60', description: '设备', tagCount: 1, categories: [
      { id: 'phone_device', name: '手机电话', tagCount: 1, tags: [{ id: 'smartphone', name: 'smartphone', cn: '智能手机', count: 1, nsfw: false }] }
    ] },
    { id: 'clothing_detail', name: '服装细节', icon: '◫', accent: '#b4ce68', description: '结构', tagCount: 3, categories: [
      { id: 'other_structure', name: '其他结构', tagCount: 2, tags: [{ id: 'crinoline', name: 'crinoline', cn: '裙撑', count: 10, nsfw: false, wiki: '用于支撑裙装轮廓的硬质内衬结构。' }, { id: 'petticoat', name: 'petticoat', cn: '衬裙', count: 5, nsfw: false }] },
      { id: 'open_wear', name: '开合状态', tagCount: 1, tags: [{ id: 'open_shirt', name: 'open_shirt', cn: '敞开衬衫', count: 1, nsfw: false }] }
    ] },
    { id: 'head_accessories', name: '头部配饰', icon: '✦', accent: '#e3c459', description: '发饰', tagCount: 1, categories: [
      { id: 'hair_accessory', name: '发饰', tagCount: 1, tags: [{ id: 'hair_ribbon', name: 'hair_ribbon', cn: '发带', count: 1, nsfw: false }] }
    ] },
    { id: 'face', name: '面部五官', icon: '◉', accent: '#43c2df', description: '五官', tagCount: 2, categories: [
      { id: 'eyebrows', name: '眉毛', tagCount: 1, tags: [{ id: 'eyebrows', name: 'eyebrows', cn: '眉毛', count: 1, nsfw: false }] },
      { id: 'nose', name: '鼻子', tagCount: 1, tags: [{ id: 'nose', name: 'nose', cn: '鼻子', count: 1, nsfw: false }] }
    ] },
    { id: 'text_meta', name: '文字符号', icon: '#', accent: '#9aa4b8', description: '符号', tagCount: 1, categories: [
      { id: 'music_symbol', name: '乐谱符号', tagCount: 1, tags: [{ id: 'notes', name: 'notes', cn: '音符', count: 1, nsfw: false }] }
    ] },
    { id: 'sensitive', name: '暴力敏感', icon: '!', accent: '#c94f62', description: '敏感', tagCount: 1, categories: [
      { id: 'blood', name: '血液', tagCount: 1, tags: [{ id: 'blood', name: 'blood', cn: '血液', count: 1, nsfw: true }] }
    ] }
  ]
};

catalog.folders.unshift({
  id: 'stress_library', name: '多分类测试', icon: '◎', accent: '#78a7ff', description: '布局压力测试',
  tagCount: 28,
  categories: Array.from({ length: 28 }, (_, index) => ({
    id: `stress_${index + 1}`,
    name: `细分类${index + 1}`,
    tagCount: 1,
    tags: [{ id: `stress_tag_${index + 1}`, name: `stress_tag_${index + 1}`, cn: `测试${index + 1}`, count: 1, nsfw: false }]
  }))
});

const legacyEdits = {
  schemaVersion: 1,
  baseCatalogVersion: 6,
  updatedAt: null,
  added: { folders: [], categories: [], tags: [
    { id: 'custom-smartphone', folderId: 'culture_objects', categoryId: 'phone_computer', name: 'smartphone', cn: '智能手机', count: 0, nsfw: false }
  ] },
  overrides: { folders: {}, categories: {} },
  removed: { folders: [], categories: [], tags: [['hair', 'hair_accessory', 'hair_ribbon']] }
};

let browser;
(async () => {
  browser = await chromium.launch({
    headless: true,
    executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
  });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1008 } });
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  page.on('console', message => { if (message.type() === 'error') errors.push(message.text()); });
  await page.route('http://prompt.test/**', async route => {
    const url = new URL(route.request().url());
    if (url.pathname === '/api/catalog') {
      await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(catalog) });
      return;
    }
    const filename = url.pathname === '/' ? 'index.html' : url.pathname.slice(1);
    const filePath = path.join(root, filename);
    const contentType = filename.endsWith('.css') ? 'text/css' : filename.endsWith('.js') ? 'text/javascript' : 'text/html';
    await route.fulfill({ status: 200, contentType, body: fs.readFileSync(filePath) });
  });
  await page.addInitScript(({ legacyEdits }) => {
    localStorage.setItem('prompt-atelier-ui-scale', '125');
    localStorage.setItem('prompt-atelier-library-v1', JSON.stringify(legacyEdits));
    Object.defineProperty(navigator, 'clipboard', {
      configurable: true,
      value: {
        writeText: async text => { window.__copiedText = String(text); }
      }
    });
  }, { legacyEdits });
  await page.goto('http://prompt.test/', { waitUntil: 'networkidle' });
  console.log('ui loaded');
  await page.locator('.library-card').first().waitFor();
  assert.strictEqual(await page.evaluate(() => document.documentElement.style.zoom), '1.25');
  assert.strictEqual(await page.locator('#open-settings').isVisible(), true);
  assert.strictEqual(await page.locator('#brand-mark .brand-logo-image').isVisible(), true);
  assert((await page.locator('#app-favicon').getAttribute('href')).includes('grimoire-logo-transparent-v2-256.png'));
  const stressLayout = await page.evaluate(() => {
    const tabs = document.querySelector('#category-tabs');
    const head = document.querySelector('.category-head').getBoundingClientRect();
    const cloud = document.querySelector('#tag-cloud').getBoundingClientRect();
    const add = document.querySelector('#add-category').getBoundingClientRect();
    const tabsRect = tabs.getBoundingClientRect();
    const title = document.querySelector('#folder-title').getBoundingClientRect();
    return {
      scrolls: tabs.scrollWidth > tabs.clientWidth,
      scrollWidth: tabs.scrollWidth,
      clientWidth: tabs.clientWidth,
      tabCount: tabs.querySelectorAll('.category-tab').length,
      flexWrap: getComputedStyle(tabs).flexWrap,
      tabsDisplay: getComputedStyle(tabs).display,
      headHeight: head.height,
      cloudHeight: cloud.height,
      addAligned: Math.abs(add.top - tabsRect.top) < 12,
      sameRow: Math.min(title.bottom, tabsRect.bottom) - Math.max(title.top, tabsRect.top) > 8
    };
  });
  assert.strictEqual(stressLayout.scrolls, true, JSON.stringify(stressLayout));
  assert(stressLayout.headHeight < 210, `subcategory header grew to ${stressLayout.headHeight}px`);
  assert(stressLayout.cloudHeight > 160, `tag cloud collapsed to ${stressLayout.cloudHeight}px`);
  assert.strictEqual(stressLayout.addAligned, true);
  assert.strictEqual(stressLayout.sameRow, true, JSON.stringify(stressLayout));
  console.log('horizontal stress layout ok');
  await page.evaluate(() => [...document.querySelectorAll('.category-tab')].at(-1).click());
  await page.waitForTimeout(50);
  const activeVisible = await page.evaluate(() => {
    const tabs = document.querySelector('#category-tabs').getBoundingClientRect();
    const active = document.querySelector('.category-tab.active').closest('.category-tab-wrap').getBoundingClientRect();
    return active.top >= tabs.top - 1 && active.bottom <= tabs.bottom + 1;
  });
  assert.strictEqual(activeVisible, true);
  console.log('active category reveal ok');

  await page.locator('#tag-search-input').fill('crinoline');
  await page.locator('.search-result').first().waitFor();
  const searchControlOrder = await page.evaluate(() => {
    const clear = document.querySelector('#clear-search').getBoundingClientRect();
    const scope = document.querySelector('.search-scope').getBoundingClientRect();
    return clear.right <= scope.left;
  });
  assert.strictEqual(searchControlOrder, true, 'clear search should sit before the scope selector');
  const searchResultText = await page.locator('.search-result').first().innerText();
  assert(searchResultText.includes('裙撑'));
  assert(searchResultText.includes('服装细节'));
  assert(searchResultText.includes('其他结构'));
  assert(searchResultText.includes('支撑裙装轮廓'));
  await page.locator('.search-result').first().click();
  assert.strictEqual(await page.locator('#folder-title').textContent(), '服装细节');
  assert.strictEqual(await page.locator('#category-name').textContent(), '其他结构');
  assert.strictEqual(await page.locator('[data-action="toggle-tag"][data-tag="crinoline"]').evaluate(node => node.classList.contains('active')), true);
  assert.strictEqual(await page.locator('#prompt-editor').inputValue(), 'crinoline');
  assert.strictEqual(await page.evaluate(() => window.__copiedText), 'crinoline');
  await page.locator('#tag-search-input').fill('petticoat');
  await page.locator('.search-result').first().click();
  assert.strictEqual(await page.locator('#prompt-editor').inputValue(), 'crinoline, petticoat');
  assert.strictEqual(await page.evaluate(() => window.__copiedText), 'petticoat');
  await page.locator('#search-scope-library').click();
  await page.locator('#tag-search-input').fill('open_shirt');
  await page.locator('.search-result').first().waitFor();
  assert((await page.locator('.search-result').first().innerText()).includes('服装细节'));
  await page.locator('#search-scope-local').click();
  await page.locator('.search-empty').waitFor();
  assert.strictEqual(await page.locator('.search-result').count(), 0);
  await page.locator('#tag-search-input').fill('crinoline');
  assert.strictEqual(await page.locator('.search-result').count(), 1);
  await page.locator('#clear-search').click();
  await page.evaluate(() => { window.__copiedText = 'not-copied'; });
  const directTag = page.locator('[data-action="toggle-tag"][data-tag="petticoat"]');
  await directTag.click();
  assert.strictEqual(await page.evaluate(() => window.__copiedText), 'petticoat');
  assert.strictEqual(await directTag.evaluate(node => node.classList.contains('active')), false);
  const toastTheme = await page.locator('#toast').evaluate(node => {
    const style = getComputedStyle(node);
    const marker = getComputedStyle(node, '::before');
    return {
      background: style.backgroundColor,
      border: style.borderColor,
      fontSize: parseFloat(style.fontSize),
      height: node.getBoundingClientRect().height,
      markerWidth: parseFloat(marker.width),
      text: node.textContent
    };
  });
  assert(!toastTheme.background.includes('240, 243, 248'), JSON.stringify(toastTheme));
  assert(toastTheme.fontSize <= 12, JSON.stringify(toastTheme));
  assert(toastTheme.height < 44, JSON.stringify(toastTheme));
  assert(toastTheme.markerWidth >= 5, JSON.stringify(toastTheme));
  assert(toastTheme.text.includes('petticoat'));
  await directTag.click();
  assert.strictEqual(await page.evaluate(() => window.__copiedText), 'petticoat');
  assert.strictEqual(await directTag.evaluate(node => node.classList.contains('active')), true);
  console.log('global/library/local search, copy and jump-select ok');

  await page.locator('#toggle-manage').click();
  const management = await page.evaluate(() => {
    const firstShell = document.querySelector('.library-card-shell.manage-shell');
    const shellRect = firstShell.getBoundingClientRect();
    const actionsRect = firstShell.querySelector('.item-manage-actions').getBoundingClientRect();
    return {
      folderCount: document.querySelectorAll('.library-card-shell.manage-shell').length,
      folderEditCount: document.querySelectorAll('[data-action="edit-folder"]').length,
      folderDeleteCount: document.querySelectorAll('[data-action="delete-folder"]').length,
      categoryDraggable: [...document.querySelectorAll('.category-tab-wrap.manage-shell')].every(node => node.draggable),
      tagDraggable: [...document.querySelectorAll('.tag-chip-wrap.manage-shell')].every(node => node.draggable),
      tagEditCount: document.querySelectorAll('[data-action="edit-tag"]').length,
      actionsInside: actionsRect.top >= shellRect.top - 1 && actionsRect.bottom <= shellRect.bottom + 1,
      categoryRightPadding: (() => {
        const wrapper = document.querySelector('.category-tab-wrap.manage-shell').getBoundingClientRect();
        const lastControl = document.querySelector('.category-tab-wrap.manage-shell [data-action="delete-category"]').getBoundingClientRect();
        return wrapper.right - lastControl.right;
      })()
    };
  });
  assert.strictEqual(management.folderEditCount, management.folderCount);
  assert.strictEqual(management.folderDeleteCount, management.folderCount);
  assert.strictEqual(management.categoryDraggable, true);
  assert.strictEqual(management.tagDraggable, true);
  assert.strictEqual(management.tagEditCount, 2);
  assert.strictEqual(management.actionsInside, true, JSON.stringify(management));
  assert(management.categoryRightPadding >= 5, `category controls lack padding: ${management.categoryRightPadding}px`);
  const stickyHeaderProtected = await page.evaluate(() => {
    const panel = document.querySelector('.library-panel');
    panel.scrollTop = 90;
    const button = document.querySelector('#toggle-manage');
    const rect = button.getBoundingClientRect();
    const topElement = document.elementFromPoint(rect.left + rect.width / 2, rect.top + rect.height / 2);
    const protectedHeader = Boolean(topElement?.closest('#toggle-manage'));
    panel.scrollTop = 0;
    return protectedHeader;
  });
  assert.strictEqual(stickyHeaderProtected, true, 'scrolling cards covered the 完成 button');
  await page.locator('[data-action="edit-folder"]').first().click();
  assert.strictEqual(await page.locator('.folder-field').first().isVisible(), true);
  assert.strictEqual(await page.locator('.tag-field').first().isVisible(), false);
  await page.locator('#cancel-library-editor').click();

  const dragOrder = await page.evaluate(() => {
    function dragFirstToSecond(selector) {
      const [source, target] = [...document.querySelectorAll(selector)];
      source.querySelector('.manage-drag').dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }));
      const transfer = new DataTransfer();
      source.dispatchEvent(new DragEvent('dragstart', { bubbles: true, cancelable: true, dataTransfer: transfer }));
      target.dispatchEvent(new DragEvent('dragover', { bubbles: true, cancelable: true, dataTransfer: transfer }));
      target.dispatchEvent(new DragEvent('drop', { bubbles: true, cancelable: true, dataTransfer: transfer }));
    }
    dragFirstToSecond('.library-card-shell.manage-shell');
    dragFirstToSecond('.category-tab-wrap.manage-shell');
    dragFirstToSecond('.tag-chip-wrap.manage-shell');
    return JSON.parse(localStorage.getItem('bubblelens-library-v1')).order;
  });
  assert.strictEqual(dragOrder.folders[0], 'digital_media');
  assert.deepStrictEqual(dragOrder.categories.clothing_detail, ['open_wear', 'other_structure']);
  assert.deepStrictEqual(dragOrder.tags[JSON.stringify(['clothing_detail', 'other_structure'])], ['petticoat', 'crinoline']);
  await page.locator('[data-action="edit-tag"]').first().click();
  assert.strictEqual(await page.locator('#library-editor-title').textContent(), '编辑标签');
  assert.strictEqual(await page.locator('#library-name').inputValue(), 'petticoat');
  await page.locator('#library-name').fill('petticoat_edited');
  await page.locator('#library-cn').fill('衬裙（已编辑）');
  await page.locator('#library-editor-form button[type="submit"]').click();
  await page.locator('[data-action="toggle-tag"][data-tag="petticoat_edited"]').waitFor();
  const editedData = await page.evaluate(() => JSON.parse(localStorage.getItem('bubblelens-library-v1')));
  assert.strictEqual(editedData.overrides.tags[JSON.stringify(['clothing_detail', 'other_structure', 'petticoat'])].name, 'petticoat_edited');
  console.log('management controls and persistent drag ordering ok');

  await page.locator('.category-tab', { hasText: '开合状态' }).click();
  await page.locator('#add-tag').click();
  assert.strictEqual(await page.locator('#tag-source-field').isVisible(), true);
  assert.strictEqual(await page.locator('#tag-database-panel').isVisible(), true);
  assert.strictEqual(await page.locator('#library-editor').evaluate(node => node.classList.contains('database-tag-mode')), true);
  await page.locator('#database-tag-search').fill('crinoline');
  const databaseChoice = page.locator('[data-database-tag="crinoline"]');
  await databaseChoice.waitFor();
  const databaseChoiceText = await databaseChoice.innerText();
  assert(databaseChoiceText.includes('裙撑'));
  assert(databaseChoiceText.includes('用于支撑裙装轮廓的硬质内衬结构。'));
  assert(databaseChoiceText.includes('服装细节'));
  assert(databaseChoiceText.includes('其他结构'));
  await databaseChoice.click();
  assert.strictEqual(await page.locator('#library-editor-submit').textContent(), '复制 1 个标签');
  await page.locator('#library-editor-submit').click();
  await page.locator('[data-action="toggle-tag"][data-tag="crinoline"]').waitFor();
  const copiedData = await page.evaluate(() => JSON.parse(localStorage.getItem('bubblelens-library-v1')));
  const copiedCrinoline = copiedData.added.tags.find(tag => tag.folderId === 'clothing_detail'
    && tag.categoryId === 'open_wear' && tag.name === 'crinoline');
  assert(copiedCrinoline);
  assert.strictEqual(copiedCrinoline.cn, '裙撑');
  assert.strictEqual(copiedCrinoline.wiki, '用于支撑裙装轮廓的硬质内衬结构。');
  assert.strictEqual(copiedCrinoline.count, 10);
  assert.strictEqual(copiedCrinoline.nsfw, false);

  await page.locator('#add-tag').click();
  await page.locator('#database-tag-search').fill('crinoline');
  await databaseChoice.waitFor();
  assert.strictEqual(await databaseChoice.isDisabled(), true);
  assert((await databaseChoice.innerText()).includes('当前分类已有'));
  await page.locator('#database-tag-search').fill('blood');
  await page.locator('.database-tag-empty').waitFor();
  assert((await page.locator('#database-tag-result-count').textContent()).includes('已隐藏 1 个敏感标签'));
  await page.locator('#tag-source-manual').click();
  assert.strictEqual(await page.locator('#library-name-field').isVisible(), true);
  assert.strictEqual(await page.locator('#tag-database-panel').isVisible(), false);
  await page.locator('#cancel-library-editor').click();
  console.log('database tag picker, descriptions, copy, duplicate and NSFW rules ok');

  const migrated = await page.evaluate(() => JSON.parse(localStorage.getItem('bubblelens-library-v1')));
  assert.strictEqual(migrated.baseCatalogVersion, 9);
  assert.deepStrictEqual([migrated.added.tags[0].folderId, migrated.added.tags[0].categoryId], ['digital_media', 'phone_device']);
  assert.deepStrictEqual(migrated.removed.tags[0], ['head_accessories', 'hair_accessory', 'hair_ribbon']);
  await page.locator('#open-settings').click();
  assert.strictEqual(await page.locator('#settings-panel').isVisible(), true);
  const layerOrder = await page.evaluate(() => ({
    sticky: Number(getComputedStyle(document.querySelector('.library-panel .sticky-head')).zIndex),
    backdrop: Number(getComputedStyle(document.querySelector('#settings-backdrop')).zIndex),
    settings: Number(getComputedStyle(document.querySelector('#settings-panel')).zIndex)
  }));
  assert(layerOrder.sticky < layerOrder.backdrop && layerOrder.backdrop < layerOrder.settings, JSON.stringify(layerOrder));
  page.once('dialog', dialog => dialog.accept());
  await page.locator('#restore-builtin').click();
  const restored = await page.evaluate(() => JSON.parse(localStorage.getItem('bubblelens-library-v1')));
  assert.deepStrictEqual(restored.order, { folders: [], categories: {}, tags: {} });
  assert.deepStrictEqual(restored.overrides, { folders: {}, categories: {}, tags: {} });
  assert.deepStrictEqual(restored.removed, { folders: [], categories: [], tags: [] });
  await page.locator('#font-scale').fill('140');
  await page.locator('#save-settings').click();
  assert.strictEqual(await page.evaluate(() => localStorage.getItem('bubblelens-ui-scale')), '140');
  assert.strictEqual(await page.evaluate(() => localStorage.getItem('prompt-atelier-logo-style')), null);
  assert.strictEqual(await page.evaluate(() => localStorage.getItem('bubblelens-logo-style')), null);
  assert.strictEqual(await page.evaluate(() => document.documentElement.style.zoom), '1.4');
  const maxScaleLayout = await page.evaluate(() => {
    const tabs = document.querySelector('#category-tabs');
    return {
      scrolls: tabs.scrollWidth > tabs.clientWidth,
      headHeight: document.querySelector('.category-head').getBoundingClientRect().height,
      cloudHeight: document.querySelector('#tag-cloud').getBoundingClientRect().height,
      searchVisible: document.querySelector('#tag-search').getBoundingClientRect().width > 220,
      libraryFits: document.querySelector('#library-list').scrollWidth <= document.querySelector('#library-list').clientWidth + 2
    };
  });
  assert.strictEqual(maxScaleLayout.scrolls, true);
  assert(maxScaleLayout.headHeight < 240, `140% subcategory header grew to ${maxScaleLayout.headHeight}px`);
  assert(maxScaleLayout.cloudHeight > 120, `140% tag cloud collapsed to ${maxScaleLayout.cloudHeight}px`);
  assert.strictEqual(maxScaleLayout.searchVisible, true, JSON.stringify(maxScaleLayout));
  assert.strictEqual(maxScaleLayout.libraryFits, true, JSON.stringify(maxScaleLayout));
  assert.deepStrictEqual(errors, []);
  console.log('settings and migration ok');
  await browser.close();
  console.log('headless UI + persistent layout scale: ok');
})().catch(async error => {
  console.error(error);
  await browser?.close().catch(() => {});
  process.exitCode = 1;
});
