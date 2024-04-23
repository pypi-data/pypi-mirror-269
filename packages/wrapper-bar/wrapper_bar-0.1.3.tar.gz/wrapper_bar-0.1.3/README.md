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
pip install wrapper-bar==0.1.3
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

    Working of `pyShellWrapper`:

    - `pyShellWrapper` takes two compulsory parameters => `pythoncodes` and `dependencies`. To explain them, let us see below

      ```python
      # pythoncodes and dependencies can have any python code except 
      # return, print or yield statements.

      # let us take this as an example:
      >>> pythoncodes = ["""a = b+c""", """b=c+d"""]

      # Now for the above python codes, values of 'b', 'c' and 'd' 
      # are a dependency. Therefore
      
      >>> dependencies = ["""b=10""", """c=10\nd=20\n"""] 
      
      # try to keep one statement only inside """...""", 
      # but if need be, then you can also put multiple 
      # statements followed by '\n'. Like """c=10\nd=20\n"""

      # and now we will execute them with the loading bar as the 
      # front.
      
      >>> from wrapper_bar.wrapper import Wrapper
      >>> w = Wrapper("Loading:")
      >>> w.pyShellWrapper(pythoncodes, dependencies) # this will output the following:
      Loading: |▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓|Time: 0:00:10
      
      # To fetch the outputs, we will use a property 'pyShellWrapperResults' 
      # defined under the `Wrapper Class`

      >>> a = w.pyShellWrapperResults['a'] # this will be 20
      >>> b = w.pyShellWrapperResults['b'] # this will be 30
      ```

## Uninstall

To uninstall `wrapper-bar`, use pip.

```bash
pip uninstall wrapper-bar
```
