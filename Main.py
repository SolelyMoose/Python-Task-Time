import psutil
import time
import win32gui
import win32process
import tkinter as tk
from tkinter import ttk

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

def update_gui():
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

def main():
    print("Starting main function...")
    global opened_processes_list, closed_processes_list  # Declare process_list as a global variable

    root = tk.Tk()
    root.title("Process Timer")

    notebook = ttk.Notebook(root)
    notebook.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    opened_processes_frame = ttk.Frame(notebook)
    closed_processes_frame = ttk.Frame(notebook)

    notebook.add(opened_processes_frame, text="Opened Processes")
    notebook.add(closed_processes_frame, text="Closed Processes")

    opened_processes_list = tk.Listbox(opened_processes_frame, width=50, height=20)
    opened_processes_list.pack(padx=10, pady=10)

    closed_processes_list = tk.Listbox(closed_processes_frame, width=50, height=20)
    closed_processes_list.pack(padx=10, pady=10)

    # Update the GUI at regular intervals
    def update():
        update_gui()
        root.after(UPDATE_INTERVAL_MS, update)

    root.after(0, update)

    # Start timers for currently running processes
    for process_name, pid in list_visible_processes().items():
        if pid not in process_start_times:
            start_timer(pid)

    root.mainloop()

if __name__ == "__main__":
    main()
