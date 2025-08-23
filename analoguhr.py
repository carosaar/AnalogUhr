#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analoge Uhr mit römischen Ziffern, Stundenschlag und Datum.
Beep‑Töne bei jeder vollen Stunde (Anzahl = Stunde).
Stundenschlag lässt sich per Button stummschalten.

Author:   Dein Name
Date:     2025‑08‑23
"""

import tkinter as tk
import math
import locale
from datetime import datetime

# ------------------------------------------------------------------
#  Locale – Deutsch
# ------------------------------------------------------------------
def set_german_locale():
    """Versucht, die Locale auf Deutsch zu setzen."""
    for loc in ('de_DE.UTF-8', 'de_DE', 'German'):
        try:
            locale.setlocale(locale.LC_TIME, loc)
            return True
        except locale.Error:
            continue
    return False


USE_LOCALE = set_german_locale()

# Manuelle Übersetzung, falls Locale nicht verfügbar
GERMAN_WEEKDAYS = {
    0: 'Montag', 1: 'Dienstag', 2: 'Mittwoch',
    3: 'Donnerstag', 4: 'Freitag', 5: 'Samstag', 6: 'Sonntag'
}
GERMAN_MONTHS = {
    1: 'Januar', 2: 'Februar', 3: 'März',
    4: 'April', 5: 'Mai', 6: 'Juni',
    7: 'Juli', 8: 'August', 9: 'September',
    10: 'Oktober', 11: 'November', 12: 'Dezember'
}

def german_date_string(dt: datetime) -> str:
    """Gibt das Datum im Format 'Dienstag, 23. August 2025' zurück."""
    if USE_LOCALE:
        return dt.strftime('%A, %d. %B %Y')
    else:
        weekday = GERMAN_WEEKDAYS[dt.weekday()]
        month   = GERMAN_MONTHS[dt.month]
        return f"{weekday}, {dt.day:02d}. {month} {dt.year}"


# ------------------------------------------------------------------
#  Hilfsfunktionen
# ------------------------------------------------------------------
def angle_to_xy(angle_deg, length, offset=0):
    """
    Wandelt einen Winkel (in Grad) in ein (x, y) Koordinatenpaar um.
    0° = 12 Uhr; positive Werte laufen im Uhrzeigersinn.
    """
    rad = math.radians(angle_deg - 90 + offset)   # 0° nach oben
    return CENTER_X + length * math.cos(rad), \
           CENTER_Y + length * math.sin(rad)


# ------------------------------------------------------------------
#  Konstanten
# ------------------------------------------------------------------
WINDOW_SIZE   = 400            # Fenstergröße (px)
CLOCK_RADIUS  = 160            # Radius der Uhr
CENTER_X      = WINDOW_SIZE // 2
CENTER_Y      = WINDOW_SIZE // 2
HAND_COLORS   = {'hour': 'black', 'minute': 'blue', 'second': 'red'}

# Römische Ziffern 1–12
ROMAN_NUMERALS = {
    1:  'I',  2: 'II',  3: 'III', 4: 'IV',
    5:  'V',  6: 'VI',  7: 'VII', 8: 'VIII',
    9:  'IX', 10: 'X', 11: 'XI', 12: 'XII'
}


# ------------------------------------------------------------------
#  Hauptklasse
# ------------------------------------------------------------------
class RomanClock(tk.Canvas):
    """
    Canvas‑Widget, das die analoge Uhr zeichnet.
    """
    def __init__(self, parent, date_var=None, **kwargs):
        super().__init__(parent, width=WINDOW_SIZE, height=WINDOW_SIZE,
                         bg='white', highlightthickness=0, **kwargs)
        self.pack()

        self.last_hour = None   # für Stundenschlag
        self.mute      = False  # Beep‑Schalter
        self.date_var  = date_var

        # Kreis der Uhr
        self.create_oval(CENTER_X - CLOCK_RADIUS, CENTER_Y - CLOCK_RADIUS,
                         CENTER_X + CLOCK_RADIUS, CENTER_Y + CLOCK_RADIUS,
                         outline='black', width=4)

        # Römische Ziffern platzieren
        for hour, roman in ROMAN_NUMERALS.items():
            angle = hour * 30               # 360° / 12
            x, y = angle_to_xy(angle, CLOCK_RADIUS - 30)
            self.create_text(x, y, text=roman, font=('Helvetica', 14, 'bold'))

        # Hands
        self.hour_hand   = self.create_line(0, 0, 0, 0, width=6, fill=HAND_COLORS['hour'])
        self.minute_hand = self.create_line(0, 0, 0, 0, width=4, fill=HAND_COLORS['minute'])
        self.second_hand = self.create_line(0, 0, 0, 0, width=2, fill=HAND_COLORS['second'])

        # Stummschalter‑Button
        self.mute_button = tk.Button(parent,
                                     text="Stummschaltung ein",
                                     command=self.toggle_mute)
        self.mute_button.pack(pady=5)

        # Initiales Update
        self.update_clock()

    # ---------- Stummschalter ----------
    def toggle_mute(self):
        self.mute = not self.mute
        self.mute_button.config(text="Stummschaltung aus" if self.mute else "Stummschaltung ein")

    # ---------- Beep‑Sequenz ----------
    def play_beeps(self, count):
        """Beep‑Sequenz ohne UI‑Blockierung, nutzt `after`."""
        def beep_step(step):
            if step < count:
                self.bell()                      # Tkinter‑Standard‑Beep
                # 0.4 s zwischen den Tönen
                self.after(400, lambda: beep_step(step + 1))
        beep_step(0)

    # ---------- Uhr‑Update ----------
    def update_clock(self):
        now = datetime.now()
        hour   = now.hour % 12
        minute = now.minute
        second = now.second

        # Winkel für jede Hand
        hour_angle   = (hour + minute / 60) * 30
        minute_angle = (minute + second / 60) * 6
        second_angle = second * 6

        # Handlängen
        hour_len   = CLOCK_RADIUS * 0.5
        minute_len = CLOCK_RADIUS * 0.7
        second_len = CLOCK_RADIUS * 0.9

        # Koordinaten der Endpunkte
        xh, yh = angle_to_xy(hour_angle,   hour_len)
        xm, ym = angle_to_xy(minute_angle, minute_len)
        xs, ys = angle_to_xy(second_angle, second_len)

        # Hände aktualisieren
        self.coords(self.hour_hand,   CENTER_X, CENTER_Y, xh, yh)
        self.coords(self.minute_hand, CENTER_X, CENTER_Y, xm, ym)
        self.coords(self.second_hand, CENTER_X, CENTER_Y, xs, ys)

        # --- Stundenschlag prüfen ---
        if minute == 0 and second == 0:
            if self.last_hour != now.hour:
                if not self.mute:
                    # 1‑12 (oder 0 für 12 Uhr)
                    self.play_beeps(now.hour if now.hour != 0 else 12)
                self.last_hour = now.hour

        # Datum aktualisieren, falls Variable vorhanden
        if self.date_var is not None:
            self.date_var.set(german_date_string(now))

        # Wiederholung alle 1 s
        self.after(1000, self.update_clock)


# ------------------------------------------------------------------
#  Hauptfunktion
# ------------------------------------------------------------------
def main():
    root = tk.Tk()
    root.title("Analoge Uhr – Römische Ziffern")
    root.resizable(False, False)

    # Frame für Uhr und Button
    frame = tk.Frame(root, bg='white')
    frame.pack(padx=10, pady=10)

    # Variable für Datum
    date_var = tk.StringVar()

    # Uhr
    clock = RomanClock(frame, date_var=date_var)

    # Datum‑Label unterhalb der Uhr
    date_label = tk.Label(root, textvariable=date_var,
                          font=('Helvetica', 12), bg='white')
    date_label.pack(pady=(0, 10))

    root.mainloop()


if __name__ == "__main__":
    main()
