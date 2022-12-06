# Utilities

The `utils` folder contains all the helper functions and classes used in the project.
Those are mainly used to abstract away the complexity of the underlying libraries and to provide a consistent interface.
Additionally, this reduces the overall redundancy of the code.

## Abstract Classes

Abstract classes are used to provide a consistent interface for the different libraries used in the project.

One example is the abstraction of each individual use case class.

::: aswe.utils.abstract

## Date

The `date` module contains helper functions to work with dates and times.

::: aswe.utils.date

## Error

This project even includes custom error classes for raising exceptions specific to this project.

::: aswe.utils.error

## Requests

::: aswe.utils.request

## Shell

This module contains helper functions to execute shell commands. For example, to clear the terminal.

::: aswe.utils.shell
