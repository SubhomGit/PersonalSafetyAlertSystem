import tkinter as tk
import subprocess

def start_monitoring():
    global process
    process = subprocess.Popen(['python', 'personal_safety_alert_system.py'])

def stop_monitoring():
    if process:
        process.terminate()

root = tk.Tk()
root.title("Personal Safety Alert System")

start_button = tk.Button(root, text="Start Monitoring", command=start_monitoring)
start_button.pack()

stop_button = tk.Button(root, text="Stop Monitoring", command=stop_monitoring)
stop_button.pack()

root.mainloop()
