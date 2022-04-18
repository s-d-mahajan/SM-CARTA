import unittest
from click.testing import CliRunner
from captable.scripts.cli import captable
from unittest.mock import patch
from captable.scripts.row import OutputRow


class Testcli(unittest.TestCase):
    def setUp(self):
        OutputRow.resolution = 0

    def tearDown(self):
        OutputRow.resolution = 0

    def test_captable_command(self):
        runner = CliRunner()
        result = runner.invoke(captable, ["example.csv", "2027-02-01", "8"])
        assert result.exit_code == 0

    def test_invalid_path_input(self):
        runner = CliRunner()
        runner.invoke(captable, ["/Users/test", "2027-02-01", "8"])
        assert SystemExit

    def test_target_date_required(self):
        runner = CliRunner()
        result = runner.invoke(captable, ["example.csv"])
        assert "Missing argument 'TARGET_DATE'" in result.stdout

    def test_path_required(self):
        runner = CliRunner()
        result = runner.invoke(
            captable,
        )
        assert "Missing argument 'FILENAME'" in result.stdout

    @patch("captable.scripts.cli.CapitalizationTable")
    def test_capitalizationtable_was_initialised(self, MockCapitalizationTable):
        runner = CliRunner()
        result = runner.invoke(captable, ["example.csv", "2027-02-01", "8"])
        assert MockCapitalizationTable.called
