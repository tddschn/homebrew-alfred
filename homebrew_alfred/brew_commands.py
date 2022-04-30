#!/usr/local/opt/python@3.10/bin/python3
import json
import os
import sys
# import sys

# yes, you can use ~ in this string.
homebrew_icon_path = '~/config/scripts/alfred/homebrew-search/homebrew.png'

homebrew_package_commands: list[str] = [
    'install',
    'upgrade',
    'uninstall',
    'uninstall --zap',
    'home',
    # 'services',
    'info',
]

brew_services_subcommands = ['start', 'stop', 'restart', 'run', 'kill', 'info']

homebrew_package_commands.extend(
    ['services ' + x for x in brew_services_subcommands])


def generate_alfred_script_filter_json_for_failure(reason: str):
    """
    Generates a JSON string that can be used to populate the
    Alfred Script Filter for a failure.

    Args:
        reason: The reason for the failure.

    Returns:
        A JSON string that can be used to populate the Alfred Script Filter.
    """
    return {
        'items': [{
            'valid': False,
            'uid': 'error',
            'title': 'Error',
            'arg': 'error',
            'subtitle': reason,
            'autocomplete': 'error',
            'icon': {
                'path': homebrew_icon_path
            }
        }]
    }


def generate_alfred_script_filter_json(
        package_name: str,
        package_commands: list[str] = homebrew_package_commands,
        package_commands_prefix: str = 'brew ') -> dict:
    """
    Generates a JSON string that can be used to populate the
    Alfred Script Filter.

    Args:
        package_name: The name of the package to generate the JSON for.
        package_commands: The list of commands to generate the JSON for.
        package_commands_prefix: The prefix to use for the package commands.

    Returns:
        A JSON string that can be used to populate the Alfred Script Filter.
    """
    package_commands_json = []
    for package_command in package_commands:
        brew_command_str = package_commands_prefix + package_command + ' ' + package_name
        package_commands_json.append({
            'uid': package_command,
            'title': package_command,
            'arg': package_command,
            'subtitle': brew_command_str,
            'autocomplete': brew_command_str,
            'icon': {
                'path': homebrew_icon_path
            }
        })
    return {'items': package_commands_json}


def test_generate_alfred_script_filter_json():
    """
    Tests the generate_alfred_script_filter_json function.
    """
    package_name = 'git'
    package_commands = homebrew_package_commands
    package_commands_prefix = 'brew '
    package_commands_json = generate_alfred_script_filter_json(
        package_name, package_commands, package_commands_prefix)
    print(json.dumps(package_commands_json, indent=4))


def main() -> None:
    """
    Main function.
    """
    package = os.getenv('package', '')
    if not package:
        d = generate_alfred_script_filter_json_for_failure(
            'No package specified.')
        # sys.exit()
    else:
        package_commands_prefix = 'brew '
        if len(args := sys.argv) == 1:
            package_commands = homebrew_package_commands
        else:
            arg = args[1].lower()
            package_commands = [
                x for x in homebrew_package_commands if arg in x
            ]
        package_commands_json = generate_alfred_script_filter_json(
            package, package_commands, package_commands_prefix)
        d = package_commands_json
    print(json.dumps(d, indent=4))


if __name__ == '__main__':
    main()