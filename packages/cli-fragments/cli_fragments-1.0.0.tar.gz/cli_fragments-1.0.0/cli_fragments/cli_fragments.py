from typing import Callable


def error(text: str):
    """Prints an error statement."""

    line = "\033[31m[✕] " + text + "\033[m"
    line = "\n" + line

    print(line)


def success(text: str):
    """Prints a success statement."""

    line = "\033[32m[✓] " + text + "\033[m"
    line = "\n" + line

    print(line)


def warning(text: str):
    """Prints a warning statement."""

    line = "\033[33m[!] " + text + "\033[m"
    line = "\n" + line

    print(line)


def text(text: str):
    """Prints a text statement."""

    line = text
    line = "\n" + line

    print(line)


def debug(text: str):
    """Prints a notice statement."""

    line = "[#] " + text
    line = "\n" + line

    print(line)


def notice(text: str):
    """Prints a notice statement."""

    line = "\033[34m[~] " + text + "\033[m"
    line = "\n" + line

    print(line)


def ask(question: str, default, validator=Callable[[str], str]):
    """Asks to the user an input and validates the value with the given validator function."""

    line = "\n[?] " + question

    if default:
        line += " [" + str(default) + "]"

    line += ": "

    while True:
        value = str(input(line))

        try:
            validator(value)
            return value
        except ValueError as e:
            error(str(e))
