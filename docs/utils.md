# Utilities

The `utils` folder contains all the helper functions and classes used in the project.
Those are mainly used to abstract away the complexity of the underlying libraries and to provide a consistent interface.
Additionally, this reduces the overall redundancy of the code.

## Abstract Classes

Abstract classes are used to provide a consistent interface for the different libraries used in the project.

One example is the abstraction of each individual use case class.

<!-- prettier-ignore -->
::: aswe.utils.abstract
    options:
        heading_level: 3

## Date

The `date` module contains helper functions to work with dates and times.

<!-- prettier-ignore -->
::: aswe.utils.date
    options:
        heading_level: 3

## Error

This project even includes custom error classes for raising exceptions specific to this project.

<!-- prettier-ignore -->
::: aswe.utils.error
    options:
        heading_level: 3

## Requests

<!-- prettier-ignore -->
::: aswe.utils.request
    options:
        heading_level: 3

## Shell

This module contains helper functions to execute shell commands. For example, to clear the terminal.

<!-- prettier-ignore -->
::: aswe.utils.shell
    options:
        heading_level: 3

## Text

<!-- prettier-ignore -->
::: aswe.utils.text
    options:
        heading_level: 3
