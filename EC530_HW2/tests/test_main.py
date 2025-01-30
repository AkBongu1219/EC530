import unittest
import os
import pandas as pd
import logging

# Configure logging for tests
logging.basicConfig(
    filename="app.log",  # Ensure logs are written to this file
    filemode="w",  # Overwrites previous logs each run
    level=logging.DEBUG,  # Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",
)


from EC530_HW2.EC530_2 import (
    haversine,
    validate_coordinate,
    match_closest_points,
    read_coordinates_from_csv,
    generate_dataframe_from_coordinates,
    match_points_from_csv,
    parse_coordinate,
    dms_to_decimal,
)


class TestGeolocationFunctions(unittest.TestCase):

    ### TEST Haversine ###
    def test_haversine(self):
        # Expected distance should match the function's output
        self.assertAlmostEqual(
            haversine(12.9716, 77.5946, 13.0827, 80.2707), 290.17, places=2
        )

        # Test invalid input handling
        self.assertIsNone(haversine(None, 77.5946, 13.0827, 80.2707))

    ### TEST Coordinate Validation ###
    def test_validate_coordinate(self):
        # Valid latitude
        self.assertEqual(validate_coordinate("45.0", "latitude"), 45.0)

        # Invalid latitude
        self.assertIsNone(validate_coordinate("100.0", "latitude"))

        # Valid longitude
        self.assertEqual(validate_coordinate("90.0", "longitude"), 90.0)

        # Invalid longitude
        self.assertIsNone(validate_coordinate("200.0", "longitude"))

    ### TEST DMS to Decimal Conversion ###
    def test_dms_to_decimal(self):
        self.assertAlmostEqual(dms_to_decimal(45, 30, 15, "N"), 45.5042, places=4)
        self.assertAlmostEqual(dms_to_decimal(45, 30, 15, "S"), -45.5042, places=4)
        self.assertAlmostEqual(dms_to_decimal(120, 15, 30, "E"), 120.2583, places=4)
        self.assertAlmostEqual(dms_to_decimal(120, 15, 30, "W"), -120.2583, places=4)

    ### TEST Parsing Coordinate Formats ###
    def test_parse_coordinate(self):
        # Decimal Degrees
        self.assertEqual(parse_coordinate("45.678"), 45.678)
        self.assertEqual(parse_coordinate("-78.123"), -78.123)

        # Degrees + Direction
        self.assertEqual(parse_coordinate("78 N"), 78.0)
        self.assertEqual(parse_coordinate("78 S"), -78.0)
        self.assertEqual(parse_coordinate("120 W"), -120.0)
        self.assertEqual(parse_coordinate("120 E"), 120.0)

        # DMS Format
        self.assertAlmostEqual(parse_coordinate("45°30'15\" N"), 45.5042, places=4)
        self.assertAlmostEqual(parse_coordinate("45°30'15\" S"), -45.5042, places=4)
        self.assertAlmostEqual(parse_coordinate("120°15'30\" W"), -120.2583, places=4)
        self.assertAlmostEqual(parse_coordinate("120°15'30\" E"), 120.2583, places=4)

        # Invalid Inputs
        self.assertIsNone(parse_coordinate("invalid data"))
        self.assertIsNone(parse_coordinate("100°N"))  # Out of range latitude
        self.assertIsNone(parse_coordinate("190°E"))  # Out of range longitude

    ### TEST Closest Point Matching ###
    def test_match_closest_points(self):
        array1 = [(12.9716, 77.5946), (28.7041, 77.1025)]
        array2 = [(13.0827, 80.2707), (22.5726, 88.3639)]
        matches = match_closest_points(array1, array2)

        # Check distance calculations
        self.assertAlmostEqual(matches[0][2], 290.17, places=2)

        # Test first point matches
        self.assertEqual(matches[0][1], (13.0827, 80.2707))

        # Test second point matches
        self.assertEqual(matches[1][1], (22.5726, 88.3639))

    ### SETUP & TEARDOWN for CSV Tests ###
    def setUp(self):
        """Create temporary CSV files for testing and trigger logging setup."""
        logging.info("Test suite setup started.")  # Test logging works

        with open("test_valid.csv", "w") as f:
            f.write("12.9716,77.5946\n28.7041,77.1025\n")

        with open("test_invalid.csv", "w") as f:
            f.write("invalid_data\n")

        with open("test_valid_2.csv", "w") as f:
            f.write("13.0827,80.2707\n22.5726,88.3639\n")

        with open("test_dms.csv", "w") as f:
            f.write("45°30'15\" N,120°15'30\" W\n60°45'20\" S,90°30'10\" E\n")

    def tearDown(self):
        """Remove temporary CSV files after tests."""
        os.remove("test_valid.csv")
        os.remove("test_invalid.csv")
        os.remove("test_valid_2.csv")
        os.remove("test_dms.csv")

    ### TEST CSV Reading ###
    def test_read_coordinates_from_csv_valid(self):
        """Test reading valid CSV coordinates."""
        coordinates = read_coordinates_from_csv("test_valid.csv")
        expected = [(12.9716, 77.5946), (28.7041, 77.1025)]
        self.assertEqual(coordinates, expected)

    def test_read_coordinates_from_csv_invalid(self):
        """Test handling of invalid CSV input."""
        coordinates = read_coordinates_from_csv("test_invalid.csv")
        self.assertEqual(coordinates, [])

    def test_read_coordinates_from_csv_dms(self):
        """Test reading and converting DMS format coordinates from CSV."""
        coordinates = read_coordinates_from_csv("test_dms.csv")
        expected = [(45.5042, -120.2583), (-60.7556, 90.5028)]

        # Debugging logs to check what was read
        print(f"Read coordinates: {coordinates}")

        self.assertEqual(len(coordinates), len(expected))  # Ensure correct count

        for i in range(len(expected)):
            self.assertAlmostEqual(coordinates[i][0], expected[i][0], places=4)
            self.assertAlmostEqual(coordinates[i][1], expected[i][1], places=4)

    ### TEST Dataframe Generation ###
    def test_generate_dataframe_from_coordinates(self):
        """Test converting coordinates list to DataFrame."""
        coordinates = [(12.9716, 77.5946), (28.7041, 77.1025)]
        df = generate_dataframe_from_coordinates(coordinates)

        # Check DataFrame structure
        self.assertEqual(list(df.columns), ["Latitude", "Longitude"])
        self.assertEqual(len(df), 2)  # Expect 2 rows
        self.assertEqual(df.iloc[0]["Latitude"], 12.9716)
        self.assertEqual(df.iloc[0]["Longitude"], 77.5946)

    ### TEST CSV-Based Point Matching ###
    def test_match_points_from_csv(self):
        """Test matching points using CSV files."""
        match_points_from_csv("test_valid.csv", "test_valid_2.csv")


if __name__ == "__main__":
    unittest.main()
