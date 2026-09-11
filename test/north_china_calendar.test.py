#!/usr/bin/env python3
"""Regression tests for the separate North China activity subscription feed."""

import datetime as dt
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("north_china", ROOT / "generate_north_china_calendar.py")
calendar = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(calendar)


class NorthChinaCalendarTests(unittest.TestCase):
    def setUp(self):
        self.generated_at = dt.datetime(2026, 9, 11, 9, 30, tzinfo=calendar.CHINA_TZ)
        self.events = calendar.load_events(ROOT / "data" / "north-china-activities.json")

    def test_seed_ledger_excludes_manga_events(self):
        self.assertGreaterEqual(len(self.events), 1)
        for event in self.events:
            self.assertIsNone(calendar.EXCLUDED_PATTERN.search(event["title"] + event["category"]))

    def test_timed_ticket_event_has_time_location_and_purchase_link(self):
        event = next(item for item in self.events if item["id"] == "montagne-sauvage-tianjin-2026")
        ics = calendar.ics_calendar("测试", [event], self.generated_at).replace("\r\n ", "")
        self.assertIn("DTSTART;TZID=Asia/Shanghai:20260917T200000", ics)
        self.assertIn("DTEND;TZID=Asia/Shanghai:20260917T220000", ics)
        self.assertIn("BEGIN:VTIMEZONE", ics)
        self.assertIn("TZID:Asia/Shanghai", ics)
        self.assertIn("LOCATION:", ics)
        self.assertIn("购票/报名：https://www.showstart.com/event/306377", ics)
        self.assertIn("URL:https://www.showstart.com/event/306377", ics)

    def test_date_only_event_stays_all_day(self):
        event = next(item for item in self.events if item["id"] == "namoc-rooted-oil-2026")
        ics = calendar.ics_calendar("测试", [event], self.generated_at)
        self.assertIn("DTSTART;VALUE=DATE:20260908", ics)
        self.assertIn("DTEND;VALUE=DATE:20260920", ics)
        self.assertNotIn("DTSTART;TZID=Asia/Shanghai", ics)

    def test_generate_creates_combined_and_per_city_feeds(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "north-china"
            payload = calendar.generate(
                ROOT / "data" / "north-china-activities.json", output, self.generated_at)
            self.assertEqual(payload["counts"]["北京市"], 5)
            self.assertEqual(payload["counts"]["天津市"], 3)
            self.assertEqual(payload["counts"]["石家庄市"], 2)
            self.assertEqual(payload["counts"]["保定市"], 0)
            self.assertTrue((output / "ics" / "all.ics").exists())
            self.assertTrue((output / "ics" / "北京市.ics").exists())
            self.assertTrue((output / "ics" / "保定市.ics").exists())
            data = json.loads((output / "data.json").read_text(encoding="utf-8"))
            self.assertEqual(data["count"], 10)


if __name__ == "__main__":
    unittest.main()
