
from bondzai.idetect40_interface.dict import check_dict_equity, get_dict_update, get_dict_value, set_dict_value


def test_compare_dict():
    ref_dict = {"a": 1, "b": 2, "c": {"d": True}}
    compared_dict = {"a": 1, "b": 2, "c": {"d": True}}
    assert check_dict_equity(ref_dict, compared_dict)
    compared_dict = {"a": 1, "b": 2, "c": {"d": False}}
    assert not check_dict_equity(ref_dict, compared_dict)
    compared_dict = {"a": 1, "b": 2, "c": 4}
    assert not check_dict_equity(ref_dict, compared_dict)
    compared_dict = {"a": 1, "b": 2}
    assert not check_dict_equity(ref_dict, compared_dict)


def test_get_update():
    previous_dict = {"a": 1, "b": 2, "c": {"d": True}}

    new_dict = {"a": 1, "b": 3, "c": {"d": True}}
    res = get_dict_update(previous_dict, new_dict)
    assert check_dict_equity(res, {"b": 3})

    new_dict = {"a": 1, "b": 3, "c": {"d": 4}}
    res = get_dict_update(previous_dict, new_dict)
    assert check_dict_equity(res, {"b": 3, "c": {"d": 4}})

    new_dict = {"b": 3, "c": {"d": 4}}
    res = get_dict_update(previous_dict, new_dict)
    assert check_dict_equity(res, {"b": 3, "c": {"d": 4}})

    new_dict = {"a": 1, "b": 2, "c": {"d": True}, "e": 5}
    res = get_dict_update(previous_dict, new_dict)
    assert check_dict_equity(res, {"e": 5})

def test_get_dict_value():
    ref_dict = {"a": 1, "b": 2, "c": {"d": True}}
    assert get_dict_value(ref_dict, ["a"]) == 1
    assert get_dict_value(ref_dict, ["c", "d"]) == True
    assert check_dict_equity(get_dict_value(ref_dict, ["c"]), {"d": True})
    assert get_dict_value(ref_dict, ["e"]) is None
    assert get_dict_value(ref_dict, ["c", "d", "e", "f"]) is None

def test_set_dict_value():
    ref_dict = {"a": 1, "b": 2, "c": {"d": True}}
    set_dict_value(ref_dict, ["a"], 7)
    assert check_dict_equity(ref_dict, {"a": 7, "b": 2, "c": {"d": True}})
    set_dict_value(ref_dict, ["c", "d"], "str")
    assert check_dict_equity(ref_dict, {"a": 7, "b": 2, "c": {"d": "str"}})
    set_dict_value(ref_dict, ["c"], {"d": True})
    assert check_dict_equity(ref_dict, {"a": 7, "b": 2, "c": {"d": True}})
    set_dict_value(ref_dict, ["c", "f"], 45)
    assert check_dict_equity(ref_dict, {"a": 7, "b": 2, "c": {"d": True, "f": 45}})
    set_dict_value(ref_dict, ["c", "f", "r"], 51)
    assert check_dict_equity(ref_dict, {"a": 7, "b": 2, "c": {"d": True, "f": {"r": 51}}})
