import unittest
from EC530_2 import haversine, validate_coordinate, match_closest_points

class TestGeolocationFunctions(unittest.TestCase):
    def test_haversine(self):
        # Test valid distance
        self.assertAlmostEqual(haversine(12.9716, 77.5946, 13.0827, 80.2707), 291.93, places=2)

        # Test invalid input handling
        self.assertIsNone(haversine(None, 77.5946, 13.0827, 80.2707))

    def test_validate_coordinate(self):
        # Valid latitude
        self.assertEqual(validate_coordinate("45.0", "latitude"), 45.0)

        # Invalid latitude
        self.assertIsNone(validate_coordinate("100.0", "latitude"))

        # Valid longitude
        self.assertEqual(validate_coordinate("90.0", "longitude"), 90.0)

        # Invalid longitude
        self.assertIsNone(validate_coordinate("200.0", "longitude"))

    def test_match_closest_points(self):
        array1 = [(12.9716, 77.5946), (28.7041, 77.1025)]
        array2 = [(13.0827, 80.2707), (22.5726, 88.3639)]
        matches = match_closest_points(array1, array2)

        # Test first point matches
        self.assertEqual(matches[0][1], (13.0827, 80.2707))
        self.assertAlmostEqual(matches[0][2], 291.93, places=2)

        # Test second point matches
        self.assertEqual(matches[1][1], (22.5726, 88.3639))

if __name__ == "__main__":
    unittest.main()
