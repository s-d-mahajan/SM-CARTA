from datetime import datetime
from typing import List
from captable.config import DATE_FORMAT
from captable.scripts.row import Row
from captable.config import EVENT


class Employee:
    """
    Class to store data corresponding to each unique employee
    """

    employee_id: str
    employee_name: str
    exhaustive_events: list
    filter: str
    awards: list
    vested_events: list
    cancelled_events: list

    def __init__(self, employee_id, employee_name, exhaustive_events):
        self.employee_id = employee_id
        self.employee_name = employee_name
        self.exhaustive_events = exhaustive_events

    @property
    def vested_events(self):
        """
        Stores all vested events Rows for give employee
        :return:
        """
        vested_events = []
        for row_data in self.exhaustive_events:
            if row_data.event == EVENT.get("vested"):
                vested_events.append(row_data)
        return vested_events

    @property
    def cancelled_events(self):
        """
        Stores all cancelled events Rows for give employee
        :return:
        """
        cancelled_events = []
        for row_data in self.exhaustive_events:
            if row_data.event == EVENT.get("cancelled"):
                cancelled_events.append(row_data)
        return cancelled_events

    @property
    def awards(self):
        """
        Store unique award ids that a give employee has received
        :return:
        """
        unique_awards = []
        for row_data in self.exhaustive_events:
            unique_awards.append(row_data.award_id)
        return list(sorted(set(unique_awards)))

    @property
    def target_date(self):
        """
        Stores target date for which we want to calculate the vesting schedule for
        :return:
        """
        return datetime.strptime(self.filter, DATE_FORMAT)

    def get_shares_vested_by_target_date(self) -> dict:
        """
        Calculates the shares vested per award by target date
        :return:
        """
        vested_shares_per_award = {}
        for award in self.awards:
            vested_shares_total = 0
            cancelled_shares_total = 0
            for row_data in self.vested_events:
                if (
                    row_data.award_id == award
                    and row_data.award_date <= self.target_date
                ):
                    vested_shares_total += row_data.quantity
            for row_data in self.cancelled_events:
                if (
                    row_data.award_id == award
                    and row_data.award_date <= self.target_date
                ):
                    cancelled_shares_total += row_data.quantity
            total_shares = vested_shares_total - cancelled_shares_total
            if total_shares < 0:
                # Check to confirm the vested share on a target date are not negative
                raise Exception(
                    "Vested - Cancelled shares by target date should not be negative"
                )
            else:
                vested_shares_per_award.update({award: total_shares})
        return vested_shares_per_award

    @classmethod
    def create_employee_from_exhaustive_data(
        cls, employee_id: str, employee_name: str, data: List[Row]
    ):
        """
        Method to create Employee
        The assumption is each employee has unique employee id
        :param employee_name:
        :param employee_id:
        :param data:
        :return:
        """
        events_of_employee = []
        for row_data in data:
            if row_data.employee_id == employee_id:
                events_of_employee.append(row_data)
        return cls(
            employee_id=employee_id,
            employee_name=employee_name,
            exhaustive_events=events_of_employee,
        )
