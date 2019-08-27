import unittest
from cube_helper.cube_loader import load_from_dir, load_from_filelist
from cube_helper.cube_equaliser import (equalise_attributes,equalise_time_units,
                                        equalise_data_type, remove_attributes)

class TestCubeEqualiser(unittest.TestCase):

    def test_equalise_attributes(self):
        filepath = 'test_data/air_temp'
        test_load = load_from_dir(filepath, filetype='.pp')
        equalise_attributes(test_load)
        for cubes in test_load:
            self.assertEqual(cubes.attributes, test_load[0].attributes)

    def test_unify_time_units(self):
        filepath = 'test_data/air_temp'
        test_load = load_from_dir(filepath, filetype='.pp')
        equalise_time_units(test_load)
        for index,cube in enumerate(test_load):
            for time_coords in cube.coords():
                if time_coords.units.is_time_reference():
                    self.assertEqual(cube[index].units.calendar,
                                     cube[index-1].units.calendar)

    def test_remove_attributes(self):
        filepath = 'test_data/air_temp'
        test_load = load_from_dir(filepath, filetype='.pp')
        remove_attributes(test_load)
        keys = list(test_load[0].attributes.keys())
        for cube in test_load:
            for key in keys:
                self.assertEqual(cube.attributes[key], '')

    def test_equalise_data_type(self):
        filepath = 'test_data/air_temp'
        test_load = load_from_dir(filepath, filetype='.pp')
        test_load_datatype = test_load[0].dtype
        equalise_data_type(test_load)
        self.assertEqual(test_load_datatype,'float32')



if __name__ == "__main__":
    unittest.main()

