#! /usr/bin/env python

import unittest
import sys
import os
import shutil
sys.path.insert(0, os.path.abspath("../.."))
from make.py.make_log import start_make_logging, set_option, end_make_logging
from make.py.dir_mod import check_manifest, clear_output_dirs
from make.py.run_program import run_stata
from nostderrout import nostderrout


class testSetOption(unittest.TestCase):

    def test_set_option(self):
        with nostderrout():
            set_option(makelog='../customoutput/custommake.log',
                       temp_dir='../customtemp/',
                       output_dir='../customoutput/',
                       manifest='../customoutput/data_file_manifest.log')
            clear_output_dirs()
            start_make_logging()
            run_stata(program='./input/stata_test_script_alt.do')
        self.remove_manifest_entry('../customoutput/data_file_manifest.log', 1)
        with nostderrout():
            check_manifest()
            end_make_logging()
        self.assertTrue(os.path.isdir('../customoutput/'))
        self.assertTrue(os.path.isdir('../customtemp/'))
        self.assertTrue(os.path.isfile('../customoutput/custommake.log'))
        self.assertTrue(self.check_results('../customoutput/custommake.log',
                                           1, 0))

    def remove_manifest_entry(self, manifest, entry_to_remove):
        manifest_data = open(manifest, 'r').readlines()
        removed = 0
        fileno = 0
        for line in manifest_data:
            if removed == 0:
                if line.startswith('File:'):
                    fileno += 1
                    if fileno == entry_to_remove:
                        manifest_data.remove(line)
                        removed = 1

        outfile = open(manifest, 'w')
        outfile.write(''.join(manifest_data))
        outfile.close()

    def check_results(self, logfile, num_errors, num_warnings):
        logfile_data = open(logfile, 'r').readlines()
        errors = 0
        warnings = 0
        for line in logfile_data:
            if 'Warning!' in line:
                warnings += 1
                if warnings > num_warnings:
                    return False
            if 'CritError:' in line:
                errors += 1
                if errors > num_errors:
                    return False

        return (warnings == num_warnings and errors == num_errors)

    def tearDown(self):
        if os.path.isdir('../customtemp/'):
            shutil.rmtree('../customtemp/')
        if os.path.isdir('../customoutput/'):
            shutil.rmtree('../customoutput/')
        with nostderrout():
            set_option(makelog='../output/make.log', temp_dir='../temp/',
                       output_dir='../output/',
                       manifest='../output/data_file_manifest.log')


if __name__ == '__main__':
    os.getcwd()
    unittest.main()
