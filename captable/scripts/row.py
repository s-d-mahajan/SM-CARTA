from dataclasses import dataclass, field
from datetime import datetime
from captable.config import DATE_FORMAT


@dataclass
class Row:
    """
    Class to store the input event data
    """

    event: str
    employee_id: str
    employee_name: str
    award_id: str
    award_date_str: str
    quantity_string: str

    @classmethod
    def from_csv_line_dict(cls, csv_line_dict: dict):
        """
        Method to create Row for each event
        :param csv_line_dict:
        :return:
        """
        event = csv_line_dict.get("event")
        employee_id = csv_line_dict.get("employee_id")
        employee_name = csv_line_dict.get("employee_name")
        award_id = csv_line_dict.get("award_id")
        award_date_str = csv_line_dict.get("date")
        quantity_string = csv_line_dict.get("quantity")
        return cls(
            event=event,
            employee_id=employee_id,
            employee_name=employee_name,
            award_id=award_id,
            award_date_str=award_date_str,
            quantity_string=quantity_string,
        )

    @property
    def quantity(self):
        """
        Stores the float value of share quantity
        :return:
        """
        return float(self.quantity_string)

    @property
    def award_date(self):
        """
        Stores the award date in datetime format
        :return:
        """
        return datetime.strptime(self.award_date_str, DATE_FORMAT)


@dataclass()
class OutputRow:
    """
    Class to store the output vesting schedule
    """

    employee_id: str
    employee_name: str
    award_id: str
    quantity: float
    resolution = 0

    @classmethod
    def from_output_line_dict(cls, output_line_dict: dict):
        """
        Method to create OutputRow for each output line
        :param output_line_dict:
        :return:
        """
        employee_id = output_line_dict.get("employee_id")
        employee_name = output_line_dict.get("employee_name")
        award_id = output_line_dict.get("award_id")
        quantity = output_line_dict.get("quantity")

        return cls(
            employee_id=employee_id,
            employee_name=employee_name,
            award_id=award_id,
            quantity=quantity,
        )

    def __str__(self):
        """
        Special method to print the output in the right format
        :return:
        """
        return f"{self.employee_id},{self.employee_name},{self.award_id},{self.quantity:.{self.resolution}f}"
