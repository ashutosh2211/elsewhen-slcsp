# test_slcsp.py
import os
import unittest

from slcsp_calc import Plan, ZipCode, SlcspFinder, read_plans, read_zipcodes, read_slcsp


class TestSlcsp(unittest.TestCase):
    def setUp(self):
        self.plans = [
            Plan("1", "CA", "Silver", 200.0, 1),
            Plan("2", "CA", "Silver", 250.0, 1),
            Plan("3", "CA", "Gold", 300.0, 1),
            Plan("4", "CA", "Silver", 150.0, 2),
            Plan("5", "CA", "Silver", 100.0, 2),
        ]
        self.zip_codes = [
            ZipCode("12345", "CA", [("001", "County1")], [1]),
            ZipCode("54321", "CA", [("002", "County2")], [2]),
            ZipCode("99999", "CA", [("003", "County3")], [3]),
            ZipCode("11111", "CA", [("001", "County1"), ("002", "County2")], [1, 2]),
        ]
        self.slcsp_finder = SlcspFinder(self.plans, self.zip_codes)

    def test_find_slcsp_for_zipcode_valid(self):
        self.assertEqual(self.slcsp_finder.find_slcsp_for_zipcode("12345"), "250.00")
        self.assertEqual(self.slcsp_finder.find_slcsp_for_zipcode("54321"), "150.00")

    def test_find_slcsp_for_zipcode_invalid(self):
        self.assertEqual(self.slcsp_finder.find_slcsp_for_zipcode("00000"), "")

    def test_find_slcsp_for_zipcode_no_silver_plans(self):
        self.assertEqual(self.slcsp_finder.find_slcsp_for_zipcode("99999"), "")

    def test_find_slcsp_for_zipcode_multiple_rate_areas(self):
        self.assertEqual(self.slcsp_finder.find_slcsp_for_zipcode("11111"), "")

    def test_find_slcsp_for_all(self):
        zip_codes = ["12345", "54321", "99999", "11111"]
        expected_results = [("12345", "250.00"), ("54321", "150.00"), ("99999", ""), ("11111", "")]
        self.assertEqual(self.slcsp_finder.find_slcsp_for_all(zip_codes), expected_results)

    def test_read_plans(self):
        file_path = os.path.join(os.path.dirname(__file__), "test_plans.csv")
        plans = read_plans(file_path)
        self.assertEqual(len(plans), 3)
        self.assertEqual(plans[0].plan_id, "1")
        self.assertEqual(plans[1].state, "NY")
        self.assertEqual(plans[2].metal_level, "Gold")

    def test_read_zipcodes(self):
        file_path = os.path.join(os.path.dirname(__file__), "test_zips.csv")
        zip_codes = read_zipcodes(file_path)
        self.assertEqual(len(zip_codes), 2)
        self.assertEqual(zip_codes[0].zip_code, "12345")
        self.assertEqual(zip_codes[1].state, "NY")
        self.assertEqual(zip_codes[0].counties, [("001", "County1")])
        self.assertEqual(zip_codes[1].rate_areas, [1, 2])

    def test_read_slcsp(self):
        file_path = os.path.join(os.path.dirname(__file__), "test_slcsp.csv")
        slcsp_zip_codes = read_slcsp(file_path)
        self.assertEqual(len(slcsp_zip_codes), 3)
        self.assertEqual(slcsp_zip_codes[0], "12345")
        self.assertEqual(slcsp_zip_codes[1], "54321")
        self.assertEqual(slcsp_zip_codes[2], "99999")


if __name__ == "__main__":
    unittest.main()
