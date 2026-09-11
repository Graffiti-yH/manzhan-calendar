# 日历订阅：B站漫展与华北城市活动

本仓库维护两套互不混合的 iCalendar 订阅：B站会员购的漫展日历，以及北京、天津、石家庄、保定的非漫展城市活动日历。两者可分别添加到 Google 日历 / Apple 日历。

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

## 华北城市活动订阅（独立于漫展）

这套订阅只收录已核验的美术展、博物馆展、音乐、戏剧、市集、讲座与工作坊；采集规则会排除漫展、同人展、动漫展、Cosplay，以及已经出现在 B站漫展日历中的活动。

- 全部四城：`https://Graffiti-yH.github.io/manzhan-calendar/north-china/ics/all.ics`
- 北京：`https://Graffiti-yH.github.io/manzhan-calendar/north-china/ics/%E5%8C%97%E4%BA%AC%E5%B8%82.ics`
- 天津：`https://Graffiti-yH.github.io/manzhan-calendar/north-china/ics/%E5%A4%A9%E6%B4%A5%E5%B8%82.ics`
- 石家庄：`https://Graffiti-yH.github.io/manzhan-calendar/north-china/ics/%E7%9F%B3%E5%AE%B6%E5%BA%84%E5%B8%82.ics`
- 保定：`https://Graffiti-yH.github.io/manzhan-calendar/north-china/ics/%E4%BF%9D%E5%AE%9A%E5%B8%82.ics`

日历事件会保留来源给出的时间、场地和地址；只有公开的官方购票或报名页才会写进事件的 `URL` 与描述。仅有日期的展览会作为全天事件写入，不虚构开放时段。

活动台账位于 `data/north-china-activities.json`，由 `north-china-activity-collection` Skill 更新。`generate_north_china_calendar.py` 会把已核验的台账生成 `site/north-china/ics/` 中的全部城市与单城订阅源。

## 漫展事件内容

每条日历事件包含：活动名称、起止日期（全天事件）、地点/场馆、购票链接（点击直达 B 站会员购详情页）。

## 数据说明

- 数据源：B 站会员购「漫展演出」频道，仅保留「漫展」「Only同人展」两类活动，排除主题餐厅/音乐会/电竞赛事等。
- 已取消/延期的活动会被过滤。
- 每天北京时间 00:00 由 GitHub Actions 自动抓取刷新。

## 本地运行

```bash
python3 fetch.py                         # 生成 B站漫展数据与订阅源
python3 generate_north_china_calendar.py # 生成华北城市活动订阅源
```

依赖：仅 Python 标准库，无第三方包。

## 目录结构

```
fetch.py                        # 抓取 + 生成脚本
generate_north_china_calendar.py # 华北活动台账 → ICS 生成脚本
data/north-china-activities.json # 已核验的华北活动台账
site/index.html                 # 订阅筛选前端（静态）
site/data.json                  # 生成：全量活动数据
site/ics/all.ics                # 生成：全部城市订阅
site/ics/{城市}.ics             # 生成：每城市订阅
site/north-china/ics/all.ics    # 生成：华北活动全部城市订阅
.github/workflows/update.yml    # 每日定时抓取 + 发布 Pages
```
