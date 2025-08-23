#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analoge Uhr – Römische Ziffern (Version 1.2.0)
----------------------------------------------
- Analoganzeige mit römischen Ziffern
- Deutsche Datumsanzeige
- Farbanpassung für Hintergrund, Zifferblatt, Zeiger, Ziffern und Datum
- Speichern/Laden der Farben in/für eine INI-Datei
- Menüpunkt „Farben ändern“ wird während des Dialogs gesperrt
- Stummschaltung mit akustischem Stundenschlag
"""

import tkinter as tk
import math
import locale
from datetime import datetime
from tkinter import colorchooser
import configparser
import os

# ------------- Lokalisierung -------------------
def set_german_locale():
    for loc in ("de_DE.UTF-8", "de_DE", "German"):
        try:
            locale.setlocale(locale.LC_TIME, loc)
            return True
        except locale.Error:
            continue
    return False

USE_LOCALE = set_german_locale()

GERMAN_WEEKDAYS = {
    0: "Montag", 1: "Dienstag", 2: "Mittwoch",
    3: "Donnerstag", 4: "Freitag", 5: "Samstag", 6: "Sonntag"
}
GERMAN_MONTHS = {
    1: "Januar", 2: "Februar", 3: "März", 4: "April",
    5: "Mai", 6: "Juni", 7: "Juli", 8: "August",
    9: "September", 10: "Oktober", 11: "November", 12: "Dezember"
}

def german_date_string(now: datetime) -> str:
    if USE_LOCALE:
        return now.strftime("%A, %d. %B %Y")
    else:
        weekday = GERMAN_WEEKDAYS[now.weekday()]
        month = GERMAN_MONTHS[now.month]
        return f"{weekday}, {now.day:02d}. {month} {now.year}"

# ------------- Konstanten -------------------
ROMAN_NUMERALS = {
    1:'I', 2:'II', 3:'III', 4:'IV', 5:'V', 6:'VI',
    7:'VII', 8:'VIII', 9:'IX', 10:'X', 11:'XI', 12:'XII'
}

WINDOW_TITLE = "Analoge Uhr – Römische Ziffern"
INI_FILE = "colors.ini"

DEFAULT_COLORS = {
    "background": "#FFFFFF",
    "face": "#EEEEEE",
    "hands": "#000000",
    "digits": "#000000",
    "date": "#000000"
}

CANVAS_SIZE = 400
CLOCK_RADIUS = 150

# ------------- RomanClock Klasse -------------------
class RomanClock(tk.Canvas):
    def __init__(self, master, date_var: tk.StringVar, **kwargs):
        super().__init__(master,
                         width=CANVAS_SIZE,
                         height=CANVAS_SIZE,
                         bg=DEFAULT_COLORS["background"],
                         highlightthickness=0,
                         **kwargs)
        self.mute = False
        self.last_hour = None
        self.date_var = date_var
        self._color_swaps = {}

        self.colors = self.load_colors()
        self.face_id = None
        self.hand_ids = {}
        self.digit_ids = {}

        self.create_clock_face()
        self.create_hands()
        self.apply_colors()
        self.update_clock()

    def load_colors(self):
        config = configparser.ConfigParser()
        if os.path.exists(INI_FILE):
            config.read(INI_FILE)
            if "Colors" in config.sections():
                colors = {}
                for key in DEFAULT_COLORS.keys():
                    colors[key] = config.get("Colors", key, fallback=DEFAULT_COLORS[key])
                return colors
        return DEFAULT_COLORS.copy()

    def save_colors(self):
        config = configparser.ConfigParser()
        config["Colors"] = self.colors
        with open(INI_FILE, "w") as f:
            config.write(f)

    def apply_colors(self):
        self.master.configure(bg=self.colors["background"])
        self.configure(bg=self.colors["background"])
        if self.face_id:
            self.itemconfig(self.face_id, fill=self.colors["face"])
        for id_ in self.digit_ids.values():
            self.itemconfig(id_, fill=self.colors["digits"])
        for id_ in self.hand_ids.values():
            self.itemconfig(id_, fill=self.colors["hands"])
        if hasattr(self, 'date_label'):
            self.date_label.config(
                fg=self.colors['date'],
                bg=self.colors['background']   # <- Hier Hintergrund setzen!
            )

    def create_clock_face(self):
        center = CANVAS_SIZE / 2
        self.face_id = self.create_oval(
            center - CLOCK_RADIUS, center - CLOCK_RADIUS,
            center + CLOCK_RADIUS, center + CLOCK_RADIUS,
            outline="black", width=3, fill=self.colors["face"]
        )
        for hour, roman in ROMAN_NUMERALS.items():
            angle_deg = (hour % 12) * 30
            x, y = self.polar_to_xy(angle_deg, CLOCK_RADIUS - 30)
            self.digit_ids[hour] = self.create_text(
                x, y,
                text=roman,
                font=("Helvetica", 14, "bold"),
                fill=self.colors["digits"]
            )

    def create_hands(self):
        center = CANVAS_SIZE / 2
        self.hand_ids["hour"] = self.create_line(center, center, center, center,
                                                 width=6, fill=self.colors["hands"])
        self.hand_ids["minute"] = self.create_line(center, center, center, center,
                                                   width=4, fill=self.colors["hands"])
        self.hand_ids["second"] = self.create_line(center, center, center, center,
                                                   width=2, fill=self.colors["hands"])

    def polar_to_xy(self, angle_deg: float, radius: float):
        rad = math.radians(angle_deg - 90)
        x = CANVAS_SIZE / 2 + radius * math.cos(rad)
        y = CANVAS_SIZE / 2 + radius * math.sin(rad)
        return x, y

    def update_clock(self):
        now = datetime.now()
        hour = now.hour % 12
        minute = now.minute
        second = now.second

        hour_angle = (hour + minute / 60) * 30
        minute_angle = (minute + second / 60) * 6
        second_angle = second * 6

        hour_len = CLOCK_RADIUS * 0.5
        minute_len = CLOCK_RADIUS * 0.7
        second_len = CLOCK_RADIUS * 0.9

        xh, yh = self.polar_to_xy(hour_angle, hour_len)
        xm, ym = self.polar_to_xy(minute_angle, minute_len)
        xs, ys = self.polar_to_xy(second_angle, second_len)

        self.coords(self.hand_ids["hour"], CANVAS_SIZE/2, CANVAS_SIZE/2, xh, yh)
        self.coords(self.hand_ids["minute"], CANVAS_SIZE/2, CANVAS_SIZE/2, xm, ym)
        self.coords(self.hand_ids["second"], CANVAS_SIZE/2, CANVAS_SIZE/2, xs, ys)

        if minute == 0 and second == 0:
            if self.last_hour != now.hour:
                if not self.mute:
                    self.play_beeps(now.hour if now.hour != 0 else 12)
                self.last_hour = now.hour

        if self.date_var:
            self.date_var.set(german_date_string(now))

        self.after(1000, self.update_clock)

    def play_beeps(self, count):
        def beep_step(n):
            if n < count:
                self.master.bell()
                self.after(400, lambda: beep_step(n+1))
        beep_step(0)

    def open_color_dialog(self):
        dialog = tk.Toplevel(self.master)
        dialog.title("Farben ändern")
        dialog.resizable(False, False)
        dialog.transient(self.master)
        dialog.grab_set()

        self._color_swaps = {}

        def on_color_select(varname):
            # Sperre Hauptdialog, damit nicht mehrfach geöffnet wird
            dialog.attributes("-disabled", True)
            color = colorchooser.askcolor(title=f"Farbe für {varname}",
                                        color=self.colors[varname])[1]
            dialog.attributes("-disabled", False)
            if color:
                self.colors[varname] = color
                self.apply_colors()
                if varname in self._color_swaps:
                    self._color_swaps[varname].config(bg=color)
                self.save_colors()

        def reset_colors():
            self.colors = DEFAULT_COLORS.copy()
            self.apply_colors()
            for varname, sw in self._color_swaps.items():
                sw.config(bg=self.colors[varname])
            self.save_colors()

        names = [
            ("Hintergrund", "background"),
            ("Zifferblatt", "face"),
            ("Zeiger", "hands"),
            ("Ziffern", "digits"),
            ("Datumsanzeige", "date")
        ]

        for idx, (label, varname) in enumerate(names):
            lbl = tk.Label(dialog, text=label)
            lbl.grid(row=idx, column=0, padx=5, pady=5, sticky="e")
            btn = tk.Button(dialog, text="Auswählen",
                            command=lambda n=varname: on_color_select(n))
            btn.grid(row=idx, column=1, padx=5, pady=5, sticky="w")
            sw = tk.Label(dialog, bg=self.colors[varname], width=3)
            sw.grid(row=idx, column=2, padx=5, pady=5)
            self._color_swaps[varname] = sw

        reset_btn = tk.Button(dialog, text="Zurücksetzen", command=reset_colors)
        reset_btn.grid(row=len(names), column=0, padx=5, pady=10, sticky="w")

        close_btn = tk.Button(dialog, text="Schließen", command=dialog.destroy)
        close_btn.grid(row=len(names), column=1, columnspan=2, padx=5, pady=10)

        dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)



    def toggle_mute_in_menu(self, menu, idx):
        self.mute = not self.mute
        label = "Stummschaltung aus" if self.mute else "Stummschaltung ein"
        menu.entryconfig(idx, label=label)

# ------------- Hauptfenster und Menü -------------------
def main():
    root = tk.Tk()
    root.title(WINDOW_TITLE)
    root.geometry(f"{CANVAS_SIZE+20}x{CANVAS_SIZE+70}")

    date_var = tk.StringVar()
    date_lbl = tk.Label(root,
                        textvariable=date_var,
                        font=("Helvetica", 12),
                        bg=DEFAULT_COLORS["background"],
                        fg=DEFAULT_COLORS["date"])
    date_lbl.pack(side="bottom", pady=10)

    clock = RomanClock(root, date_var=date_var)
    clock.pack(padx=10, pady=10)
    clock.date_label = date_lbl
    clock.apply_colors()  # nochmal aufrufen, damit Hintergrund richtig gesetzt wird


    menubar = tk.Menu(root)
    submenu = tk.Menu(menubar, tearoff=0)

    def toggle_mute():
        clock.toggle_mute_in_menu(submenu, 0)

    submenu.add_command(label="Stummschaltung ein", command=toggle_mute)
    farben_index = 1
    submenu.add_command(label="Farben ändern", command=clock.open_color_dialog)
    submenu.add_separator()
    submenu.add_command(label="Beenden", command=root.destroy)

    menubar.add_cascade(label="Menü", menu=submenu)
    root.config(menu=menubar)

    clock.farben_menu = submenu
    clock.farben_index = farben_index

    root.mainloop()

if __name__ == "__main__":
    main()
