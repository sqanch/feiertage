#!/usr/bin/env python3

import datetime
import sys

def berechne_ostersonntag(jahr):
    """
    Berechnet den Ostersonntag für das angegebene Jahr
    nach der Meeus–Jones–Butcher-Formel.
    """
    a = jahr % 19
    b = jahr // 100
    c = jahr % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    monat = (h + l - 7 * m + 114) // 31
    tag = ((h + l - 7 * m + 114) % 31) + 1
    return datetime.date(jahr, monat, tag)

def erzeuge_ics(jahr, events):
    """
    Erzeugt den ICS-Text (iCalendar) aus der Liste der Feiertage.
    Jeder Feiertag wird als ganztägiges Event eingetragen.
    """
    ics_lines = []
    ics_lines.append("BEGIN:VCALENDAR")
    ics_lines.append("VERSION:2.0")
    ics_lines.append("PRODID:-//Feiertage in Deutschland//python-script//DE")
    ics_lines.append("CALSCALE:GREGORIAN")
    
    for name, datum in events:
        dtstart = datum.strftime("%Y%m%d")
        # Für ganztägige Events ist das Enddatum exklusiv: daher den nächsten Tag
        dtend = (datum + datetime.timedelta(days=1)).strftime("%Y%m%d")
        dtstamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        # UID: Entferne Leerzeichen und Sonderzeichen
        uid = f"{name.replace(' ', '').replace('.', '').lower()}_{jahr}@feiertage.de"
    
        ics_lines.append("BEGIN:VEVENT")
        ics_lines.append(f"UID:{uid}")
        ics_lines.append(f"DTSTAMP:{dtstamp}")
        ics_lines.append(f"DTSTART;VALUE=DATE:{dtstart}")
        ics_lines.append(f"DTEND;VALUE=DATE:{dtend}")
        ics_lines.append(f"SUMMARY:{name}")
        ics_lines.append("END:VEVENT")
    
    ics_lines.append("END:VCALENDAR")
    return "\n".join(ics_lines)

def main():
    # Abfrage des Jahres (entweder als Programmparameter oder per Eingabe)
    print("test")
    if len(sys.argv) > 1:
        try:
            jahr = int(sys.argv[1])
        except ValueError:
            print("Bitte geben Sie ein gültiges Jahr als Zahl ein.")
            sys.exit(1)

    # Berechne den Ostersonntag, da mehrere bewegliche Feiertage davon abhängen
    ostersonntag = berechne_ostersonntag(jahr)
    
    # Liste der bundesweiten Feiertage in Deutschland:
    feiertage = [
        ("Neujahr", datetime.date(jahr, 1, 1)),
        ("3 Könige", datetime.date(jahr, 1, 6)),
        ("Karfreitag", ostersonntag - datetime.timedelta(days=2)),
        ("Ostersonntag", ostersonntag),
        ("Ostermontag", ostersonntag + datetime.timedelta(days=1)),
        ("Tag der Arbeit", datetime.date(jahr, 5, 1)),
        ("Christi Himmelfahrt", ostersonntag + datetime.timedelta(days=39)),
        ("Pfingstsonntag", ostersonntag + datetime.timedelta(days=49)),
        ("Pfingstmontag", ostersonntag + datetime.timedelta(days=50)),
        ("Fronleichnam", ostersonntag + datetime.timedelta(days=60)),
        ("Tag der Deutschen Einheit", datetime.date(jahr, 10, 3)),
        ("Allerheiligen", datetime.date(jahr, 11,1)),
        ("Heiligabend", datetime.date(jahr, 12, 24)),
        ("1. Weihnachtsfeiertag", datetime.date(jahr, 12, 25)),
        ("2. Weihnachtsfeiertag", datetime.date(jahr, 12, 26)),
        ("Silvester", datetime.date(jahr, 12, 31)),
    ]
    # Sortiere die Feiertage nach Datum
    feiertage.sort(key=lambda x: x[1])
    
    ics_content = erzeuge_ics(jahr, feiertage)
    dateiname = f"feiertage_{jahr}.ics"
    with open(dateiname, "w", encoding="utf-8") as f:
        f.write(ics_content)
    
    print(f"ICS-Datei '{dateiname}' wurde erfolgreich erstellt.")

if __name__ == "__main__": main()
