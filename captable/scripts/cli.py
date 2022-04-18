import click
import csv
from captable.config import CSV_FILE_HEADERS
from captable.scripts.row import OutputRow
from captable.scripts.employee import Employee
from captable.scripts.capitalization import CapitalizationTable


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.argument("target_date", required=True)
@click.argument("precision", required=False)
def captable(filename, target_date, precision):

    capitalization = CapitalizationTable()
    # set the target date for which we want vesting schedule
    Employee.filter = target_date
    # set output precision
    if precision:
        OutputRow.resolution = int(precision)

    # read data
    with open(filename, "r") as csv_file:
        csv_data = csv.DictReader(csv_file, fieldnames=CSV_FILE_HEADERS)
        capitalization.create_row_data(csv_data)

    # create data per employee
    capitalization.create_employee_data()

    # get vesting schedule
    capitalization.get_capitalization_table_for_target_date()
