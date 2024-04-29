import pytest

from backend.lib.parser import parse_csv
from backend.model import Coordinate


@pytest.fixture
def sample_csv_data():
    return """Point,Latitude,Longitude
    A,50.448069,30.5194453
    B,50.448616,30.5116673
    C,50.913788,34.7828343"""


def test_parse_csv(sample_csv_data):
    expected_points = [
        Coordinate(name="A", lat=50.448069, lon=30.5194453),
        Coordinate(name="B", lat=50.448616, lon=30.5116673),
        Coordinate(name="C", lat=50.913788, lon=34.7828343),
    ]
    parsed_points = parse_csv(sample_csv_data)
    assert len(parsed_points) == len(expected_points)
    for parsed_point, expected_point in zip(parsed_points, expected_points):
        assert parsed_point.name == expected_point.name
        assert parsed_point.lat == expected_point.lat
        assert parsed_point.lon == expected_point.lon


def test_parse_csv_invalid_data():
    with pytest.raises(Exception):
        parse_csv("Invalid CSV data")
