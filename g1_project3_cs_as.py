import tkinter as tk
from tkinter import simpledialog
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
    tk.messagebox.showinfo("Success", "Feedback logged successfully.")

def view_feedback():
    """
    Views all logged feedback and logs action.
    """
    feedback_log = load_feedback()
    feedback_str = '\n'.join([f"{entry['Timestamp']}: {entry['Feedback']}" for entry in feedback_log])
    tk.messagebox.showinfo("Feedback Log", feedback_str if feedback_str else "No feedback yet.")
    logging.info("Viewed feedback log.")

def ask_feedback():
    """
    Prompts the user to enter feedback.
    """
    feedback = simpledialog.askstring("Feedback", "Enter your feedback:")
    if feedback:
        log_feedback(feedback)
    else:
        logging.info("No feedback entered.")

def setup_ui():
    root = tk.Tk()
    root.title("Feedback System")
    
    tk.Label(root, text="Feedback System", font=('Arial', 14)).pack(pady=10)
    
    tk.Button(root, text="Enter Feedback", command=ask_feedback).pack(pady=5)
    tk.Button(root, text="View Feedback", command=view_feedback).pack(pady=5)
    
    root.mainloop()

setup_ui()
