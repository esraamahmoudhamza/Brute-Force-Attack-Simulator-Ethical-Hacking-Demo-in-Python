import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import string
import winsound

# ========== Fake DB ==========
users_db = {
    "esraa": "abc",
    "admin": "123",
    "user": "1a2"
}

# ========== GUI Colors ==========
BG = "#1A1A2E"
FG = "#EAEAEA"
BTN = "#00ADB5"
TEXT_BG = "#16213E"
FONT = ("Segoe UI", 12)
TITLE_FONT = ("Segoe UI", 18, "bold")

# ========== Brute Force Class ==========
class BruteForce:
    def __init__(self):
        self.username = ""
        self.target_password = ""
        self.charset = ""
        self.max_length = 4
        self.found = False
        self.attempts = 0
        self.start_time = 0
        self.total_attempts = 0

    def start_attack(self):
        self.username = username_entry.get()
        self.target_password = users_db.get(self.username)

        if not self.target_password:
            status_label.config(text="❌ Username not found!")
            return

        self.charset = charset_entry.get()
        try:
            self.max_length = int(length_spinbox.get())
        except:
            status_label.config(text="❌ Invalid max length!")
            return

        self.total_attempts = sum(len(self.charset) ** i for i in range(1, self.max_length + 1))

        self.attempts = 0
        self.found = False
        self.start_time = time.time()
        text_widget.delete(1.0, tk.END)
        progress_bar['value'] = 0
        status_label.config(text="🔍 Cracking password...")

        threading.Thread(target=self._brute_force, args=("",)).start()

    def _brute_force(self, current):
        if self.found or len(current) > self.max_length:
            return
        for char in self.charset:
            attempt = current + char
            self.attempts += 1

            text_widget.insert(tk.END, f"Trying: {attempt}\n")
            text_widget.see(tk.END)

            if attempt == self.target_password:
                self.found = True
                elapsed = time.time() - self.start_time

                progress_bar['value'] = 100

                status_label.config(
                    text=f"✅ Password found: {attempt} in {self.attempts} tries, Time: {elapsed:.2f}s"
                )

                winsound.Beep(1500, 300)

                self.show_popup(attempt, elapsed)

                return
            else:
                percent = (self.attempts / self.total_attempts) * 100
                progress_bar['value'] = percent
                root.update()

            self._brute_force(attempt)

    def show_popup(self, password, elapsed):
        msg = f"🎉 Password for '{self.username}' has been cracked!\n\nPassword: {password}\nAttempts: {self.attempts}\nTime: {elapsed:.2f} seconds"
        messagebox.showinfo("✅ Crack Success!", msg)

# ========== GUI ==========
root = tk.Tk()
root.title("🎯 Brute Force Cracker GUI")
root.geometry("750x600")
root.config(bg=BG)

# ==== Title ====
tk.Label(root, text="💥 Brute Force Login Simulator", bg=BG, fg=BTN, font=TITLE_FONT).pack(pady=10)

# ==== Inputs ====
form = tk.Frame(root, bg=BG)
form.pack(pady=10)

tk.Label(form, text="Username:", bg=BG, fg=FG, font=FONT).grid(row=0, column=0, padx=8, pady=8)
username_entry = tk.Entry(form, font=FONT, width=20)
username_entry.grid(row=0, column=1, padx=8)

tk.Label(form, text="Charset (e.g. abc123):", bg=BG, fg=FG, font=FONT).grid(row=1, column=0, padx=8, pady=8)
charset_entry = tk.Entry(form, font=FONT, width=20)
charset_entry.insert(0, "abc123")
charset_entry.grid(row=1, column=1, padx=8)

tk.Label(form, text="Max Length:", bg=BG, fg=FG, font=FONT).grid(row=2, column=0, padx=8, pady=8)
length_spinbox = tk.Spinbox(form, from_=1, to=6, font=FONT, width=5)
length_spinbox.grid(row=2, column=1, padx=8, sticky="w")

# ==== Start Button ====
tk.Button(root, text="🚀 Start Attack", bg=BTN, fg="black", font=("Segoe UI", 14, "bold"),
          command=lambda: brute.start_attack(), padx=15, pady=5).pack(pady=10)

# ==== Progress Bar ====
progress_bar = ttk.Progressbar(root, length=500, mode="determinate")
progress_bar.pack(pady=5)

# ==== Output Area ====
output_frame = tk.Frame(root)
output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

text_widget = tk.Text(output_frame, bg=TEXT_BG, fg=FG, font=("Courier", 11))
text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(output_frame, command=text_widget.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_widget.config(yscrollcommand=scrollbar.set)

# ==== Status ====
status_label = tk.Label(root, text="Status: Waiting...", bg=BG, fg=FG, font=FONT)
status_label.pack(pady=5)

# ==== Run App ====
brute = BruteForce()
root.mainloop()
