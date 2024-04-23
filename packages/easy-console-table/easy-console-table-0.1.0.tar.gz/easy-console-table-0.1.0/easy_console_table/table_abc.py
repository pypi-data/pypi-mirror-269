from abc import ABC, abstractmethod
from easy_console_table.table_error import TableError

alignment = {"left": "<", "center": "^", "right": ">"}


class TableABC(ABC):
    """ Abstract class for tables of easy-console-table package, implemented with a dict """
    def __init__(self, **kwargs):
        self._table = {}
        self._options = {"alignment": "right",
                         "title_separator": "-",
                         "column_separator": "|",
                         "line_separator": "_",
                         "alignment_title": "center"}
        self.config(**kwargs)
        self._filter = []

    def config(self, **kwargs):
        """ Method to configure the options for the table to show
            :param kwargs: dict -> Valid options :
             alignment:str, title_separator:str, column_separator:str, line_separator:str, alignment_title:str
        """
        # exception tests
        for key, val in kwargs.items():
            if not isinstance(key, str):
                raise TableError(f"Invalid {key} type, it must be str")
            if key not in self._options.keys():
                raise TableError(f"Invalid {key} argument, argument should be in : "
                                 f"{', '.join(self._options.keys())}")
            if key not in ["alignment", "alignment_title"]:
                if len(val) > 1:
                    raise TableError(f"Invalid {key} lenght, must be a single character")
        if "alignment" in kwargs.keys():
            if kwargs["alignment"] not in alignment.keys():
                raise TableError(f"Invalid alignment {kwargs['alignmen']} argument,"
                                 f" it should be in : {', '.join(alignment.keys())}")
        elif "alignment_title" in kwargs.keys():
            if kwargs["alignment_title"] not in alignment.keys():
                raise TableError(f"Invalid alignment {kwargs['alignmen']} argument,"
                                 f" it should be in : {', '.join(alignment.keys())}")

        # config
        for key, value in kwargs.items():
            if "\n" in value:
                raise TableError(f"Invalid character, it should not contains '\\n' character")
            self._options[key] = value

    def get_table(self) -> dict:
        """ Method to get the table
            :return: dict -> the whole table
        """
        return self._table

    def get_filter(self) -> list:
        """ Method to get the filter
            :return: list -> the filter
        """
        return self._filter

    @abstractmethod
    def add_filter(self, key: str):
        """ Method to add a filter
            :param key: str -> key filtered
        """
        pass

    def remove_filter(self, *args: str):
        """ Method to remove a filter
            :param args: str -> keys to remove
        """
        for key in args:
            if key not in self._filter:
                raise TableError("You can only remove a key that is filtered")
            self._filter.remove(key)

    def clear_filter(self):
        """ Method to clear the filter """
        self._filter = []

    @abstractmethod
    def export_as_csv(self, file_name: str):
        """ Method to export into a CSV file with filter
            :param file_name: str -> file name to use
        """
        pass
