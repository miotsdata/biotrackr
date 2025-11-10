import requests
import sqlite3
import datetime
from datetime import timezone

def fetch_github_releases(repos, token=None, since_days=7):
    conn = sqlite3.connect("watchdog.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS github_releases (
            repo TEXT,
            tag TEXT,
            published TEXT,
            url TEXT,
            PRIMARY KEY (repo, tag)
        )
    """)

    headers = {"Authorization": f"token {token}"} if token else {}
    cutoff = datetime.datetime.now(timezone.utc) - datetime.timedelta(days=since_days)

    for repo in repos:
        url = f"https://api.github.com/repos/{repo}/releases"
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            for rel in r.json():
                published_at = rel.get("published_at")
                if not published_at:
                    continue
                # Convert to timezone-aware datetime in UTC
                pub = datetime.datetime.fromisoformat(
                    published_at.replace("Z", "+00:00")
                )
                if pub > cutoff:
                    cur.execute(
                        "INSERT OR IGNORE INTO github_releases VALUES (?,?,?,?)",
                        (repo, rel["tag_name"], rel["published_at"], rel["html_url"]),
                    )
        else:
            print(f"⚠️ Failed to fetch {repo}: {r.status_code} {r.text}")

    conn.commit()
    conn.close()

