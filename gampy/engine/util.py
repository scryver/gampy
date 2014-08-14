__author__ = 'michiel'


def remove_empty_strings(data):
    result = []

    for i in range(len(data)):
        if data[i] != '':
            result.append(data[i])

    return result