from pyvisjs import Node

def test_node_init_default():
    # init
    NODE_ID = 1

    # mock

    # call
    n = Node(NODE_ID)
    
    # assert
    assert n.id == NODE_ID

def test_node_init_positional_params():
    # init
    NODE_ID = 1
    NODE_LABEL = "label"
    NODE_COLOR = "lime"
    NODE_SHAPE = "circle"
    NODE_SIZE = 50

    # mock

    # call
    n = Node(NODE_ID, NODE_LABEL, NODE_COLOR, NODE_SHAPE, NODE_SIZE)
    
    # assert
    assert (n.id, n.label, n.color, n.shape, n.size) == (NODE_ID, NODE_LABEL, NODE_COLOR, NODE_SHAPE, NODE_SIZE)

def test_node_to_dict():
    # init
    NODE_ID = 1
    NODE_LABEL = "label"
    NODE_COLOR = "lime"
    NODE_SHAPE = "circle"
    NODE_SIZE = 50
    NODE_DICT = {
            "id": NODE_ID,
            "label": NODE_LABEL,
            "color": NODE_COLOR,
            "shape": NODE_SHAPE,
            "size": NODE_SIZE,
        }

    # mock

    # call
    n = Node(NODE_ID, NODE_LABEL, NODE_COLOR, NODE_SHAPE, NODE_SIZE)
    
    # assert
    assert n.to_dict() == NODE_DICT

def test_node_to_json():
    # init
    NODE_ID = 1
    NODE_LABEL = "label1"
    NODE_COLOR = "lime"
    NODE_SHAPE = "circle"
    NODE_SIZE = 50
    NODE_JSON = f"""{{"id": {NODE_ID}, "label": "{NODE_LABEL}", "color": "{NODE_COLOR}", "shape": "{NODE_SHAPE}", "size": {NODE_SIZE}}}"""

    # mock

    # call
    n = Node(NODE_ID, NODE_LABEL, NODE_COLOR, NODE_SHAPE, NODE_SIZE)
    
    # assert
    assert n.to_json() == NODE_JSON