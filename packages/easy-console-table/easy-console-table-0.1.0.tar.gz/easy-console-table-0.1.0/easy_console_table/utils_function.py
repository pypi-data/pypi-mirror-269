def get_max_lenght_key(keys: list[str]) -> int:
    """ Private function to get the longest line name value
        :param keys: list[str] -> line values

        :return: int -> lenght
    """
    max_digit_key = 0
    splitted_lines = []
    for key in keys:
        if "\n" in key:
            splitted_lines.append(key.split("\n"))
        else:
            splitted_lines.append([key])

    for line in splitted_lines:
        max_line_length = len(max(line, key=lambda x: len(x)))
        if max_line_length > max_digit_key:
            max_digit_key = max_line_length

    return max_digit_key + 1
