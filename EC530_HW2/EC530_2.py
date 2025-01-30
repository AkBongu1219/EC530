import math
import random
import csv
import pandas as pd
import re

# Haversine formula to calculate the distance between two GPS coordinates
def haversine(lat1, lon1, lat2, lon2):
    try:
        # Distance between latitudes and longitudes
        dLat = (lat2 - lat1) * math.pi / 180.0
        dLon = (lon2 - lon1) * math.pi / 180.0

        # Convert to radians
        lat1 = lat1 * math.pi / 180.0
        lat2 = lat2 * math.pi / 180.0

        # Apply Haversine formula
        a = pow(math.sin(dLat / 2), 2) + pow(math.sin(dLon / 2), 2) * math.cos(
            lat1
        ) * math.cos(lat2)
        rad = 6371  # Radius of Earth in kilometers
        c = 2 * math.asin(math.sqrt(a))
        return rad * c
    except Exception as e:
        print(f"Error in haversine calculation: {e}")
        return None


# Function to convert DMS (Degrees, Minutes, Seconds) to Decimal Degrees
def dms_to_decimal(degrees, minutes, seconds, direction):
    decimal_value = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if direction in ["S", "W"]:  # South or West should be negative
        decimal_value *= -1
    return decimal_value


# Function to parse latitude/longitude from decimal or DMS format
def parse_coordinate(value):
    try:
        # Check if it's in decimal degrees (e.g., "45.678")
        if re.match(r"^-?\d+(\.\d+)?$", value):
            return float(value)

        # Check if it's in DMS format with direction (e.g., "45°30'15\" N")
        match = re.match(r"(\d+)°(\d+)'(\d+)\"?\s*([NSEW])", value, re.IGNORECASE)
        if match:
            degrees, minutes, seconds, direction = match.groups()
            return dms_to_decimal(
                int(degrees), int(minutes), int(seconds), direction.upper()
            )

        # Check if it's in degrees + direction format (e.g., "78 N", "78 S")
        match = re.match(r"(-?\d+(\.\d+)?)\s*([NSEW])", value, re.IGNORECASE)
        if match:
            degrees, _, direction = match.groups()
            return (
                float(degrees) if direction.upper() in ["N", "E"] else -float(degrees)
            )

        raise ValueError(f"Invalid coordinate format: {value}")

    except Exception as e:
        print(f"Error parsing coordinate: {e}")
        return None


# Function to validate and parse input coordinates
def validate_coordinate(coord, coord_type="latitude"):
    try:
        coord = parse_coordinate(coord)
        if coord is None:
            return None
        if coord_type == "latitude" and (-90 <= coord <= 90):
            return coord
        elif coord_type == "longitude" and (-180 <= coord <= 180):
            return coord
        else:
            raise ValueError(f"{coord_type.capitalize()} out of bounds: {coord}")
    except ValueError as e:
        print(f"Invalid {coord_type}: {e}")
        return None


# Function to match points in array1 to the closest point in array2
def match_closest_points(array1, array2):
    closest_points = []
    for point1 in array1:
        lat1, lon1 = point1
        closest_point = None
        min_distance = float("inf")
        for point2 in array2:
            lat2, lon2 = point2
            distance = haversine(lat1, lon1, lat2, lon2)
            if distance is not None and distance < min_distance:
                min_distance = distance
                closest_point = point2
        closest_points.append((point1, closest_point, min_distance))
    return closest_points


# Function to read coordinates from CSV file and return as a list of tuples
def read_coordinates_from_csv(file_path):
    coordinates = []
    try:
        with open(file_path, newline="") as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if len(row) == 2:  # Ensure there are exactly two columns (lat, lon)
                    lat = validate_coordinate(row[0], "latitude")
                    lon = validate_coordinate(row[1], "longitude")
                    if lat is not None and lon is not None:
                        coordinates.append((lat, lon))
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    return coordinates


# Function to generate a dataframe for dynamic testing
def generate_dataframe_from_coordinates(coordinates):
    df = pd.DataFrame(coordinates, columns=["Latitude", "Longitude"])
    return df


# Function to match closest points from two arrays read from CSV files
def match_points_from_csv(file1, file2):
    array1 = read_coordinates_from_csv(file1)
    array2 = read_coordinates_from_csv(file2)

    if array1 and array2:
        print("\nMatching Closest Points from CSV Coordinates:")
        matches = match_closest_points(array1, array2)
        for point1, closest_point, distance in matches:
            print(
                f"Point {point1} is closest to {closest_point} with distance: {distance:.2f} km"
            )
    else:
        print("One or both arrays are empty. Please check your CSV files.")


# Function to allow static input for testing
def manual_input_coordinates():
    array1 = []
    array2 = []

    format_choice = input(
        "Enter coordinate format (1 for Decimal Degrees, 2 for DMS): "
    )

    num_points = int(input("Enter the number of points for each array: "))

    print("\nEnter coordinates for Array 1:")
    for _ in range(num_points):
        lat = input("Enter latitude: ")
        lon = input("Enter longitude: ")
        array1.append(
            (
                validate_coordinate(lat, "latitude"),
                validate_coordinate(lon, "longitude"),
            )
        )

    print("\nEnter coordinates for Array 2:")
    for _ in range(num_points):
        lat = input("Enter latitude: ")
        lon = input("Enter longitude: ")
        array2.append(
            (
                validate_coordinate(lat, "latitude"),
                validate_coordinate(lon, "longitude"),
            )
        )

    return array1, array2


# Main function to run the script interactively
def main():
    print("Choose an option:")
    print("1. Manually input coordinates")
    print("2. Read coordinates from CSV files")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        array1, array2 = manual_input_coordinates()
    elif choice == "2":
        file1 = input("Enter the path to the first CSV file: ")
        file2 = input("Enter the path to the second CSV file: ")
        array1 = read_coordinates_from_csv(file1)
        array2 = read_coordinates_from_csv(file2)
    else:
        print("Invalid choice. Exiting.")
        return

    if array1 and array2:
        print("\nClosest Point Matches:")
        matches = match_closest_points(array1, array2)
        for point1, closest_point, distance in matches:
            print(
                f"Point {point1} is closest to {closest_point} with distance: {distance:.2f} km"
            )
    else:
        print("One or both arrays are empty. Please check your input.")


# Ensure the script only runs interactively when executed directly
if __name__ == "__main__":
    main()
