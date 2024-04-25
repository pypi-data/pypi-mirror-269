use dbase::{FieldValue};
use pyo3::prelude::*;
use pyo3::types::{PyList, PyString, PyTuple};
use pyo3::wrap_pyfunction;

#[pyclass]
#[derive(Clone, Copy)]
enum FieldType {
    Character,
    Numeric,
    Date,
    Logical,
}

/// This struct represents a field in a dbf file.
/// # Fields
/// * `name` - A string that represents the name of the field
/// * `field_type` - A string that represents the type of the field
/// * `size` - A u8 that represents the size of the field
#[pyclass]
#[derive(Clone)]
struct Field {
    name: String,
    field_type: FieldType,
    size: u8,
    decimals: Option<u8>,
}

/// This struct represents a list of fields in a dbf file.
/// # Fields
/// * `fields` - A vector of Field objects that represent the fields in the dbf file
/// # Example
/// ```python
/// fields = Fields()
/// fields.add("field1", "C", 10)
/// fields.add("field2", "N", 10)
/// fields.list_fields()
#[pyclass]
#[derive(Clone)]
struct Fields {
    fields: Vec<Field>,
}

#[pymethods]
impl Fields {
    #[new]
    fn new() -> Self {
        Fields {
            fields: Vec::new(),
        }
    }

    fn add_character_field(&mut self, name: String, size: u8) {
        let field = Field {
            name,
            field_type: FieldType::Character,
            size,
            decimals: None,
        };
        self.fields.push(field);
    }

    fn add_numeric_field(&mut self, name: String, size: u8, decimals: u8) {
        let field = Field {
            name,
            field_type: FieldType::Numeric,
            size,
            decimals: Some(decimals),
        };
        self.fields.push(field);
    }

    fn add_date_field(&mut self, name: String) {
        let field = Field {
            name,
            field_type: FieldType::Date,
            size: 8,
            decimals: None,
        };
        self.fields.push(field);
    }

    fn add_logical_field(&mut self, name: String) {
        let field = Field {
            name,
            field_type: FieldType::Logical,
            size: 1,
            decimals: None,
        };
        self.fields.push(field);
    }
}

#[pyfunction]
fn get_record_count(path: String) -> PyResult<usize> {
    let mut reader = dbase::Reader::from_path_with_encoding(path, dbase::yore::code_pages::CP437).unwrap();
    Ok(reader.iter_records().count())
}

/// This function takes a path to a dbf file and returns a list of fields
/// that are in the dbf file.
/// # Arguments
/// * `path` - A string that represents the path to the dbf file
/// # Returns
/// * A list of strings that represent the fields in the dbf file
/// # Example
/// ```python
/// import dbfrs
/// fields = dbfrs.get_dbf_fields("path/to/dbf")
/// print(fields)
/// ```
#[pyfunction]
fn get_dbf_fields<'py>(py: Python<'py>, path: String) -> PyResult<Bound<'py, PyList>> {
    let fields = PyList::empty_bound(py);
    let reader = dbase::Reader::from_path_with_encoding(path, dbase::yore::code_pages::CP437).unwrap();

    for field in reader.fields() {
        if field.name() == "DeletionFlag" {
            continue;
        }
        fields.append(field.name()).unwrap();
    }

    Ok(fields)
}


/// # Note
/// This function is not meant to be used directly. It is used by the `load_dbf` function.
/// TODO: Make only_fields optional and load all fields if not provided
///
/// # Arguments
/// * `path` - A string that represents the path to the dbf file
/// * `only_fields` - A list of strings that represent the fields to be loaded
/// # Returns
/// * A list of lists that represent the records in the dbf file
/// # Example
/// ```python
/// import dbfrs
/// records = dbfrs.load_dbf("path/to/dbf", ["field1", "field2"])
/// print(records)
/// ```
#[pyfunction]
fn load_dbf<'py>(py: Python<'py>, path: String, only_fields: Option<Vec<String>>) -> PyResult<Bound<'py, PyList>> {
    let list = PyList::empty_bound(py);

    let mut reader = dbase::Reader::from_path_with_encoding(&path, dbase::yore::code_pages::CP437).unwrap();

    // Determine fields to load
    let fields_to_load = if let Some(fields) = only_fields {
        fields
    } else {
        // If only_fields is None, use get_dbf_fields to fetch all fields
        get_dbf_fields(py, path.clone())?.extract::<Vec<String>>()?
    };

    for record_result in reader.iter_records() {
        let record = record_result.unwrap();
        let mut local = Vec::new();  // Use a Rust Vec to collect Py objects for this record

        for field_name in fields_to_load.iter() {
            let value = record.get(field_name);

            let py_value = match value {
                None => py.None(),
                Some(value) => match value {
                    FieldValue::Character(Some(string)) => string.into_py(py),
                    FieldValue::Numeric(value) => value.into_py(py),
                    FieldValue::Date(date) => date.expect("Error").to_string().into_py(py),
                    FieldValue::Logical(bool) => bool.into_py(py),
                    FieldValue::Character(v) => v.clone().into_py(py),
                    _ => panic!("Unhandled Type: {}", value)
                }
            };
            local.push(py_value);
        }
        list.append(PyTuple::new_bound(py, &local))?;  // Convert each record's Vec to PyTuple and append to the list
    }
    Ok(list)  // Return the list of tuples
}

