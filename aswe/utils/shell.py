import os
from sys import platform


def clear_shell() -> None:
    """Clears any previous text in the shell"""
    if platform in ["linux", "linux2", "darwin"]:
        os.system("clear")
    elif platform == "win32":
        os.system("cls")
