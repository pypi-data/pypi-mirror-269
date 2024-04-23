from abc import abstractmethod
from typing import Callable

from easy_console_table.table_abc import TableABC
from easy_console_table.table_error import TableError


class TableABCSEntry(TableABC):
    """ Base abstract class for every tables which is implemented with 1 type of key (line, column, for example) """
    def set_table(self, table: dict):
        """ Method to set a table with a dict
            :param table: dict -> table to set
        """
        if not isinstance(table, dict):
            raise TableError("Table passed must be a dict")
        for key, value in table.keys():
            if not isinstance(key, str):
                raise TableError(f"Key {key} must be a string")
            if not isinstance(value, list):
                raise TableError(f"Values {value} must be a list")
        self._table = table

    def add_key(self, name: str, datas: list):
        """ Method to create a column to the table
            :param name: str -> column's name to create
            :param datas: list -> column's values to create
        """
        if not isinstance(datas, list):
            raise TableError("Column must be a list type")
        elif not isinstance(name, str):
            raise TableError("Name must be a str type")
        self._table[name] = datas

    def remove_key(self, name: str):
        """ Method to delete a column to the table
            :param name: str -> column's name to delete
        """
        if name not in self._table.keys():
            raise TableError("Column's name not in table")
        if name in self._filter:
            self.remove_filter(name)
        self._table.pop(name)

    def get_key(self, name: str) -> list:
        """ Method to get the column list with the name
            :param name: str -> column's name to get

            :return: list -> the column
        """
        if name not in self._table.keys():
            raise TableError("Column's name not in table")
        return self._table[name]

    def get_is_perfect(self) -> bool:
        """ Method to know if all column's lenght is the same
            :return: bool -> True if it is the same, False if it is not the same
        """
        values = [v for k, v in self._table.items() if k not in self._filter]
        default_len = len(max(values, key=lambda x: len(x)))
        for value in self._table.values():
            if len(value) != default_len:
                return False
        return True

    def add_filter(self, *args: str):
        """ Method to add a filter
            :param args: str -> key filtered
        """
        for key in args:
            if key not in self._table.keys():
                raise TableError(f"Key {key} not in table keys")
            self._filter.append(key)

    def sort_table_from_key(self, column_name: str, reverse: bool = False, key: Callable = lambda x: x):
        """ Method to sort the table from depending on sorting a column
            :param column_name: str -> column name use to sort all the table
            :param reverse: bool -> if it has to be reversed or not
            :param key: Callable -> to pass as key sorted parameter
        """
        if not self.get_is_perfect():
            raise TableError("Table values should have the same lenght")
        from_column = self._table[column_name]
        sorted_indices = sorted(range(len(from_column)), key=lambda i: key(from_column[i]), reverse=reverse)

        for k, value in self._table.items():
            self._table[k] = [value[i] for i in sorted_indices]

    @abstractmethod
    def export_as_csv(self, file_name: str):
        """ Method to export into a CSV file with filter
            :param file_name: str -> file name to use
        """
        pass

    def _get_longest_column(self, keys: list[str]) -> int:
        """ Private method to get the longest list contained in the table
            :param keys: list[str] -> keys to test
            :return: int -> longest column lenght
        """
        values = [self._table[key] for key in keys]
        return len(max(values, key=lambda x: len(x)))
