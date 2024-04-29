from backend.lib.link_service import get_links
from backend.model import Coordinate


def test_get_links_single():
    links = get_links([Coordinate(name="A", lon=0, lat=0), Coordinate(name="B", lon=1, lat=1)])
    assert len(links) == 1
    assert links[0].name == "AB"
    assert 0 < links[0].distance < 157420


def test_get_links_multiple():
    links = get_links(
        [Coordinate(name="A", lon=0, lat=0), Coordinate(name="B", lon=1, lat=1), Coordinate(name="C", lon=2, lat=2)]
    )
    assert len(links) == 3
    assert {link.name for link in links} == {"AB", "AC", "BC"}
    assert all(0 < link.distance < 300000 for link in links)


def test_get_links_empty():
    links = get_links([Coordinate(name="A", lon=0, lat=0)])
    assert len(links) == 0
