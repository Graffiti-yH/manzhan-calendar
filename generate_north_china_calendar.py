#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate a separate, source-linked North China activity calendar.

Input is a verified ledger maintained by the north-china-activity-collection
skill.  Output is deliberately separate from Bilibili's manga calendar:

  site/north-china/data.json
  site/north-china/ics/all.ics
  site/north-china/ics/{city}.ics

Only standard-library modules are used so GitHub Actions can regenerate the
subscription feeds every day.  Events with precise times use Asia/Shanghai
timestamps; events whose sources state only dates remain all-day events.
"""

import datetime as dt
import json
import re
from pathlib import Path
from urllib.parse import urlparse


ROOT_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT = ROOT_DIR / "data" / "north-china-activities.json"
DEFAULT_OUTPUT = ROOT_DIR / "site" / "north-china"
CHINA_TZ = dt.timezone(dt.timedelta(hours=8))
CITIES = ("北京市", "天津市", "石家庄市", "保定市")
EXCLUDED_PATTERN = re.compile(r"漫展|同人展|动漫展|二次元|cosplay|comicup", re.IGNORECASE)


def ics_escape(value):
    return (str(value).replace("\\", "\\\\")
                      .replace(";", "\\;")
                      .replace(",", "\\,")
                      .replace("\r\n", "\\n")
                      .replace("\n", "\\n"))


def fold_line(line):
    """Fold an iCalendar content line to RFC 5545's 75-octet limit."""
    data = line.encode("utf-8")
    if len(data) <= 75:
        return line
    chunks = []
    start = 0
    first = True
    while start < len(data):
        limit = 75 if first else 74
        end = min(start + limit, len(data))
        while end > start and end < len(data) and (data[end] & 0xC0) == 0x80:
            end -= 1
        chunks.append(data[start:end].decode("utf-8"))
        start = end
        first = False
    return "\r\n ".join(chunks)


def is_public_url(value):
    parsed = urlparse(value or "")
    return parsed.scheme == "https" and bool(parsed.netloc)


