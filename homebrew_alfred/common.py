#!/usr/bin/env python3

import json, sys
from pathlib import Path
from typing import Any, Callable

# import snoop


# @snoop
def get_item_key_lower(item: dict, key) -> str:
    # item['desc'] can be None even if the 'desc' key is present!
    value = item.get(key) or ''

    # item['key'] might be a list, in case of it's a cask and key == 'name'.
    if isinstance(value, list):
        value = ' '.join(value)
    return value.lower()


# import snoop


# @snoop
def get_item_key_lower_split(item: dict, key) -> list[str]:
    lower_str: str = get_item_key_lower(item=item, key=key)
    return lower_str.split()


def rename_key(target_dict: dict, key_orig, key_new) -> dict:
    """rename the key `key_orig` in `target_dict` to `key_new`.
    """
    target_dict[key_new] = target_dict.pop(key_orig)
    return target_dict


# %%


def sort_by_number(item: dict) -> int:
    """get a int representing the `number` i.e. the install count of the `item` dict
    by parsing the `title` value of `item`.
    Use this as the sorting function for a list of `item`s.

    Args:
        item (dict): a single dict containing info about a formula or a cask

    Returns:
        int: the install count.
    """
    title: str = item['title']
    number_with_hash: str = title.split()[2]
    number: str = number_with_hash.removeprefix('#')
    return int(number)


# %%


def get_stats_formula(stats_path: Path) -> dict[str, dict]:
    stats: list[dict] = json.loads(stats_path.read_bytes())['items']
    stats_keyed: dict[str, dict] = {
        item['formula']: rename_key(item, 'formula', 'name')
        for item in stats
    }

    return stats_keyed


def get_combined_formula(formula_path: Path, stats_path: Path) -> list[dict]:
    """get combined list of dicts for formulas. See the description of `combined`, i.e. the return value.

    Args:
        formula_path (Path, optional): Path to the formula.json file.
        stats_path (Path, optional): Path to the formula stats file (formula-30d.json).

    Returns:
        list[dict]: combined list of dicts of describing dict & stats dict.
    """
    formula: list[dict] = json.loads(formula_path.read_bytes())
    stats_keyed: dict[str, dict] = get_stats_formula(stats_path=stats_path)

    # stats_dummy = {"number": int(9E+9), "name": "", "count": "0", "percent": "0"}
    def get_stats_dummy(name: str) -> dict:
        return {
            "number": int(9E+9),
            "name": name,
            "count": "0",
            "percent": "0"
        }

    # stats_keyed might not have that key
    # combined = [item | stats_keyed[item['name']] for item in formula]
    combined: list[dict] = [
        item | stats_keyed.get(item['name'], get_stats_dummy(item['name']))
        for item in formula
    ]
    return combined


# %%


def get_combined_cask(cask_path: Path, stats_path: Path) -> list[dict]:
    cask = json.loads(cask_path.read_bytes())
    stats = json.loads(stats_path.read_bytes())['formulae']

    stats_dummy = [{
        "count": "0",
    }]

    # stats_keyed might not have that key
    # combined = [item | stats_keyed[item['name']] for item in cask]

    # combined = deepcopy(cask)
    combined = cask
    for item in combined:
        token = item['token']
        item['count'] = stats.get(token, stats_dummy)[0]['count']

    # sort by `count`
    combined.sort(key=sort_by_count, reverse=True)

    # add `number` field
    for i, item in enumerate(combined):
        number = i + 1
        combined[i]['number'] = number

    return combined


# %%


def format_title(item: dict, use_token: bool = False) -> str:
    """generate the value for the `title` key of `item` dict. 
    Format the value string according to the length of the value `name` or `token` of `item`.

    Args:
        item (dict): a single dict containing info about a formula or a cask
        use_token (bool, optional): use the key 'token' as the cask / formula name. 
        Set this to True when `item` is a cask dict. Defaults to False.

    Returns:
        str: see the summary
    """

    number = item['number']
    count = item['count']
    name = item['token'] if use_token else item['name']
    version = item['version'] if use_token else item['versions']['stable']
    # arg_list = [name, version, number, count]
    arg_dict = dict(
        zip(['name', 'version', 'number', 'count'],
            [name, version, number, count]))
    # template_str = '{name:<50}{version:<15}#{number:<15}{count}' if len(
    #     name) > 24 else '{name:<30}{version:<15}#{number:<15}\t{count}'

    len_name_field = len_name + 6 if ((len_name := len(name)) > 24) else 30
    len_version_field = len_version + 4 if (
        (len_version := len(version)) > 11) else 15
    len_number_field = 15
    # len_count_field = len_count + 6 if (len_count := len(count) > 24) else 24

    template_str_name = '{{name:<{length}}}'.format(length=len_name_field)
    template_str_version = '{{version:<{length}}}'.format(
        length=len_version_field)
    template_str_number = '#{{number:<{length}}}'.format(
        length=len_number_field)
    template_str_count = '{count}'

    template_str = '{}{}{}{}'.format(template_str_name, template_str_version,
                                     template_str_number, template_str_count)

    formatted_str = template_str.format(**arg_dict)
    return formatted_str


