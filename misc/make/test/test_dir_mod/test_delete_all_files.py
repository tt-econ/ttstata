#! /usr/bin/env python

import unittest
import sys
import os
import shutil
import glob
sys.path.insert(0, os.path.abspath("../.."))
from make.py.dir_mod import delete_all_files
from nostderrout import nostderrout


class testDeleteAllFiles(unittest.TestCase):

    def setUp(self):
        self.delete_files = './input/externals_delete_all_files/'
        self.private = './input/externals_delete_all_files/private'
        self.dir_mod = './input/externals_delete_all_files/dir_mod.py'
        if os.path.isdir(self.delete_files):
            shutil.rmtree(self.delete_files)
        shutil.copytree('../py', './input/externals_delete_all_files')
        if os.path.isdir('./input/externals_delete_all_files/__pycache__'):
            shutil.rmtree('./input/externals_delete_all_files/__pycache__')
        if os.path.isdir('./input/externals_delete_all_files/private/__pycache__'):
            shutil.rmtree('./input/externals_delete_all_files/private/__pycache__')

    def test_all(self):
        file_list = glob.glob(os.path.join(self.delete_files, '*'))
        self.assertTrue(len(file_list) > 0)
        subdirectory_file_list = glob.glob(os.path.join(self.private, '*'))
        self.assertTrue(len(subdirectory_file_list) > 0)
        with nostderrout():
            delete_all_files(self.delete_files)
        file_list = glob.glob(os.path.join(self.delete_files, '*'))
        self.assertEqual(len(file_list), 1)
        subdirectory_file_list = glob.glob(os.path.join(self.private, '*'))
        self.assertEqual(len(subdirectory_file_list), 0)

    def test_except(self):
        file_list = glob.glob(os.path.join(self.delete_files, '*'))
        self.assertTrue(len(file_list) > 0)
        subdirectory_file_list = glob.glob(os.path.join(self.private, '*'))
        self.assertTrue(len(subdirectory_file_list) > 0)
        with nostderrout():
            delete_all_files(self.delete_files, 'dir_mod.py')
        file_list = glob.glob(os.path.join(self.delete_files, '*'))
        self.assertEqual(len(file_list), 2)
        self.assertTrue(os.path.isfile(self.dir_mod))
        subdirectory_file_list = glob.glob(os.path.join(self.private, '*'))
        self.assertEqual(len(subdirectory_file_list), 0)

    def tearDown(self):
        if os.path.isdir(self.delete_files):
            shutil.rmtree(self.delete_files)


if __name__ == '__main__':
    os.getcwd()
    unittest.main()
