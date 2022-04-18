from typing import List
from captable.scripts.row import Row, OutputRow
from captable.scripts.employee import Employee
from dataclasses import field, dataclass


@dataclass
class CapitalizationTable:
    """
    Main class that handles reading storing and creating output
    """

    data: list = field(default_factory=list)
    unique_employees_id_name: List[tuple] = field(default_factory=list)
    employees: List[Employee] = field(default_factory=list)
    output: List[OutputRow] = field(default_factory=list)

    def create_row_data(self, csv_data):
        """
        Method to create all events' data Rows and update uniques pair of employee id and name
        :param csv_data:
        :return:
        """
        unique = []
        for line in csv_data:
            row_obj = Row.from_csv_line_dict(line)
            self.data.append(row_obj)
            unique.append((line["employee_id"], line["employee_name"]))
        self.unique_employees_id_name = list(set(unique))

    def create_employee_data(self):
        """
        Method to create all list of all Employees
        :return:
        """
        for employee_id, employee_name in self.unique_employees_id_name:
            employees_obj = Employee.create_employee_from_exhaustive_data(
                employee_id=employee_id, employee_name=employee_name, data=self.data
            )
            self.employees.append(employees_obj)

    def get_capitalization_table_for_target_date(self):
        """
        Method to print output in required format
        :return:
        """
        out = []
        for employee in self.employees:
            for award in employee.awards:
                output_line_dict = {
                    "employee_id": employee.employee_id,
                    "employee_name": employee.employee_name,
                    "award_id": award,
                    "quantity": employee.get_shares_vested_by_target_date()[award],
                }
                out.append(OutputRow.from_output_line_dict(output_line_dict))

        # Output needs to be sorted as per employee id and award id
        for output in sorted(out, key=lambda x: (x.employee_id, x.award_id)):
            print(output)
