from pyproj import Geod

from backend.model import Coordinate, Link


geoid = Geod(ellps="WGS84")  # Assume that ellipsoid is WGS84, which is used in GPS


def get_links(coordinates: list[Coordinate]) -> list[Link]:
    """Get links between all points in coordinates list"""
    result = []
    for i in range(len(coordinates) - 1):
        for j in range(i + 1, len(coordinates)):
            point_1 = coordinates[i]
            point_2 = coordinates[j]
            length = geoid.line_length([point_1.lon, point_2.lon], [point_2.lat, point_2.lat])
            result.append(Link(name=point_1.name + point_2.name, distance=length))
    return result
