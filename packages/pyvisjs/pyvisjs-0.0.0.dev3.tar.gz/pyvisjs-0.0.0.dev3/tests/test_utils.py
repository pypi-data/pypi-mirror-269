import os
import platform
from pyvisjs.utils import save_file, open_file
from unittest.mock import patch


@patch("os.makedirs")
@patch("builtins.open")
@patch("os.getcwd")
def test_save_file_with_file_name(mock_getcwd, mock_open, mock_makedirs):
    # init
    FULL_PATH = os.path.join("working_dir", "output.html")
    DIR_PATH, _ = os.path.split(FULL_PATH)

    # mock
    mock_getcwd.return_value = "working_dir"
    mock_write = mock_open.return_value.__enter__().write

    # call
    file_result = save_file("output.html", "<html>hello</html>") # <------------------

    # assert
    mock_getcwd.assert_called_once()
    mock_makedirs.assert_called_once_with(DIR_PATH, exist_ok=True)
    mock_open.assert_called_once_with(FULL_PATH, "w")
    mock_write.assert_called_once_with("<html>hello</html>")
    assert file_result == FULL_PATH


@patch("os.makedirs")
@patch("builtins.open")
@patch("os.getcwd")
def test_save_file_with_relative_path(mock_getcwd, mock_open, mock_makedirs):
    # init
    REL_PATH = os.path.join("relative_dir", "output.html")
    FULL_PATH = os.path.join("working_dir", REL_PATH)
    DIR_PATH, _ = os.path.split(FULL_PATH)

    # mock
    mock_getcwd.return_value = "working_dir"
    mock_write = mock_open.return_value.__enter__().write

    # call
    file_result = save_file(REL_PATH, "<html>hello</html>") # <------------------

    # assert
    mock_getcwd.assert_called_once()
    mock_makedirs.assert_called_once_with(DIR_PATH, exist_ok=True)
    mock_open.assert_called_once_with(FULL_PATH, "w")
    mock_write.assert_called_once_with("<html>hello</html>")
    assert file_result == FULL_PATH


@patch("os.makedirs")
@patch("builtins.open")
@patch("os.getcwd")
def test_save_file_with_absolute_path(mock_getcwd, mock_open, mock_makedirs):
    # init
    if platform.system() == "Windows":
        FULL_PATH = os.path.join("c:" + os.sep, "relative_dir", "output1.html")
    elif platform.system() == "Linux":
        FULL_PATH = os.path.join(os.sep, "relative_dir", "output1.html")
        
    DIR_PATH, _ = os.path.split(FULL_PATH)

    # mock
    mock_write = mock_open.return_value.__enter__().write

    # call
    file_result = save_file(FULL_PATH, "<html>hello</html>") # <------------------

    # assert
    mock_getcwd.assert_not_called()
    mock_makedirs.assert_called_once_with(DIR_PATH, exist_ok=True)
    mock_open.assert_called_once_with(FULL_PATH, "w")
    mock_write.assert_called_once_with("<html>hello</html>")
    assert file_result == FULL_PATH
