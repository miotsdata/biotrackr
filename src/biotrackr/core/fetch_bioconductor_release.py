import requests
import sqlite3
import datetime

def fetch_bioconductor_release():
    """Check if a new Bioconductor release has appeared since last check."""
    conn = sqlite3.connect("watchdog.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bioc_releases (
            version TEXT PRIMARY KEY,
            release_date TEXT,
            notes_url TEXT
        )
    """)

    # 1️⃣ Get the current release number directly from the Bioconductor API
    url = "https://bioconductor.org/config.yaml"
    r = requests.get(url)
    r.raise_for_status()

    # The config.yaml text contains "release_version: '3.22'" etc
    for line in r.text.splitlines():
        if "release_version:" in line:
            version = line.split(":")[1].strip().strip("'\"")
            break
    else:
        print("⚠️ Could not find release_version in Bioconductor config.")
        conn.close()
        return

    # 2️⃣ Check whether we already have this version stored
    cur.execute("SELECT 1 FROM bioc_releases WHERE version = ?", (version,))
    if cur.fetchone() is None:
        # 3️⃣ New release detected
        release_date = datetime.date.today().isoformat()
        notes_url = f"https://bioconductor.org/news/bioc_{version.replace('.', '_')}_release.html"
        cur.execute(
            "INSERT INTO bioc_releases VALUES (?, ?, ?)",
            (version, release_date, notes_url)
        )
        conn.commit()
        print(f"🧬 New Bioconductor release detected: {version}")
    else:
        print(f"✅ Bioconductor is still at {version}")

    conn.close()