def gen_single_item(item: dict, use_token: bool = False) -> dict:
    """generate a single `item` dict for the `items` array in 
    alfred script filter json output

    Args:
        item (dict): a single dict containing info about a formula or a cask
        use_token (bool, optional): use the key 'token' as the cask / formula name. 
        Set this to True when `item` is a cask dict. Defaults to False.

    Returns:
        dict: a single `item` dict for the `items` array in 
        alfred script filter json output
    """

    def get_mods_cmd():
        return {
            'valid': True,
            'arg': item['homepage'],
            'subtitle': item['homepage']
        }

    def get_mods_alt():
        return {
            'valid': True,
            'arg': (arg := item['token'] if use_token else item['name']),
            'subtitle': arg
        }

    def get_mods_ctrl():
        if use_token:
            arg = '/usr/local/Homebrew/Library/Taps/homebrew/homebrew-cask/Casks/{}.rb'.format(
                item['token']),
        else:
            arg = '/usr/local/Homebrew/Library/Taps/homebrew/homebrew-core/Formula/{}.rb'.format(
                item['name']),
        # arg appears to be a list or a tuple containing only the string i want, don't know why.
        return {'valid': True, 'arg': 'file://' + arg[0], 'subtitle': arg[0]}

    if use_token:
        item_dict = {
            'title':
            # number isn't present in cask-30d.json
            format_title(item=item, use_token=use_token),
            'subtitle':
            '{}  |  {}'.format(item['name'][0], item['desc']),
            'quicklookurl':
            '/usr/local/Homebrew/Library/Taps/homebrew/homebrew-cask/Casks/{}.rb'
            .format(item['token']),
            # 'https://formulae.brew.sh/cask/{}'.format(item['token']),
            'arg':
            item['token'],
            'mods': {
                "cmd": get_mods_cmd(),
                "alt": get_mods_alt(),
                "ctrl": get_mods_ctrl(),
            },
            'icon': {
                'path': '~/config/scripts/alfred/homebrew-search/cask-icon.png'
            },
            'count':
            item['count']
        }
    else:
        item_dict = {
            'title':
            format_title(item=item, use_token=use_token),
            'subtitle':
            item['desc'],
            'quicklookurl':
            '/usr/local/Homebrew/Library/Taps/homebrew/homebrew-core/Formula/{}.rb'
            .format(item['name']),
            # 'https://formulae.brew.sh/formula/{}'.format(item['name']),
            'arg':
            item['name'],
            'mods': {
                "cmd": get_mods_cmd(),
                "alt": get_mods_alt(),
                "ctrl": get_mods_ctrl(),
            },
            'count':
            item['count']
        }
    return item_dict


def get_items_list(
    combined: list[dict],
    use_token: bool = False,
    search_arg_in: Callable[[dict, Any], Any] = get_item_key_lower
    # search_arg_in: Callable[[dict, Any], str | list[str]] = get_item_key_lower
) -> list[dict]:
    """filter and sort the items obtained from `gen_single_item()`, and put the result dicts in a list

    Args:
        combined (list[dict]): combined list of dicts of describing dict & stats dict.
        use_token (bool, optional): use the key 'token' as the cask / formula name. 
        Set this to True when `item` is a cask dict. Defaults to False.
        search_arg_in: 

    Returns:
        list[dict]: a list of `item` dicts ready for used as the value of `items`
        of an alfred script filter output.
    """
    if len(args := sys.argv) == 1:
        output = [
            gen_single_item(item=item, use_token=use_token)
            for item in combined
        ]
        # output.sort(key=sort_by_number)
        output.sort(key=sort_by_count, reverse=True)
    else:
        arg = args[1]

        output = [
            gen_single_item(item=item, use_token=use_token)
            for item in combined if any(
                map(lambda key: arg.lower() in search_arg_in(item, key),
                    ['name', 'token', 'desc']))
        ]
        # output.sort(key=sort_by_number)
        output.sort(key=sort_by_count, reverse=True)
    return output


def output_script_filter_json(items: list[dict]) -> None:
    d = dict(items=items)
    s: str = json.dumps(d)
    print(s)


def sort_by_count(item: dict) -> int:
    """Sorting function for a list of `item` dicts. 
    Removes commas in the `count` value of the `item`, and output it as an int.

    Args:
        item (dict): a single dict containing info about a formula or a cask

    Returns:
        int: install count
    """
    count: str = item['count'].replace(',', '')
    return int(count)


# %%
