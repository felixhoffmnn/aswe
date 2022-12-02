from pytest_mock import MockFixture

from aswe.utils.shell import clear_shell, os  # type: ignore


def test_clear_shell(mocker: MockFixture) -> None:
    """Test `clear_shell`"""
    # ? spy on system method
    system_import_path = "aswe.utils.shell.os.system"
    mocker.patch(system_import_path, new=lambda x: None)
    spy_system = mocker.spy(os, "system")

    platform_import_path = "aswe.utils.shell.platform"

    # ? platform == "" (invalid platform)
    mocker.patch(platform_import_path, new="")
    clear_shell()
    spy_system.assert_not_called()
    spy_system.reset_mock()

    # ? platform == "linux"
    mocker.patch(platform_import_path, new="linux")
    clear_shell()
    spy_system.assert_called_once_with("clear")
    spy_system.reset_mock()

    # ? plaform == "linux2"
    mocker.patch(platform_import_path, new="linux2")
    clear_shell()
    spy_system.assert_called_once_with("clear")
    spy_system.reset_mock()

    # ? plaform == "darwin"
    mocker.patch(platform_import_path, new="darwin")
    clear_shell()
    spy_system.assert_called_once_with("clear")
    spy_system.reset_mock()

    # ? plaform == "win32"
    mocker.patch(platform_import_path, new="win32")
    clear_shell()
    spy_system.assert_called_once_with("cls")
    spy_system.reset_mock()
