#! /usr/bin/env python

import unittest
import sys
import os
import shutil
sys.path.insert(0, os.path.abspath("../.."))
from make.py.make_log import start_make_logging
from make.py.dir_mod import clear_output_dirs
from make.py.run_program import run_rinstall
from nostderrout import nostderrout


class testRunRInstall(unittest.TestCase):

    def setUp(self):
        makelog_file = '../output/make.log'
        output_dir = '../output/'
        with nostderrout():
            clear_output_dirs(output_dir, '')
            start_make_logging(makelog_file)

    def test_default_log(self):
        with nostderrout():
            run_rinstall(
                package='./input/rinstall_test_package/Ecdat_0.1-6.1.tar.gz')
        self.assertTrue(self.last_line_equals('../output/make.log',
                        '* DONE (Ecdat)\n'))
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('Time   : ', logfile_data)

    def test_specify_lib(self):
        self.assertFalse(os.path.isdir('../output/Ecdat/'))
        self.assertFalse(os.path.isfile('../output/Ecdat/INDEX'))
        with nostderrout():
            run_rinstall(
                package='./input/rinstall_test_package/Ecdat_0.1-6.1.tar.gz',
                lib='../output/')
        self.assertTrue(self.last_line_equals('../output/make.log',
                        '* DONE (Ecdat)\n'))
        self.assertTrue(os.path.isdir('../output/Ecdat/'))
        self.assertTrue(os.path.isfile('../output/Ecdat/INDEX'))

    def test_custom_log(self):
        os.remove('../output/make.log')
        makelog_file = '../output/custom_make.log'
        output_dir = '../output/'
        with nostderrout():
            clear_output_dirs(output_dir, '')
            start_make_logging(makelog_file)
            run_rinstall(
                package='./input/rinstall_test_package/Ecdat_0.1-6.1.tar.gz',
                makelog='../output/custom_make.log')
        self.assertTrue(self.last_line_equals(
                        '../output/custom_make.log', '* DONE (Ecdat)\n'))

    def test_independent_log(self):
        with nostderrout():
            run_rinstall(
                package='./input/rinstall_test_package/Ecdat_0.1-6.1.tar.gz',
                log='../output/R.log')
        self.assertTrue(
            self.last_line_equals('../output/make.log', '* DONE (Ecdat)\n'))
        self.assertTrue(self.last_line_equals('../output/R.log',
                                              '* DONE (Ecdat)\n'))

    def test_executable(self):
        with nostderrout():
            run_rinstall(
                package='./input/rinstall_test_package/Ecdat_0.1-6.1.tar.gz',
                executable='R CMD INSTALL')
        self.assertTrue(self.last_line_equals('../output/make.log',
                        '* DONE (Ecdat)\n'))

    def test_bad_executable(self):
        with nostderrout():
            run_rinstall(
                package='./input/rinstall_test_package/Ecdat_0.1-6.1.tar.gz',
                executable='nonexistent_R_executable')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('executed with errors', logfile_data)

    def test_no_package(self):
        with nostderrout():
            run_rinstall(package='nonexistent_R_package')
        logfile_data = open('../output/make.log', 'r').readlines()
        self.assertIn('CritError:', logfile_data[-1])

    def test_option(self):
        self.assertFalse(os.path.isdir('../output/Ecdat/'))
        self.assertFalse(os.path.isfile('../output/Ecdat/INDEX'))
        with nostderrout():
            run_rinstall(
                package='./input/rinstall_test_package/Ecdat_0.1-6.1.tar.gz',
                lib='../output/', option='--no-data')
        self.assertTrue(os.path.isdir('../output/Ecdat/'))
        self.assertTrue(os.path.isfile('../output/Ecdat/INDEX'))
        self.assertFalse(os.path.isdir('../output/Ecdat/data/'))

    def last_line_equals(self, filename, string):
        file_data = open(filename, 'rb')
        file_data.seek(-2, 2)
        file_data.read(2)
        string_len = len(string)
        file_data.seek(-string_len, 2)
        lastline = file_data.read(string_len).decode("utf-8")

        return string == lastline

    def tearDown(self):
        if os.path.isdir('../output/'):
            shutil.rmtree('../output/')


if __name__ == '__main__':
    os.getcwd()
    unittest.main()
