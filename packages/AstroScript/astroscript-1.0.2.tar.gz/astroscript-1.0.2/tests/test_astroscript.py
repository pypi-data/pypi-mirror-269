import pytest
from datetime import datetime
import pytz
from astroscript.astroscript import convert_to_utc, get_coordinates, calculate_house_positions

def test_convert_to_utc():
    # Given
    local_datetime = datetime(2021, 1, 1, 12)  # Noon on New Year's Day
    local_timezone = pytz.timezone("America/New_York")  # Eastern Standard Time
    expected_utc_datetime = datetime(2021, 1, 1, 17, tzinfo=pytz.utc)  # EST is UTC-5

    # When
    result = convert_to_utc(local_datetime, local_timezone)

    # Then
    assert result == expected_utc_datetime, "The UTC conversion did not match the expected result."

from unittest.mock import patch
from geopy.location import Location

# @pytest.fixture
# def mock_geolocator():
#     return patch('your_module.Nominatim')

# def test_get_coordinates(mock_geolocator):
#     # Given
#     location_name = "Empire State Building, New York"
#     expected_coordinates = (40.748817, -73.985428)
#     mock_geolocator.return_value.geocode.return_value = Location(('Empire State Building', (40.748817, -73.985428)))

#     # When
#     result = get_coordinates(location_name)

#     # Then
#     assert result == expected_coordinates, "The coordinates do not match the expected result."

# def test_calculate_house_positions():
#     # Given
#     date = datetime(2021, 1, 1, 12)
#     latitude = 34.052235  # Los Angeles
#     longitude = -118.243683
#     planets_positions = {'Sun': {'longitude': 280.46}}  # Some made-up position
#     expected_house_positions = {'Sun': {'longitude': 280.46, 'house': 6}}  # Expected house might depend on system used

#     # When
#     house_positions, _ = calculate_house_positions(date, latitude, longitude, planets_positions, notime=False, h_sys='P')

#     # Then
#     assert house_positions['Sun']['house'] == expected_house_positions['Sun']['house'], "House positions are incorrect."
