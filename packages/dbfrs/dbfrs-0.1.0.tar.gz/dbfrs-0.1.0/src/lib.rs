use dbase::{FieldValue};
use pyo3::prelude::*;
use pyo3::types::{PyList, PyString, PyTuple};
use pyo3::wrap_pyfunction;

#[pyclass]
#[derive(Clone)]
struct Field {
    name: String,
    field_type: String,
    size: u8,
}

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

    fn add(&mut self, name: String, field_type: String, size: u8) {
        let field = Field {
            name,
            field_type,
            size,
        };
        self.fields.push(field);
    }

    pub fn list_fields(&self) {
        for field in &self.fields {
            println!("Name: {}, Size: {}, Type: {}", field.name, field.size, field.field_type);
        }
    }
}

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


#[pyfunction]
fn load_dbf<'py>(py: Python<'py>, path: String, only_fields: Vec<String>) -> PyResult<Bound<'py, PyList>> {
    let list = PyList::empty_bound(py);

    let mut reader = dbase::Reader::from_path_with_encoding(path, dbase::yore::code_pages::CP437).unwrap();

    for record_result in reader.iter_records() {
        let record = record_result.unwrap();
        let local = PyList::empty_bound(py);

        for field in only_fields.iter() {
            let value = record.get(field);

            match value {
                None => local.append(py.None()),
                Some(value) => match value {
                    FieldValue::Character(Some(string)) => local.append(string),
                    FieldValue::Numeric(value) => local.append(value),
                    FieldValue::Date(date) => local.append(date.expect("Error").to_string()),
                    FieldValue::Logical(bool) => local.append(bool),
                    FieldValue::Character(v) => local.append(v),
                    _ => panic!("Unhandled Type: {}", value)
                }
            }.expect("Something went wrong");
        }
        list.append(local).unwrap();
    }
    Ok(list)
}

#[pyfunction]
fn write_dbf<'py>(fields: Fields, records: &Bound<'py, PyList>, path: String) -> PyResult<()> {
    let mut builder = dbase::TableWriterBuilder::with_encoding(dbase::yore::code_pages::CP437);

    for field in &fields.fields {
        let field_name = dbase::FieldName::try_from(field.name.as_str()).unwrap();
        builder = builder.add_character_field(field_name, field.size); // Capture the possibly new writer
    }

    let mut writer = builder.build_with_file_dest(path).unwrap();

    for item in records.iter() {
        let tuple = item.downcast::<PyTuple>()?;

        let mut record = dbase::Record::default();

        for field in &fields.fields {
            if field.field_type == "N" {
                let value_py: &Bound<'py, PyAny> = &tuple.get_item(0)?;
                let value: f64 = value_py.extract()?;
                record.insert(field.name.clone(), dbase::FieldValue::Numeric(Some(value)));
            } else if field.field_type == "D" {
                let value_py: &Bound<'py, PyString> = &tuple.get_item(0)?.downcast_into()?;
                let value = value_py.to_string();
                record.insert(field.name.clone(), dbase::FieldValue::Date(Some(value.parse().unwrap())));
            } else if field.field_type == "L" {
                let value_py: &Bound<'py, PyAny> = &tuple.get_item(0)?;
                let value: bool = value_py.extract()?;
                record.insert(field.name.clone(), dbase::FieldValue::Logical(Some(value)));
            } else if field.field_type == "C" {
                let value_py: &Bound<'py, PyString> = &tuple.get_item(0)?.downcast_into()?;
                let value = value_py.to_string();
                record.insert(field.name.clone(), dbase::FieldValue::Character(Some(value.clone())));
            } else {
                panic!("Unhandled Type: {}", field.field_type);
            }
        }

        writer.write_record(&record).unwrap();
    }

    Ok(())
}

/// A Python module implemented in Rust.
#[pymodule]
fn dbfrs(m: &Bound<'_, PyModule>) -> PyResult<()>{
    m.add_class::<Fields>()?;
    m.add_class::<Field>()?;

    m.add_function(wrap_pyfunction!(load_dbf, m)?)?;
    m.add_function(wrap_pyfunction!(get_dbf_fields, m)?)?;
    m.add_function(wrap_pyfunction!(write_dbf, m)?)?;
    Ok(())
}
