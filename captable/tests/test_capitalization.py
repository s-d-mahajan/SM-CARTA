import unittest
from captable.scripts.employee import Employee
from captable.scripts.capitalization import CapitalizationTable
import csv
from captable.config import CSV_FILE_HEADERS


class TestCapitalizationTable(unittest.TestCase):
    def setUp(self):
        Employee.filter = "2021-01-01"

    def test_create_row_data(self):
        with open("captable/tests/test_example.csv", "r") as csv_file:
            self.csv_data = csv.DictReader(csv_file, fieldnames=CSV_FILE_HEADERS)
            instance = CapitalizationTable()
            instance.create_row_data(self.csv_data)
            assert len(instance.unique_employees_id_name) == 3
            assert ("E001", "Alice Smith") in instance.unique_employees_id_name
            instance.create_employee_data()
            assert len(instance.employees) == 3

    def test_create_employee_data(self):
        with open("captable/tests/test_example.csv", "r") as csv_file:
            self.csv_data = csv.DictReader(csv_file, fieldnames=CSV_FILE_HEADERS)
            instance = CapitalizationTable()
            instance.create_row_data(self.csv_data)
            assert ("E001", "Alice Smith") in instance.unique_employees_id_name
            instance.create_employee_data()
            assert len(instance.employees) == 3
