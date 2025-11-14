from .core import *
"""
fetch_papers(cfg["keywords"])
fetch_bioconductor_release()
fetch_github_releases(cfg["github_repos"], token=None)  # Add GH token if rate-limited
generate_digest()
"""

import argparse
from pathlib import Path
from .config import load_config
from .database import get_db_path, init_db, get_session

def main():
    parser = argparse.ArgumentParser(prog="biotrackr", description="BioTrackr CLI")
    parser.add_argument("--config", type=str, help="Path to a custom config file")
    args = parser.parse_args()

    # Load config
    config = load_config(Path(args.config) if args.config else None)

    # Setup DB
    db_path = get_db_path(config)
    engine = init_db(db_path)
    session = get_session(engine)

    fetch_bioconductor_release(session)    
    
    keywords = config.get("keywords", [])
    if keywords:
        fetch_papers(session, keywords)

    github_repos = config.get("github_repos", [])
    if github_repos:
        fetch_github(session, github_repos)


    generate_digest(session)

if __name__ == "__main__":
    main()

