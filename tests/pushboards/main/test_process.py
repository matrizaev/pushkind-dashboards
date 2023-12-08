from pushboards.main.upload.process import update_value_list_dict


def test_update_value_list_dict():
    value_list_dict = {
        "key1": ["value1", "value2"],
        "key2": ["value3", "value4"],
    }
    update_value_list_dict(value_list_dict, "key1", "value5")
    assert value_list_dict == {
        "key1": ["value1", "value2", "value5"],
        "key2": ["value3", "value4"],
    }
    update_value_list_dict(value_list_dict, "key1", "value6")
    assert value_list_dict == {
        "key1": ["value1", "value2", "value5", "value6"],
        "key2": ["value3", "value4"],
    }
    update_value_list_dict(value_list_dict, "key3", "value7")
    assert value_list_dict == {
        "key1": ["value1", "value2", "value5", "value6"],
        "key2": ["value3", "value4", ""],
        "key3": ["", "", "", "value7"],
    }
