# homebrew-alfred
Python scripts for searching and displaying Homebrew package metadata, and executing common brew commands, made for Alfred Workflow.

- [homebrew-alfred](#homebrew-alfred)
  - [Features](#features)
    - [The Alfred workflow](#the-alfred-workflow)
  - [Demo](#demo)
  - [Install](#install)
  - [Usage](#usage)
    - [Alfred workflow usage](#alfred-workflow-usage)
    - [Command line usage](#command-line-usage)
  - [Project layout](#project-layout)
    - [Core](#core)
    - [Config and utility](#config-and-utility)
    - [The callers (Alfred Workflow scripts filter entry points)](#the-callers-alfred-workflow-scripts-filter-entry-points)
    - [Secondary script filter scripts](#secondary-script-filter-scripts)
    - [Command runners](#command-runners)
  - [FAQ](#faq)
    - [How do the scripts search for formulae and casks?](#how-do-the-scripts-search-for-formulae-and-casks)
    - [How do you make these scripts work with Alfred?](#how-do-you-make-these-scripts-work-with-alfred)

## Features
- Fast filtering of packages: Implemented in pure python, searches across 6000+ core formulae and 4000+ casks package metadata and installation statistics in 4 files (~18 MB in total), without noticeable delay.
- Functions are modular and documented in detail.
### The Alfred workflow
- Search-as-you-type: See the [demo](#demo) below.
- Displays rich information about packages: name, homepage URL, formula and cask definition, version, description, and installation statistics.
- Run brew command on selected packages. Supported commands: `['install', 'upgrade', 'uninstall', 'home', 'info', 'services']
  

## Demo




https://user-images.githubusercontent.com/45612704/164175793-c6899cc7-133e-47f4-86dc-37e4807897ae.mp4






## Install
First, clone this repo:
```
$ git clone https://github.com/tddschn/homebrew-alfred.git
```
Then download the [Alfred workflow](https://github.com/tddschn/homebrew-alfred/releases/download/0.1.0/homebrew.search.alfredworkflow), open it, and modify the scripts paths to the ones in the clone repository.

Depending on your local python installation, you may need to edit the shebangs of the scripts to `python3.10+`.

## Usage
### Alfred workflow usage
- Default keyword trigger for [formula_and_cask.py](homebrew_alfred/formula_and_cask.py) is `bb`.
  See [Project layout](#the-callers) for more info.
  Use `bb` if you don't know which trigger to use.
- <kbd>cmd</kbd>: Show package homepage
- <kbd>cmd</kbd> + <kbd>Enter</kbd>: Open package homepage
- <kbd>opt</kbd>: Show package name
- <kbd>cmd</kbd> + <kbd>C</kbd>: Copy the package name to be used with `brew`
- <kbd>shift</kbd>: Activate the quicklook for the formula and cask definition ruby file
- <kbd>enter</kbd>: Execute supported brew command on the selected package. See [Features](#the-alfred-workflow) for supported commands.

### Command line usage
```
$ ./formula_and_cask.py docker
# Outputs JSON formatted data that conforms to the schema (https://www.alfredapp.com/help/workflows/inputs/script-filter/json/) specified in the Alfred doc
# 
{
  "items": [
    {
      "title": "docker                        20.10.14       #38             72,922",
      "subtitle": "Pack, ship and run any application as a lightweight container",
      "quicklookurl": "/usr/local/Homebrew/Library/Taps/homebrew/homebrew-core/Formula/docker.rb",
      "arg": "docker",
      "mods": {
        "cmd": {
          "valid": true,
          "arg": "https://www.docker.com/",
          "subtitle": "https://www.docker.com/"
        },
        "alt": {
          "valid": true,
          "arg": "docker",
          "subtitle": "docker"
        },
        "ctrl": {
          "valid": true,
          "arg": "file:///usr/local/Homebrew/Library/Taps/homebrew/homebrew-core/Formula/docker.rb",
          "subtitle": "/usr/local/Homebrew/Library/Taps/homebrew/homebrew-core/Formula/docker.rb"
        }
      },
      "count": "72,922"
    },
	{
      "title": "docker-compose                2.4.1          #69             38,168",
      "subtitle": "Isolated development environments using Docker",
      "quicklookurl": "/usr/local/Homebrew/Library/Taps/homebrew/homebrew-core/Formula/docker-compose.rb",
      "arg": "docker-compose",
      "mods": {
        "cmd": {
          "valid": true,
          "arg": "https://docs.docker.com/compose/",
          "subtitle": "https://docs.docker.com/compose/"
        },
        "alt": {
          "valid": true,
          "arg": "docker-compose",
          "subtitle": "docker-compose"
        },
        "ctrl": {
          "valid": true,
          "arg": "file:///usr/local/Homebrew/Library/Taps/homebrew/homebrew-core/Formula/docker-compose.rb",
          "subtitle": "/usr/local/Homebrew/Library/Taps/homebrew/homebrew-core/Formula/docker-compose.rb"
        }
      },
      "count": "38,168"
    },
	...
}
```

```
$ package=docker ./brew_commands.py stall
# the script only outputs entries with commands where the string 'stall' is in the command.

{
    "items": [
        {
            "uid": "install",
            "title": "install",
            "arg": "install",
            "subtitle": "brew install docker",
            "autocomplete": "brew install docker",
            "icon": {
                "path": "~/config/scripts/alfred/homebrew-search/homebrew.png"
            }
        },
        {
            "uid": "uninstall",
            "title": "uninstall",
            "arg": "uninstall",
            "subtitle": "brew uninstall docker",
            "autocomplete": "brew uninstall docker",
            "icon": {
                "path": "~/config/scripts/alfred/homebrew-search/homebrew.png"
            }
        }
    ]
}
```



## Project layout

### Core
Most of the logic is in [common.py](homebrew_alfred/common.py)

### Config and utility
- [config.py](homebrew_alfred/config.py) Sets the URL to the APIs and the paths to store the downloaded JSON files.
- [download_jsons.py](homebrew_alfred/download_jsons.py) A utility script that downloads Homebrew formulae and casks JSON metadata from the [Homebrew API](https://formulae.brew.sh/docs/api/)

### The callers (Alfred Workflow scripts filter entry points)

The default keyboard triggers for the scripts and what they do:
- <kbd>bbf</kbd> [formula.py](homebrew_alfred/formula.py) Searches Homebrew core formulae.
	- <kbd>bbfw</kbd> [formula_word.py](homebrew_alfred/formula_word.py): Searches only whole words, like `grep -w`.
- <kbd>bbc</kbd> [cask.py](homebrew_alfred/cask.py) Searches Homebrew core casks.
	- <kbd>bbcw</kbd> [cask_word.py](homebrew_alfred/cask_word.py): Searches only whole words.
- <kbd>bb</kbd> [formula_and_cask.py](homebrew_alfred/formula_and_cask.py) Searches Homebrew core formulae and casks.
	- <kbd>bbw</kbd> [formula_and_cask_word.py](homebrew_alfred/formula_and_cask_word.py): Searches only whole words.
  
When the user press <kbd>enter</kbd> on the result in alfred, the package name is stored in the workflow run and used by [Secondary script filter scripts](#secondary-script-filter-scripts) and [Command runners](#command-runners).

### Secondary script filter scripts
- [brew_commands.py](homebrew_alfred/brew_commands.py) Lists brew commands and filters the outputs based on user input. Preview of the full command is shown to the user for confirmation. The command chosen is passed to the command runner.

### Command runners
- [brew_do.py](homebrew_alfred/brew_do.py) Run the selected command on the selected package, track the status code return by the command and display success or error messages to the user (via Alfred's [Large Type](https://www.alfredapp.com/help/features/large-type/).

## FAQ

### How do the scripts search for formulae and casks?

The scripts take in a query term and filter the downloaded JSON metadata on these fields: `token`, `name`, `desc`. 

See the [example cask metadata](https://formulae.brew.sh/api/cask.json) and [example cask stats metadata](https://formulae.brew.sh/api/analytics/cask-install/homebrew-cask/30d.json).

```python

# common.py
        output = [
            gen_single_item(item=item, use_token=use_token)
            for item in combined if any(
                map(lambda key: arg.lower() in search_arg_in(item, key),
                    ['name', 'token', 'desc']))
        ]
```
When using the scripts directly, i.e. not from the Alfred workflow, you have more control over what data is spit out from the scripts.

### How do you make these scripts work with Alfred?

By outputting JSON formatted data that conforms to the [schema](https://www.alfredapp.com/help/workflows/inputs/script-filter/json/) specified in the Alfred doc.

