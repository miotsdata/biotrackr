import datetime
import requests
from biotrackr.models import Paper
from sqlalchemy import insert, select, func


def fetch_papers(session, keywords, since_days=7):
    """Fetch new papers from Europe PMC based on keywords and store them in the database."""
    if not keywords:
        return
    base_url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    since_date = (datetime.date.today() - datetime.timedelta(days=since_days)).isoformat()

    papers_to_add = []

    for kw in keywords:
            query = f"({kw}) AND FIRST_PDATE:[{since_date} TO *]"
            params = {"query": query, "format": "json", "pageSize": 25}
            resp = requests.get(base_url, params=params)
            resp.raise_for_status()

            for r in resp.json().get("resultList", {}).get("result", []):
                pub_date_str = r.get("firstPublicationDate")
                try:
                    pub_date = datetime.datetime.strptime(pub_date_str, "%Y-%m-%d").date()
                except Exception:
                    pub_date = None

                papers_to_add.append({
                    "pmid": r["id"],
                    "title": r["title"],
                    "doi": r.get("doi") or None,
                    "url": f"https://pubmed.ncbi.nlm.nih.gov/{r.get('pmid')}",
                    "published_on": pub_date 
                })
    before = session.scalar(select(func.count()).select_from(Paper))


    if papers_to_add:
        stmt = (
            insert(Paper)
            .prefix_with("OR IGNORE")
            .values(papers_to_add)
        )
        session.execute(stmt)
        session.commit()
    after = session.scalar(select(func.count()).select_from(Paper))
    added = after - before
    print(f"📖 Added {added} new papers (ignored duplicates).")
