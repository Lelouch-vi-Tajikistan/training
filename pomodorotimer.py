import time
from os import system

def pomodoro_timer(work_duration=25, break_duration=5, intervals=4):
    for interval in range(1, intervals + 1):
        print(f"Interval {interval}/{intervals}")
        print(f"Work for {work_duration} minutes.")
        for _ in range(work_duration * 60):
            time.sleep(1)
        print(f"Take a {break_duration} minute break.")
        for _ in range(break_duration * 60):
            time.sleep(1)

    print("Congratulations! You've completed all intervals.")

def main():
    work_duration = int(input("Enter the work duration in minutes (default: 25): ") or 25)
    break_duration = int(input("Enter the break duration in minutes (default: 5): ") or 5)
    intervals = int(input("Enter the number of intervals (default: 4): ") or 4)

    system("clear")  # For Linux and MacOS; use "system("cls")" for Windows
    pomodoro_timer(work_duration, break_duration, intervals)

if __name__ == "__main__":
    main()
