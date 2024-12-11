from typing import List, Dict, Any


def group_by(array: List[Dict[str, Any]], key: str) -> Dict[Any, List[Dict[str, Any]]]:
    """
    按照指定键对数组中的元素进行分组。

    参数:
        array (List[Dict[str, Any]]): 要分组的字典列表。
        key (str): 用于分组的键。

    返回:
        Dict[Any, List[Dict[str, Any]]]: 按键值分组后的字典。
    """
    grouped_dict = {}
    for item in array:
        group_key = item.get(key)
        if group_key is None:
            continue  # 可以根据需求处理缺失键值的情况
        if group_key not in grouped_dict:
            grouped_dict[group_key] = []
        grouped_dict[group_key].append(item)
    return grouped_dict
