import os
from pyfakefs.fake_filesystem_unittest import TestCase

from sardadmin.folders import count_sard_folders, rename_sard_folder


class FoldersTest(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_count_sard_folders(self):
        filepath = '/a/b/c/image.dd'
        self.fs.create_file(filepath)
        self.assertEqual(count_sard_folders(filepath), 0)
        self.fs.create_dir('/a/b/c/SARD')
        self.assertEqual(count_sard_folders(filepath), 1)
        self.fs.create_dir('/a/b/c/sard')
        self.assertEqual(count_sard_folders(filepath), 1)
        self.fs.create_dir('/a/b/c/SARD.old')
        self.assertEqual(count_sard_folders(filepath), 2)
        self.fs.create_dir('/a/b/c/SARDold')
        self.assertEqual(count_sard_folders(filepath), 3)


    def test_rename_sard_folder(self):
        filepath = '/a/b/c/image.dd'
        self.fs.create_file(filepath)
        self.assertEqual(rename_sard_folder(filepath), False)

        self.fs.create_dir('/a/b/c/SARD')
        self.assertEqual(rename_sard_folder(filepath), True)
        self.assertEqual(os.path.exists('/a/b/c/SARD'), False)
        self.assertEqual(os.path.exists('/a/b/c/SARD.old'), True)
        self.assertEqual(os.path.exists('/a/b/c/SARD.old2'), False)
        self.assertEqual(os.path.exists('/a/b/c/SARD.old3'), False)
        
        self.fs.create_dir('/a/b/c/SARD')
        self.assertEqual(rename_sard_folder(filepath), True)
        self.assertEqual(os.path.exists('/a/b/c/SARD'), False)
        self.assertEqual(os.path.exists('/a/b/c/SARD.old'), True)
        self.assertEqual(os.path.exists('/a/b/c/SARD.old2'), True)
        self.assertEqual(os.path.exists('/a/b/c/SARD.old3'), False)
        
        
        self.fs.create_dir('/a/b/c/SARD')
        self.assertEqual(rename_sard_folder(filepath), True)
        self.assertEqual(os.path.exists('/a/b/c/SARD'), False)
        self.assertEqual(os.path.exists('/a/b/c/SARD.old'), True)
        self.assertEqual(os.path.exists('/a/b/c/SARD.old2'), True)
        self.assertEqual(os.path.exists('/a/b/c/SARD.old3'), True)
        
