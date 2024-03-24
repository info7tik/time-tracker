import unittest
import time
from datetime import datetime
from timetracker import TimeTracker


class TestTimeTracker(unittest.TestCase):
    def test_load_json_file(self):
        counter_stats = {
            "start_timestamp_seconds": 0,
            "current_day": 0,
            "today_seconds": 0,
            "current_week": 0,
            "week_working_days": 0,
            "week_seconds": 0,
            "week_history": [],
            "extra_time_seconds": 0,
        }
        tracker = TimeTracker()
        tracker.save_empty_json_file()
        time_info = tracker.load_json_file()
        self.assertEqual(time_info, counter_stats)

    def test_save_json_file(self):
        counter_stats = {
            "start_timestamp_seconds": 1,
            "current_day": 2,
            "today_seconds": 3,
            "current_week": 4,
            "week_working_days": 5,
            "week_seconds": 6,
            "week_history": [],
            "extra_time_seconds": 7,
        }
        tracker = TimeTracker()
        tracker.save_counter_stats(counter_stats)
        time_info = tracker.load_json_file()
        self.assertEqual(time_info["start_timestamp_seconds"], 1)
        self.assertEqual(time_info["current_day"], 2)
        self.assertEqual(time_info["week_seconds"], 6)

    def test_start_counter(self):
        tracker = TimeTracker()
        tracker.save_empty_json_file()
        now = int(time.time())
        tracker.start_counter()
        time_info = tracker.load_json_file()
        elapsed_time = now - time_info["start_timestamp_seconds"]
        self.assertTrue(elapsed_time < 2)
        today = datetime.today()
        self.assertEqual(time_info["current_day"], today.day)
        self.assertEqual(time_info["current_week"], today.isocalendar()[1])
        print(time_info["week_history"])
        self.assertEqual(len(time_info["week_history"]), 0)

    def test_update_stats_from_stop(self):
        tracker = TimeTracker()
        current_day = datetime.today().day
        current_week = datetime.today().isocalendar()[1]
        counter_stats = {
            "start_timestamp_seconds": int(time.time()) - 10,
            "today_seconds": 0,
            "current_day": current_day,
            "current_week": current_week,
            "week_working_days": 0,
            "week_seconds": 0,
            "week_history": [],
            "extra_time_seconds": 0,
        }
        tracker.update_stats_before_stopping(counter_stats)
        self.assertEqual(counter_stats["start_timestamp_seconds"], 0)
        self.assertEqual(counter_stats["today_seconds"], 10)
        self.assertEqual(counter_stats["current_day"], current_day)
        self.assertEqual(counter_stats["current_week"], current_week)
        self.assertEqual(counter_stats["week_working_days"], 0)
        self.assertEqual(counter_stats["extra_time_seconds"], 0)

    def test_update_stats_with_yesterday_data(self):
        tracker = TimeTracker()
        current_day = datetime.today().day
        current_week = datetime.today().isocalendar()[1]
        counter_stats = {
            "start_timestamp_seconds": 0,
            "today_seconds": 20,
            "current_day": current_day - 1,
            "current_week": current_week - 1,
            "week_working_days": 0,
            "week_seconds": 0,
            "week_history": [],
            "extra_time_seconds": 0,
        }
        tracker.update_stats_with_yesterday_data(counter_stats)
        self.assertEqual(counter_stats["start_timestamp_seconds"], 0)
        self.assertEqual(counter_stats["today_seconds"], 0)
        self.assertEqual(counter_stats["week_working_days"], 1)
        self.assertEqual(counter_stats["week_seconds"], 20)
        self.assertEqual(counter_stats["current_day"], current_day - 1)
        self.assertEqual(counter_stats["current_week"], current_week - 1)

    def test_update_stats_with_last_week_data(self):
        tracker = TimeTracker()
        current_day = datetime.today().day
        current_week = datetime.today().isocalendar()[1]
        counter_stats = {
            "start_timestamp_seconds": 0,
            "today_seconds": 0,
            "current_day": current_day,
            "current_week": current_week - 1,
            "week_working_days": 3,
            "week_seconds": 20,
            "week_history": [],
            "extra_time_seconds": 0,
        }
        tracker.update_stats_with_last_week_data(counter_stats)
        self.assertEqual(counter_stats["start_timestamp_seconds"], 0)
        self.assertEqual(counter_stats["today_seconds"], 0)
        self.assertEqual(counter_stats["week_working_days"], 0)
        self.assertEqual(counter_stats["week_seconds"], 0)
        self.assertEqual(counter_stats["current_day"], current_day)
        self.assertEqual(counter_stats["current_week"], current_week - 1)
        self.assertEqual(len(counter_stats["week_history"]), 1)
        last_week_stats = counter_stats["week_history"][0]
        self.assertEqual(last_week_stats["week"], current_week - 1)
        self.assertEqual(last_week_stats["working_days"], 3)
        self.assertEqual(last_week_stats["seconds"], 20)

    def test_full_sequence(self):
        tracker = TimeTracker()
        current_day = datetime.today().day
        current_week = datetime.today().isocalendar()[1]
        counter_stats = {
            "start_timestamp_seconds": int(time.time()) - 20,
            "today_seconds": 20,
            "current_day": current_day - 1,
            "current_week": current_week - 1,
            "week_working_days": 3,
            "week_seconds": 0,
            "week_history": [],
            "extra_time_seconds": 0,
        }
        tracker.update_stats_before_stopping(counter_stats)
        self.assertEqual(counter_stats["today_seconds"], 40)
        self.assertEqual(counter_stats["week_working_days"], 3)
        tracker.update_stats_with_yesterday_data(counter_stats)
        self.assertEqual(counter_stats["today_seconds"], 0)
        self.assertEqual(counter_stats["week_seconds"], 40)
        self.assertEqual(counter_stats["week_working_days"], 4)
        tracker.update_stats_with_last_week_data(counter_stats)
        self.assertEqual(counter_stats["start_timestamp_seconds"], 0)
        self.assertEqual(counter_stats["today_seconds"], 0)
        self.assertEqual(counter_stats["week_working_days"], 0)
        self.assertEqual(counter_stats["week_seconds"], 0)
        self.assertEqual(counter_stats["current_day"], current_day - 1)
        self.assertEqual(counter_stats["current_week"], current_week - 1)

if __name__ == "__main__":
    unittest.main()
