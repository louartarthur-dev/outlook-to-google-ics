import requests
import re

SOURCE_URL = "URL_DU_FLUX_ICS_OUTLOOK"
TARGET_TZ = "Europe/Paris"
MS_TZ_LIST = ["Romance Standard Time", "W. Europe Standard Time"]

def main():
    r = requests.get(SOURCE_URL, timeout=30)
    r.raise_for_status()
    text = r.text

    # 1️⃣ Remplacer tous les TZID Microsoft par Europe/Paris
    for ms_tz in MS_TZ_LIST:
        text = text.replace(ms_tz, TARGET_TZ)

    # 2️⃣ Remplacer les timestamps UTC (finissant par Z) par TZID=Europe/Paris
    text = re.sub(r'DTSTART:(\d{8}T\d{6})Z', rf'DTSTART;TZID={TARGET_TZ}:\1', text)
    text = re.sub(r'DTEND:(\d{8}T\d{6})Z', rf'DTEND;TZID={TARGET_TZ}:\1', text)

    # 3️⃣ Remplacer le bloc VTIMEZONE Microsoft par un bloc standard IANA
    vtimezone_pattern = r'BEGIN:VTIMEZONE.*?END:VTIMEZONE'
    iana_vtimezone = f"""BEGIN:VTIMEZONE
TZID:{TARGET_TZ}
X-LIC-LOCATION:{TARGET_TZ}
BEGIN:DAYLIGHT
TZOFFSETFROM:+0100
TZOFFSETTO:+0200
DTSTART:19700329T020000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
DTSTART:19701025T030000
RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU
END:STANDARD
END:VTIMEZONE"""
    text = re.sub(vtimezone_pattern, iana_vtimezone, text, flags=re.DOTALL)

    # 4️⃣ Ajouter la ligne X-WR-TIMEZONE si absente
    if 'X-WR-TIMEZONE' not in text:
        text = re.sub(r'(VERSION:2.0)', rf'\1\nX-WR-TIMEZONE:{TARGET_TZ}', text, count=1)

    # 5️⃣ Écrire le fichier corrigé
    with open("calendar.ics", "w", encoding="utf-8") as f:
        f.write(text)

    print("✅ Fichier ICS corrigé généré avec TZID=Europe/Paris pour tous les événements.")

if __name__ == "__main__":
    main()
