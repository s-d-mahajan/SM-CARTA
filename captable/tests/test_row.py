import unittest
from datetime import datetime
from captable.scripts.row import Row, OutputRow


class TestRow(unittest.TestCase):
    def setUp(self):
        self.csv_line_dict_1 = {
            "event": "VEST",
            "employee_id": "E001",
            "employee_name": "Alice Smith",
            "award_id": "ISO-001",
            "date": "2020-01-01",
            "quantity": "1000",
        }
        self.row_1 = Row.from_csv_line_dict(csv_line_dict=self.csv_line_dict_1)

    def test_from_csv_line_dict(self):
        instance = Row.from_csv_line_dict(csv_line_dict=self.csv_line_dict_1)
        assert isinstance(instance, Row)

    def test_quantity(self):
        assert self.row_1.quantity == 1000
        assert type(self.row_1.quantity) == float

    def test_award_date(self):
        assert self.row_1.award_date == datetime(day=1, month=1, year=2020)
        assert type(self.row_1.award_date) == datetime


class TestOutputRow(unittest.TestCase):
    def setUp(self):
        OutputRow.resolution = 0
        self.output_line_dict = {
            "employee_id": "E001",
            "employee_name": "Alice Smith",
            "award_id": "ISO-001",
            "quantity": float(1000),
        }
        self.output_row_1 = OutputRow.from_output_line_dict(
            output_line_dict=self.output_line_dict
        )

    def tearDown(self):
        OutputRow.resolution = 0

    def test_from_output_line_dict(self):
        instance = OutputRow.from_output_line_dict(
            output_line_dict=self.output_line_dict
        )
        assert isinstance(instance, OutputRow)

    def test_print_format(self):
        assert "E001,Alice Smith,ISO-001,1000" == self.output_row_1.__str__()

    def test_precision_format(self):
        OutputRow.resolution = 3
        print(self.output_row_1.__str__())
        assert "E001,Alice Smith,ISO-001,1000.000" == self.output_row_1.__str__()
