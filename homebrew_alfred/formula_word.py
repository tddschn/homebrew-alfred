#!/usr/bin/env python3

# %%

from config import formula_30d_install_on_requests_stats_file_path, formula_json_file_path
from common import get_combined_formula, get_items_list, output_script_filter_json
from common import get_item_key_lower_split

# formula_json_file_path = Path.home() / 'testdir' / 'test' / 'formula.json'
# formula_30d_install_on_requests_stats_file_path = Path.home(
# ) / 'testdir' / 'test' / '30d.json'


def main() -> None:
    combined = get_combined_formula(
        formula_path=formula_json_file_path,
        stats_path=formula_30d_install_on_requests_stats_file_path)
    output_script_filter_json(items=get_items_list(
        combined=combined, search_arg_in=get_item_key_lower_split))


if __name__ == '__main__':
    main()