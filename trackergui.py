#!/bin/python3

import subprocess, traceback
from tkinter import *
from timetracker import TimeTracker


class MyWindow:
    def __init__(self, tk_gui):
        self.gui = tk_gui
        self.tracker = TimeTracker()
        self.recording_status = Label(tk_gui)
        self.recording_status.config(bg="lightyellow")
        self.recording_status.place(x=220, y=10, height=10, width=10)
        self.time_information = Label(tk_gui, text="Welcome to TimeTracker")
        self.time_information.place(x=30, y=15)
        self.start_button = Button(tk_gui, text="Start", fg="green")
        self.start_button.bind("<Button-1>", self.start_counter)
        self.start_button.place(x=50, y=70, height=30, width=120)
        self.end_button = Button(tk_gui, text="Stop", fg="orange")
        self.end_button.bind("<Button-1>", self.stop_counter)
        self.end_button.place(x=50, y=105, height=30, width=120)
        self.reset_button = Button(tk_gui, text="Delete", fg="grey")
        self.reset_button.bind("<Button-1>", self.delete_stats)
        self.reset_button.place(x=50, y=140, height=30, width=120)
        self.command_result = Label(tk_gui, text="")
        self.command_result.place(x=10, y=175)
        self.display_tracker_information()

    def start_counter(self, event):
        try:
            self.tracker.start_counter()
            self.command_result.config(text="Timer started")
        except Exception as e:
            self.command_result.config(text=str(e))

    def stop_counter(self, event):
        try:
            self.tracker.stop_counter()
            self.command_result.config(text="Timer stopped")
        except Exception as e:
            self.command_result.config(text=str(e))

    def delete_stats(self, event):
        try:
            self.tracker.delete_json_file()
            self.command_result.config(text="All stats are deleted")
        except Exception as e:
            self.command_result.config(text=str(e))

    def update_tracker_information(self):
        self.display_tracker_status()
        self.display_tracker_information()

    def display_tracker_status(self):
        if self.tracker.is_running():
            self.recording_status.config(bg="red")
        else:
            self.recording_status.config(bg="grey")

    def display_tracker_information(self):
        tracker_information = self.tracker.get_information()
        information_to_display = "Today: " + tracker_information["today_hours"] + "\n"
        information_to_display += "Week: " + tracker_information["week_hours"] + "\n"
        information_to_display += "Extra time: " + tracker_information["extra_time"] + "\n"
        self.time_information.config(text=information_to_display)

    def run_shell_command(self, command, label):
        result = subprocess.run(command.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode("utf-8").splitlines()
        if len(output) > 0:
            label.config(text=output[-1])
        else:
            output = result.stderr.decode("utf-8").splitlines()
            if len(output) > 0:
                label.config(text=output[-1])


def update_status_loop(gui, tracker_window):
    tracker_window.update_tracker_information()
    gui.after(2000, update_status_loop, gui, tracker_window)


def main():
    tk_gui = Tk()
    mywin = MyWindow(tk_gui)
    tk_gui.title("Time Tracker")
    tk_gui.geometry("240x200+10+10")
    update_status_loop(tk_gui, mywin)
    tk_gui.mainloop()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
