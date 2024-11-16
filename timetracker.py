from datetime import datetime
import json, os, time

NB_WORKING_HOURS_PER_DAY = 7
JSON_FILE = "/home/remy/Documents/time-tracker/timetracker.json"
COMMANDS = {
    "help": {"function": "print_usage", "description": "show the help"},
    "start": {"function": "set_start_timestamp", "description": "start the timer"},
    "stop": {"function": "set_stop_timestamp", "description": "stop the timer"},
    "reset": {"function": "reset_start_timestamp", "description": "reset the start timer"},
    "delete": {"function": "delete_json_file", "description": "delete all the information about the working hours"},
    "show": {"function": "print_times", "description": "show the information about the working hours"},
}
EMPTY_FILE_CONTENT = {
    "start_timestamp_seconds": 0,
    "current_day": 0,
    "current_week": 0,
    "today_seconds": 0,
    "week_working_days": 0,
    "week_seconds": 0,
    "week_history": [],
    "extra_time_seconds": 0,
}


# Do not use the counter around midnight, the is_new_day and is_new_week functions could be unsynchronized
class TimeTracker:
    def function_caller(self, command):
        if command in COMMANDS:
            globals()[COMMANDS[command]["function"]]()
        else:
            print("command '%s' does not exist." % command)

    def print_usage(self):
        print("usage: time-track.py command")
        print("command values:")
        for command in COMMANDS:
            print("    " + command + ": " + COMMANDS[command]["description"])

    def get_information(self):
        counter_stats = self.load_json_file()
        self.update_today_time(counter_stats)
        today_seconds = counter_stats["today_seconds"]
        today_remained_information = self.compute_today_remainded_information(today_seconds)
        return {
            "today_hours": self.format_time(today_seconds) + today_remained_information,
            "week_hours": self.format_time(counter_stats["week_seconds"]),
            "extra_time": self.format_time(counter_stats["extra_time_seconds"]),
        }

    def compute_today_remainded_information(self, today_seconds):
        seconds_per_day = NB_WORKING_HOURS_PER_DAY * 3600
        today_remained_seconds = today_seconds - seconds_per_day
        return " (%s)" % self.format_time(today_remained_seconds)

    def format_time(self, time_seconds):
        is_negative = time_seconds < 0
        if is_negative:
            time_seconds *= -1
        hours = 0
        days = 0
        minutes = int(time_seconds / 60)
        if minutes > 59:
            hours = int(minutes / 60)
            minutes = minutes % 60
        if hours >= NB_WORKING_HOURS_PER_DAY:
            days = int(hours / NB_WORKING_HOURS_PER_DAY)
            hours = hours % NB_WORKING_HOURS_PER_DAY
        result = "%ds" % time_seconds
        if minutes > 0:
            result = "%dmin" % minutes
        if hours > 0:
            result = "%dh%dmin" % (hours, minutes)
        if days > 0:
            result = "%d days and %dh%dmin" % (days, hours, minutes)
        if is_negative:
            return "-" + result
        else:
            return result

    def start_counter(self):
        counter_stats = self.load_json_file()
        if not self.is_running(counter_stats):
            self.update_stats_with_yesterday_data(counter_stats)
            self.update_stats_with_last_week_data(counter_stats)
            self.update_counters_before_starting(counter_stats)
            self.save_counter_stats(counter_stats)
        else:
            raise Exception("ERROR: the counter is already running!")

    def update_stats_with_yesterday_data(self, counter_stats):
        if self.is_new_day(counter_stats):
            today_seconds = counter_stats["today_seconds"]
            if today_seconds > 0:
                counter_stats["today_seconds"] = 0
                extra_time = today_seconds - NB_WORKING_HOURS_PER_DAY * 3600
                counter_stats["extra_time_seconds"] += extra_time
                counter_stats["week_seconds"] += today_seconds
                counter_stats["week_working_days"] += 1

    def is_new_day(self, counter_stats):
        return counter_stats["current_day"] != datetime.today().day

    def update_stats_with_last_week_data(self, counter_stats):
        if counter_stats["week_seconds"] != 0 and self.is_new_week(counter_stats):
            counter_stats["week_history"].append(
                {
                    "week": counter_stats["current_week"],
                    "working_days": counter_stats["week_working_days"],
                    "seconds": counter_stats["week_seconds"],
                }
            )
            counter_stats["week_working_days"] = 0
            counter_stats["week_seconds"] = 0

    def update_counters_before_starting(self, counter_stats):
        today = datetime.today()
        counter_stats["start_timestamp_seconds"] = int(time.time())
        counter_stats["current_day"] = today.day
        counter_stats["current_week"] = today.isocalendar()[1]

    def stop_counter(self):
        counter_stats = self.load_json_file()
        if self.is_running(counter_stats):
            self.update_stats_before_stopping(counter_stats)
            self.save_counter_stats(counter_stats)
        else:
            raise Exception("Timer is not running!")

    def is_running(self, time_info=None):
        if time_info is None:
            time_info = self.load_json_file()
        return time_info["start_timestamp_seconds"] != 0

    def update_stats_before_stopping(self, counter_stats):
        self.update_today_time(counter_stats)
        return counter_stats

    def update_today_time(self, counter_stats):
        if self.is_running(counter_stats):
            current_timestamp = int(time.time())
            elapsed_seconds = current_timestamp - counter_stats["start_timestamp_seconds"]
            counter_stats["today_seconds"] += elapsed_seconds
            counter_stats["start_timestamp_seconds"] = 0

    def is_new_week(self, counter_stats):
        return datetime.today().isocalendar()[1] != counter_stats["current_week"]

    def reset_counter(self):
        time_info = self.load_json_file()
        time_info["start_timestamp_seconds"] = 0
        self.save_counter_stats(time_info)

    def load_json_file(self):
        if not os.path.isfile(JSON_FILE):
            self.save_empty_json_file()
        with open(JSON_FILE, "r") as reader:
            return json.load(reader)

    def save_empty_json_file(self):
        with open(JSON_FILE, "w") as writer:
            json_content = json.dumps(EMPTY_FILE_CONTENT, indent=4)
            writer.write(json_content)

    def save_counter_stats(self, json_content_dict):
        with open(JSON_FILE, "w") as writer:
            json_content = json.dumps(json_content_dict, indent=4)
            writer.write(json_content)

    def delete_json_file(self):
        os.remove(JSON_FILE)
        self.save_empty_json_file()
