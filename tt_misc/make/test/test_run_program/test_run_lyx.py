#! /usr/bin/env python

import unittest
import sys
import os
import shutil
sys.path.insert(0, os.path.abspath("../.."))
from make.py.make_log import start_make_logging
from make.py.dir_mod import clear_output_dirs
from make.py.run_program import run_lyx
from nostderrout import nostderrout


class testRunLyx(unittest.TestCase):

    def setUp(self):
        makelog_file = '../output/make.log'
        output_dir = '../output/'
        with nostderrout():
            clear_output_dirs(output_dir, '')
            start_make_logging(makelog_file)

    def test_default_log(self):
        with nostderrout():
            run_lyx(program='./input/lyx_test_file.lyx')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('LaTeX', logfile_data)
        self.assertIn('Time   : ', logfile_data)
        self.assertTrue(os.path.isfile('../output/lyx_test_file.pdf'))

    def test_custom_log(self):
        os.remove('../output/make.log')
        makelog_file = '../output/custom_make.log'
        output_dir = '../output/'
        with nostderrout():
            clear_output_dirs(output_dir, '')
            start_make_logging(makelog_file)
            run_lyx(program='./input/lyx_test_file.lyx',
                    makelog='../output/custom_make.log')
        logfile_data = open('../output/custom_make.log', 'r').read()
        self.assertIn('LaTeX', logfile_data)
        self.assertTrue(os.path.isfile('../output/lyx_test_file.pdf'))

    def test_independent_log(self):
        with nostderrout():
            run_lyx(program='./input/lyx_test_file.lyx',
                    log='../output/lyx.log')
        makelog_data = open('../output/make.log', 'r').read()
        self.assertIn('LaTeX', makelog_data)
        self.assertTrue(os.path.isfile('../output/lyx.log'))
        lyxlog_data = open('../output/lyx.log', 'r').read()
        self.assertIn('LaTeX', lyxlog_data)
        self.assertIn(lyxlog_data, makelog_data)
        self.assertTrue(os.path.isfile('../output/lyx_test_file.pdf'))

    def test_no_extension(self):
        with nostderrout():
            run_lyx(program='./input/lyx_test_file')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('LaTeX', logfile_data)
        self.assertTrue(os.path.isfile('../output/lyx_test_file.pdf'))

    def test_executable(self):
        with nostderrout():
            run_lyx(program='./input/lyx_test_file.lyx', executable='lyx')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('LaTeX', logfile_data)
        self.assertTrue(os.path.isfile('../output/lyx_test_file.pdf'))

    def test_bad_executable(self):
        with nostderrout():
            run_lyx(program='./input/lyx_test_file.lyx',
                    executable='nonexistent_lyx_executable')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('executed with errors', logfile_data)

    def test_no_program(self):
        with nostderrout():
            run_lyx(program='./input/nonexistent_lyx_file.lyx')
        logfile_data = open('../output/make.log', 'r').readlines()
        self.assertIn('CritError:', logfile_data[-1])

    def test_change_dir(self):
        with nostderrout():
            run_lyx(program='./input/lyx_test_file.lyx', changedir=True)
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('LaTeX', logfile_data)
        self.assertTrue(os.path.isfile('../output/lyx_test_file.pdf'))

    def test_pdfout(self):
        with nostderrout():
            run_lyx(program='./input/lyx_test_file.lyx',
                    pdfout='../output/custom_outfile.pdf')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('LaTeX', logfile_data)
        self.assertTrue(os.path.isfile('../output/custom_outfile.pdf'))
        self.assertFalse(os.path.isfile('./input/lyx_test_file.pdf'))

    def tearDown(self):
        if os.path.isdir('../output/'):
            shutil.rmtree('../output/')


if __name__ == '__main__':
    os.getcwd()
    unittest.main()
