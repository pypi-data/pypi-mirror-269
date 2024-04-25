"""Module for exporting map data as tiffs files from the DIPAAL data warehouse."""

from .exporter import Exporter
from sqlalchemy import Engine, CursorResult
from pathlib import Path
from aau_ais_utilities.engines import dipaal_engine
from pydantic import BaseModel, field_validator
from typing import Optional


class MapParams(BaseModel):
    START_DATE: int
    END_DATE: int
    RESOLUTION: int
    CONFIDENCE: float
    MOBILE_TYPE: str
    RASTER_TYPE: str
    ENC: str
    SHIP_TYPE: str
    MONTHLY: Optional[bool] = False

    @field_validator("CONFIDENCE")
    def validate_confidence(cls, value):
        if value < 0 or value > 1:
            raise ValueError("CONFIDENCE must be between 0 and 1.")
        return value

    @field_validator("START_DATE", "END_DATE")
    def validate_dates(cls, values):
        if values["START_DATE"] > values["END_DATE"]:
            raise ValueError("START_DATE must be before or equal to END_DATE.")
        return values

    @field_validator("RESOLUTION")
    def validate_resolution(cls, value):
        if value not in [50, 200, 1000, 5000]:
            raise ValueError("RESOLUTION must be one of 50, 200, 1000, or 5000.")
        return value


class MapExporter(Exporter):
    """Class for exporting map data as tiffs files from the DIPAAL data warehouse."""

    @property
    def sql_dir(self) -> Path:
        """Return the path to the directory containing the SQL files for the map exporter."""
        return Path(__file__).parent.joinpath("sql").joinpath("map_exporter")

    def __init__(self, *, export_path: Path, engine: Engine = dipaal_engine) -> None:
        super().__init__(export_path=export_path, engine=engine)

    def validate_enc(self) -> None:
        """Check if the ENC exists in the database."""
        query = self._read_sql_file(Path(self.sql_dir, "exists", "enc.sql"))
        result = self.connection.execute(query, self.params)

        if int(result.fetchone()[0]) == 0:
            raise ValueError(f"ENC {self.params['ENC']} does not exist in the database.")

    def validate_ship_type(self) -> None:
        """Check if the ship type exists in the database."""
        query = self._read_sql_file(Path(self.sql_dir, "exists", "ship_type.sql"))
        result = self.connection.execute(query, self.params)

        if int(result.fetchone()[0]) == 0:
            raise ValueError(f"Ship type {self.params['SHIP_TYPE']} does not exist in the database.")

    def _validate_params(self) -> None:
        """Validate that all expected parameters are present in the params dictionary (self.params)."""
        params_model = MapParams(**self.params)

        self.validate_enc()
        self.validate_ship_type()


    def _get_file_name(self) -> str:
        """Return the file name for the exported file."""

        file_name = (f"enc_{self.params['ENC']}_"
                     f"date_{self.params['START_DATE']}_{self.params['END_DATE']}_"
                     f"res_{self.params['RESOLUTION']}_"
                     f"conf_{self.params['CONFIDENCE']}_"
                     f"mob_{self.params['MOBILE_TYPE']}_"
                     f"raster_{self.params['RASTER_TYPE']}_"
                     f"st_{self.params['SHIP_TYPE']}")

        return file_name

    def _get_file_extension(self) -> str:
        """Return the file extension for the exported file."""
        return ".tiff"

    def _monthly_query(self) -> str:
        """Return the query to use for exporting the map data monthly."""
        query = self.sql_dir.joinpath("monthly.sql").read_text()
        pass

    def get_query(self) -> str:
        """Return the query to use for exporting the map data."""
        monthly = self.params.get("MONTHLY", False)

        if monthly:
            return self._monthly_query()

    def _save_result(self, result: CursorResult) -> None:

        result = result.fetchone()[0]

        with open(self._get_file_path(), "wb") as file:
            file.write(result)
