#! /usr/bin/env python

import unittest
import sys
import os
import shutil
sys.path.insert(0, os.path.abspath("../.."))
from make.py.make_log import start_make_logging
from make.py.dir_mod import clear_output_dirs
from make.py.run_program import run_mathematica
from nostderrout import nostderrout


class testRunMathematica(unittest.TestCase):

    def setUp(self):
        makelog_file = '../output/make.log'
        output_dir = '../output/'
        with nostderrout():
            clear_output_dirs(output_dir, '')
            start_make_logging(makelog_file)

    def test_default_log(self):
        with nostderrout():
            run_mathematica(program='./input/mathematica_test_script.m')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('mathematica test ended', logfile_data)
        self.assertIn('Time   : ', logfile_data)
        self.assertTrue(os.path.isfile('output_plot.eps'))

    def test_custom_log(self):
        os.remove('../output/make.log')
        makelog_file = '../output/custom_make.log'
        output_dir = '../output/'
        with nostderrout():
            clear_output_dirs(output_dir, '')
            start_make_logging(makelog_file)
            run_mathematica(program='./input/mathematica_test_script.m',
                            makelog='../output/custom_make.log')
        logfile_data = open('../output/custom_make.log', 'r').read()
        self.assertIn('mathematica test ended', logfile_data)
        self.assertTrue(os.path.isfile('output_plot.eps'))

    def test_independent_log(self):
        with nostderrout():
            run_mathematica(program='./input/mathematica_test_script.m',
                            log='../output/mathematica.log')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('mathematica test ended', logfile_data)
        self.assertTrue(os.path.isfile('../output/mathematica.log'))
        mathematicalog_data = open('../output/mathematica.log', 'r').read()
        self.assertIn('mathematica test ended', mathematicalog_data)
        self.assertTrue(os.path.isfile('output_plot.eps'))

    def test_no_extension(self):
        with nostderrout():
            run_mathematica(program='./input/mathematica_test_script')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('mathematica test ended', logfile_data)
        self.assertTrue(os.path.isfile('output_plot.eps'))

    def test_executable(self):
        with nostderrout():
            if sys.platform.startswith('darwin'):
                run_mathematica(program='./input/mathematica_test_script.m',
                                executable='mathematicascript')
            else:
                run_mathematica(program='./input/mathematica_test_script.m',
                                executable='mathkernel')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('mathematica test ended', logfile_data)
        self.assertTrue(os.path.isfile('output_plot.eps'))

    def test_bad_executable(self):
        with nostderrout():
            run_mathematica(program='./input/mathematica_test_script.m',
                            executable='nonexistent_mathematica_executable')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('executed with errors', logfile_data)

    def test_no_program(self):
        with nostderrout():
            run_mathematica(program='./input/nonexistent_mathematica_script.m')
        logfile_data = open('../output/make.log', 'r').readlines()
        self.assertIn('CritError:', logfile_data[-1])

    def test_option(self):
        with nostderrout():
            run_mathematica(program='./input/mathematica_test_script.m',
                            option='-initfile ' +
                            './input/mathematica_init_script.m')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('mathematica test ended', logfile_data)

    def test_change_dir(self):
        with nostderrout():
            run_mathematica(program='./input/mathematica_test_script.m',
                            changedir=True)
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('mathematica test ended', logfile_data)
        self.assertTrue(os.path.isfile('./input/output_plot.eps'))

    def tearDown(self):
        if os.path.isdir('../output/'):
            shutil.rmtree('../output/')
        if os.path.isfile('output_plot.eps'):
            os.remove('output_plot.eps')
        if os.path.isfile('./input/output_plot.eps'):
            os.remove('./input/output_plot.eps')


if __name__ == '__main__':
    os.getcwd()
    unittest.main()
