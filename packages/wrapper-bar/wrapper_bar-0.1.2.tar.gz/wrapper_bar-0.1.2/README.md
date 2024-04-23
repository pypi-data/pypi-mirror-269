# Overview

`Wrapper-Bar` is a python module to help wrap commands with the progress bar. `Wrapper-Bar` helps in wrapping shell commands, or even python scripts with a progress bar and ETA.

## Badges

![PyPI - Version](https://img.shields.io/pypi/v/wrapper-bar)
![PyPI - Status](https://img.shields.io/pypi/status/wrapper-bar)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wrapper-bar)
![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/wrapper-bar)
![PyPI - License](https://img.shields.io/pypi/l/wrapper-bar)

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Uninstall](#uninstall)

## Installation

To install `wrapper-bar`, use pip.

```bash
pip install wrapper-bar==0.1.2
```

## Usage

- Import the Wrapper class.

  ```python
  >>> from wrapper_bar.wrapper import Wrapper
  ```

- Initialize the Wrapper Class.

  ```python
  >>> wrapControl = Wrapper(*params) # for parameters, check docstring.
  ```

- Docstring

  ```bash
  # to check docstring, in terminal/CMD, run:
  $ pydoc wrapper_bar.wrapper.Wrapper
  ```

- Methods

  - `decoy`

    ```python
    >>> wrapControl.decoy(*params) # parameters are in the docstring.
    # decoy is for creating empty progressbar.
    ```
  
  - `shellWrapper`

    ```python
    >>> wrapControl.shellWrapper(*params) # parameters are in the docstring.
    # shellWrapper can wrap list of shell commands across the progressbar.
    ```

  - `pyWrapper`

    ```python
    >>> wrapControl.pyWrapper(*params) # parameters are in the docstring.
    # pyWrapper can wrap list of python scripts across the progressbar.
    ```
  
  - `pyShellWrapper`
  
    ```python
    >>> wrapControl.pyShellWrapper(*params) # parametes are in the docstring.
    # pyShellWrapper can wrap inline python code across a progressbar.
    ```

## Uninstall

To uninstall `wrapper-bar`, use pip.

```bash
pip uninstall wrapper-bar
```
