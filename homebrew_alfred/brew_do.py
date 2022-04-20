#!/usr/local/opt/python@3.10/bin/python3
"""
Do things with Homebrew with the passed in $command and $package
"""

import json
import subprocess, os
import sys
from brew_commands import generate_alfred_script_filter_json_for_failure, generate_alfred_script_filter_json, brew_services_subcommands

brew_env = os.environ
brew_env |= dict( HOMEBREW_NO_INSTALL_CLEANUP='1', HOMEBREW_NO_AUTO_UPDATE='1', HOMEBREW_NO_ANALYTICS='1')
brew_env['PATH'] = '/opt/homebrew/bin:/usr/local/bin:{}'.format(os.getenv('PATH'))


def run_brew_command(command: str, package: str) -> subprocess.CompletedProcess:
    """
    Run the passed in command with the passed in package.

    Args:
        command: The command to run.
        package: The package to run the command with.

    Returns:
        The output of the command and the return code.
    """
    # if command == 'service info':
    #     command_to_run = ['brew', 'info', '--json', package]
    # else:
    #     # split the command, in case command == 'services ...'
    command_to_run = ['brew', *command.split(), package]
    print(f'Running command: {" ".join(command_to_run)}')
    proc = subprocess.run(command_to_run, capture_output=True, env=brew_env)
    return proc


def main() -> None:
    package = os.getenv('package', '')  # guranteed to be non-empty
    command = os.getenv('command', '')
    if command:
        match command:
            # case 'services':
            #     d = generate_alfred_script_filter_json(package, brew_services_subcommands, 'brew services ')
            #     print(json.dumps(d, indent=4))
            case 'info':
                proc = run_brew_command(command, package)
                print(proc.stdout.decode()) # print it to pass it to the next action
            case _:
                proc = run_brew_command(command, package)
                error = proc.returncode
                if error:
                    print(f'❌ brew {command} {package} failed.')
                    print()
                    print(proc.stderr.decode())
                    # d = generate_alfred_script_filter_json_for_failure(proc.stderr.decode('utf-8'))
                    # print(json.dumps(d, indent=4))
                else:
                    print(f'✅ brew {command} {package} succeeded.')
                    print()
                    print(proc.stdout.decode())
    else:
        print('❌ No command passed in.', file=sys.stderr)
        d = generate_alfred_script_filter_json_for_failure('No command passed in.')
        print(json.dumps(d, indent=4))

if __name__ == '__main__':
    main()