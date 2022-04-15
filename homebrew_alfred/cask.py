#!/usr/bin/env python3

# %%

from config import cask_30d_install_on_requests_stats_file_path, cask_json_file_path
from common import get_combined_cask, output_script_filter_json, get_items_list

# cask_json_file_path = Path.home() / 'testdir' / 'test' / 'cask.json'
# cask_30d_install_on_requests_stats_file_path = Path.home(
# ) / 'testdir' / 'test' / 'cask-30d.json'

# %%


def main() -> None:
    combined = get_combined_cask(
        cask_path=cask_json_file_path,
        stats_path=cask_30d_install_on_requests_stats_file_path)
    output_script_filter_json(
        items=get_items_list(combined=combined, use_token=True))


if __name__ == '__main__':
    main()