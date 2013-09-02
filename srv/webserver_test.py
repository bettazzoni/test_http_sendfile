#!/usr/bin/env python3

import unittest
import os, shutil, tempfile
import webserver as ws

def create_a_tmp_file(target_dir):
    fd, file_abspath = tempfile.mkstemp(suffix='.delete.me', prefix='', dir=target_dir)
    os.write(fd, "Hello".encode(encoding='utf_8'))
    os.close(fd)
    return file_abspath

    
class Test(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp(suffix='.delete.me')

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)
                
    def test_dirlist(self):
        self.assertEqual("", ws.dirlist(self.tmp_dir))
        file1_abspath=create_a_tmp_file(self.tmp_dir)
        self.assertEqual(os.path.basename(file1_abspath), ws.dirlist(self.tmp_dir))
        file2_abspath=create_a_tmp_file(self.tmp_dir)
        two_files =  ws.dirlist(self.tmp_dir, "fancy separator")
        self.assertTrue(os.path.basename(file1_abspath) in two_files)
        self.assertTrue(os.path.basename(file2_abspath) in two_files)
        self.assertTrue("fancy separator" in two_files)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_dirlist']
    unittest.main()



    
    
    