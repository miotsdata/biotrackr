import sqlite3, datetime

def generate_digest():
    conn = sqlite3.connect("watchdog.db")
    cur = conn.cursor()
    today = datetime.date.today().isoformat()

    html = [f"<h2>Weekly Digest – {today}</h2>"]

    for table, label in [
        ("papers", "🧾 New Papers"),
        ("bioc_releases", "💻 Bioconductor Releases"),
        ("github_releases", "🐍 GitHub Releases")
    ]:
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()
        if rows:
            html.append(f"<h3>{label}</h3><ul>")
            for r in rows:
                if table == "papers":
                    html.append(f"<li><b>{r[1]}</b> – {r[2]} (<a href='{r[5]}'>link</a>)</li>")
                elif table == "bioc_releases":
                    html.append(f"<li>{r[0]} {r[1]} – {r[2]}</li>")
                elif table == "github_releases":
                    html.append(f"<li>{r[0]} {r[1]} (<a href='{r[3]}'>link</a>)</li>")
            html.append("</ul>")

    with open("digest.html", "w", encoding="utf-8") as f:
        f.write("\n".join(html))
    print("✅ Digest written to digest.html")

