import dbfrs

input_data = [
    ("John", "Doe", 33, True),
    ("Jane", "Smith", 44, False),
]


def test_write_and_read():
    fields = dbfrs.Fields()
    fields.add_character_field("first_name", 20)
    fields.add_character_field("last_name", 20)
    fields.add_numeric_field("age", 20, 1)
    fields.add_logical_field("is_happy")

    dbfrs.write_dbf(fields, input_data, "test.dbf")

    count = dbfrs.get_record_count("test.dbf")
    data = dbfrs.load_dbf("test.dbf")

    assert count == len(input_data)
    assert data == input_data
