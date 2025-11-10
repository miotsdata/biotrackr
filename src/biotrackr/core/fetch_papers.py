import requests, datetime, sqlite3, urllib.parse

def fetch_papers(keywords, since_days=7):
    conn = sqlite3.connect("watchdog.db")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS papers 
                   (id TEXT PRIMARY KEY, title TEXT, authors TEXT, journal TEXT, 
                    date TEXT, url TEXT, source TEXT)""")

    base_url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    since_date = (datetime.date.today() - datetime.timedelta(days=since_days)).isoformat()

    for kw in keywords:
        query = f'({kw}) AND FIRST_PDATE:[{since_date} TO *]'
        params = {"query": query, "format": "json", "pageSize": 25}
        resp = requests.get(base_url, params=params)
        resp.raise_for_status()
        for r in resp.json().get("resultList", {}).get("result", []):
            cur.execute("INSERT OR IGNORE INTO papers VALUES (?,?,?,?,?,?,?)", (
                r["id"], r["title"], r.get("authorString", ""), r.get("journalTitle", ""),
                r.get("firstPublicationDate", ""), r.get("fullTextUrlList", {}).get("fullTextUrl", [{}])[0].get("url", ""),
                r.get("source", "")
            ))
    conn.commit()
    conn.close()


