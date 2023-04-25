import time
from os import system
from pynput import keyboard

exit_flag = False

def on_press(key):
    global exit_flag
    try:
        if key.char == 'q':
            exit_flag = True
    except AttributeError:
        pass

def pomodoro_timer(work_duration=25, break_duration=5, intervals=4):
    global exit_flag
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    for interval in range(1, intervals + 1):
        print(f"Interval {interval}/{intervals}")
        print(f"Work for {work_duration} minutes. Press 'q' to stop the timer.")
        for _ in range(work_duration * 60):
            if exit_flag:
                break
            time.sleep(1)
        if exit_flag:
            break

        print(f"Take a {break_duration} minute break. Press 'q' to stop the timer.")
        for _ in range(break_duration * 60):
            if exit_flag:
                break
            time.sleep(1)
        if exit_flag:
            break

    if not exit_flag:
        print("Congratulations! You've completed all intervals.")
    else:
        print("Pomodoro timer stopped.")

def main():
    work_duration = int(input("Enter the work duration in minutes (default: 25): ") or 25)
    break_duration = int(input("Enter the break duration in minutes (default: 5): ") or 5)
    intervals = int(input("Enter the number of intervals (default: 4): ") or 4)

    system("clear")  # For Linux and MacOS; use "system("cls")" for Windows
    pomodoro_timer(work_duration, break_duration, intervals)

if __name__ == "__main__":
    main()
