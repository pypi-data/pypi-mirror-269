import os
import json
from pathlib import Path

# Define the directory path for user-specific data
user_data_dir = Path.home() / '.astroscript'
user_data_dir.mkdir(exist_ok=True)  # Create the directory if it doesn't exist

# Define full paths to the JSON files
saved_locations_file = user_data_dir / 'saved_locations.json'
saved_events_file = user_data_dir / 'saved_events.json'

# Function to update or add new entries to the JSON file
def update_json_file(filename, new_data):
    # Check if the file exists
    if os.path.exists(filename):
        # File exists, so read the current data
        with open(filename, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                # File is empty or corrupted
                data = {}
    else:
        # File does not exist, start with an empty dictionary
        data = {}

    # Update the dictionary with new_data
    # This will add new entries and update existing ones with the same keys
    data.update(new_data)

    # Write the updated dictionary back to the file
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def check_and_create_file(file_path):
    """ Ensure the JSON file exists, create it with empty dict if not. """
    if not file_path.exists():
        with open(file_path, 'w') as file:
            json.dump({}, file)  # Create an empty JSON object in the file

def load_location(location_name):
    """
    Load and return the details of a specified location from a JSON file.
    """
    check_and_create_file(saved_locations_file)  # Ensure the file exists
    
    with open(saved_locations_file, 'r') as file:
        data = json.load(file)
    
    return data.get(location_name)

def save_location(location_name, latitude, longitude):
    """
    Save a location with its latitude and longitude to a JSON file.
    """
    check_and_create_file(saved_locations_file)  # Ensure the file exists

    with open(saved_locations_file, 'r+') as file:
        data = json.load(file)
        data[location_name] = {'latitude': latitude, 'longitude': longitude}
        file.seek(0)
        file.truncate()  # Clear the file
        json.dump(data, file, indent=4)

def check_and_create_file(file_path):
    """ Ensure the JSON file exists, create it with an empty dict if not. """
    if not file_path.exists():
        with open(file_path, 'w') as file:
            json.dump({}, file)  # Create an empty JSON object in the file

def load_event(event_name):
    """
    Load and return the details of a specified event from a JSON file.
    """
    check_and_create_file(saved_events_file)  # Ensure the file exists

    with open(saved_events_file, 'r') as file:
        data = json.load(file)

    return data.get(event_name)

def save_event(event_name, details):
    """
    Save event details to a JSON file. 'details' should be a dictionary containing
    event-specific data such as date, time, location, etc.
    """
    check_and_create_file(saved_events_file)  # Ensure the file exists

    with open(saved_events_file, 'r+') as file:
        data = json.load(file)
        data[event_name] = details
        file.seek(0)
        file.truncate()  # Clear the file
        json.dump(data, file, indent=4)

def update_event(event_name, new_details):
    """
    Update existing event details. This function assumes that the event already exists.
    """
    check_and_create_file(saved_events_file)  # Ensure the file exists

    with open(saved_events_file, 'r+') as file:
        data = json.load(file)
        if event_name in data:
            data[event_name].update(new_details)
        else:
            return f"Event named {event_name} does not exist."
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=4)

def delete_event(event_name):
    """
    Delete an event from the JSON file.
    """
    check_and_create_file(saved_events_file)  # Ensure the file exists

    with open(saved_events_file, 'r+') as file:
        data = json.load(file)
        if event_name in data:
            del data[event_name]
        else:
            return f"Event named {event_name} does not exist."
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=4)
        
# Example new data to add/update
# new_people_data = {
#     "John Doe": {
#         "location": "Gothenburg, Sweden",
#         "datetime": datetime(1990, 5, 24, 14, 30).isoformat(),
#         "latitude": 57.7089,
#         "longitude": 11.9746
#     },
#     "Alice Johnson": {
#         "location": "Malmö, Sweden",
#         "datetime": datetime(1992, 11, 5, 8, 45).isoformat(),
#         "latitude": 55.6050,
#         "longitude": 13.0038
#     },
#     "Pelle Hansson": {
#         "location": "Stockholm, Sweden",
#         "datetime": datetime(1932, 3, 12, 10, 45).isoformat(),
#         "latitude": 555.6050,
#         "longitude": 13.0038
#     },
# }