import os
import sys
import psutil
import time
import win32gui
import win32process
import tkinter as tk
from tkinter import ttk

# Determine the directory containing main.py
script_dir = os.path.dirname(os.path.abspath(__file__))

# Add the directory containing main.py to the sys.path list
sys.path.append(script_dir)

# Import the gui module from the directory containing main.py
import gui

# Dictionary to store process IDs and their respective start times
process_start_times = {}

# Update interval in milliseconds
UPDATE_INTERVAL_MS = 1000

def start_timer(process_id):
    process_start_times[process_id] = time.time()
    print(f"Started timer for process ID: {process_id}")

def stop_timer(process_id):
    start_time = process_start_times.pop(process_id)
    elapsed_time = time.time() - start_time
    print(f"Stopped timer for process ID: {process_id}. Elapsed time: {elapsed_time}")
    # You can save the elapsed time to a file or database as required
    return elapsed_time

def is_window_visible(hwnd):
    '''Check if a window is visible'''
    if win32gui.IsWindowVisible(hwnd):
        min_window = win32gui.GetWindow(hwnd, win32gui.GW_OWNER)
        if min_window:
            return False
        else:
            return True
    return False

def list_visible_processes():
    processes = {}
    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            process_name = process.name()
            if process_name not in processes:
                processes[process_name] = pid
        return True
    win32gui.EnumWindows(callback, None)
    return processes

def update_gui(opened_processes_list, closed_processes_list):
    print("Updating GUI...")
    opened_processes_list.delete(0, tk.END)
    closed_processes_list.delete(0, tk.END)
    visible_processes = list_visible_processes()
    for process_name, pid in visible_processes.items():
        if pid in process_start_times:
            elapsed_time = time.time() - process_start_times[pid]
            timer_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
            opened_processes_list.insert(tk.END, f"{process_name} - {timer_str}")
        else:
            closed_processes_list.insert(tk.END, process_name)

def update_interval_changed():
    global UPDATE_INTERVAL_MS
    try:
        new_interval_seconds = int(update_interval_entry.get())
        if 1 <= new_interval_seconds <= 3600:
            UPDATE_INTERVAL_MS = new_interval_seconds * 1000
            print(f"Update interval changed to {new_interval_seconds} seconds")
        else:
            print("Update interval must be between 1 and 3600 seconds.")
    except ValueError:
        print("Please enter a valid integer for the update interval.")

def main():
    print("Starting main function...")

    root = tk.Tk()
    root.title("Process Timer")

    opened_processes_list, closed_processes_list, update_interval_entry = gui.setup_gui(root, update_interval_changed, update_gui)

    # Update the GUI at regular intervals
    def update():
        print("Running update loop...")
        update_gui(opened_processes_list, closed_processes_list)
        root.after(UPDATE_INTERVAL_MS, update)

    root.after(0, update)

    # Start timers for currently running processes
    for process_name, pid in list_visible_processes().items():
        if pid not in process_start_times:
            start_timer(pid)

    root.mainloop()

if __name__ == "__main__":
    main()
