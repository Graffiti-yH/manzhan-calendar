/* 日历订阅 URL 生成逻辑（浏览器与 Node 通用，供 index.html 与回归测试共用） */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.manzhanUrls = factory();
  }
})(typeof self !== 'undefined' ? self : this, function () {
  // 指定订阅目录中的 .ics 路径：城市名经 encodeURIComponent 编码一次。
  // feedRoot 默认为原有漫展目录，第三个参数用于独立的活动订阅目录。
  function feedPath(feedRoot, city) {
    var root = (feedRoot || 'ics').replace(/^\/+|\/+$/g, '');
    return root + '/' + (city === 'all' ? 'all.ics' : encodeURIComponent(city) + '.ics');
  }

  // 向后兼容：漫展订阅的原有单城市路径。
  function icsPath(city) {
    return feedPath('ics', city);
  }

  // https 订阅地址（「复制」按钮用）
  function icsUrl(base, city, feedRoot) {
    return base + feedPath(feedRoot || 'ics', city);
  }

  // 转为 webcal 协议
  function toWebcal(url) {
    return url.replace(/^https?:\/\//, 'webcal://');
  }

  // Google 日历一键添加：cid 传 webcal 订阅地址（原样，不做二次编码）
  function googleUrl(base, city, feedRoot) {
    return 'https://calendar.google.com/calendar/r?cid=' + toWebcal(icsUrl(base, city, feedRoot));
  }

  // Apple 日历：webcal 直链
  function appleUrl(base, city, feedRoot) {
    return toWebcal(icsUrl(base, city, feedRoot));
  }

  return {
    feedPath: feedPath,
    icsPath: icsPath,
    icsUrl: icsUrl,
    googleUrl: googleUrl,
    appleUrl: appleUrl
  };
});
