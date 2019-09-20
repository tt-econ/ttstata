#! /usr/bin/env python

import unittest
import sys
import os
import shutil
sys.path.insert(0, os.path.abspath("../.."))
from make.py.make_log import start_make_logging
from make.py.dir_mod import clear_output_dirs
from make.py.run_program import run_matlab
from nostderrout import nostderrout


class testRunMatlab(unittest.TestCase):

    def setUp(self):
        makelog_file = '../output/make.log'
        output_dir = '../output/'
        with nostderrout():
            clear_output_dirs(output_dir, '')
            start_make_logging(makelog_file)

    def test_default_log(self):
        with nostderrout():
            run_matlab(program='./input/matlab_test_script.m')
        self.assert_proper_output('../output/make.log')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('Time   : ', logfile_data)
        self.assertTrue(os.path.isfile('../output/matlab_test.mat'))
        self.assertTrue(os.path.isfile('../output/matlab_test.eps'))

    def test_custom_log(self):
        os.remove('../output/make.log')
        makelog_file = '../output/custom_make.log'
        output_dir = '../output/'
        with nostderrout():
            clear_output_dirs(output_dir, '')
            start_make_logging(makelog_file)
            run_matlab(program='./input/matlab_test_script.m',
                       makelog='../output/custom_make.log')
        self.assert_proper_output('../output/custom_make.log')
        self.assertTrue(os.path.isfile('../output/matlab_test.mat'))
        self.assertTrue(os.path.isfile('../output/matlab_test.eps'))

    def test_independent_log(self):
        with nostderrout():
            run_matlab(program='./input/matlab_test_script.m',
                       log='../output/matlab.log')
        self.assert_proper_output('../output/make.log')
        self.assertTrue(os.path.isfile('../output/matlab.log'))
        self.assert_proper_output('../output/matlab.log')
        self.assertTrue(os.path.isfile('../output/matlab_test.mat'))
        self.assertTrue(os.path.isfile('../output/matlab_test.eps'))

    def test_no_extension(self):
        with nostderrout():
            run_matlab(program='./input/matlab_test_script')
        self.assert_proper_output('../output/make.log')
        self.assertTrue(os.path.isfile('../output/matlab_test.mat'))
        self.assertTrue(os.path.isfile('../output/matlab_test.eps'))

    def test_executable(self):
        with nostderrout():
            run_matlab(program='./input/matlab_test_script.m',
                       executable='matlab')
        self.assert_proper_output('../output/make.log')
        self.assertTrue(os.path.isfile('../output/matlab_test.mat'))
        self.assertTrue(os.path.isfile('../output/matlab_test.eps'))

    def test_bad_executable(self):
        with nostderrout():
            run_matlab(program='./input/matlab_test_script.m',
                       executable='nonexistent_matlab_executable')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('executed with errors', logfile_data)

    def test_no_program(self):
        with nostderrout():
            run_matlab(program='./input/nonexistent_matlab_script.m')
        logfile_data = open('../output/make.log', 'r').readlines()
        self.assertIn('CritError:', logfile_data[-1])

    def test_option(self):
        with nostderrout():
            run_matlab(program='./input/matlab_test_script.m', option='-h')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('-help', logfile_data)

    def assert_proper_output(self, filename):
        file_data = open(filename, 'r').read()
        self.assertIn('0.8147', file_data)
        self.assertNotIn('Error', file_data)

    def tearDown(self):
        if os.path.isdir('../output/'):
            shutil.rmtree('../output/')


if __name__ == '__main__':
    os.getcwd()
    unittest.main()