/// This function writes a dbf file to the specified path.
/// # Arguments
/// * `fields` - A Fields object that represents the fields in the dbf file
/// * `records` - A list of lists that represent the records in the dbf file
/// * `path` - A string that represents the path to the dbf file
/// # Example
/// ```python
/// import dbfrs
/// fields = dbfrs.Fields()
/// fields.add_character_field("first_name", 20)
/// fields.add_character_field("last_name", 20)
/// fields.add_numeric_field("age", 20, 1)
/// fields.add_logical_field("is_happy")
/// records = [("John", "Doe", 33, True), ("Jane", "Smith", 44, False)]
/// dbfrs.write_dbf(fields, records, "path/to/dbf")
/// ```
/// # Note
/// * The fields in the Fields object must match the fields in the records
/// * The order of the fields in the Fields object must match the order of the fields in the records
#[pyfunction]
fn write_dbf<'py>(fields: Fields, records: &Bound<'py, PyList>, path: String) -> PyResult<()> {
    let mut builder = dbase::TableWriterBuilder::with_encoding(dbase::yore::code_pages::CP437);

    for field in &fields.fields {
        let field_name = dbase::FieldName::try_from(field.name.as_str()).unwrap();

        match field.field_type {
            FieldType::Character => {
                builder = builder.add_character_field(field_name, field.size);
            }
            FieldType::Numeric => {
                builder = builder.add_numeric_field(field_name, field.size, field.decimals.unwrap());
            }
            FieldType::Date => {
                builder = builder.add_date_field(field_name);
            }
            FieldType::Logical => {
                builder = builder.add_logical_field(field_name);
            }
        }
    }

    let mut writer = builder.build_with_file_dest(path).unwrap();

    for item in records.iter() {
        let tuple = item.downcast::<PyTuple>()?;

        let mut record = dbase::Record::default();

        for (index, field) in fields.fields.iter().enumerate() {
            match field.field_type {
                FieldType::Character => {
                    let value_py: &Bound<'py, PyString> = &tuple.get_item(index)?.downcast_into()?;
                    let value = value_py.to_string();
                    record.insert(field.name.clone(), dbase::FieldValue::Character(Some(value.clone())));
                }
                FieldType::Numeric => {
                    let value_py: &Bound<'py, PyAny> = &tuple.get_item(index)?;
                    let value: f64 = value_py.extract()?;
                    record.insert(field.name.clone(), dbase::FieldValue::Numeric(Some(value)));
                }
                FieldType::Date => {
                    let value_py: &Bound<'py, PyString> = &tuple.get_item(index)?.downcast_into()?;
                    let value = value_py.to_string();
                    record.insert(field.name.clone(), dbase::FieldValue::Date(Some(value.parse().unwrap())));
                }
                FieldType::Logical => {
                    let value_py: &Bound<'py, PyAny> = &tuple.get_item(index)?;
                    let value: bool = value_py.extract()?;
                    record.insert(field.name.clone(), dbase::FieldValue::Logical(Some(value)));
                }
            }
        }

        writer.write_record(&record).unwrap();
    }

    Ok(())
}

/// This module is a python module that provides functions to read and write dbf files.
#[pymodule]
fn dbfrs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Fields>()?;
    m.add_class::<Field>()?;
    m.add_class::<FieldType>()?;

    m.add_function(wrap_pyfunction!(load_dbf, m)?)?;
    m.add_function(wrap_pyfunction!(get_dbf_fields, m)?)?;
    m.add_function(wrap_pyfunction!(write_dbf, m)?)?;
    m.add_function(wrap_pyfunction!(get_record_count, m)?)?;

    Ok(())
}