def parse_date(value, field, event_id):
    try:
        return dt.date.fromisoformat(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{event_id}: {field} 必须是 YYYY-MM-DD") from error


def parse_local_datetime(value, field, event_id):
    try:
        parsed = dt.datetime.fromisoformat(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{event_id}: {field} 必须是带时区的 ISO 时间") from error
    if parsed.tzinfo is None:
        raise ValueError(f"{event_id}: {field} 缺少时区")
    return parsed.astimezone(CHINA_TZ)


def validate_event(event):
    required = ("id", "title", "city", "category", "status", "source_url", "source_tier", "retrieved_at", "all_day", "start_at")
    missing = [field for field in required if not event.get(field) and event.get(field) is not False]
    if missing:
        raise ValueError(f"事件缺少字段：{', '.join(missing)}")

    event_id = str(event["id"])
    if event["city"] not in CITIES:
        raise ValueError(f"{event_id}: 不支持的城市 {event['city']}")
    if event["status"] != "verified":
        raise ValueError(f"{event_id}: 只有 verified 活动可以进入订阅源")
    if EXCLUDED_PATTERN.search(" ".join((event["title"], event["category"]))):
        raise ValueError(f"{event_id}: 命中漫展排除规则")
    if not is_public_url(event["source_url"]):
        raise ValueError(f"{event_id}: source_url 必须是公开 https URL")
    if event.get("ticket_url") and not is_public_url(event["ticket_url"]):
        raise ValueError(f"{event_id}: ticket_url 必须是公开 https URL")
    if event.get("all_day"):
        start = parse_date(event["start_at"], "start_at", event_id)
        end = parse_date(event.get("end_at") or event["start_at"], "end_at", event_id)
        if end < start:
            raise ValueError(f"{event_id}: end_at 不能早于 start_at")
    else:
        start = parse_local_datetime(event["start_at"], "start_at", event_id)
        end = None
        if event.get("end_at"):
            end = parse_local_datetime(event["end_at"], "end_at", event_id)
            if end <= start:
                raise ValueError(f"{event_id}: end_at 必须晚于 start_at")
    return event


def load_events(input_path):
    with Path(input_path).open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    events = payload.get("events")
    if not isinstance(events, list):
        raise ValueError("活动台账的 events 必须是数组")
    seen = set()
    verified = []
    for event in events:
        validate_event(event)
        if event["id"] in seen:
            raise ValueError(f"重复的活动 id：{event['id']}")
        seen.add(event["id"])
        verified.append(event)
    return verified


def event_sort_key(event):
    return event["start_at"], event["title"]


def format_timed(value):
    return parse_local_datetime(value, "时间", "活动").strftime("%Y%m%dT%H%M%S")


def event_description(event):
    lines = [
        f"类别：{event['category']}",
        f"城市：{event['city']}",
    ]
    if event.get("address"):
        lines.append(f"地址：{event['address']}")
    if event.get("doors_at"):
        lines.append(f"入场：{event['doors_at']}")
    lines.append(f"活动来源：{event['source_url']}")
    if event.get("ticket_url"):
        lines.append(f"购票/报名：{event['ticket_url']}")
    lines.append(f"最后核验：{event['retrieved_at']}")
    return "\n".join(lines)


def ics_calendar(calname, events, generated_at):
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//manzhan-calendar//North China Activity Calendar//CN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:" + ics_escape(calname),
        "X-WR-TIMEZONE:Asia/Shanghai",
        "BEGIN:VTIMEZONE",
        "TZID:Asia/Shanghai",
        "X-LIC-LOCATION:Asia/Shanghai",
        "BEGIN:STANDARD",
        "TZOFFSETFROM:+0800",
        "TZOFFSETTO:+0800",
        "TZNAME:CST",
        "DTSTART:19700101T000000",
        "END:STANDARD",
        "END:VTIMEZONE",
    ]
    dtstamp = generated_at.astimezone(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for event in events:
        location = " · ".join(value for value in (event.get("venue"), event.get("address")) if value)
        event_url = event.get("ticket_url") or event["source_url"]
        lines.extend((
            "BEGIN:VEVENT",
            f"UID:{event['id']}@north-china-activity-calendar",
            f"DTSTAMP:{dtstamp}",
            "STATUS:CONFIRMED",
            "SUMMARY:" + ics_escape(event["title"]),
        ))
        if event["all_day"]:
            start = parse_date(event["start_at"], "start_at", event["id"])
            end = parse_date(event.get("end_at") or event["start_at"], "end_at", event["id"])
            lines.append("DTSTART;VALUE=DATE:" + start.strftime("%Y%m%d"))
            lines.append("DTEND;VALUE=DATE:" + (end + dt.timedelta(days=1)).strftime("%Y%m%d"))
        else:
            lines.append("DTSTART;TZID=Asia/Shanghai:" + format_timed(event["start_at"]))
            if event.get("end_at"):
                lines.append("DTEND;TZID=Asia/Shanghai:" + format_timed(event["end_at"]))
        if location:
            lines.append("LOCATION:" + ics_escape(location))
        lines.append("URL:" + ics_escape(event_url))
        lines.append("DESCRIPTION:" + ics_escape(event_description(event)))
        lines.append("END:VEVENT")
    lines.append("END:VCALENDAR")
    return "\r\n".join(fold_line(line) for line in lines) + "\r\n"


def build_payload(events, generated_at):
    cities = list(CITIES)
    counts = {city: 0 for city in cities}
    for event in events:
        counts[event["city"]] += 1
    return {
        "updated": generated_at.astimezone(CHINA_TZ).isoformat(timespec="seconds"),
        "count": len(events),
        "cities": cities,
        "counts": counts,
        "events": events,
    }


def generate(input_path=DEFAULT_INPUT, output_dir=DEFAULT_OUTPUT, generated_at=None):
    events = sorted(load_events(input_path), key=event_sort_key)
    output_dir = Path(output_dir)
    ics_dir = output_dir / "ics"
    ics_dir.mkdir(parents=True, exist_ok=True)
    generated_at = generated_at or dt.datetime.now(CHINA_TZ)

    with (output_dir / "data.json").open("w", encoding="utf-8") as handle:
        json.dump(build_payload(events, generated_at), handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    feeds = [("all", "华北城市活动日历 · 全部", events)]
    feeds.extend((city, "华北城市活动日历 · " + city,
                  [event for event in events if event["city"] == city]) for city in CITIES)
    for slug, calname, subset in feeds:
        with (ics_dir / f"{slug}.ics").open("w", encoding="utf-8", newline="") as handle:
            handle.write(ics_calendar(calname, subset, generated_at))
    return build_payload(events, generated_at)


def main():
    payload = generate()
    print(f"已生成 {payload['count']} 条华北城市活动订阅事件")
    print("城市：" + "、".join(f"{city} {payload['counts'][city]}" for city in CITIES))


if __name__ == "__main__":
    main()
