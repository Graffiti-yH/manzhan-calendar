#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""抓取 B 站会员购「漫展演出」频道的漫展活动，生成 iCalendar 订阅文件。

数据来源（无需登录）：
- 列表接口 listV2?filter=start_time&p_type=-1（按时间排序，可稳定分页）
  注意：需携带 buvid3/buvid4 cookie（由 api.bilibili.com/x/frontend/finger/spi 获取），
  否则 filter 排序失效、分页会重复返回首页数据。
- 列表已包含 start_time / end_time（YYYY-MM-DD）、third_category_name（分类）、
  city / venue_name / district_name，无需再调用详情接口。
购票链接：https://show.bilibili.com/platform/detail.html?id={id}

产物（写入 site/ 目录）：
- data.json      全量活动数据（前端筛选页读取）
- ics/all.ics    全部城市
- ics/{城市}.ics 每个城市一个订阅源
"""
import datetime
import json
import os
import time
import urllib.parse
import urllib.request

# 只保留真正的漫展活动（排除主题餐厅/音乐会/电竞赛事等同类频道的其他内容）
CATEGORIES = {"漫展", "Only同人展"}

LIST_API = ("https://show.bilibili.com/api/ticket/project/listV2"
            "?version=134&pagesize=20&area=-1&filter=start_time"
            "&platform=web&p_type=-1&page={page}")
DETAIL_URL = "https://show.bilibili.com/platform/detail.html?id={pid}"
SPI_API = "https://api.bilibili.com/x/frontend/finger/spi"

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36")

SITE_DIR = "site"
ICS_DIR = os.path.join(SITE_DIR, "ics")
CHINA_TZ = datetime.timezone(datetime.timedelta(hours=8))
MAX_PAGES = 200
DELAY_LIST = 0.2


def http_json(url, cookies=None):
    headers = {"User-Agent": UA, "Referer": "https://show.bilibili.com/"}
    if cookies:
        headers["Cookie"] = cookies
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_buvid():
    """获取 buvid3/buvid4 cookie（B 站设备指纹，保证排序与分页生效）。"""
    data = http_json(SPI_API).get("data") or {}
    b3 = data.get("b_3") or ""
    b4 = data.get("b_4") or ""
    if b3 and b4:
        return "buvid3=%s; buvid4=%s" % (b3, b4)
    return None


def fetch_list(cookies):
    """分页拉取频道全部活动（以 isLastBrush 判尾）。"""
    items = []
    for page in range(1, MAX_PAGES + 1):
        data = http_json(LIST_API.format(page=page), cookies).get("data") or {}
        result = data.get("result") or []
        items.extend(result)
        if data.get("isLastBrush") or not result:
            break
        time.sleep(DELAY_LIST)
    return items


def build_events(raw_items):
    """筛选分类、规范化字段，返回事件列表。"""
    events = []
    for item in raw_items:
        if item.get("third_category_name") not in CATEGORIES:
            continue
        pid = item.get("id")
        name = (item.get("project_name") or "").strip()
        start = item.get("start_time")
        end = item.get("end_time") or start
        if not pid or not name or not start:
            continue
        if "取消" in name or "延期" in name:  # 跳过已取消/延期的活动
            continue
        events.append({
            "id": pid,
            "name": name,
            "city": (item.get("city") or "").strip(),
            "venue": (item.get("venue_name") or "").strip(),
            "district": (item.get("district_name") or "").strip(),
            "start": start,
            "end": end,
            "link": DETAIL_URL.format(pid=pid),
        })
    return events


def date_plus_one(datestr):
    dt = datetime.datetime.strptime(datestr, "%Y-%m-%d")
    return (dt + datetime.timedelta(days=1)).strftime("%Y-%m-%d")


def ics_escape(text):
    return (text.replace("\\", "\\\\")
                .replace(";", "\\;")
                .replace(",", "\\,")
                .replace("\r\n", "\\n")
                .replace("\n", "\\n"))


def ics_calendar(calname, events):
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//manzhan-calendar//Bilibili Manzhan Calendar//CN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:" + ics_escape(calname),
        "X-WR-TIMEZONE:Asia/Shanghai",
    ]
    dtstamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for e in events:
        start = e["start"].replace("-", "")
        end = date_plus_one(e["end"]).replace("-", "")
        location = " · ".join(x for x in [e["venue"], e["district"]] if x)
        desc = "购票：" + e["link"]
        if e["city"]:
            desc += "\n城市：" + e["city"]
        lines += [
            "BEGIN:VEVENT",
            "UID:" + str(e["id"]) + "@show.bilibili.com",
            "DTSTAMP:" + dtstamp,
            "DTSTART;VALUE=DATE:" + start,
            "DTEND;VALUE=DATE:" + end,
            "SUMMARY:" + ics_escape(e["name"]),
        ]
        if location:
            lines.append("LOCATION:" + ics_escape(location))
        lines.append("DESCRIPTION:" + ics_escape(desc))
        lines.append("END:VEVENT")
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"


def main():
    cookies = get_buvid()
    print("[1/4] 抓取漫展列表 ...")
    raw = fetch_list(cookies)
    print(f"      频道活动 {len(raw)} 条")

    print("[2/4] 筛选漫展分类 ...")
    events = build_events(raw)
    print(f"      漫展活动 {len(events)} 条（分类：{'/'.join(sorted(CATEGORIES))}）")

    events.sort(key=lambda e: (e["start"], e["name"]))
    cities = sorted({e["city"] for e in events if e["city"]})

    os.makedirs(ICS_DIR, exist_ok=True)

    print("[3/4] 生成 ics ...")
    with open(os.path.join(ICS_DIR, "all.ics"), "w", encoding="utf-8") as f:
        f.write(ics_calendar("B站漫展日历 · 全部", events))
    for city in cities:
        subset = [e for e in events if e["city"] == city]
        fname = urllib.parse.quote(city, safe="") + ".ics"
        with open(os.path.join(ICS_DIR, fname), "w", encoding="utf-8") as f:
            f.write(ics_calendar("B站漫展日历 · " + city, subset))
    print(f"      城市 {len(cities)} 个")

    print("[4/4] 生成 data.json ...")
    payload = {
        "updated": datetime.datetime.now(CHINA_TZ).isoformat(timespec="seconds"),
        "count": len(events),
        "cities": cities,
        "events": events,
    }
    with open(os.path.join(SITE_DIR, "data.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print("完成。")


if __name__ == "__main__":
    main()
