# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.
import unittest
import os
import iris
from iris.tests import stock
import cf_units
from glob import glob
from cube_helper.cube_loader import (load_from_dir,
                                     load_from_filelist,
                                     _parse_directory,
                                     _sort_by_date,
                                     file_sort_by_earliest_date,
                                     sort_by_earliest_date)


class TestCubeLoader(unittest.TestCase):

    def setUp(self):
        super(TestCubeLoader, self).setUp()
        abs_path = os.path.dirname(os.path.abspath(__file__))
        self.tmp_dir_time = abs_path + '/' + 'tmp_dir_time/'
        self.tmp_dir = abs_path + '/' + 'tmp_dir/'
        if not os.path.exists(self.tmp_dir_time):
            os.mkdir(self.tmp_dir_time)
        if not os.path.exists(self.tmp_dir):
            os.mkdir(self.tmp_dir)
        base_cube = stock.realistic_3d()
        cube_1 = base_cube[0:2]
        cube_2 = base_cube[2:4]
        cube_3 = base_cube[4:]
        self.temp_1 = 'temp_1.nc'
        self.temp_2 = 'temp_2.nc'
        self.temp_3 = 'temp_3.nc'
        iris.save(cube_1, self.tmp_dir + self.temp_1)
        iris.save(cube_2, self.tmp_dir + self.temp_2)
        iris.save(cube_3, self.tmp_dir + self.temp_3)
        cube_1 = base_cube[0:2]
        cube_2 = base_cube[2:4]
        cube_3 = base_cube[4:]
        new_time = cf_units.Unit('hours since 1980-01-01 00:00:00',
                                 'gregorian')
        cube_2.dim_coords[0].convert_units(new_time)
        new_time = cf_units.Unit('hours since 1990-01-01 00:00:00',
                                 'gregorian')
        cube_3.dim_coords[0].convert_units(new_time)
        self.temp_1_time = 'temp_1_time.nc'
        self.temp_2_time = 'temp_2_time.nc'
        self.temp_3_time = 'temp_3_time.nc'
        iris.save(cube_1, self.tmp_dir_time + self.temp_1_time)
        iris.save(cube_2, self.tmp_dir_time + self.temp_2_time)
        iris.save(cube_3, self.tmp_dir_time + self.temp_3_time)

    def test_load_from_filelist(self):
        filelist = [self.tmp_dir + self.temp_1,
                    self.tmp_dir + self.temp_2,
                    self.tmp_dir + self.temp_1]
        test_load, test_names = load_from_filelist(filelist,
                                                   '.nc')
        print(test_names)
        self.assertIsInstance(test_load, list)
        self.assertIsInstance(test_names, list)
        for cube in test_load:
            self.assertIsInstance(cube, iris.cube.Cube)
        for name in test_names:
            self.assertIsInstance(name, str)
            self.assertTrue(os.path.exists(name))


    def test_load_from_dir(self):
        test_load, test_names = load_from_dir(self.tmp_dir, '.nc')
        self.assertIsInstance(test_load, list)
        self.assertIsInstance(test_names, list)
        for cube in test_load:
            self.assertIsInstance(cube, iris.cube.Cube)
        for name in test_names:
            self.assertIsInstance(name, str)
            self.assertTrue(os.path.exists(name))


    def test_parse_directory(self):
        directory = 'test_data/realistic_3d/realistic_3d_0.nc'
        self.assertEqual(_parse_directory(directory),
                         '/test_data/realistic_3d/realistic_3d_0.nc/')


    def test_sort_by_earliest_date(self):
        glob_path = self.tmp_dir_time + '*.nc'
        filepaths = glob(glob_path)
        test_load = [iris.load_cube(cube) for cube in filepaths]
        test_load = iris.cube.CubeList(test_load)
        test_load.sort(key=sort_by_earliest_date)
        self.assertEqual(test_load[0].dim_coords[0].units.origin,
                         "hours since 1970-01-01 00:00:00")
        self.assertEqual(test_load[1].dim_coords[0].units.origin,
                         "hours since 1980-01-01 00:00:00")
        self.assertEqual(test_load[2].dim_coords[0].units.origin,
                         "hours since 1990-01-01 00:00:00")


    def test_file_sort_by_earliest_date(self):
        glob_path = self.tmp_dir_time + '*.nc'
        filepaths = glob(glob_path)
        filepaths.sort(key=file_sort_by_earliest_date)
        test_load = [iris.load_cube(cube) for cube in filepaths]
        self.assertEqual(test_load[0].dim_coords[0].units.origin,
                         "hours since 1970-01-01 00:00:00")
        self.assertEqual(test_load[1].dim_coords[0].units.origin,
                         "hours since 1980-01-01 00:00:00")
        self.assertEqual(test_load[2].dim_coords[0].units.origin,
                         "hours since 1990-01-01 00:00:00")


    def tearDown(self):
        super(TestCubeLoader, self).tearDown()
        if os.path.exists(self.tmp_dir + self.temp_1):
            os.remove(self.tmp_dir + self.temp_1)
        if os.path.exists(self.tmp_dir + self.temp_2):
            os.remove(self.tmp_dir + self.temp_2)
        if os.path.exists(self.tmp_dir + self.temp_3):
            os.remove(self.tmp_dir + self.temp_3)
        if os.path.exists(self.tmp_dir_time + self.temp_1_time):
            os.remove(self.tmp_dir_time + self.temp_1_time)
        if os.path.exists(self.tmp_dir_time + self.temp_2_time):
            os.remove(self.tmp_dir_time + self.temp_2_time)
        if os.path.exists(self.tmp_dir_time + self.temp_3_time):
            os.remove(self.tmp_dir_time + self.temp_3_time)
        os.removedirs(self.tmp_dir)
        os.removedirs(self.tmp_dir_time)


if __name__ == '__main__':
    unittest.main()