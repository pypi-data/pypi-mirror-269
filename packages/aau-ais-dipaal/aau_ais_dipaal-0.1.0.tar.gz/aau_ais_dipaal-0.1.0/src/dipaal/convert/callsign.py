from convert.converter import Converter
from sqlalchemy import Engine


class CallsignConverter(Converter):
    """Convert callsigns to other formats.

    This class requires a connection to a database containing the relevant data.
    """

    def __init__(self, engine: Engine) -> None:
        super().__init__(engine)

    def to_mmsi(self, callsign: str) -> str:
        """Convert a callsign to an MMSI number.

        Args:
            callsign: The callsign to convert.

        Returns:
            The MMSI number.
        """

        return self.convert_within_table(
            from_format="callsign",
            to_format="mmsi",
            table="public.dim_ship",
            value=callsign)


    def to_imo(self, callsign: str) -> str:
        """Convert a callsign to an IMO number.

        Args:
            callsign: The callsign to convert.

        Returns:
            The IMO number.
        """

        return self.convert_within_table(
            from_format="callsign",
            to_format="imo",
            table="public.dim_ship",
            value=callsign)


# Example usage:
if __name__ == "__main__":

    from sqlalchemy import create_engine

    user = "jupyter"
    password = "thick40ice43"
    host = "s1.dipaal.dk"
    port = "30036"
    database = "dipaal2"

    engine = create_engine(f'postgresql+psycopg://{user}:{password}@{host}:{port}/{database}')

    callsign_converter = CallsignConverter(engine)
    print(callsign_converter.to_mmsi("VRES3"))