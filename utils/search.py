def search_list_of_dicts(list_of_dicts, key, value):
    list_of_dicts = sorted(list_of_dicts, key=lambda k: k[key])
    low = 0
    high = len(list_of_dicts) - 1
    while low <= high:
        mid = (low + high) // 2
        if list_of_dicts[mid][key] > value:
            high = mid - 1
        elif list_of_dicts[mid][key] < value:
            low = mid + 1
        else:
            return list_of_dicts[mid]
    return None
