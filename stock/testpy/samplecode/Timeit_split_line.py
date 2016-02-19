import timeit


FILENAME = "mylargefile.csv"
DELIMITER = "\n"


def splitlines_read():
    """Read the file then split the lines from the splitlines builtin method.

    Returns:
        lines (list): List of file lines.
    """
    with open(FILENAME, "r") as file:
        lines = file.read().splitlines()
    return lines
# end splitlines_read

def split_read():
    """Read the file then split the lines.

    This method will return empty strings for blank lines (Same as the other methods).
    This method may also have an extra additional element as an empty string (compared to
    splitlines_read).

    Returns:
        lines (list): List of file lines.
    """
    with open(FILENAME, "r") as file:
        lines = file.read().split(DELIMITER)
    return lines
# end split_read

def strip_read():
    """Loop through the file and create a new list of lines and removes any "\n" by rstrip

    Returns:
        lines (list): List of file lines.
    """
    with open(FILENAME, "r") as file:
        lines = [line.rstrip(DELIMITER) for line in file]
    return lines
# end strip_readline

def strip_readlines():
    """Loop through the file's read lines and create a new list of lines and removes any "\n" by
    rstrip. ... will probably be slower than the strip_read, but might as well test everything.

    Returns:
        lines (list): List of file lines.
    """
    with open(FILENAME, "r") as file:
        lines = [line.rstrip(DELIMITER) for line in file.readlines()]
    return lines
# end strip_readline

def compare_times():
    run = 100
    splitlines_t = timeit.timeit(splitlines_read, number=run)
    print("Splitlines Read:", splitlines_t)

    split_t = timeit.timeit(split_read, number=run)
    print("Split Read:", split_t)

    strip_t = timeit.timeit(strip_read, number=run)
    print("Strip Read:", strip_t)

    striplines_t = timeit.timeit(strip_readlines, number=run)
    print("Strip Readlines:", striplines_t)
# end compare_times

def compare_values():
    """Compare the values of the file.

    Note: split_read fails, because has an extra empty string in the list of lines. That's the only
    reason why it fails.
    """
    splr = splitlines_read()
    sprl = split_read()
    strr = strip_read()
    strl = strip_readlines()

    print("splitlines_read")
    print(repr(splr[:10]))

    print("split_read", splr == sprl)
    print(repr(sprl[:10]))

    print("strip_read", splr == strr)
    print(repr(strr[:10]))

    print("strip_readline", splr == strl)
    print(repr(strl[:10]))
# end compare_values

if __name__ == "__main__":
    compare_values()
    compare_times()