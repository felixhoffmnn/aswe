import os
from unittest.mock import MagicMock, call, patch

from pytest_mock import MockFixture

from aswe.utils.shell import clear_shell, get_int, print_options


def test_clear_shell(mocker: MockFixture) -> None:
    """Test `clear_shell`"""
    # * spy on system method
    system_import_path = "aswe.utils.shell.os.system"
    mocker.patch(system_import_path, new=lambda x: None)
    spy_system = mocker.spy(os, "system")

    platform_import_path = "aswe.utils.shell.platform"

    # * platform == "" (invalid platform)
    mocker.patch(platform_import_path, new="")
    clear_shell()
    spy_system.assert_not_called()
    spy_system.reset_mock()

    # * platform == "linux"
    mocker.patch(platform_import_path, new="linux")
    clear_shell()
    spy_system.assert_called_once_with("clear")
    spy_system.reset_mock()

    # * plaform == "linux2"
    mocker.patch(platform_import_path, new="linux2")
    clear_shell()
    spy_system.assert_called_once_with("clear")
    spy_system.reset_mock()

    # * plaform == "darwin"
    mocker.patch(platform_import_path, new="darwin")
    clear_shell()
    spy_system.assert_called_once_with("clear")
    spy_system.reset_mock()

    # * plaform == "win32"
    mocker.patch(platform_import_path, new="win32")
    clear_shell()
    spy_system.assert_called_once_with("cls")
    spy_system.reset_mock()


@patch("builtins.print")
def test_print_options(mocked_print: MagicMock) -> None:
    """Test `aswe.utils.shell.print_options`

    Parameters
    ----------
    mocked_print : MagicMock
        Mock of builtin `print` function
    """
    # * test empty options
    print_options([])
    assert mocked_print.mock_calls == [call()]
    mocked_print.reset_mock()

    # * test valid input
    print_options(["test_option_1", "test_option_2"])
    assert mocked_print.mock_calls == [call(), call("1: test_option_1"), call("2: test_option_2")]


@patch("builtins.print")
@patch("builtins.input")
def test_get_int(mocked_input: MagicMock, mocked_print: MagicMock) -> None:
    """Test `aswe.utils.shell.get_int`

    Parameters
    ----------
    mocked_input : MagicMock
        Mock of builtin `input` method
    mocked_print : MagicMock
        Mock of builtin `print` method

    Note
    ----------
    Hard to test invalid input since endless loop will be triggered. Therefore left out.
    """
    get_int([])
    assert mocked_print.mock_calls == [call()]
    mocked_print.reset_mock()

    mocked_input.return_value = 10
    assert get_int(["test_option_1"], 10) == 10
