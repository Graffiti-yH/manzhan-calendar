#!/usr/bin/env python3
"""抓取与 iCalendar 生成回归测试。运行：python3 test/fetch.test.py"""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import fetch  # noqa: E402


class FetchTests(unittest.TestCase):
    def test_cover_url_accepts_bilibili_protocol_relative_cover(self):
        self.assertEqual(
            fetch.cover_url({"cover": "//i0.hdslb.com/bfs/show/test.jpg"}),
            "https://i0.hdslb.com/bfs/show/test.jpg",
        )

    def test_build_events_keeps_cover_as_image(self):
        events = fetch.build_events([{
            "id": 42,
            "project_name": "测试漫展",
            "third_category_name": "漫展",
            "start_time": "2026-08-20",
            "end_time": "2026-08-21",
            "cover": "https://i0.hdslb.com/bfs/show/test.jpg",
        }])
        self.assertEqual(events[0]["image"], "https://i0.hdslb.com/bfs/show/test.jpg")

    def test_ics_emits_rfc_7986_image_property(self):
        ics = fetch.ics_calendar("测试", [{
            "id": 42,
            "name": "测试漫展",
            "city": "",
            "venue": "",
            "district": "",
            "start": "2026-08-20",
            "end": "2026-08-20",
            "link": "https://show.bilibili.com/platform/detail.html?id=42",
            "image": "https://i0.hdslb.com/bfs/show/test.jpg",
        }])
        unfolded = ics.replace("\r\n ", "")
        self.assertIn(
            "IMAGE;VALUE=URI;DISPLAY=GRAPHIC;FMTTYPE=image/jpeg:"
            "https://i0.hdslb.com/bfs/show/test.jpg",
            unfolded,
        )

    def test_image_mime_type_ignores_url_query(self):
        self.assertEqual(
            fetch.image_mime_type("https://i0.hdslb.com/test.png?width=480"),
            "image/png",
        )


if __name__ == "__main__":
    unittest.main()
