import unittest
import os
from osu_mapper import osu_parser

class TestOsuParser(unittest.TestCase):

    def setUp(self):
        # Path to the test file. Note: This assumes the test is run from the project root.
        # This is a bit fragile, but fine for our purposes.
        self.test_file_path = os.path.join(
            "C:", os.sep, "Users", "river", ".gemini", "tmp", 
            "be193df148da9dc89bbdc73ec8922bdbb09c4f63ea297764ce3b61baf725d0c5",
            "beatmap_765778",
            "Icon For Hire - Make a Move (Speed Up Ver.) (Sotarks) [Riven's Extreme].osu"
        )

    def test_parse_osu_file(self):
        """
        Tests that the .osu file parser correctly extracts data from a real beatmap file.
        """
        self.assertTrue(os.path.exists(self.test_file_path), f"Test file not found at: {self.test_file_path}")
        
        beatmap = osu_parser.parse_osu_file(self.test_file_path)

        # 1. Assert that parsing was successful
        self.assertIsNotNone(beatmap)

        # 2. Assert metadata is parsed correctly
        self.assertEqual(beatmap.title, "Make a Move (Speed Up Ver.)")
        self.assertEqual(beatmap.artist, "Icon For Hire")
        self.assertEqual(beatmap.creator, "Sotarks")
        self.assertEqual(beatmap.version, "Riven's Extreme")

        # 3. Assert that we have data for timing points and hit objects
        self.assertGreater(len(beatmap.timing_points), 0)
        self.assertGreater(len(beatmap.hit_objects), 0)

        # 4. Assert the properties of the first hit object
        first_hit_object = beatmap.hit_objects[0]
        self.assertEqual(first_hit_object.x, 3)
        self.assertEqual(first_hit_object.y, 127)
        self.assertEqual(first_hit_object.time, 4431)
        self.assertEqual(first_hit_object.obj_type, 6) # Slider + New Combo
        self.assertTrue(first_hit_object.obj_type & 2, "First object should be a slider")

if __name__ == '__main__':
    unittest.main()
