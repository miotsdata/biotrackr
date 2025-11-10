import yaml
from core import *
import os

script_dir: str = os.path.dirname(os.path.abspath(__file__))
default_config_file: str = os.path.join(script_dir, 'config', 'base.yaml')

with open(default_config_file) as f:
    cfg = yaml.safe_load(f)

fetch_papers(cfg["keywords"])
fetch_bioconductor_release()
fetch_github_releases(cfg["github_repos"], token=None)  # Add GH token if rate-limited
generate_digest()


