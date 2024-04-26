# pycntrparser

## Description

`pycntrparser` is a syntax checker designed for [CNTR transcriptions](https://github.com/Center-for-New-Testament-Restoration/transcriptions), utilizing ANTLR4 for parsing and validation.

## Installation

You can easily install `pycntrparser` using pip:

```bash
pip install pycntrparser
```

## Usage

To check for syntax errors in CNTR transcriptions, use the following command:

```bash
cntr-check "transcriptions/class 1" "transcriptions/class 2"
```

Replace the paths within quotes with the actual paths to the CNTR transcriptions you want to check. The tool will then validate the syntax and report any errors it finds.

## Upgrade

To upgrade to the latest version of `pycntrparser`, use the following command:

```bash
pip install --upgrade pycntrparser
```

This will ensure that you have the latest features and bug fixes.
