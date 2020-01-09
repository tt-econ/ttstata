#! /usr/bin/env python

import unittest
import sys
import os
import shutil
sys.path.insert(0, os.path.abspath("../.."))
from make.py.make_log import start_make_logging
from make.py.dir_mod import clear_output_dirs
from make.py.run_program import run_perl
from nostderrout import nostderrout


class testRunPerl(unittest.TestCase):

    def setUp(self):
        makelog_file = '../output/make.log'
        output_dir = '../output/'
        with nostderrout():
            clear_output_dirs(output_dir, '')
            start_make_logging(makelog_file)

    def test_default_log(self):
        with nostderrout():
            run_perl(program='./input/perl_test_script.pl')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('Test script completed', logfile_data)
        self.assertIn('Time   : ', logfile_data)
        self.assertTrue(os.path.isfile('output.txt'))

    def test_custom_log(self):
        os.remove('../output/make.log')
        makelog_file = '../output/custom_make.log'
        output_dir = '../output/'
        with nostderrout():
            clear_output_dirs(output_dir, '')
            start_make_logging(makelog_file)
            run_perl(program='./input/perl_test_script.pl',
                     makelog='../output/custom_make.log')
        logfile_data = open('../output/custom_make.log', 'r').read()
        self.assertIn('Test script completed', logfile_data)
        self.assertTrue(os.path.isfile('output.txt'))

    def test_independent_log(self):
        with nostderrout():
            run_perl(program='./input/perl_test_script.pl',
                     log='../output/perl.log')
        self.assertTrue(os.path.isfile('../output/perl.log'))
        logfile_data = open('../output/perl.log', 'r').read()
        self.assertIn('Test script completed', logfile_data)
        self.assertTrue(os.path.isfile('output.txt'))

    def test_no_extension(self):
        with nostderrout():
            run_perl(program='./input/perl_test_script')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('Test script completed', logfile_data)
        self.assertTrue(os.path.isfile('output.txt'))

    def test_executable(self):
        with nostderrout():
            run_perl(program='./input/perl_test_script.pl', executable='perl')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('Test script completed', logfile_data)
        self.assertTrue(os.path.isfile('output.txt'))

    def test_bad_executable(self):
        with nostderrout():
            run_perl(program='./input/perl_test_script.pl',
                     executable='nonexistent_perl_executable')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('executed with errors', logfile_data)

    def test_no_program(self):
        with nostderrout():
            run_perl(program='./input/nonexistent_perl_script.pl')
        logfile_data = open('../output/make.log', 'r').readlines()
        self.assertIn('CritError:', logfile_data[-1])

    def test_option(self):
        with nostderrout():
            run_perl(program='./input/perl_test_script.pl', option='-h')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('Usage:', logfile_data)

    def test_args(self):
        with nostderrout():
            run_perl(program='./input/perl_test_script.pl', args='\'Input\'')
        output_data = open('output.txt', 'r').read()
        self.assertIn('Input', output_data)

    def test_change_dir(self):
        with nostderrout():
            run_perl(program='./input/perl_test_script.pl', changedir=True)
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('Test script completed', logfile_data)
        self.assertTrue(os.path.isfile('./input/output.txt'))

    def test_perl_error(self):
        with nostderrout():
            run_perl(program='./input/perl_test_script_error.pl')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('executed with errors', logfile_data)

    def tearDown(self):
        if os.path.isdir('../output/'):
            shutil.rmtree('../output/')
        if os.path.isfile('output.txt'):
            os.remove('output.txt')
        if os.path.isfile('./input/output.txt'):
            os.remove('./input/output.txt')


if __name__ == '__main__':
    os.getcwd()
    unittest.main()
