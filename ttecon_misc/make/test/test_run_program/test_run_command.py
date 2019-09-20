#! /usr/bin/env python

import unittest
import sys
import os
import shutil
sys.path.insert(0, os.path.abspath("../.."))
from make.py.make_log import start_make_logging
from make.py.dir_mod import clear_output_dirs
from make.py.run_program import run_command
from nostderrout import nostderrout


class testRunCommand(unittest.TestCase):

    def setUp(self):
        makelog_file = '../output/make.log'
        output_dir = '../output/'
        with nostderrout():
            clear_output_dirs(output_dir, '')
            start_make_logging(makelog_file)

    def test_default_log(self):
        self.assertFalse(os.path.isfile('test_data.txt'))
        with nostderrout():
            if sys.platform.startswith('win'):
                run_command(command='wzunzip ./input/zip_test_file.zip ./')
            else:
                run_command(command='unzip ./input/zip_test_file.zip')
        logfile_data = open('../output/make.log', 'r').readlines()
        self.assertIn('test_data.txt', logfile_data[-1])
        self.assertIn('Time   : ', logfile_data[6])
        self.assertTrue(os.path.isfile('test_data.txt'))

    def test_custom_log(self):
        self.assertFalse(os.path.isfile('test_data.txt'))
        os.remove('../output/make.log')
        makelog_file = '../output/custom_make.log'
        output_dir = '../output/'
        with nostderrout():
            clear_output_dirs(output_dir, '')
            start_make_logging(makelog_file)
            if sys.platform.startswith('win'):
                run_command(command='wzunzip ./input/zip_test_file.zip ./',
                            makelog='../output/custom_make.log')
            else:
                run_command(command='unzip ./input/zip_test_file.zip',
                            makelog='../output/custom_make.log')
        logfile_data = open('../output/custom_make.log', 'r').readlines()
        self.assertIn('test_data.txt', logfile_data[-1])
        self.assertTrue(os.path.isfile('test_data.txt'))

    def test_independent_log(self):
        self.assertFalse(os.path.isfile('test_data.txt'))
        with nostderrout():
            if sys.platform.startswith('win'):
                run_command(command='wzunzip ./input/zip_test_file.zip ./',
                            log='../output/command.log')
            else:
                run_command(command='unzip ./input/zip_test_file.zip',
                            log='../output/command.log')
        makelog_data = open('../output/make.log', 'r').readlines()
        self.assertIn('test_data.txt', makelog_data[-1])
        self.assertTrue(os.path.isfile('../output/command.log'))
        commandlog_data = open('../output/command.log', 'r').readlines()
        self.assertIn('test_data.txt', commandlog_data[-1])
        self.assertTrue(os.path.isfile('test_data.txt'))

    def tearDown(self):
        if os.path.isdir('../output/'):
            shutil.rmtree('../output/')
        if os.path.isfile('test_data.txt'):
            os.remove('test_data.txt')


if __name__ == '__main__':
    os.getcwd()
    unittest.main()
