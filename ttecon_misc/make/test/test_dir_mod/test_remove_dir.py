#! /usr/bin/env python

import unittest
import sys
import os
import shutil
sys.path.insert(0, os.path.abspath("../.."))
from make.py.dir_mod import remove_dir
from make.py.make_links import make_links
from nostderrout import nostderrout


class testRemoveDir(unittest.TestCase):

    def setUp(self):
        shutil.copytree('../py', './externals')
        make_links('./input/links_remove_dir.txt',
                   makelog='',
                   quiet=True)

    def test_data_links(self):
        self.assertTrue(os.path.exists('../external_links/externals/'))
        file_list_dest = os.listdir('../external_links/externals/')
        file_list_src = os.listdir('./externals/')
        self.assertTrue(file_list_src == file_list_dest)

        self.assertTrue(os.path.exists('../external_links/externals/private/'))
        subdir_file_list_dest = \
            os.listdir('../external_links/externals/private/')
        subdir_file_list_src = os.listdir('./externals/private/')
        self.assertTrue(subdir_file_list_src == subdir_file_list_dest)

        with nostderrout():
            remove_dir('../external_links')

        self.assertFalse(os.path.exists('../external_links/'))
        file_list_src_old = file_list_src
        file_list_src_new = os.listdir('./externals/')
        self.assertTrue(file_list_src_old == file_list_src_new)

    def test_standard(self):
        self.assertTrue(os.path.exists('./externals/'))
        file_list = os.listdir('./externals/')
        self.assertTrue(len(file_list) > 0)
        with nostderrout():
            remove_dir('./externals/')
        self.assertFalse(os.path.exists('./externals/'))

    def tearDown(self):
        if os.path.isdir('./externals/'):
            shutil.rmtree('./externals/')
        if os.path.isdir('../external_links/'):
            remove_dir('../external_links/')

if __name__ == '__main__':
    os.getcwd()
    unittest.main()
