from easy_console_table.table_abc import TableABC, alignment
from easy_console_table.table_error import TableError
from easy_console_table.utils_function import get_max_lenght_key


def _get_lenght_key(key: str) -> int:
    """ Function to get the lenght of a title if it was on multi line
        :param key: str -> the key to verif

        :return: int -> the lenght
    """
    if "\n" in key:
        splitted_list = key.split("\n")
    else:
        splitted_list = [key]

    return len(max(splitted_list, key=lambda x: len(x)))


class TwoEntryTable(TableABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._columns = []
        self._lines = []
        self._options = {"alignment": "right",
                         "title_separator": "#",
                         "column_separator": "|",
                         "line_separator": "-",
                         "alignment_title": "center"}
        self.title = ""
        self.config(**kwargs)

    def get_line_names(self) -> list[str]:
        """ Method to get all the lines
            :return: list[str] -> all the lines
        """
        return self._lines

    def get_column_names(self) -> list[str]:
        """ Method to get all the columns
            :return: list[str] -> all the columns
        """
        return self._columns

    def add_column_names(self, *args: str):
        """ Method to add line keys to the table
            :param args: list[str]
        """
        for key in args:
            if not isinstance(key, str):
                raise TableError("Key name needs to be a str")
            if key in self._lines or key in self._columns:
                raise TableError("Key already exists")
            self._columns.append(key)

    def add_line_names(self, *args: str):
        """ Method to add line keys to the table
            :param args: list[str]
        """
        for key in args:
            if not isinstance(key, str):
                raise TableError("Key name needs to be a str")
            if key in self._lines or key in self._columns:
                raise TableError("Key already exists")
            self._lines.append(key)

    def add_values(self, key: str, values: list):
        """ Method to add values to a key in lines or columns
            :param key: str -> key to put
            :param values: list -> values to bind on the key
        """
        if key in self._lines:
            if not len(values) <= len(self._columns):
                raise TableError("Not enought lines to store the values")
            self._add_line_values(key, values)
        elif key in self._columns:
            if not len(values) <= len(self._lines):
                raise TableError("Not enought columns to store the values")
            self._add_column_values(key, values)
        else:
            raise "Key doesn't exist"

    def _add_column_values(self, key: str, values: list):
        """ Method to add values from to a specific column
            :param key: str -> column key to add
            :param values: list -> values to add
        """
        assert key in self._columns, "Key doesn't exist"
        assert len(values) <= len(self._lines), "Not enought lines to store the values"
        for i in range(len(values)):
            self._table[(key, self._lines[i])] = values[i]

    def _add_line_values(self, key: str, values: list):
        """ Method to add values from to a specific line
            :param key: str -> line key to add
            :param values: list -> values to add
        """
        if key not in self._lines:
            raise TableError("Key doesn't exist")
        if not len(values) <= len(self._columns):
            raise TableError("Not enought columns to store the values")
        for i in range(len(values)):
            self._table[(self._columns[i]), key] = values[i]

    def get_values(self, key: str):
        """ Method to get values from a key in lines or columns
            :param key: str -> key's values to get
        """
        if key in self._lines:
            return self._get_line_values(key)
        elif key in self._columns:
            return self._get_column_values(key)
        else:
            raise TableError("Key doesn't exist")

    def _get_line_values(self, key: str) -> list:
        """ Method to get values from a line name
            :param key: str -> line name

            :return: list -> values to get
        """
        values = []
        columns = [key for key in self._columns if key not in self._filter]
        for column in columns:
            try:
                values.append(self._table[(column, key)])
            except KeyError:
                break

        return values

    def _get_column_values(self, key: str) -> list:
        """ Method to get values from a column name
            :param key: str -> column name

            :return: list -> values to get
        """
        values = []
        lines = [key for key in self._lines if key not in self._filter]
        for line in lines:
            try:
                values.append(self._table[(key, line)])
            except KeyError:
                break

        return values

    def remove_key(self, key: str):
        """ Method to remove key and values with a key
            :param key: str -> key to remove
        """
        if key in self._lines:
            self._to_remove(key, "lines")
        elif key in self._columns:
            self._to_remove(key, "columns")
        else:
            raise TableError(f"Key {key} doesn't exist")

    def _to_remove(self, key: str, to_remove_in: str):
        """ Private method to remove a key from a line or a column
            :param key: str -> key to remove
            :param to_remove_in: str -> where to remove, "lines" or "columns"
        """
        assert to_remove_in in ["columns", "lines"], f"Remove in : {to_remove_in} not 'columns' or 'lines'"
        if to_remove_in == "columns":
            values = self._columns
        else:
            values = self._lines

        for value in values:
            if to_remove_in == "columns":
                try:
                    self._table.pop((value, key))
                except KeyError:
                    continue
            else:
                try:
                    self._table.pop((key, value))
                except KeyError:
                    continue

        # filter
        if to_remove_in == "lines":
            self._lines.remove(key)

            if key in self._filter:
                self._filter.remove_key(key)
        else:
            self._columns.remove(key)

            if key in self._filter:
                self._filter.remove(key)

    def add_filter(self, *args: str):
        """ Method to add a filter
            :param args: str -> keys to filter
        """
        for key in args:
            if key not in self._lines + self._columns:
                raise TableError("You can't filter something that is not in columns or lines keys")
            self._filter.append(key)

    def export_as_csv(self, file_name: str):
        """ Method to export into a CSV file with filter
            :param file_name: str -> file name to use
        """
        lines = [key for key in self._lines if key not in self._filter]
        columns = [key.replace("\n", " ") for key in self._columns if key not in self._filter]
        with open(f"{file_name}.csv", "w", encoding="utf-8") as f:
            f.write("," + ",".replace("\n", " ").join(columns) + "\n")
            for line in lines:
                values = [val.replace("\n", " ") for val in self._get_line_values(line)]
                f.write(str(line).replace("\n", " ") + "," + ",".join(values) + "\n")

    def _get_max_lenght_value_line(self, line_name: str) -> int:
        """ Private method to get the max lenght value to get the right format to display
            :return: int -> max lenght value
        """
        if line_name not in self._columns:
            raise TableError("Key doesn't exist")

        max_value = max(_get_lenght_key(line_name), _get_lenght_key(self.title))
        for val in self._lines:
            try:
                lines = str(self._table[(line_name, val)]).split('\n')
                max_line_length = max(len(line) for line in lines)
                if max_line_length > max_value:
                    max_value = max_line_length
            except KeyError:
                continue

        return max_value + 1  # +1 to have a better result

    def _draw_titles(self,
                     keys: list[str],
                     line_names: list[str],
                     column_separator: str,
                     title_separator: str,
                     align_title: str) -> list[str]:
        """ Private method to draw the titles of the table
            :param keys: list[str] -> keys to draw
            :param line_names: list[str] -> make possible to draw the gap at the beginning
            :param column_separator: str -> char to separate columns

            :return: list[str] -> a list that contains the lines
        """
        # get datas
        splitted_lines = []
        for key in keys:
            if "\n" in key:
                splitted_lines.append(key.split("\n"))
            else:
                splitted_lines.append([key])

        splitted_title = self.title.split("\n")

        # uniformize datas
        max_line = len(max(splitted_lines, key=lambda x: len(x)))
        max_line = max(len(splitted_title), max_line)
        for column in splitted_lines:
            while len(column) != max_line:
                column.append("")

        # draw lines
        lines: list[str] = [title_separator for _ in range(max_line)]

        for i in range(len(splitted_lines)):
            max_lenght = self._get_max_lenght_value_line(keys[i])

            for j in range(max_line):
                value = splitted_lines[i][j]
                lines[j] += f" {value: {align_title}{max_lenght + 3}} {column_separator}"

        # align to a Two Entry format (puting space for lines keys drawing)
        max_digits = get_max_lenght_key(line_names + [self.title])
        while len(splitted_title) != max_line:
            splitted_title.append("")
        for i, val in enumerate(splitted_title):
            lines[i] = f"{title_separator} {val: ^{max_digits + 3}} " + lines[i]

        return lines

    def _draw_line(self,
                   lines: list[str],
                   columns: list[str],
                   key: str,
                   title_separator: str,
                   column_separator: str,
                   align: str,
                   align_title: str) -> list[str]:
        """ Private method to draw a line (supports multi-line)
            :param lines: list[str] -> lines
            :param columns: list[str] -> columns
            :param key: str -> key to draw
            :param title_separator: str -> separator of title
            :param column_separator: str -> character use to separate columns
            :param align: str -> character used to align (<, ^, >)
            :param align_title: str -> character used to align title (<, ^, >)

            :return: str -> multi-lines
        """
        # get datas
        splitted_lines: list[list[str]] = []
        if "\n" in key:
            splitted_lines.append(key.split("\n"))
        else:
            splitted_lines.append([key])

        for column in columns:
            try:
                splitted_lines.append(str(self._table[column, key]).split("\n"))
            except KeyError:
                splitted_lines.append([])

        while len(splitted_lines) - 1 != len(columns):
            splitted_lines.append([""])

        # uniformize datas
        max_line: int = len(max(splitted_lines, key=lambda x: len(x)))
        for column in splitted_lines:
            while len(column) != max_line:
                column.append("")

        # draw lines
        to_return: list[str] = ["" for _ in range(max_line)]

        # key
        max_digit_key = get_max_lenght_key(lines + [self.title])
        for i, val in enumerate(splitted_lines[0]):
            to_return[i] += f"{title_separator} {val: {align_title}{max_digit_key + 3}} {title_separator}"

        # values
        for i in range(1, len(splitted_lines)):
            max_digit_value = self._get_max_lenght_value_line(columns[i - 1])

            for j in range(max_line):
                value = splitted_lines[i][j]
                to_return[j] += f" {value: {align}{max_digit_value + 3}} {column_separator}"

        return to_return

    def __str__(self) -> str:
        """ Special method to get the str format of the table
            :return: str -> the table
        """
        # get datas
        columns: list[str] = [value for value in list(self._columns) if value not in self._filter]
        lines: list[str] = [value for value in list(self._lines) if value not in self._filter]
        align: str = alignment[self._options["alignment"]]
        title_separator: str = self._options["title_separator"]
        column_separator: str = self._options["column_separator"]
        line_separator: str = self._options["line_separator"]
        alignment_title: str = alignment[self._options["alignment_title"]]

        if len(lines + columns) == 0:
            if self.title != "":
                max_digits = get_max_lenght_key([self.title])
                line = title_separator*(max_digits+7)
                to_print = [line]
                for i, val in enumerate(self.title.split("\n")):
                    to_print.append(f"{title_separator} {val: ^{max_digits + 3}} {title_separator}")
                to_print.append(line)
                return "\n".join(to_print)
            return ""

        # titles display
        # draw a column * amount of column (don't take last chars depending of amount of columns)
        # separators construct
        to_return: list[str] = []
        max_digits = get_max_lenght_key(lines + [self.title])
        title_separator_line = title_separator * (max_digits + 6)
        separator_values_lines = f"{title_separator} {((max_digits + 3) * title_separator)} {title_separator}"
        for key in columns:
            max_digit_value = self._get_max_lenght_value_line(key)
            title_separator_line += (title_separator * (max_digit_value + 7))
            separator_values_lines += f" {line_separator * (max_digit_value + 3)} {column_separator}"

        if len(columns) > 1:
            title_separator_line = title_separator_line[:-len(columns) + 1]
        to_return.append(title_separator_line)

        # draw titles
        title = self._draw_titles(columns, lines, column_separator, title_separator, alignment_title)
        for line in title:
            to_return.append(line)

        to_return.append(title_separator_line)

        # display values
        for key in lines:
            to_print = self._draw_line(lines, columns, key, title_separator, column_separator, align, alignment_title)
            for line in to_print:
                to_return.append(line)

            to_return.append(separator_values_lines)

        return "\n".join(to_return)
