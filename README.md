# homebrew-alfred
Python scripts for searching and displaying Homebrew package metadata, made for Alfred.

- [homebrew-alfred](#homebrew-alfred)
	- [Features](#features)
		- [The Alfred workflow](#the-alfred-workflow)
	- [Install](#install)
	- [Usage](#usage)
		- [Alfred workflow usage](#alfred-workflow-usage)
		- [Command line usage](#command-line-usage)
	- [Demo](#demo)
	- [Project layout](#project-layout)
		- [Core](#core)
		- [Config and utility](#config-and-utility)
		- [The callers](#the-callers)
	- [FAQ](#faq)
		- [How do the scripts search for formulae and casks?](#how-do-the-scripts-search-for-formulae-and-casks)
		- [How do you make these scripts work with Alfred?](#how-do-you-make-these-scripts-work-with-alfred)

## Features
- Fast: Implemented in pure python, searches across 6000+ core formulae and 4000+ casks package metadata and installation statistics in 4 files (~18 MB in total), without noticeable delay.
- Functions are modular and documented in detail.
### The Alfred workflow
- Search-as-you-type: See the [demo](#demo) below.
- Displays rich information about packages: name, homepage URL, formula and cask definition, version, description, and installation statistics.
  

## Install
First, clone this repo:
```
$ git clone https://github.com/tddschn/homebrew-alfred.git
```
Then download the [Alfred workflow](https://github.com/tddschn/homebrew-alfred/releases/download/0.1.0/homebrew.search.alfredworkflow), open it, and modify the scripts paths to the ones in the clone repository.

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

## Demo


https://user-images.githubusercontent.com/45612704/163528051-3e3afe9f-dc06-4ebe-828e-b95b49007159.mov


## Project layout

### Core
Most of the logic is in [common.py](homebrew_alfred/common.py)

### Config and utility
- [config.py](homebrew_alfred/config.py) Sets the URL to the APIs and the paths to store the downloaded JSON files.
- [download_jsons.py](homebrew_alfred/download_jsons.py) A utility script that downloads Homebrew formulae and casks JSON metadata from the [Homebrew API](https://formulae.brew.sh/docs/api/)

### The callers

The default keyboard triggers for the scripts and what they do:
- <kbd>bbf</kbd> [formula.py](homebrew_alfred/formula.py) Searches Homebrew core formulae.
	- <kbd>bbfw</kbd> [formula_word.py](homebrew_alfred/formula_word.py): Searches only whole words, like `grep -w`.
- <kbd>bbc</kbd> [cask.py](homebrew_alfred/cask.py) Searches Homebrew core casks.
	- <kbd>bbcw</kbd> [cask_word.py](homebrew_alfred/cask_word.py): Searches only whole words.
- <kbd>bb</kbd> [formula_and_cask.py](homebrew_alfred/formula_and_cask.py) Searches Homebrew core formulae and casks.
	- <kbd>bbw</kbd> [formula_and_cask_word.py](homebrew_alfred/formula_and_cask_word.py): Searches only whole words.


## FAQ

### How do the scripts search for formulae and casks?

The scripts take in a query term and filter the downloaded JSON metadata on these fields: `token`, `name`, `desc`.
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

