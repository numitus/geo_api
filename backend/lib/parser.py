import csv
from io import StringIO

from backend.model import Coordinate


def parse_csv(csv_data: str) -> list[Coordinate]:
    """
    Parse the content of a CSV file and return a list of coordinates.
    """
    reader = csv.DictReader(StringIO(csv_data), delimiter=",", quotechar="\\")
    headers = reader.fieldnames
    if set(headers) != {"Point", "Latitude", "Longitude"}:
        raise Exception("Invalid CSV file")
    points: list[Coordinate] = []
    for row in reader:
        name = row["Point"].strip()
        latitude = float(row["Latitude"])
        longitude = float(row["Longitude"])
        points.append(Coordinate(name=name, lat=latitude, lon=longitude))
    return points
