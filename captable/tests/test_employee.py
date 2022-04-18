import unittest
from captable.scripts.employee import Employee
from captable.scripts.row import Row
from captable.config import EVENT
from datetime import datetime


class TestOutputRow(unittest.TestCase):
    def setUp(self):
        Employee.filter = "2020-01-01"

        self.csv_line_dict_1 = {
            "event": "VEST",
            "employee_id": "E001",
            "employee_name": "Alice Smith",
            "award_id": "ISO-001",
            "date": "2020-01-01",
            "quantity": "1000",
        }
        self.csv_line_dict_2 = {
            "event": "VEST",
            "employee_id": "E001",
            "employee_name": "Alice Smith",
            "award_id": "ISO-001",
            "date": "2021-01-01",
            "quantity": "1000",
        }
        self.csv_line_dict_3 = {
            "event": "CANCEL",
            "employee_id": "E001",
            "employee_name": "Alice Smith",
            "award_id": "ISO-001",
            "date": "2021-01-01",
            "quantity": "700",
        }
        self.csv_line_dict_4 = {
            "event": "VEST",
            "employee_id": "E002",
            "employee_name": "Bobby Jones",
            "award_id": "NSO-001",
            "date": "2020-01-02",
            "quantity": "100",
        }
        self.csv_line_dict_5 = {
            "event": "CANCEL",
            "employee_id": "E002",
            "employee_name": "Bobby Jones",
            "award_id": "NSO-001",
            "date": "2020-01-02",
            "quantity": "200",
        }
        self.row_1 = Row.from_csv_line_dict(csv_line_dict=self.csv_line_dict_1)
        self.row_2 = Row.from_csv_line_dict(csv_line_dict=self.csv_line_dict_2)
        self.row_3 = Row.from_csv_line_dict(csv_line_dict=self.csv_line_dict_3)
        self.row_4 = Row.from_csv_line_dict(csv_line_dict=self.csv_line_dict_4)
        self.row_5 = Row.from_csv_line_dict(csv_line_dict=self.csv_line_dict_5)
        self.list_data = [self.row_1, self.row_2, self.row_3, self.row_4, self.row_5]

        self.employee_e001 = Employee.create_employee_from_exhaustive_data(
            employee_id="E001", employee_name="Alice Smith", data=self.list_data
        )
        self.employee_e002 = Employee.create_employee_from_exhaustive_data(
            employee_id="E002", employee_name="Bobby Jones", data=self.list_data
        )

    def tearDown(self):
        pass

    def test_create_employee_from_exhaustive_data(self):
        assert isinstance(self.employee_e001, Employee)

    def test_only_give_employee_events_should_be_in_exhaustive_events(self):
        assert len(self.employee_e001.exhaustive_events) == 3

    def test_only_vest_events_should_be_in_vested_events(self):
        for event in self.employee_e001.vested_events:
            assert event.event != EVENT.get("cancelled")
            assert event.event == EVENT.get("vested")

    def test_only_cancel_events_should_be_in_cancelled_events(self):
        for event in self.employee_e001.cancelled_events:
            assert event.event != EVENT.get("vested")
            assert event.event == EVENT.get("cancelled")

    def test_awards(self):
        assert self.employee_e001.awards == ["ISO-001"]

    def test_target_date(self):
        assert self.employee_e001.target_date == datetime(day=1, month=1, year=2020)

    def test_get_shares_vested_by_target_date_1(self):
        Employee.filter = "2020-01-01"
        assert "NSO-001" in self.employee_e002.get_shares_vested_by_target_date().keys()
        assert self.employee_e002.get_shares_vested_by_target_date()["NSO-001"] == 0

    def test_get_shares_vested_by_target_date_2(self):
        Employee.filter = "2020-02-01"
        assert "ISO-001" in self.employee_e001.get_shares_vested_by_target_date().keys()
        assert self.employee_e001.get_shares_vested_by_target_date()["ISO-001"] == 1000

    def test_check_negative_quantity_error(self):
        Employee.filter = "2020-02-01"
        # print(self.employee_e002.get_shares_vested_by_target_date())
        with self.assertRaises(Exception):
            self.employee_e002.get_shares_vested_by_target_date()
