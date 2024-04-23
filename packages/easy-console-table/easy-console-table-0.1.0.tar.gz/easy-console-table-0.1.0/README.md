# Easy Console Table Package
A package to easily create a console table that can render this :
```
-------------------------
|   Hello   |   World   |
-------------------------
|     Hello |         1 |
| _________ | _________ |
|     World |         2 |
| _________ | _________ |
|           |         3 |
| _________ | _________ |
```

---
## Summary
* [How this works ?](#how-this-works-)
  * [Shared Functionnalities](#shared-functionalities)
    * [Multi-line](#multiline-)
    * [Filter](#filter-methods-)
    * [Configuration](#configuration-method-)
    * [Export](#export-method-)
  * [Single key tables](#single-key-tables-verticaltable--horizontaltable)
    * [Interact](#table-interaction-methods-)
    * [Perfect](#perfect-method-)
    * [Sort](#sorting-method-)
  * [TwoEntryTable](#twoentrytable)
    * [Title](#table-title-)
    * [Interact](#interact-table-)
* [Some examples](#some-examples)
  * [Large Example](#large-example-)
  * [Quick Example](#quick-example-)
* [Github](#github-link)

## How to install ?
You can install the package ``easy-console-table`` by running the following command in your terminal :

```
pip install easy_console_table
```

It doesn't depend on another library.

To use it you can see the documentation [here](#how-this-works-). 

---
## How this works ?
This library provides a total of 3 classes that allows you to create 3 types of table :
* [HorizontalTable](#single-key-tables-verticaltable--horizontaltable)
 
* [VerticalTable](#single-key-tables-verticaltable--horizontaltable)

* [TwoEntryTable](#single-key-tables-verticaltable--horizontaltable)

First of all, HorizontalTable and VerticalTable are implemented mostly using the same Abstract class 
(TableABCSEntry which is itself implemented using TableABC) that means that the methods are the exact same ones.

TwoEntryTable class is implemented with TableABC.

A table with a single key means that there is only 1 key attached to the values. It is the HorizontalTable and the VerticalTable.
A table with 2 different keys means that there are 2 keys attached to each values. It is the TwoEntryTable.
(see [large example](#large-example-) for a better understanding)

### Shared functionalities
#### Multiline :
> Multi-line supports for every tables ! 
> Which means you can put `\n` in your key names, values or whatever you want that you can pass as argument to be in the table
> (except config method) and it will be displayed properly.

#### Filter methods :
Tables include a filter functionnality which makes possible to not draw a line / column by adding it in a filter (like a blacklist).
> ``get_filter`` returns a list of all filtered keys.

> ``add_filter`` add keys to filter. It takes *args str arguments as parameters. 
> 
> Example : ``table.add_filter(key1, key2, key3)``

> ``remove_filter`` remove keys to filter. It takes *args str arguments as parameters. 
> 
> Example : ``table.remove_filter(key1, key2, key3)`` 

> ``clear_filter`` remove all the filter and set it back to an empty list ``[]``.

> ``get_table`` returns the table in dict type.

#### Configuration method :
You can configure some parameters to edit the render by changing some characters and alignments.
> ``config`` used to configure some character. Parameter is a *kwargs that takes the following parameters : 
> "alignment", "title_separator", "column_separator", "line_separator", "alignment_title".
> 
> By default Tables has this configuration :
> 
> HorizontalTable : "alignment": "right", "title_separator": "-", "column_separator": "|", "line_separator": "_", "alignment_title": "center"
> 
> VerticalTable : "alignment": "right", "title_separator": "#", "column_separator": "|", "line_separator": "-", "alignment_title": "center"
> 
> TwoEntryTable : "alignment": "right", "title_separator": "#", "column_separator": "|", "line_separator": "-", "alignment_title": "center"
> 
> Note 1 : parameters given must be str and not contains special \ characters (otherwise it could not work).
> 
> Note 2 : parameters given must be a single character.

#### Export method :
> ``export_as_csv`` export the current table in a CSV file with the str parameter as name.
> 
> Note 1 : the table type change the format it gets exported (it will be exported exactly like if it was print in a file).
> 
> Note 2 : filter works on the export which means that filtered keys will not be shown.

### Single key Tables (VerticalTable / HorizontalTable)
The table is implemented using a dictionnary with str as keys that store values in list. 
#### Table interaction methods :
> ``set_table`` set a full table implemented with a dict. It takes as parameter a table dict.

> ``add_key`` add a key (column or line) to the table. Takes as parameter a name in str and values to add in list.
> 
> Note : if you pass a key that already exists it will replace the old values by the new ones.
> 
> Example : ``table.add_key("Hello", ["Hello\nWorld", "Hello", "World])``

> ``remove_key`` remove a key (column or line) to the table. Takes as parameter a name in str that must be in the table's keys.
> 
> Note : if the key is filtered it removes the key in the filter.
> 
> Example : ``table.remove_key("Hello")``

> ``get_key`` get values from a key. Takes as parameter a key as str that must be in table's keys and returns a list of values.

#### Perfect method :
A perfect table is a table that has all its cells filled. It has the same lenght in all its columns.
> ``get_is_perfect`` returns True if the table is perfect or False if not (filtered keys don't count).

#### Sorting method :
You can sort a whole table from the sorting of a key's values.
> ``sort_table_from_key`` sort the current table by following the key's parameter values sorting. 
> There is a reverse default argument set as True and a key default argument set at lambda x: x. 
> It manages the way you want to sort and will be pass to the sorted method.
> 
> Note 1 : table must be perfect to use this method.
> 
> Note 2 : filtered keys will also be sorted
> 
> Example : ``table.sort_table_from_key("Hello", reverse=True, key=lambda x: len(x)``

### TwoEntryTable
#### Table Title :
You can define a title for the table that is displayed at the top right corner of the table.
For this, you need to interract with the ``title`` attribut which is a string.
You can, as well, set this title to a multi-line title by using the ``\n`` character.

#### Interact table :
The table is implemented using a dictionnary and 2 lists (line names and column names). 
The keys dictionnary are a tuple of column and line and values are a single cell value.
All the keys in line names and column names are unique which means that you can't add key that already exists in lines or columns.
> ``get_line_names`` returns the line names in list.

> ``get_column_names``returns the column names in list.

> ``add_line_names`` add lines to the table. Parameter is a *args in str.
> 
> Example : ``table.add_line_names(key1, key2, key3)``

> ``add_column_names`` add columns to the table. Parameter is a *args in str.
> 
> Example : ``table.add_column_names(key4, key5, key6)``

> ``get_values`` returns a list of all the values of a given key (line or column).

> ``add_values`` add values to the given parameter key. 
> It understands if the given key is a line or column and add it to fill the right cells.
> 
> Note 1 : the values you add to a line key must have a lenght equal or lower than the lenght of columns (filtered doesn't count).
> Conversely it works the same if the key is a column, lenght of values must be equal or lower than the lenght of lines.
> 
> Note 2 : if you pass a value to a cell that already exists it will replace the old value by the new one.
> 
> Example : ``table.add_values(key1, ["Hello\nWorld", "Hello", "World])``

> ``remove_key`` removes a key and all the linked values associated.
> 
> Note : if the key is filtered it removes the key in the filter.

---
## Some examples
### Large example :
```
Horizontal Table :
--------------------------------------------------------------------------------------
|   Hello   |   World   |                           Multi                            |
|           |           |                            Line                            |
--------------------------------------------------------------------------------------
|     Hello |         1 |                                                      Multi |
|           |           |                                                       line |
| _________ | _________ | __________________________________________________________ |
|     World |         2 |                                                    Support |
| _________ | _________ | __________________________________________________________ |
|           |         3 |                                                         As |
|           |           |                                                       Well |
| _________ | _________ | __________________________________________________________ |
|           |           |                                                            |
|           |           |      _   _      _ _        __        __         _     _ _  |
|           |           |     | | | | ___| | | ___   \ \      / /__  _ __| | __| | | |
|           |           |     | |_| |/ _ \ | |/ _ \   \ \ /\ / / _ \| '__| |/ _` | | |
|           |           |     |  _  |  __/ | | (_) |   \ V  V / (_) | |  | | (_| |_| |
|           |           |     |_| |_|\___|_|_|\___/     \_/\_/ \___/|_|  |_|\__,_(_) |
|           |           |                                                            |
| _________ | _________ | __________________________________________________________ |

Vertical Table :
#############-----------|-------------|----------|------------------------------------------------------------|
#   Hello   #     Hello |       World |          |                                                            |
#############-----------|-------------|----------|------------------------------------------------------------|
#   World   #         1 |           2 |        3 |                                                            |
#############-----------|-------------|----------|------------------------------------------------------------|
#   Multi   #     Multi |     Support |       As |                                                            |
#   Line    #      line |             |     Well |      _   _      _ _        __        __         _     _ _  |
#           #           |             |          |     | | | | ___| | | ___   \ \      / /__  _ __| | __| | | |
#           #           |             |          |     | |_| |/ _ \ | |/ _ \   \ \ /\ / / _ \| '__| |/ _` | | |
#           #           |             |          |     |  _  |  __/ | | (_) |   \ V  V / (_) | |  | | (_| |_| |
#           #           |             |          |     |_| |_|\___|_|_|\___/     \_/\_/ \___/|_|  |_|\__,_(_) |
#           #           |             |          |                                                            |
#############-----------|-------------|----------|------------------------------------------------------------|

Two Entry Table :
############################################################################################################################
#    Yeah !    #   Hello    |                           Multi                            |         Of         |   Course   |
#              #   World    |                            Line                            |                    |            |
############################################################################################################################
#    Hello     #       Hehe |                                                      Multi |               Nice |        123 |
#              #            |                                                       line |                    |            |
# ############ # ---------- | ---------------------------------------------------------- | ------------------ | ---------- |
#    World     #            |                                                    Support |                    |            |
# ############ # ---------- | ---------------------------------------------------------- | ------------------ | ---------- |
#   Working    #        Hey |                                                         As |     Are you Okay ? |            |
#              #            |                                                       Well |                    |            |
# ############ # ---------- | ---------------------------------------------------------- | ------------------ | ---------- |
#   Properly   #            |                                                            |                    |            |
#              #            |      _   _      _ _        __        __         _     _ _  |                    |            |
#              #            |     | | | | ___| | | ___   \ \      / /__  _ __| | __| | | |                    |            |
#              #            |     | |_| |/ _ \ | |/ _ \   \ \ /\ / / _ \| '__| |/ _` | | |                    |            |
#              #            |     |  _  |  __/ | | (_) |   \ V  V / (_) | |  | | (_| |_| |                    |            |
#              #            |     |_| |_|\___|_|_|\___/     \_/\_/ \___/|_|  |_|\__,_(_) |                    |            |
#              #            |                                                            |                    |            |
# ############ # ---------- | ---------------------------------------------------------- | ------------------ | ---------- |
```

Done by running :
```py
from easy_console_table import TwoEntryTable, HorizontalTable, VerticalTable

HELLO_WORLD = \
    r"""
 _   _      _ _        __        __         _     _ _ 
| | | | ___| | | ___   \ \      / /__  _ __| | __| | |
| |_| |/ _ \ | |/ _ \   \ \ /\ / / _ \| '__| |/ _` | |
|  _  |  __/ | | (_) |   \ V  V / (_) | |  | | (_| |_|
|_| |_|\___|_|_|\___/     \_/\_/ \___/|_|  |_|\__,_(_)
"""

print("Horizontal Table :")
t = HorizontalTable()
t.add_key("Hello", ["Hello", "World"])
t.add_key("World", [1, 2, 3])
t.add_key("Multi\nLine", ["Multi\nline", "Support", "As\nWell", HELLO_WORLD])
print(t)

print()
print("Vertical Table :")
t = VerticalTable()
t.add_key("Hello", ["Hello", "World"])
t.add_key("World", [1, 2, 3])
t.add_key("Multi\nLine", ["Multi\nline", "Support", "As\nWell", HELLO_WORLD])
print(t)

print()
print("Two Entry Table :")
t = TwoEntryTable()
t.add_line_names("Hello", "World", "Working", "Properly")
t.add_column_names("Hello\nWorld", "Multi\nLine", "Of", "Course")
t.add_values("Hello", ["Hehe", "", "Nice"])
t.add_values("Working", ["Hey", "", "Are you Okay ?"])
t.add_values("Multi\nLine", ["Multi\nline", "Support", "As\nWell", HELLO_WORLD])
t.add_values("Course", [123])
t.title = "Yeah !"
print(t)
```

### Quick example :
```
#####################################
| Hello     I Sort     I trash      I
#####################################
|   World   I    2     I    Dont    I
I --------- I -------- I ---------- I
|     !     I    3     I    Work    I
I --------- I -------- I ---------- I
|   Hello   I    1     I     As     I
I --------- I -------- I ---------- I
|           I          I     It     I
I --------- I -------- I ---------- I
|           I          I   Should   I
I --------- I -------- I ---------- I

########################
| Hello     I Sort     I
########################
|   World   I    2     I
I --------- I -------- I
|     !     I    3     I
I --------- I -------- I
|   Hello   I    1     I
I --------- I -------- I

-------------
|   Hello   |
-------------
|     Hello |
| _________ |
|     World |
| _________ |
|         ! |
| _________ |
```

Done by running :
```py
from easy_console_table import HorizontalTable

t = HorizontalTable(alignment="center", title_separator="#", line_separator="-", column_separator="I", alignment_title="left")
t.add_key("Hello", ["World", "!", "Hello"])
t.add_key("Sort", [2, 3, 1])
t.add_key("trash", ["Dont", "Work", "As", "It", "Should"])

print(t)
print()

t.add_filter("trash")
print(t)
print()

t.remove_key("trash")
t.sort_table_from_key("Sort")
t.config(alignment="right", title_separator="-", line_separator="_", column_separator="|", alignment_title="center")
t.add_filter("Sort")
print(t)
```

---
## [Github link](https://github.com/flastar-fr/easy_console_table)