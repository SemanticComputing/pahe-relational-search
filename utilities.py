import csv

def binary_search(values, target):
    low = 0
    high = len(values) - 1
    while low <= high:
        mid = (high + low) // 2
        if values[mid] == target:
            return mid
        elif target < values[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return -1

# returns the index before the first?
def find_index(name, list):
    index = binary_search(list, name)
    if index < 0:
        return index
    else:
        while list[index] > name and index > 0:
            index = index - 1
    return index

def make_list(csv):
    names = []
    uris = []
    for row in csv:
        names.append(row[0])
        uris.append(row[1])
    return names, uris