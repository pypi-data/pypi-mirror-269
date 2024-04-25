from convert.converter import Converter
from sqlalchemy import Engine


class MMSIConverter(Converter):
    """Convert MMSI numbers to other formats.

    This class requires a connection to a database containing the relevant data.
    """

    def __init__(self, engine: Engine) -> None:
        super().__init__(engine)

    def to_imo(self, mmsi: str) -> str:
        """Convert an MMSI number to an IMO number.

        Args:
            mmsi: The MMSI number to convert.

        Returns:
            The IMO number.
        """

        return self.convert_within_table(
            from_format="mmsi",
            to_format="imo",
            table="public.dim_ship",
            value=mmsi)

    def to_callsign(self, mmsi: str) -> str:
        """Convert an MMSI number to a callsign.

        Args:
            mmsi: The MMSI number to convert.

        Returns:
            The callsign.
        """

        return self.convert_within_table(
            from_format="mmsi",
            to_format="callsign",
            table="public.dim_ship",
            value=mmsi)
