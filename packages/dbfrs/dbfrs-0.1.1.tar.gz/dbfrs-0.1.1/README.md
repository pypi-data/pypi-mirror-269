# dbfrs

Minimalist DBF reader and writer for Python 3 written in Rust. The state of DBF libraries in 2024
is abysmal, yet still companies rely on this format.
This library aims to provide a simple, easy-to-use interface for reading
and writing DBF files.

Most libraries are either outdated, have a lot of dependencies, are too complex, or a really slow.
Most of them offer only reading capabilities. The main focus of `dbfrs` is to be minimalistic and fast. 

## Installation

```bash
pip install dbfrs
```

## Usage

### Reading a file into a DataFrame

```python
import dbfrs
import pandas as pd

filename = 'file.dbf'

fields = dbfrs.get_fields_from_file(filename)
records = dbfrs.load_dbf(filename, fields)
df = pd.DataFrame(records, columns=fields)
```

### Writing a DataFrame to a file

```python
import dbfrs
import pandas as pd

filename = 'file.dbf'
df = pd.DataFrame({'field1': [1, 2, 3], 'field2': ['a', 'b', 'c']})

fields = dbfrs.Fields()
fields.add_field('field1', 'N', 10)
fields.add_field('field2', 'C', 10)

records = [tuple(x) for x in df.values.tolist()]

dbfrs.write_dbf(filename, fields, records)
```
