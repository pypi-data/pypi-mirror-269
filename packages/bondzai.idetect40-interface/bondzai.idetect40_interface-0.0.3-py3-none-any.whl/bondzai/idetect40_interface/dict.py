from typing import Any

def get_dict_update(previous_dict: dict, new_dict: dict) -> dict:
    """Return a dict with only values that have be updated between the two dicts

    Args:
        previous_dict (dict): initial dict
        new_dict (dict): updated dict

    Returns:
        update_dict: dict with only updates
    """
    update_dict = {}
    for key, value in new_dict.items():
        if isinstance(value, dict):
            _update_dict = get_dict_update(previous_dict[key], value)
            if _update_dict:
                update_dict[key] = _update_dict
        else:
            if key not in previous_dict.keys() or value != previous_dict[key]:
                update_dict[key] = value
    return update_dict

def get_dict_value(d: dict, key_list: list) -> Any:
    """Get dict value from a list of nested keys

    Args:
        d (dict): dict
        key_list (list): list of nested keys

    Returns:
        value: any possible value
    """
    if len(key_list) > 0 and d is not None:
        if isinstance(d, dict): 
            sub_key_list = key_list[1:]
            first_key = key_list[0]
            value = get_dict_value(d.get(first_key, None), sub_key_list)
        else:
            value = None
    else:
        value = d
    return value

def set_dict_value(d: dict, key_list: list, value: Any):
    """Set value for a dict by giving list of nested keys

    Args:
        d (dict): dict
        key_list (list): list of nested keys
        value: any possible value
    """
    sub_key_list = key_list[1:]
    first_key = key_list[0]
    if len(sub_key_list) > 0 and d is not None:
        if first_key not in d.keys() or not isinstance(d[first_key], dict):
            d[first_key] = {}
        set_dict_value(d[first_key], sub_key_list, value)

    else:
        d[first_key] = value

def check_dict_equity(d: dict, d_ref: dict) -> bool:
    """Compare a dict with a reference, check the contents are the same
    Args:
        d (dict): dict to be tested
        d_ref (dict): reference dict
    Returns: 
        bool: True if the dicts are equal else False
    """
    if len(d) != len(d_ref):
        return False
    is_equal = True
    for key, value in d_ref.items():
        if isinstance(value, dict):
            is_equal = is_equal and check_dict_equity(d[key], value)
        else:
            is_equal = is_equal and (key in d.keys() and d[key] == value)
    return is_equal