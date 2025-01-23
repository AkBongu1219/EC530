import math
import random

# Haversine formula to calculate the distance between two GPS coordinates
def haversine(lat1, lon1, lat2, lon2):
     
    # Distance between latitudes and longitudes
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0
 
    # Convert to radians
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0
 
    # Apply Haversine formula
    a = (pow(math.sin(dLat / 2), 2) + pow(math.sin(dLon / 2), 2) * math.cos(lat1) * math.cos(lat2))
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    return rad * c

# Function to match points in array1 to the closest point in array2
def match_closest_points(array1, array2):
    closest_points = []
    for point1 in array1:
        lat1, lon1 = point1
        closest_point = None
        min_distance = float('inf')
        for point2 in array2:
            lat2, lon2 = point2
            distance = haversine(lat1, lon1, lat2, lon2)
            if distance < min_distance:
                min_distance = distance
                closest_point = point2
        closest_points.append((point1, closest_point, min_distance))
    return closest_points

# Function to generate a random geolocation (latitude, longitude)
def generate_random_geolocation():
    lat = random.uniform(-90, 90)  # Latitude range
    lon = random.uniform(-180, 180)  # Longitude range
    return (lat, lon)

# Function to generate two arrays of random geolocations
def generate_random_arrays(num_points=5):
    array1 = [generate_random_geolocation() for _ in range(num_points)]
    array2 = [generate_random_geolocation() for _ in range(num_points)]
    return array1, array2

# Generate random arrays of geolocations
array1, array2 = generate_random_arrays(num_points=5)

# Output the generated arrays
print("\nArray 1 (Random Geolocations):")
for point in array1:
    print(point)

print("\nArray 2 (Random Geolocations):")
for point in array2:
    print(point)

# Get closest points
matches = match_closest_points(array1, array2)

# Output results
print("\nClosest Point Matches:")
for point1, closest_point, distance in matches:
    print(f"Point {point1} is closest to {closest_point} with distance: {distance:.2f} km")
