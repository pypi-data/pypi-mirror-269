"""Module containing the abstract superclass for exporters."""
from abc import ABC, abstractmethod
from pathlib import Path
from sqlalchemy import Engine, CursorResult
from aau_ais_core.connections import PostgreSQLConnection


class NoDataFoundError(Exception):
    """Raised when there is no data to export."""

    def __init__(self, message: str = "No data found for the given parameters"):
        super().__init__(message)


# TODO: Look into using an interface instead of an abstract class.
class Exporter(ABC):
    """Abstract superclass for exporters.

    Used to export data from the data warehouse to a particular format.
    """

    @property
    @abstractmethod
    def sql_dir(self) -> Path:
        """
        Return the path to the directory containing the SQL files for the exporter.

        Each exporter should have its own directory containing the SQL files needed for the export.
        Each SQL file should be named according to the query it contains, have the .sql extension, and expect the same
        unique set of parameters.
        """
        pass

    def __init__(self, engine: Engine, *, export_path: Path = None,) -> None:
        """Initialize the exporter with the given configuration.

        Args:
            export_path: The path to the directory to export the data to.
            engine: The engine to use for connecting to the data warehouse.
        """
        self.export_path = export_path
        self.connection = PostgreSQLConnection(engine)
        self.params = {}

    def set_export_path(self, export_path: Path) -> None:
        """Set the path to export the data to."""
        self.export_path = export_path

    @abstractmethod
    def _validate_params(self) -> None:
        """Validate that all expected parameters are present in the params dictionary (self.params).

        Should do the following:
        - Check that all expected parameters are present, raising a ValueError if any are missing.
        - Check that all parameters are of the correct type, raising a TypeError if any are not.
        - If all parameters are present and of the correct type, do nothing.

        This method is called by set_params() to ensure that the parameters are validated before being used.
        """
        pass

    def set_params(self, params: dict) -> None:
        """Set the parameters for other methods to use, e.g., for generating the query and exporting the data."""
        self._validate_params()
        self.params = params

    @abstractmethod
    def _get_file_name(self) -> str:
        """Return the file name for the exported file.

        File name must be unique, given a unique set of parameters in the params dictionary (self.params).
        """
        pass

    @abstractmethod
    def _get_file_extension(self) -> str:
        """Return the file extension for the exported file, including the leading period.

        For example, return '.csv' for a CSV file, '.json' for a JSON file, etc.
        """
        pass

    def _get_file_path(self) -> Path:
        """Return the full file path for the exported file."""
        return Path(self.export_path, self._get_file_name() + self._get_file_extension())

    def file_exists(self) -> bool:
        """Return whether the exported file already exists."""
        return self._get_file_path().exists()

    @staticmethod
    def _read_sql_file(sql_file: Path) -> str:
        """Read the contents of an SQL file and return it as a string.

        Args:
            sql_file: The path to the SQL file to read.
        """
        if not sql_file.exists():
            raise FileNotFoundError(f"SQL file not found: {sql_file}")

        if sql_file.suffix != ".sql":
            raise ValueError(f"Invalid file extension: {sql_file}, expected .sql file.")

        return sql_file.read_text()

    @abstractmethod
    def get_query(self) -> str:
        """Get the final SQL query to be executed by the exporter.

        Params should not be interpolated into the query string, but can be used to determine the correct query file(s)
        to fetch from the SQL directory and how to format the final query.

        For example, if the param 'type' is 'count', the query should be fetched from the file 'count.sql', whereas if
        the param 'type' is 'sum', the query should be fetched from the file 'sum.sql'.
        """
        pass

    @abstractmethod
    def _save_result(self, result: CursorResult) -> None:
        """Write the results of the query to the exported file.

        Args:
            result: The result of the query as a CursorResult object.

        The implementation of this method should write the results to the exported file to the path returned by
        _get_file_path(). The format of the results will depend on the exporter, e.g., a CSV exporter will write the
        results as a CSV file, a JSON exporter will write the results as a JSON file, etc.
        """
        pass

    def export(self, params: dict) -> None:
        """Export data from the data warehouse to a particular format.

        Args:
            params: A dictionary of parameters to use for the export.
        """
        if self.export_path is None:
            raise ValueError("Export path must be set before exporting data.")

        if self.file_exists():
            raise FileExistsError(f"File already exists at {self._get_file_path()}")

        self.set_params(params)

        query = self.get_query()

        result = self.connection.execute_sql(
            sql=query,
            params=self.params
        )

        if result.fetchone() is None:
            raise NoDataFoundError()

        self._get_file_path().mkdir(parents=True, exist_ok=True)

        self._save_result(result)
