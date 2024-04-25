from pyvisjs import Edge

def test_edge_init_default():
    # init
    START_ID = 1
    END_ID = 2

    # mock

    # call
    e = Edge(START_ID, END_ID)
    
    # assert
    assert e.start == START_ID
    assert e.end == END_ID


def test_edge_to_dict():
    # init
    START_ID = 1
    END_ID = 2
    EDGE_DICT = {
            "from": START_ID,
            "to": END_ID,
        }

    # mock

    # call
    e = Edge(START_ID, END_ID)
    
    # assert
    assert e.to_dict() == EDGE_DICT

def test_edge_to_json():
    # init
    START_ID = 1
    END_ID = 2
    EDGE_JSON = f"""{{"from": {START_ID}, "to": {END_ID}}}"""

    # mock

    # call
    e = Edge(START_ID, END_ID)
    
    # assert
    assert e.to_json() == EDGE_JSON