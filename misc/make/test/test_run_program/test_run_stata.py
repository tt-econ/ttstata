#! /usr/bin/env python

import unittest
import sys
import os
import shutil
sys.path.insert(0, os.path.abspath("../.."))
from make.py.make_log import start_make_logging
from make.py.dir_mod import clear_output_dirs
from make.py.run_program import run_stata
from nostderrout import nostderrout


class testRunStata(unittest.TestCase):

    def setUp(self):
        makelog_file = '../output/make.log'
        output_dir = '../output/'
        with nostderrout():
            clear_output_dirs(output_dir, '')
            start_make_logging(makelog_file)

    def test_default_log(self):
        with nostderrout():
            run_stata(program='./input/stata_test_script.do')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('end of do-file', logfile_data)
        self.assertIn('Time   : ', logfile_data)

    def test_custom_log(self):
        os.remove('../output/make.log')
        makelog_file = '../output/custom_make.log'
        output_dir = '../output/'
        with nostderrout():
            clear_output_dirs(output_dir, '')
            start_make_logging(makelog_file)
            run_stata(program='./input/stata_test_script.do',
                      makelog='../output/custom_make.log')
        logfile_data = open('../output/custom_make.log', 'r').read()
        self.assertIn('end of do-file', logfile_data)

    def test_independent_log(self):
        with nostderrout():
            run_stata(program='./input/stata_test_script.do',
                      log='../output/stata.log')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('end of do-file', logfile_data)
        self.assertTrue(os.path.isfile('../output/stata.log'))
        logfile_data = open('../output/stata.log', 'r').read()
        self.assertIn('end of do-file', logfile_data)

    def test_no_extension(self):
        with nostderrout():
            run_stata(program='./input/stata_test_script')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('end of do-file', logfile_data)

    def test_executable(self):
        with nostderrout():
            if sys.platform.startswith('win'):
                run_stata(program='./input/stata_test_script.do',
                          executable='%STATAEXE%')
            elif sys.platform.startswith('darwin'):
                run_stata(program='./input/stata_test_script.do',
                          executable='stata-mp')
            else:
                run_stata(program='./input/stata_test_script.do',
                          executable='stata-mp')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('end of do-file', logfile_data)

    def test_bad_executable(self):
        with nostderrout():
            run_stata(program='./input/stata_test_script.do',
                      executable='nonexistent_stata_executable')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('executed with errors', logfile_data)

    def test_no_program(self):
        with nostderrout():
            run_stata(program='./input/nonexistent_stata_script.do')
        logfile_data = open('../output/make.log', 'r').readlines()
        self.assertIn('CritError:', logfile_data[-1])

    def test_change_dir(self):
        os.mkdir('output')
        shutil.copytree('./input/lib/', './input/input/lib')
        with nostderrout():
            run_stata(program='./input/stata_test_script.do', changedir=True)
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('end of do-file', logfile_data)
        self.assertTrue(os.path.isfile('./output/stata1.dta'))
        self.assertFalse(os.path.isfile('../output/stata1.dta'))

    def tearDown(self):
        if os.path.isdir('../output/'):
            shutil.rmtree('../output/')
        if os.path.isdir('./output/'):
            shutil.rmtree('./output/')
        if os.path.isdir('./input/input/'):
            shutil.rmtree('./input/input/')


if __name__ == '__main__':
    os.getcwd()
    unittest.main()
