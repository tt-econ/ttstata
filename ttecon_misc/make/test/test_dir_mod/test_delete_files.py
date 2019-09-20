#! /usr/bin/env python

import unittest
import sys
import os
import shutil
import glob
sys.path.insert(0, os.path.abspath("../.."))
from make.py.dir_mod import delete_files
from nostderrout import nostderrout


class testDeleteFiles(unittest.TestCase):

    def setUp(self):
        self.delete_files = './input/externals_delete_files/'
        self.dir_mod = './input/externals_delete_files/dir_mod.py'
        self.private = './input/externals_delete_files/private'
        if os.path.isdir('./input/externals_delete_files/'):
            shutil.rmtree('./input/externals_delete_files/')
        shutil.copytree('../py', './input/externals_delete_files')
        if os.path.isdir('./input/externals_delete_files/__pycache__'):
            shutil.rmtree('./input/externals_delete_files/__pycache__')
        if os.path.isdir('./input/externals_delete_files/private/__pycache__'):
            shutil.rmtree('./input/externals_delete_files/private/__pycache__')

    def test_single_file(self):
        file_list = glob.glob(os.path.join(self.delete_files, '*'))
        file_number = len(file_list)
        self.assertTrue(os.path.isfile(self.dir_mod))
        with nostderrout():
            delete_files(self.dir_mod)
        file_list = glob.glob(os.path.join(self.delete_files, '*'))
        self.assertEqual(len(file_list), file_number - 1)
        self.assertFalse(os.path.isfile(self.dir_mod))

    def test_wildcards(self):
        file_list = glob.glob(os.path.join(self.private, '*'))
        self.assertTrue(len(file_list) >= 8)
        with nostderrout():
            delete_files('./input/externals_delete_files/private/*')
        file_list = glob.glob(os.path.join(self.private, '*'))
        self.assertEqual(len(file_list), 0)

    def test_directory_fails(self):
        with nostderrout():
            with self.assertRaises(OSError):
                delete_files('./input/externals_delete_files/private/')

    def tearDown(self):
        if os.path.isdir(self.delete_files):
            shutil.rmtree(self.delete_files)


if __name__ == '__main__':
    os.getcwd()
    unittest.main()
