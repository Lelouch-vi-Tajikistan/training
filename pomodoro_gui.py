import tkinter as tk
from tkinter import messagebox
import time


class PomodoroTimer:
    def __init__(self, work_duration, break_duration, intervals):
        self.work_duration = work_duration
        self.break_duration = break_duration
        self.intervals = intervals

    def start(self):
        for interval in range(1, self.intervals + 1):
            yield f"Interval {interval}/{self.intervals}\nWork for {self.work_duration} minutes."
            time.sleep(self.work_duration * 60)

            if interval != self.intervals:
                yield f"Take a {self.break_duration} minute break."
                time.sleep(self.break_duration * 60)


class PomodoroApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Pomodoro Timer")

        self.work_duration = tk.StringVar(value=25)
        self.break_duration = tk.StringVar(value=5)
        self.intervals = tk.StringVar(value=4)

        self.create_widgets()
        self.timer_running = False

    def create_widgets(self):
        tk.Label(self.master, text="Work duration (minutes):").grid(row=0, column=0)
        tk.Entry(self.master, textvariable=self.work_duration).grid(row=0, column=1)

        tk.Label(self.master, text="Break duration (minutes):").grid(row=1, column=0)
        tk.Entry(self.master, textvariable=self.break_duration).grid(row=1, column=1)

        tk.Label(self.master, text="Number of intervals:").grid(row=2, column=0)
        tk.Entry(self.master, textvariable=self.intervals).grid(row=2, column=1)

        self.start_button = tk.Button(self.master, text="Start", command=self.start_timer)
        self.start_button.grid(row=3, column=0, columnspan=2)

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.start_button.config(text="Stop", command=self.stop_timer)

            work_duration = int(self.work_duration.get())
            break_duration = int(self.break_duration.get())
            intervals = int(self.intervals.get())

            timer = PomodoroTimer(work_duration, break_duration, intervals)
            for message in timer.start():
                if not self.timer_running:
                    break
                messagebox.showinfo("Pomodoro Timer", message)

            if self.timer_running:
                messagebox.showinfo("Pomodoro Timer", "Congratulations! You've completed all intervals.")
                self.stop_timer()

    def stop_timer(self):
        self.timer_running = False
        self.start_button.config(text="Start", command=self.start_timer)


if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
