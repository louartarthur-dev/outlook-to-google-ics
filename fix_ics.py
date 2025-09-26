import requests

SOURCE_URL = "URL_DU_FLUX_ICS_OUTLOOK"  # on mettra ça via un secret GitHub
TARGET_TZ = "Europe/Paris"
MS_TZ = "W. Europe Standard Time"

def main():
    r = requests.get(SOURCE_URL, timeout=30)
    r.raise_for_status()
    text = r.text

    # remplace le label Microsoft par un label que Google comprend
    fixed = text.replace(MS_TZ, TARGET_TZ)

    with open("calendar.ics", "w", encoding="utf-8") as f:
        f.write(fixed)

if __name__ == "__main__":
    main()
