// 日历订阅 URL 回归测试：确保 Google 按钮的 cid 始终正确（单一编码、webcal 协议、与复制按钮等价）。
// 运行：node test/urls.test.js
'use strict';

const assert = require('assert');
const urls = require('../site/urls.js');

const base = 'https://graffiti-yh.github.io/manzhan-calendar/';
let passed = 0;

function test(name, fn) {
  fn();
  passed += 1;
  console.log('  ok - ' + name);
}

console.log('# 日历订阅 URL 回归测试');

test('城市名经 encodeURIComponent 编码一次', function () {
  assert.strictEqual(urls.icsPath('上海市'), 'ics/%E4%B8%8A%E6%B5%B7%E5%B8%82.ics');
});

test('Google 按钮 cid 为 webcal 订阅协议', function () {
  const cid = urls.googleUrl(base, '上海市').split('cid=')[1];
  assert(cid.startsWith('webcal://'), 'cid 应以 webcal:// 开头，实际：' + cid);
});

test('Google 按钮 cid 不得二次编码（不含 %25）', function () {
  const cid = urls.googleUrl(base, '上海市').split('cid=')[1];
  assert(!cid.includes('%25'), 'cid 出现二次编码 %25，实际：' + cid);
});

test('Google 按钮订阅地址与「复制」按钮完全一致', function () {
  const cid = urls.googleUrl(base, '上海市').split('cid=')[1];
  const httpsUrl = 'https://' + cid.replace(/^webcal:\/\//, '');
  assert.strictEqual(httpsUrl, urls.icsUrl(base, '上海市'));
});

test('all 城市使用 all.ics（ASCII，无编码）', function () {
  const cid = urls.googleUrl(base, 'all').split('cid=')[1];
  assert.strictEqual(cid, 'webcal://graffiti-yh.github.io/manzhan-calendar/ics/all.ics');
});

test('Apple 按钮返回 webcal 直链', function () {
  assert.strictEqual(
    urls.appleUrl(base, '上海市'),
    'webcal://graffiti-yh.github.io/manzhan-calendar/ics/%E4%B8%8A%E6%B5%B7%E5%B8%82.ics'
  );
});

console.log('  ' + passed + ' 个测试全部通过');
