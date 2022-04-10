def count_lines_in_file(path):
    lines = 0
    _file = open(path, 'r')

    for line in _file:
        lines += 1

    _file.close()
    return lines


def count_words_in_line(path):
    _file = open(path, 'r')
    _line = _file.readline()
    _line = _line.replace(' ', '')
    _line = _line.strip()
    _file.close()
    return len(_line)
