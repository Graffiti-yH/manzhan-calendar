# B站漫展日历订阅

抓取 B 站会员购「漫展演出」频道的漫展活动，按城市筛选生成 iCalendar 订阅，可添加到 Google 日历 / Apple 日历。

## 使用

订阅页面（勾选城市 → 复制/添加订阅链接）：

```
https://Graffiti-yH.github.io/manzhan-calendar/
```

直接订阅（把 `{城市}` 替换为城市名，如 `上海市`、`广州市`）：

- 全部城市：`https://Graffiti-yH.github.io/manzhan-calendar/ics/all.ics`
- 单个城市：`https://Graffiti-yH.github.io/manzhan-calendar/ics/{城市}.ics`

### 添加到日历

- **Google 日历**：设置 → 添加日历 → 通过网址添加，粘贴 `https://Graffiti-yH.github.io/manzhan-calendar/ics/all.ics`
- **Apple 日历**（macOS / iOS）：文件 → 新建日历订阅，粘贴 `webcal://Graffiti-yH.github.io/manzhan-calendar/ics/all.ics`
- 订阅页提供「Google」「Apple」一键添加按钮

> 日历客户端会定期自动刷新订阅源，无需手动更新。

## 事件内容

每条日历事件包含：活动名称、起止日期（全天事件）、地点/场馆、购票链接（点击直达 B 站会员购详情页），以及 B 站提供的活动封面（作为 iCalendar `IMAGE` 事件题图）。订阅会声明 `DISPLAY=GRAPHIC`，但是否显示仍取决于日历客户端是否支持该标准属性。

## 数据说明

- 数据源：B 站会员购「漫展演出」频道，仅保留「漫展」「Only同人展」两类活动，排除主题餐厅/音乐会/电竞赛事等。
- 已取消/延期的活动会被过滤。
- 每天北京时间 00:00 由 GitHub Actions 自动抓取刷新。

## 本地运行

```bash
python3 fetch.py   # 生成 site/data.json 与 site/ics/
```

依赖：仅 Python 标准库，无第三方包。

## 目录结构

```
fetch.py                        # 抓取 + 生成脚本
site/index.html                 # 订阅筛选前端（静态）
site/data.json                  # 生成：全量活动数据
site/ics/all.ics                # 生成：全部城市订阅
site/ics/{城市}.ics             # 生成：每城市订阅
.github/workflows/update.yml    # 每日定时抓取 + 发布 Pages
```
