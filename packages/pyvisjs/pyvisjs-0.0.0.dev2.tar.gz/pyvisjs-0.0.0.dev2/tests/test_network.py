import pytest
from unittest.mock import patch
from pyvisjs import Network

def test_network_init():
    # init
    DEFAULT_WIDTH = "600px"
    DEFAULT_HEIGHT = "400px"

    # mock


    # call
    n = Network("Network1")
    
    # assert
    assert n.name == "Network1"
    assert n.width == DEFAULT_WIDTH
    assert n.height == DEFAULT_HEIGHT
    assert n.env is not None
    assert n.data == {"nodes": [], "edges": []}

@patch('pyvisjs.network.open_file')
@patch('pyvisjs.network.save_file')
@patch('pyvisjs.network.Environment')
def test_render_template_with_all_default_values(mock_Environment, mock_save_file, mock_open_file):
    # init
    RENDER_RESULT = "<html>template</html>"
    DEFAULT_TEMPLATE_FILENAME = "basic.html"
    
    # mock
    mock_get_template = mock_Environment.return_value.get_template
    mock_render = mock_get_template.return_value.render
    mock_render.return_value = RENDER_RESULT

    # call
    network = Network("Test Network")
    html_output = network.render_template() # <--------------------

    # assert
    mock_get_template.assert_called_once_with(DEFAULT_TEMPLATE_FILENAME)
    mock_save_file.assert_not_called()
    mock_open_file.assert_not_called()
    assert html_output == RENDER_RESULT


@patch('pyvisjs.network.open_file')
@patch('pyvisjs.network.save_file')
@patch('pyvisjs.network.Environment')
def test_render_template_with_open_in_browser(mock_Environment, mock_save_file, mock_open_file):
    # init
    RENDER_RESULT = "<html>template</html>"
    DEFAULT_TEMPLATE_FILENAME = "basic.html"
    DEFAULT_OUTPUT_FILENAME = "default.html"
    
    # mock
    mock_get_template = mock_Environment.return_value.get_template
    mock_render = mock_get_template.return_value.render
    mock_render.return_value = RENDER_RESULT
    mock_save_file.return_value = DEFAULT_OUTPUT_FILENAME

    # call
    network = Network("Test Network")
    html_output = network.render_template(open_in_browser=True) # <--------------------

    #assert
    mock_get_template.assert_called_once_with(DEFAULT_TEMPLATE_FILENAME)
    mock_save_file.assert_called_once_with(DEFAULT_OUTPUT_FILENAME, RENDER_RESULT)
    mock_open_file.assert_called_once_with(DEFAULT_OUTPUT_FILENAME)
    assert html_output == RENDER_RESULT


@patch('pyvisjs.network.open_file')
@patch('pyvisjs.network.save_file')
@patch('pyvisjs.network.Environment')
def test_render_template_with_save_to_output(mock_Environment, mock_save_file, mock_open_file):
    # init
    RENDER_RESULT = "<html>template</html>"
    DEFAULT_TEMPLATE_FILENAME = "basic.html"
    DEFAULT_OUTPUT_FILENAME = "default.html"
    
    # mock
    mock_get_template = mock_Environment.return_value.get_template
    mock_render = mock_get_template.return_value.render
    mock_render.return_value = RENDER_RESULT

    # call
    network = Network("Test Network")
    html_output = network.render_template(save_to_output=True) # <--------------------

    #assert
    mock_get_template.assert_called_once_with(DEFAULT_TEMPLATE_FILENAME)
    mock_save_file.assert_called_once_with(DEFAULT_OUTPUT_FILENAME, RENDER_RESULT)
    mock_open_file.assert_not_called()
    assert html_output == RENDER_RESULT


@patch('pyvisjs.network.open_file')
@patch('pyvisjs.network.save_file')
@patch('pyvisjs.network.Environment')
def test_render_template_with_open_and_save_no_defaults(mock_Environment, mock_save_file, mock_open_file):
    # init
    RENDER_RESULT = "<html>template</html>"
    CUSTOM_TEMPLATE_FILENAME = "custom_template.html"
    CUSTOM_OUTPUT_FILENAME = "custom_output.html"
    
    # mock
    mock_get_template = mock_Environment.return_value.get_template
    mock_render = mock_get_template.return_value.render
    mock_render.return_value = RENDER_RESULT
    mock_save_file.return_value = CUSTOM_OUTPUT_FILENAME

    # call
    network = Network("Test Network")
    html_output = network.render_template( # <--------------------
        open_in_browser=True, 
        save_to_output=True, 
        output_filename=CUSTOM_OUTPUT_FILENAME, 
        template_filename=CUSTOM_TEMPLATE_FILENAME)

    #assert
    mock_get_template.assert_called_once_with(CUSTOM_TEMPLATE_FILENAME)
    mock_save_file.assert_called_once_with(CUSTOM_OUTPUT_FILENAME, RENDER_RESULT)
    mock_open_file.assert_called_once_with(CUSTOM_OUTPUT_FILENAME)
    assert html_output == RENDER_RESULT