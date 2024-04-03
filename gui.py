import tkinter as tk
from tkinter import ttk

def setup_gui(root, update_interval_changed, update_gui):
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

    # Update interval input field
    update_interval_frame = tk.Frame(root)
    update_interval_frame.pack(pady=(10, 0))

    update_interval_label = tk.Label(update_interval_frame, text="Update Interval (seconds):")
    update_interval_label.pack(side=tk.LEFT, padx=(5, 0), pady=5)

    update_interval_entry = tk.Entry(update_interval_frame, width=10)
    update_interval_entry.pack(side=tk.LEFT, padx=(0, 5), pady=5)

    update_interval_button = tk.Button(update_interval_frame, text="Set Interval", command=update_interval_changed, width=10)
    update_interval_button.pack(side=tk.LEFT, pady=5)

    return opened_processes_list, closed_processes_list, update_interval_entry
