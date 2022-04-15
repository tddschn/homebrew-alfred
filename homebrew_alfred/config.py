#!/usr/bin/env python3
from pathlib import Path
import os

if not (brew_json_cache_dir := os.getenv('brew_json_cache_dir', None)):
    brew_json_cache_dir = Path.home() / 'config/pm/brew/brew-jsons'
else:
    brew_json_cache_dir = Path(brew_json_cache_dir)

# formula
formula_json_file_path = brew_json_cache_dir / 'formula.json'
formula_30d_install_on_requests_stats_file_path = brew_json_cache_dir / 'formula-30d.json'

formula_json_url = 'https://formulae.brew.sh/api/formula.json'
formula_stats_json_url = 'https://formulae.brew.sh/api/analytics/install-on-request/30d.json'

# cask
cask_json_file_path = brew_json_cache_dir / 'cask.json'
cask_30d_install_on_requests_stats_file_path = brew_json_cache_dir / 'cask-30d.json'

cask_json_url = 'https://formulae.brew.sh/api/cask.json'
cask_stats_json_url = 'https://formulae.brew.sh/api/analytics/cask-install/homebrew-cask/30d.json'

url_filepath_mapping = {
    formula_json_url: formula_json_file_path,
    formula_stats_json_url: formula_30d_install_on_requests_stats_file_path,
    cask_json_url: cask_json_file_path,
    cask_stats_json_url: cask_30d_install_on_requests_stats_file_path
}
