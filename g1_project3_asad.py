import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
import pickle
import datetime as d
import logging

logging.basicConfig(filename='FeedbackSystem.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_feedback():
    """
    Loads feedback logs from file.
    """
    try:
        with open('FeedbackLog.pkl', 'rb') as f:
            feedback_log = pickle.load(f)
    except FileNotFoundError:
        feedback_log = []
    return feedback_log

def log_feedback(feedback):
    """
    Logs user feedback in a separate file and logs action.
    """
    feedback_log = load_feedback()
    feedback_entry = {
        'Timestamp': d.datetime.now().strftime("%x, %X"),
        'Feedback': feedback
    }
    feedback_log.append(feedback_entry)
    with open('FeedbackLog.pkl', 'wb') as f:
        pickle.dump(feedback_log, f)
    logging.info(f"Feedback logged: {feedback}")
    messagebox.showinfo("Success", "Feedback logged successfully.")

def ask_feedback():
    """
    Prompts the user to enter feedback.
    """
    feedback_window = tk.Toplevel()
    feedback_window.title("Enter Feedback")
    feedback_window.geometry("330x150")
    tk.Label(feedback_window, text="Enter your feedback:", font=('Arial', 10)).grid(row=0, column=0, pady=10)

    feedback_entry = tk.Entry(feedback_window, width=50)
    feedback_entry.grid(row=1, column=0, padx=10, pady=10)


    def submit_feedback():
        feedback = feedback_entry.get()
        if feedback:
            log_feedback(feedback)
        else:
            logging.info("No feedback entered.")
        feedback_window.destroy()
    tk.Button(feedback_window, text="Submit", command=submit_feedback).grid(row=2, column=0, pady=10)


def view_feedback():
    """
    Views all logged feedback and logs action.
    """
    feedback_log = load_feedback()
    feedback_str = '\n'.join([f"{entry['Timestamp']}: {entry['Feedback']}" for entry in feedback_log])
    
    feedback_window = tk.Toplevel()
    feedback_window.title("View Feedback")
    
    feedback_display = tk.Text(feedback_window, width=80, height=20)
    feedback_display.insert(tk.END, feedback_str if feedback_str else "No feedback yet.")
    feedback_display.pack(pady=10)
    
    logging.info("Viewed feedback log.")


def load_bug_tracker():
    """
    Loads bug tracker data from files.
    """
    try:
        with open('ForestviewBugTracker.pkl', 'rb') as f:
            tracker = pickle.load(f)
    except FileNotFoundError:
        tracker = []
    try:
        with open('ForestviewSoftwareDevs.pkl', 'rb') as g:
            dev_data = pickle.load(g)
    except FileNotFoundError:
        dev_data = {}
    return tracker, dev_data

def save_bug_tracker(tracker, dev_data):
    """
    Saves bug tracker data to files.
    """
    with open('ForestviewBugTracker.pkl', 'wb') as f:
        pickle.dump(tracker, f)
    with open('ForestviewSoftwareDevs.pkl', 'wb') as g:
        pickle.dump(dev_data, g)

def check_dev(x, data):
    """
    Checks if dev is available
    """
    if data.get(x, False):
        data[x] = False
        return True
    else:
        return False

def _filter(x):
    """
    Filters for special characters
    """
    temp = ''
    for i in x:
        if (i.isalpha() or i.isdigit() or i == ' ' or i == ','):
            temp += i
    return temp

def create_bug_report(entry_log, tracker, dev_data):
    """
    Bug tracking data creation
    """
    entry_log = _filter(entry_log)
    entry_log = entry_log.split(',')
    if check_dev(entry_log[3], dev_data):
        storage = {
            'Name': entry_log[0],
            'Bug': entry_log[1],
            'Application': entry_log[2],
            'Dev Assigned': entry_log[3],
            'Timestamp': d.datetime.now().strftime("%x, %X")
        }
        tracker.append(storage)
        save_bug_tracker(tracker, dev_data)
    else:
        print("Dev is not available")

def query_bug_report(tracker, name):
    """
    Function to query bug database
    """
    out = next((i for i in tracker if i['Name'] == name), None)
    return out

def view_bug_reports():
    """
    Views all logged bug reports.
    """
    tracker, _ = load_bug_tracker()
    bug_report_str = '\n'.join([f"{entry['Timestamp']}: {entry['Name']}, {entry['Bug']}, {entry['Application']}, {entry['Dev Assigned']}" for entry in tracker])
    
    bug_report_window = tk.Toplevel()
    bug_report_window.title("View Bug Reports")
    
    bug_report_display = tk.Text(bug_report_window, width=80, height=10)
    bug_report_display.insert(tk.END, bug_report_str if bug_report_str else "No bug reports yet.")
    bug_report_display.pack(pady=10)

def ask_bug_report():
    """
    Prompts the user to enter bug report.
    """
    def add_dev(dev_name):
        """
        Adds a developer to the dev_data dictionary.
        """
        _, dev_data = load_bug_tracker()
        dev_data[dev_name] = True
        _, current_tracker = load_bug_tracker()  
        save_bug_tracker(current_tracker, dev_data)
    add_dev('asad')
    bug_report_window = tk.Toplevel()
    bug_report_window.title("Enter Bug Report")
    bug_report_window.geometry("500x250")

    fields = ["Name", "Bug", "Application", "Dev"]
    entries = []

    for i, field in enumerate(fields):
        tk.Label(bug_report_window, text=field, font=('Arial', 10)).grid(row=i, column=0, padx=10, pady=10)
        entry = tk.Entry(bug_report_window, width=50)
        entry.grid(row=i, column=1, padx=10, pady=10)
        entries.append(entry)

    def submit_bug_report():
        values = [entry.get() for entry in entries]
        if all(values):
            name, bug, app, dev = values
            tracker, dev_data = load_bug_tracker()
            if check_dev(dev, dev_data):
                storage = {
                    'Name': name,
                    'Bug': bug,
                    'Application': app,
                    'Dev Assigned': dev,
                    'Timestamp': d.datetime.now().strftime("%x, %X")
                }
                if isinstance(tracker, list):
                    tracker.append(storage)
                else:
                    tracker = [storage]  # If tracker is not a list, create a new list with storage as the first element
                save_bug_tracker(tracker, dev_data)
                messagebox.showinfo("Success", "Bug report logged successfully.", parent=bug_report_window)
            else:
                messagebox.showinfo("Error", "Dev is not available.", parent=bug_report_window)
        else:
            print("Please fill in all fields.")
        bug_report_window.destroy()

    tk.Button(bug_report_window, text="Submit", command=submit_bug_report).grid(row=len(fields), columnspan=2, pady=10)


    
def setup_ui():
    root = tk.Tk()
    root.title("Feedback & Bug Tracker")
    
    root.geometry("500x400")

    tk.Label(root, text="Feedback System", font=('Arial', 14)).pack(pady=10)
    
    tk.Button(root, text="Enter Feedback", command=ask_feedback).pack(pady=5)
    tk.Button(root, text="View Feedback", command=view_feedback).pack(pady=5)

    tk.Label(root, text="Bug Tracker", font=('Arial', 14)).pack(pady=10)
    
    tk.Button(root, text="Enter Bug Report", command=ask_bug_report).pack(pady=5)
    tk.Button(root, text="View Bug Reports", command=view_bug_reports).pack(pady=5)
    
    root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("User Agreement")

    with open("user_agreement.txt", "r", encoding='utf-8') as file:
        agreement_text = file.read()

    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, font=("Helvetica", 10))
    text_area.insert(tk.INSERT, agreement_text)
    text_area.pack(expand=True, fill="both", padx=10, pady=10)

    result = tk.BooleanVar()

    def agree():
        result.set(True)
        root.destroy()

    agree_button = tk.Button(root, text="Agree", command=agree, bg="#4CAF50", fg="white", font=("Helvetica", 12), padx=10, pady=5)
    agree_button.pack(side=tk.BOTTOM, pady=10)

    root.mainloop()

    if result.get():
        setup_ui()
    else:
        print("You must agree to the user agreement to use this program.")
        exit(1)
