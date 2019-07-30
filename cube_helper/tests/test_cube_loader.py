import sys
sys.path.append('/net/home/h01/jbedwell/Downloads/cube_helper/cube_helper')
import unittest
import iris
from cube_loader import CubeLoader





class TestCubeLoader(unittest.TestCase):
    def test_load_from_filelist(self):
        filelist = ['test_data/air_temp/air_temp_1.pp', 'test_data/air_temp/air_temp_2.pp',
                    'test_data/air_temp/air_temp_3.pp', 'test_data/air_temp/air_temp_4.pp'
                                                        'test_data/air_temp/air_temp_5.pp']
        example_case = CubeLoader.load_from_filelist(filelist, opt_filetype='.pp')
        self.assertEqual(type(example_case), list)

    def test_load_from_dir(self):
        example_case = CubeLoader.load_from_dir('test_data/air_temp', opt_filetype='.pp')
        self.assertEqual(type(example_case), list)


if __name__ == "__main__":
    unittest.main()