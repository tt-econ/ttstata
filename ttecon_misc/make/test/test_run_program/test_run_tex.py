#! /usr/bin/env python

import unittest
import sys
import os
import shutil
sys.path.insert(0, os.path.abspath("../.."))
from make.py.make_log import start_make_logging
from make.py.dir_mod import clear_output_dirs
from make.py.run_program import run_tex
from nostderrout import nostderrout


class testRunTex(unittest.TestCase):

    def setUp(self):
        makelog_file = '../output/make.log'
        output_dir = '../output/'
        with nostderrout():
            clear_output_dirs(output_dir, '')
            start_make_logging(makelog_file)

    def test_default_log(self):
        with nostderrout():
            run_tex(program='./input/draft.tex')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('pdfTeX', logfile_data)
        self.assertIn('Time   : ', logfile_data)
        self.assertFalse(os.path.isfile('./input/draft.pdf'))
        self.assertFalse(os.path.isfile('./input/draft.aux'))
        self.assertTrue(os.path.isfile('../output/draft.pdf'))

    def test_check_for_multiple_periods(self):
        with nostderrout():
            run_tex(program='./input/draft.tex')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('Check periods on line 16', logfile_data)
        self.assertIn('Check periods on line 22', logfile_data)
        self.assertNotIn('Check periods on line 12', logfile_data)
        self.assertNotIn('Check periods on line 14', logfile_data)
        self.assertNotIn('Check periods on line 18', logfile_data)
        self.assertNotIn('Check periods on line 20', logfile_data)
        self.assertNotIn('Check periods on line 45', logfile_data)
        self.assertFalse(os.path.isfile('./input/draft.pdf'))
        self.assertFalse(os.path.isfile('./input/draft.aux'))
        self.assertTrue(os.path.isfile('../output/draft.pdf'))

    def test_custom_log(self):
        os.remove('../output/make.log')
        makelog_file = '../output/custom_make.log'
        output_dir = '../output/'
        with nostderrout():
            clear_output_dirs(output_dir, '')
            start_make_logging(makelog_file)
            run_tex(program='./input/draft.tex',
                    makelog='../output/custom_make.log')
        logfile_data = open('../output/custom_make.log', 'r').read()
        self.assertIn('pdfTeX', logfile_data)
        self.assertFalse(os.path.isfile('./input/draft.pdf'))
        self.assertFalse(os.path.isfile('./input/draft.aux'))
        self.assertTrue(os.path.isfile('../output/draft.pdf'))

    def test_independent_log(self):
        with nostderrout():
            run_tex(program='./input/draft.tex', log='../output/tex.log')
        makelog_data = open('../output/make.log', 'r').read()
        self.assertIn('pdfTeX', makelog_data)
        self.assertTrue(os.path.isfile('../output/tex.log'))
        texlog_data = open('../output/tex.log', 'r').read()
        self.assertIn('pdfTeX', texlog_data)
        self.assertIn(texlog_data, makelog_data)
        self.assertFalse(os.path.isfile('./input/draft.pdf'))
        self.assertFalse(os.path.isfile('./input/draft.aux'))
        self.assertTrue(os.path.isfile('../output/draft.pdf'))

    def test_no_extension(self):
        with nostderrout():
            run_tex(program='./input/draft')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('pdfTeX', logfile_data)
        self.assertFalse(os.path.isfile('./input/draft.pdf'))
        self.assertFalse(os.path.isfile('./input/draft.aux'))
        self.assertTrue(os.path.isfile('../output/draft.pdf'))

    def test_executable(self):
        with nostderrout():
            run_tex(program='./input/draft.tex', executable='latexmk')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('pdfTeX', logfile_data)
        self.assertFalse(os.path.isfile('./input/draft.pdf'))
        self.assertFalse(os.path.isfile('./input/draft.aux'))
        self.assertTrue(os.path.isfile('../output/draft.pdf'))

    def test_bad_executable(self):
        with nostderrout():
            run_tex(program='./input/draft.tex',
                    executable='nonexistent_tex_executable')
        logfile_data = open('../output/make.log', 'r').read()
        self.assertIn('executed with errors', logfile_data)
        self.assertFalse(os.path.isfile('../input/draft.pdf'))
        self.assertFalse(os.path.isfile('../output/draft.pdf'))

    def test_no_program(self):
        with nostderrout():
            run_tex(program='./input/nonexistent_tex_file.tex')
        logfile_data = open('../output/make.log', 'r').readlines()
        self.assertIn('CritError:', logfile_data[-1])
        self.assertFalse(os.path.isfile('../input/draft.pdf'))
        self.assertFalse(os.path.isfile('../output/draft.pdf'))

    def tearDown(self):
        if os.path.isdir('../output/'):
            shutil.rmtree('../output/')


if __name__ == '__main__':
    os.getcwd()
    unittest.main()
