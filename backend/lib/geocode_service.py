import asyncio

import httpx

from backend.lib.repeater import repeat_on_error
from backend.model import Coordinate


BASE_URL = "https://geocode.maps.co/reverse"


class GeocodeService:
    """Geocode service class based on free geocode.maps.com API"""

    def __init__(self, api_key):
        self.api_key = api_key

    @repeat_on_error(retries=5)
    async def get_geocode(self, lon: float, lat: float) -> str:
        """Get geocode from coordinates"""

        async with httpx.AsyncClient() as client:
            response = await client.get(BASE_URL, params={"lat": lat, "lon": lon, "api_key": self.api_key})
            if response.json().get("error") == "Unable to geocode":
                return "Unable to geocode"
            return response.json()["display_name"]

    def batch_request(self, coordinates: list[Coordinate]) -> list[Coordinate]:
        """Batch request for geocodes"""
        return asyncio.run(self._batch_request(coordinates))

    async def _batch_request(self, coordinates: list[Coordinate]) -> list[Coordinate]:
        """Batch request for geocodes"""
        return await asyncio.gather(*[self.get_geocode(point.lon, point.lat) for point in coordinates])
