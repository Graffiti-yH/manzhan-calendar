/* 日历订阅 URL 生成逻辑（浏览器与 Node 通用，供 index.html 与回归测试共用） */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.manzhanUrls = factory();
  }
})(typeof self !== 'undefined' ? self : this, function () {
  // 单城市 .ics 路径：城市名经 encodeURIComponent 编码一次
  function icsPath(city) {
    return 'ics/' + encodeURIComponent(city) + '.ics';
  }

  // https 订阅地址（「复制」按钮用）
  function icsUrl(base, city) {
    return base + (city === 'all' ? 'ics/all.ics' : icsPath(city));
  }

  // 转为 webcal 协议
  function toWebcal(url) {
    return url.replace(/^https?:\/\//, 'webcal://');
  }

  // Google 日历一键添加：cid 传 webcal 订阅地址（原样，不做二次编码）
  function googleUrl(base, city) {
    return 'https://calendar.google.com/calendar/r?cid=' + toWebcal(icsUrl(base, city));
  }

  // Apple 日历：webcal 直链
  function appleUrl(base, city) {
    return toWebcal(icsUrl(base, city));
  }

  return {
    icsPath: icsPath,
    icsUrl: icsUrl,
    googleUrl: googleUrl,
    appleUrl: appleUrl
  };
});
