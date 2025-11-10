import sqlite3
import datetime
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

def generate_digest():
    conn = sqlite3.connect("watchdog.db")
    cur = conn.cursor()

    def fetch_table(name, columns):
        cur.execute(f"SELECT {', '.join(columns)} FROM {name}")
        return [dict(zip(columns, row)) for row in cur.fetchall()]

    data = {
        "date": datetime.date.today().isoformat(),
        "papers": fetch_table("papers", ["title", "authors", "journal", "date", "url"]),
        "github_releases": fetch_table("github_releases", ["repo", "tag", "url"]),
        "bioc_releases": fetch_table("bioc_releases", ["version", "release_date", "notes_url"])
    }
    TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("report.html.j2")

    html = template.render(**data)

    with open("report.html", "w", encoding="utf-8") as f:
        f.write(html)

    conn.close()
    print("✅ Digest generated: report.html")

