from easy_console_table.table_abc_s_entry import TableABCSEntry
from easy_console_table.table_abc import alignment
from easy_console_table.utils_function import get_max_lenght_key


class VerticalTable(TableABCSEntry):
    """ Class to create a vertical table with name as key and list as values """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._options = {"alignment": "right",
                         "title_separator": "#",
                         "column_separator": "|",
                         "line_separator": "-",
                         "alignment_title": "center"}
        self.config(**kwargs)

    def export_as_csv(self, file_name: str):
        """ Method to export into a CSV file with filter
            :param file_name: str -> file name to use
        """
        keys = [key for key in self._table.keys() if key not in self._filter]
        with open(f"{file_name}.csv", "w") as f:
            for key in keys:
                values = [val.replace("\n", " ") for val in self._table[key]]
                f.write(str(key).replace("\n", " ") + "," + ",".join(values) + "\n")

    def _search_value_in_columns_key(self, key: str, value: str) -> bool:
        """ Private method to search a value in a column
            :param key: int -> key to search on
            :param value: str -> value to search

            :return: bool -> True if value in, otherwise False
        """
        for val in self._table[key]:
            if value in val:
                return True
        return False

    def _get_max_lenght_value(self, index: int) -> int:
        """ Private method to get the max lenght value to get the right format to display
            :return: int -> max lenght value
        """
        max_value = 0
        for column in self._table.values():
            if len(column) - 1 >= index:
                if "\n" in str(column[index]):
                    lines = str(column[index]).split('\n')
                else:
                    lines = [str(column[index])]
                max_line_length = len(max(lines, key=lambda x: len(x)))
                if max_line_length > max_value:
                    max_value = max_line_length

        return max_value + 1  # +1 to have a better result

    def _draw_line(self,
                   keys: list[str],
                   key: str,
                   title_separator: str,
                   column_separator: str,
                   align: str,
                   align_title: str) -> list[str]:
        """ Private method to draw a line (supports multi-line)
            :param keys: list[str] -> all keys
            :param key: str -> key to draw
            :param title_separator: str -> separator of title
            :param column_separator: str -> character use to separate columns
            :param align: str -> character use to align (<, ^, >)

            :return: str -> multi-lines
        """
        # get datas
        splitted_lines = []
        if "\n" in key:
            splitted_lines.append(key.split("\n"))
        else:
            splitted_lines.append([key])

        for val in self._table[key]:
            if "\n" in str(val):
                splitted_lines.append(str(val).split("\n"))
            else:
                splitted_lines.append([str(val)])

        while len(splitted_lines) - 1 != self._get_longest_column(keys):
            splitted_lines.append([""])

        # uniformize datas
        max_line = len(max(splitted_lines, key=lambda x: len(x)))
        for column in splitted_lines:
            while len(column) != max_line:
                column.append("")

        # draw lines
        lines: list[str] = ["" for _ in range(max_line)]

        # key
        max_digit_key = get_max_lenght_key(keys)
        for i, val in enumerate(splitted_lines[0]):
            lines[i] += f"{title_separator} {val: {align_title}{max_digit_key + 3}} {title_separator}"

        # values
        for i in range(1, len(splitted_lines)):
            max_digit_value = self._get_max_lenght_value(i - 1)

            for j in range(max_line):
                value = splitted_lines[i][j]
                lines[j] += f" {value: {align}{max_digit_value + 3}} {column_separator}"

        return lines

    def __str__(self) -> str:
        """ Special method to get the str format of the table
            :return: str -> the table
        """
        if len(self._table) == 0:
            return ""

        keys: list[str] = [value for value in list(self._table.keys()) if value not in self._filter]
        align: str = alignment[self._options["alignment"]]
        title_separator: str = self._options["title_separator"]
        column_separator: str = self._options["column_separator"]
        line_separator: str = self._options["line_separator"]
        alignment_title: str = alignment[self._options["alignment_title"]]

        # display title
        max_key = get_max_lenght_key(keys)
        longest_column = self._get_longest_column(keys)
        separator_value_line = (max_key + 7) * title_separator
        for i in range(longest_column):
            max_digit_value = self._get_max_lenght_value(i)
            separator_value_line += line_separator * (max_digit_value + 5) + column_separator

        to_return = [separator_value_line]

        # display values
        for key in keys:
            lines = self._draw_line(keys, key, title_separator, column_separator, align, alignment_title)
            for line in lines:
                to_return.append(line)

            to_return.append(separator_value_line)

        return "\n".join(to_return)
