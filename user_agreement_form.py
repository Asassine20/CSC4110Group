import tkinter as tk
from tkinter import scrolledtext

class AgreementWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("User Agreement")
        with open("user_agreement.txt", "r") as file:
            agreement_text = file.read()

        text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=60, height=20, font=("Helvetica", 10))
        text_area.insert(tk.INSERT, agreement_text)
        text_area.pack(expand=True, fill="both", padx=10, pady=10)

        agree_button = tk.Button(self, text="Agree", command=self.destroy, bg="#4CAF50", fg="white", font=("Helvetica", 12), padx=10, pady=5)
        agree_button.pack(side=tk.BOTTOM, pady=10)

if __name__ == "__main__":
    AgreementWindow().mainloop()



