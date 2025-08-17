
# fullscreen_with_tiktokbot.py
# pip install pillow requests

import tkinter as tk
from PIL import Image, ImageTk
import requests, io, subprocess, sys, os

# --- Konfiguration ---
IMAGE_URL = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhX7NUvas8RVjQNLAXnaoOJGxn1IjXfkNnAf3cRAGItO_omJt8E0KUKbSZzLn1ba18RWKrSSLCKY7Ty__9RIEXarp8eqW1qJIOD1k0E5_cFQ45hRBDVHnd13f501wMRiDKmahS66cWms-rq/w919/mr-robot-fsociety-logo-mask-minimalist-uhdpaper.com-4K-46-wp.thumbnail.jpg"
EXIT_PASSWORD = "volesabi"

# Pfad zu deinem Skript anpassen:
EXTERNAL_SCRIPT = r"C:\Users\DEINNAME\Desktop\tool\tiktok bot.py"
# ----------------------

class FullscreenImageApp:
    def __init__(self, root, image, exit_password):
        self.root = root
        self.exit_password = exit_password

        root.title("Fullscreen Image")
        root.attributes("-fullscreen", True)
        root.attributes("-topmost", True)
        root.overrideredirect(True)
        root.config(cursor="none")

        root.protocol("WM_DELETE_WINDOW", self.on_ignore)
        root.bind_all("<Control-Shift-KeyPress-Q>", self.request_exit)

        self.canvas = tk.Canvas(root, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.img = image
        self.tkimg = None
        self.update_image()
        root.bind("<Configure>", lambda e: self.update_image())

    def update_image(self):
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        if w <= 1 or h <= 1:
            self.root.after(50, self.update_image)
            return

        img = self.img.copy()
        img_ratio = img.width / img.height
        screen_ratio = w / h

        if img_ratio > screen_ratio:
            new_w = w
            new_h = int(w / img_ratio)
        else:
            new_h = h
            new_w = int(h * img_ratio)

        img = img.resize((new_w, new_h))
        self.tkimg = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        x = (w - new_w) // 2
        y = (h - new_h) // 2
        self.canvas.create_image(x, y, anchor=tk.NW, image=self.tkimg)

    def on_ignore(self, *args):
        pass

    def request_exit(self, event=None):
        popup = tk.Toplevel(self.root)
        popup.attributes("-topmost", True)
        popup.grab_set()
        popup.geometry("320x120")
        popup.title("Passwort eingeben")

        lbl = tk.Label(popup, text="Exit-Passwort:")
        lbl.pack(pady=(10,0))
        entry = tk.Entry(popup, show="*")
        entry.pack(pady=5, padx=10, fill=tk.X)

        def submit():
            if entry.get() == self.exit_password:
                popup.destroy()
                self.cleanup_and_exit()
            else:
                lbl.config(text="Falsches Passwort!")

        btn = tk.Button(popup, text="OK", command=submit)
        btn.pack(pady=(5,10))
        entry.focus_set()
        popup.wait_window()

    def cleanup_and_exit(self):
        self.root.config(cursor="")
        self.root.overrideredirect(False)
        self.root.attributes("-fullscreen", False)
        self.root.attributes("-topmost", False)
        self.root.destroy()


if __name__ == "__main__":
    # Bild aus URL laden
    r = requests.get(IMAGE_URL, timeout=10)
    img = Image.open(io.BytesIO(r.content))

    # Python-Skript starten
    try:
        subprocess.Popen([sys.executable, EXTERNAL_SCRIPT], shell=True)
    except Exception as e:
        print("Fehler beim Start des Skripts:", e)

    root = tk.Tk()
    app = FullscreenImageApp(root, img, EXIT_PASSWORD)
    root.mainloop()
