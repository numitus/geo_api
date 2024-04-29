import pytest

from backend.lib.geocode_service import GeocodeService
from backend.model import Coordinate


@pytest.mark.asyncio
async def test_get_geocode_success(httpx_mock):
    api_key = "test_api_key"  # pragma: allowlist secret
    service = GeocodeService(api_key)
    expected_result = "Mocked Address"
    mock_response = {"display_name": expected_result}
    # First attempt to connect will raise ConnectionError
    httpx_mock.add_exception(ConnectionError("Connection error"))

    httpx_mock.add_response(json=mock_response)

    result = await service.get_geocode(10.123, 20.456)

    assert result == expected_result


@pytest.mark.asyncio
async def test_get_geocode_retry_on_error(httpx_mock):
    api_key = "test_api_key"  # pragma: allowlist secret
    service = GeocodeService(api_key)
    httpx_mock.add_exception(ConnectionError("Connection error"))

    with pytest.raises(Exception):
        await service.get_geocode(10.123, 20.456)


@pytest.mark.asyncio
async def test_get_geocode_handles_unable_to_geocode(httpx_mock):
    api_key = "test_api_key"  # pragma: allowlist secret
    service = GeocodeService(api_key)
    mock_response = {"error": "Unable to geocode"}
    httpx_mock.add_response(json=mock_response)

    result = await service.get_geocode(10.123, 20.456)

    assert result == "Unable to geocode"


def test_batch_request(httpx_mock):
    api_key = "test_api_key"  # pragma: allowlist secret
    service = GeocodeService(api_key)
    coordinates = [Coordinate(name="A", lon=10.1, lat=20.2), Coordinate(name="B", lon=30.3, lat=40.4)]
    expected_results = ["Address1", "Address2"]
    mock_responses = [{"display_name": address} for address in expected_results]
    for response in mock_responses:
        httpx_mock.add_response(json=response)

    results = service.batch_request(coordinates)

    assert results == expected_results
