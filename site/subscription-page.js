/* 两个独立订阅页共用的交互：城市筛选、ICS 地址、日历客户端跳转与真实事件预览。 */
(function () {
  'use strict';

  var config = window.subscriptionPageConfig;
  if (!config || !window.manzhanUrls) return;

  var state = {
    data: null,
    counts: {},
    selected: {}
  };
  var toastTimer = null;

  function get(id) {
    return document.getElementById(id);
  }

  function make(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text != null) node.textContent = text;
    return node;
  }

  function siteBase() {
    var clean = window.location.href.split('#')[0].split('?')[0];
    return clean.slice(0, clean.lastIndexOf('/') + 1);
  }

  function subscriptionUrl(city) {
    return manzhanUrls.icsUrl(siteBase(), city, config.feedRoot);
  }

  function googleUrl(city) {
    return manzhanUrls.googleUrl(siteBase(), city, config.feedRoot);
  }

  function appleUrl(city) {
    return manzhanUrls.appleUrl(siteBase(), city, config.feedRoot);
  }

  function toast(message) {
    var node = get('toast');
    node.textContent = message;
    node.classList.add('is-visible');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () {
      node.classList.remove('is-visible');
    }, 1800);
  }

  function fallbackCopy(text) {
    var area = document.createElement('textarea');
    area.value = text;
    area.setAttribute('readonly', '');
    area.style.position = 'fixed';
    area.style.opacity = '0';
    document.body.appendChild(area);
    area.select();
    try {
      document.execCommand('copy');
      toast('订阅地址已复制');
    } catch (error) {
      toast('复制失败，请手动复制地址');
    }
    document.body.removeChild(area);
  }

  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () {
        toast('订阅地址已复制');
      }, function () {
        fallbackCopy(text);
      });
    } else {
      fallbackCopy(text);
    }
  }

  function bindCopy(button, city) {
    button.addEventListener('click', function () {
      var initial = button.textContent;
      button.textContent = '已复制';
      clearTimeout(button._copyTimer);
      button._copyTimer = setTimeout(function () {
        button.textContent = initial;
      }, 1400);
      copyText(subscriptionUrl(city));
    });
  }

  function cityList() {
    return state.data.cities || [];
  }

  function countFor(city) {
    return Number(state.counts[city] || 0);
  }

  function selectedCities() {
    return cityList().filter(function (city) { return state.selected[city]; });
  }

  function eventCount(cities) {
    return cities.reduce(function (total, city) { return total + countFor(city); }, 0);
  }

  function formatUpdated(value) {
    if (!value) return '未知';
    return value.replace('T', ' ').replace(/([+-]\d\d:\d\d|Z)$/, '').slice(0, 16);
  }

  function datePart(value) {
    var match = String(value || '').match(/^(\d{4})-(\d{2})-(\d{2})/);
    return match ? match[2] + '.' + match[3] : '日期待确认';
  }

  function timePart(value) {
    var match = String(value || '').match(/T(\d{2}:\d{2})/);
    return match ? match[1] : '';
  }

  function eventDate(event) {
    var start = event.start_at || event.start;
    var end = event.end_at || event.end;
    var startDate = datePart(start);
    var startTime = timePart(start);
    var endDate = end ? datePart(end) : '';
    var endTime = timePart(end);

    if (startTime) {
      if (endTime && endDate === startDate) return startDate + ' · ' + startTime + '–' + endTime;
      return startDate + ' · ' + startTime;
    }
    if (endDate && endDate !== startDate) return startDate + ' – ' + endDate;
    return startDate + ' · 全天';
  }

  function eventTitle(event) {
    return event.title || event.name || '未命名活动';
  }

  function eventPlace(event) {
    return [event.venue, event.address, event.district].filter(Boolean).join(' · ') || '场地待公布';
  }

  function actionLink(label, href, primary) {
    var link = make('a', 'action-button' + (primary ? ' action-button--ticket' : ''), label);
    link.href = href;
    link.target = '_blank';
    link.rel = 'noopener';
    return link;
  }

  function renderMasthead() {
    var data = state.data;
    var status = get('feed-status');
    status.textContent = '';
    status.appendChild(make('strong', null, data.count + ' ' + config.countLabel));
    status.appendChild(document.createTextNode(' · ' + cityList().length + ' 城 · 更新于 ' + formatUpdated(data.updated)));
  }

  function renderAllFeed() {
    var url = subscriptionUrl('all');
    get('all-url').textContent = url;
    get('google-all').href = googleUrl('all');
    get('apple-all').href = appleUrl('all');
  }

  function visibleCities() {
    var query = get('city-search').value.trim();
    return cityList().filter(function (city) { return !query || city.indexOf(query) !== -1; });
  }

  function renderCityList() {
    var list = get('city-list');
    var cities = visibleCities();
    list.textContent = '';

    if (!cities.length) {
      list.appendChild(make('p', 'search-empty', '没有匹配的城市'));
      get('select-visible').textContent = '全选';
      return;
    }

    cities.forEach(function (city) {
      var label = make('label', 'city-item');
      var checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.checked = Boolean(state.selected[city]);
      checkbox.setAttribute('aria-label', '订阅 ' + city);
      checkbox.addEventListener('change', function () {
        if (checkbox.checked) state.selected[city] = true;
        else delete state.selected[city];
        renderSelectedFeeds();
        updateSelectButton();
      });
      label.appendChild(checkbox);
      label.appendChild(make('span', 'city-name', city));
      label.appendChild(make('span', 'city-count', countFor(city) + ' 条'));
      list.appendChild(label);
    });
    updateSelectButton();
  }

  function updateSelectButton() {
    var cities = visibleCities();
    var allSelected = cities.length && cities.every(function (city) { return state.selected[city]; });
    get('select-visible').textContent = allSelected ? '取消全选' : '全选';
  }

  function cityEmptyNote(city) {
    if (countFor(city) > 0) return countFor(city) + ' 条已核验活动';
    return config.zeroCityNote || '暂无已核验活动，后续新增会自动出现';
  }

  function makeFeedActions(city) {
    var actions = make('div', 'feed-actions');
    var copy = make('button', 'action-button', '复制地址');
    copy.type = 'button';
    bindCopy(copy, city);
    actions.appendChild(copy);
    actions.appendChild(actionLink('Google', googleUrl(city), false));
    actions.appendChild(actionLink('Apple', appleUrl(city), false));
    return actions;
  }

  function renderSelectedFeeds() {
    var selected = selectedCities();
    var root = get('selected-feeds');
    root.textContent = '';

    if (!selected.length) {
      root.appendChild(make('p', 'selected-empty', config.selectionEmpty));
      return;
    }

    var summary = make('p', 'selection-summary');
    summary.appendChild(make('strong', null, '已选择 ' + selected.length + ' 城'));
    summary.appendChild(document.createTextNode(' · 合计 ' + eventCount(selected) + ' 条活动 · 每城一个独立订阅源'));
    root.appendChild(summary);

    selected.forEach(function (city) {
      var row = make('article', 'city-feed');
      var copy = make('div', null);
      var heading = make('div', 'city-heading');
      heading.appendChild(make('h3', null, city));
      heading.appendChild(make('span', 'city-count', cityEmptyNote(city)));
      copy.appendChild(heading);
      copy.appendChild(make('p', 'city-note', countFor(city) ? '只订阅这个城市的内容' : cityEmptyNote(city)));
      row.appendChild(copy);
      row.appendChild(makeFeedActions(city));
      row.appendChild(make('code', 'feed-url', subscriptionUrl(city)));
      root.appendChild(row);
    });
  }

  function renderEventPreview() {
    var grid = get('event-preview');
    var events = (state.data.events || []).slice(0, 3);
    grid.textContent = '';

    if (!events.length) {
      grid.appendChild(make('p', 'selected-empty', '暂无可展示的已核验活动。'));
      return;
    }

    events.forEach(function (event) {
      var card = make('article', 'event-card');
      card.appendChild(make('div', 'event-date', eventDate(event)));
      card.appendChild(make('h3', 'event-title', eventTitle(event)));
      card.appendChild(make('p', 'event-place', eventPlace(event)));
      card.appendChild(make('p', 'event-kind', [event.city, event.category].filter(Boolean).join(' · ')));

      var ticket = event.ticket_url || event.link;
      var source = event.source_url;
      if (ticket || source) {
        var links = make('div', 'event-links');
        if (ticket) links.appendChild(actionLink('购票', ticket, true));
        if (!ticket && source) links.appendChild(actionLink('查看来源', source, false));
        else if (source && source !== ticket) links.appendChild(actionLink('查看来源', source, false));
        card.appendChild(links);
      }
      grid.appendChild(card);
    });
  }

  function renderFailure() {
    var message = '订阅数据暂时无法加载。已有日历订阅不会受影响，请稍后刷新。';
    get('feed-status').textContent = message;
    get('selected-feeds').textContent = '';
    get('selected-feeds').appendChild(make('p', 'selected-empty', message));
    get('event-preview').textContent = '';
    get('event-preview').appendChild(make('p', 'selected-empty', message));
  }

  function setupControls() {
    bindCopy(get('copy-all'), 'all');
    get('city-search').addEventListener('input', renderCityList);
    get('select-visible').addEventListener('click', function () {
      var cities = visibleCities();
      var allSelected = cities.length && cities.every(function (city) { return state.selected[city]; });
      cities.forEach(function (city) {
        if (allSelected) delete state.selected[city];
        else state.selected[city] = true;
      });
      renderCityList();
      renderSelectedFeeds();
    });
  }

  function init(data) {
    state.data = data;
    state.counts = data.counts || {};
    if (!Object.keys(state.counts).length) {
      (data.events || []).forEach(function (event) {
        state.counts[event.city] = countFor(event.city) + 1;
      });
    }
    cityList().forEach(function (city) {
      if (!Object.prototype.hasOwnProperty.call(state.counts, city)) state.counts[city] = 0;
    });
    renderMasthead();
    renderAllFeed();
    renderCityList();
    renderSelectedFeeds();
    renderEventPreview();
  }

  setupControls();
  fetch(config.dataUrl)
    .then(function (response) {
      if (!response.ok) throw new Error('HTTP ' + response.status);
      return response.json();
    })
    .then(init)
    .catch(renderFailure);
})();
