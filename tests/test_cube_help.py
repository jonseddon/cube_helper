# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.

import unittest
from iris.tests import stock
import iris
import cube_helper as ch
from glob import glob
import os
import cf_units

class TestCubeHelp(unittest.TestCase):

    def setUp(self):
        super(TestCubeHelp, self).setUp()
        abs_path = os.path.dirname(os.path.abspath(__file__))
        self.tmp_dir_time = abs_path + '/' + 'tmp_dir_time/'
        if not os.path.exists(self.tmp_dir_time):
            os.mkdir(self.tmp_dir_time)
        base_cube = stock.realistic_3d()
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


    def test_concatenate(self):
        glob_path = self.tmp_dir_time + '*.nc'
        filepaths = glob(glob_path)
        test_load = [iris.load_cube(cube) for cube in filepaths]
        test_case_a = ch.concatenate(test_load)
        test_load = iris.cube.CubeList(test_load)
        test_case_b = ch.concatenate(test_load)
        self.assertIsInstance(test_case_a, iris.cube.Cube)
        self.assertIsInstance(test_case_b, iris.cube.Cube)



    def test_load(self):
        glob_path = self.tmp_dir_time + '*.nc'
        filepaths = glob(glob_path)
        directory = self.tmp_dir_time
        test_case_a = ch.load(filepaths)
        self.assertIsInstance(test_case_a, iris.cube.Cube)
        self.assertEqual(test_case_a.dim_coords[0].units.origin,
                         "hours since 1970-01-01 00:00:00")
        self.assertEqual(test_case_a.dim_coords[0].units.calendar,
                         "gregorian")
        test_case_b = ch.load(directory)
        self.assertEqual(test_case_b.dim_coords[0].units.origin,
                         "hours since 1970-01-01 00:00:00")
        self.assertEqual(test_case_b.dim_coords[0].units.calendar,
                         "gregorian")


    def test_add_categorical(self):
        glob_path = self.tmp_dir_time + '*.nc'
        filepaths = glob(glob_path)
        test_case_a = ch.load(filepaths)
        test_case_b = [iris.load_cube(cube) for cube in filepaths]
        test_categoricals = ["season_year", "season_number",
                              "season_membership", "season",
                              "year", "month_number",
                              "month_fullname", "month",
                              "day_of_month", "day_of_year",
                              "weekday_number", "weekday_fullname",
                              "weekday", "hour"]
        for categorical in test_categoricals:
            test_case_a = ch.add_categorical(test_case_a, categorical)
            self.assertTrue(test_case_a.coord(categorical))
            test_case_a.remove_coord(categorical)

        for categorical in test_categoricals:
            for cube in test_case_b:
                cube = ch.add_categorical(cube, categorical)
                self.assertTrue(cube.coord(categorical))
                cube.remove_coord(categorical)
        test_case_a = ch.load(filepaths)
        test_case_a = ch.add_categorical(test_case_a,
                                         ["clim_season",
                                          "season_year"])
        self.assertTrue(test_case_a.coord("clim_season"))
        self.assertTrue(test_case_a.coord("season_year"))


    def test_add_categorical_compound(self):
        glob_path = self.tmp_dir_time + '*.nc'
        filepaths = glob(glob_path)
        test_case_a = ch.load(filepaths)
        test_case_a = ch.add_categorical(test_case_a,
                                         'annual_seasonal_mean')
        self.assertTrue(test_case_a.coord('season_year'))
        self.assertTrue(test_case_a.coord('clim_season'))


    def test_aggregate_categorical_compounds(self):
        glob_path = self.tmp_dir_time + '*.nc'
        filepaths = glob(glob_path)
        test_cube_a = ch.load(filepaths)
        test_cube_a = ch.aggregate_categorical(test_cube_a,
                                               'annual_seasonal_mean')
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('time').bounds[0][0],
                         394200.0)
        self.assertEqual(test_cube_a.coord('time').bounds[0][1],
                         394236.0)
        self.assertEqual(test_cube_a.coord('time').points[0],
                         394218.0)
        self.assertEqual(test_cube_a.coord('clim_season').points[0],
                         'djf')
        self.assertEqual(test_cube_a.coord('season_year').points[0],
                         2015)


    def test_aggregate_categorical_weekday(self):
        glob_path = self.tmp_dir_time + '*.nc'
        filepaths = glob(glob_path)
        test_cube_a = ch.load(filepaths)
        test_cube_a = ch.aggregate_categorical(test_cube_a,
                                               'weekday')
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('weekday').points[0],
                         'Sun')
        self.assertEqual(test_cube_a.coord('weekday').points[1],
                         'Mon')
        test_cube_a = ch.load(filepaths)
        test_cube_a = ch.aggregate_categorical(test_cube_a,
                                               'weekday_fullname')
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('weekday_fullname').points[0],
                         'Sunday')
        self.assertEqual(test_cube_a.coord('weekday_fullname').points[1],
                         'Monday')
        test_cube_a = ch.load(filepaths)
        test_cube_a = ch.aggregate_categorical(test_cube_a,
                                               'weekday_number')
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('weekday_number').points[0],
                         6)
        self.assertEqual(test_cube_a.coord('weekday_number').points[1],
                         0)


    def test_aggregate_categorical_month(self):
        glob_path = self.tmp_dir_time + '*.nc'
        filepaths = glob(glob_path)
        test_cube_a = ch.load(filepaths)
        test_cube_a = ch.aggregate_categorical(test_cube_a,
                                               'month')
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('month').points[0],
                         'Dec')
        test_cube_a = ch.load(filepaths)
        test_cube_a = ch.aggregate_categorical(test_cube_a,
                                               'month_fullname')
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('month_fullname').points[0],
                         'December')
        test_cube_a = ch.load(filepaths)
        test_cube_a = ch.aggregate_categorical(test_cube_a,
                                               'month_number')
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('month_number').points[0],
                         12)

    def test_aggregate_categorical_year(self):
        glob_path = self.tmp_dir_time + '*.nc'
        filepaths = glob(glob_path)
        test_cube_a = ch.load(filepaths)
        test_cube_a = ch.aggregate_categorical(test_cube_a,
                                               'year')
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('year').points[0],
                         2014)
        test_cube_a = ch.load(filepaths)
        test_cube_a = ch.aggregate_categorical(test_cube_a,
                                               'season_year')
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('season_year').points[0],
                         2015)

    def test_aggregate_categorical_seasons(self):
        glob_path = self.tmp_dir_time + '*.nc'
        filepaths = glob(glob_path)
        test_cube_a = ch.load(filepaths)
        test_cube_a = ch.aggregate_categorical(test_cube_a,
                                               'clim_season')
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('clim_season').points[0],
                         'djf')
        test_cube_a = ch.load(filepaths)
        test_cube_a = ch.aggregate_categorical(test_cube_a,
                                               'season')
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('season').points[0],
                         'djf')
        test_cube_a = ch.load(filepaths)
        test_cube_a = ch.aggregate_categorical(test_cube_a,
                                               'season_membership')
        self.assertIsNotNone(test_cube_a)
        self.assertEqual(test_cube_a.coord('season_membership').points[0],
                         True)


    def test_aggregate_categorical_day(self):
        glob_path = self.tmp_dir_time + '*.nc'
        filepaths = glob(glob_path)
        test_cube_a = ch.load(filepaths)
        test_cube_a = ch.aggregate_categorical(test_cube_a,
                                               'day_of_year')
        self.assertEqual(test_cube_a.coord('day_of_year').points[0],
                         355)
        test_cube_a = ch.load(filepaths)
        test_cube_a = ch.aggregate_categorical(test_cube_a,
                                               'day_of_month')
        self.assertEqual(test_cube_a.coord('day_of_month').points[0],
                         21)


    def tearDown(self):
        super(TestCubeHelp, self).tearDown()
        if os.path.exists(self.tmp_dir_time + self.temp_1_time):
            os.remove(self.tmp_dir_time + self.temp_1_time)
        if os.path.exists(self.tmp_dir_time + self.temp_2_time):
            os.remove(self.tmp_dir_time + self.temp_2_time)
        if os.path.exists(self.tmp_dir_time + self.temp_3_time):
            os.remove(self.tmp_dir_time + self.temp_3_time)
        os.removedirs(self.tmp_dir_time)

if __name__ == '__main__':
    unittest.main()
