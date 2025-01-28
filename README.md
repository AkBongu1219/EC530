# EC530
Commits for the EC530 Course

## ASSIGNMENT 1
### GeoLocation Matcher
This Python script matches random geolocation points (latitude, longitude) from two arrays and calculates the closest points using the Haversine formula to measure distance.

### Features
__Random Geolocation Generation:__ Generates two random valid GPS coordinates arrays.

__Distance Calculation:__ Uses the Haversine formula to calculate the distance between two GPS points.

__Closest Point Matching:__ Matches each point in one array to the closest point in the other array.

### How It Works
Two arrays of random geolocations are generated.
For each point in the first array, the script finds the closest point in the second array based on distance.
Results are printed, showing the closest point and the distance in kilometers.

### References: https://www.geeksforgeeks.org/haversine-formula-to-find-distance-between-two-points-on-a-sphere/

Here’s a professional and well-structured `README.md` file for your `EC530_HW2.py` project. This README provides an overview of the project, explains how to use it, and includes details about installation, testing, and contributions.

---

# EC530_HW2: Geolocation Point Matching

## Overview
This Python script matches each point in one array of GPS coordinates to the closest point in another array using the Haversine formula. The Haversine formula calculates the great-circle distance between two points on the Earth's surface, given their latitude and longitude in decimal degrees.

The project includes:
- A function to calculate the distance between two GPS coordinates using the Haversine formula.
- A function to match each point in the first array to the closest point in the second array.
- Support for both manual input and CSV file input for coordinates.
- Unit tests to validate the functionality.

---

## Features
- **Haversine Distance Calculation**: Accurately computes the distance between two GPS coordinates.
- **Point Matching**: Matches each point in the first array to the closest point in the second array.
- **Input Flexibility**: Supports manual input of coordinates or reading from CSV files.
- **Validation**: Ensures valid latitude and longitude values are provided.
- **Unit Tests**: Includes comprehensive tests to validate the core functionality.

---

## Installation

### Prerequisites
- Python 3.9 or higher
- `pandas` library (for CSV file handling)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/EC530_HW2.git
   cd EC530_HW2
   ```

2. Install the required dependencies:
   ```bash
   pip install pandas
   ```

---

## Usage

### Running the Script
To run the script interactively, execute the following command:
```bash
python EC530_HW2.py
```

You will be prompted to choose between:
1. **Manual Input**: Enter the number of points and their coordinates manually.
2. **CSV File Input**: Provide paths to two CSV files containing the coordinates.

#### Example CSV Format
Each CSV file should contain two columns: `latitude` and `longitude`. For example:
```
latitude,longitude
12.9716,77.5946
28.7041,77.1025
```

### Example Output
```
Closest Point Matches:
Point (12.9716, 77.5946) is closest to (13.0827, 80.2707) with distance: 291.93 km
Point (28.7041, 77.1025) is closest to (22.5726, 88.3639) with distance: 1234.56 km
```

---

## Testing
The project includes unit tests to ensure the correctness of the Haversine formula, coordinate validation, and point matching logic.

### Running Tests
To run the tests, use the following command:
```bash
pytest EC530_HW2/tests
```

### Test Coverage
The tests cover the following:
- **Haversine Formula**: Validates the distance calculation.
- **Coordinate Validation**: Ensures invalid latitude and longitude values are rejected.
- **Point Matching**: Verifies that the closest points are correctly matched.

---

## Code Structure
The project is organized as follows:
```
EC530_HW2/
├── EC530_2.py                # Main script for geolocation point matching
├── tests/
│   └── test_main.py          # Unit tests for the script
├── README.md                 # This file
```

---


