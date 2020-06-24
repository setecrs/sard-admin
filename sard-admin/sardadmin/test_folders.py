import os
from pyfakefs.fake_filesystem_unittest import TestCase

from sardadmin.folders import count_sard_folders, rename_sard_folder, listSubfolders, default_rw_mode, default_ro_mode, set_ro, set_rw


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
        
    def test_listsubfolders(self):
        filepath = '/operacoes/groupfolder/a/b/c/image.dd'
        self.fs.create_file(filepath)
        filepath = '/operacoes/groupfolder/f1.txt'
        self.fs.create_file(filepath)
        os.symlink('f1.txt', '/operacoes/groupfolder/f2.txt')
        self.assertTrue(os.path.exists('/operacoes/groupfolder/a/b/c/image.dd'))
        self.assertTrue(os.path.exists('/operacoes/groupfolder/f1.txt'))
        self.assertTrue(os.path.exists('/operacoes/groupfolder/f2.txt'))
        got = listSubfolders('groupfolder')
        self.assertListEqual(got, ['a'])
        self.assertListEqual(listSubfolders('groupfolder', 'a'), ['b'])
        with self.assertRaises(AssertionError):
            listSubfolders('groupfolder', '/a')
        self.assertListEqual(listSubfolders('groupfolder', 'a/b'), ['c'])
        self.assertListEqual(listSubfolders('groupfolder', 'a/b/c'), [])
        with self.assertRaises(AssertionError):
            listSubfolders('groupfolder', 'a/..')

    def test_default_rw(self):
        isDir=True
        isFile=False
        self.assertEqual(default_rw_mode('/rw_mode/', isDir), 0o070)
        self.assertEqual(default_rw_mode('/rw_mode/file.txt', isFile), 0o060)
        self.assertEqual(default_rw_mode('/rw_mode/a', isDir), 0o070)
        self.assertEqual(default_rw_mode('/rw_mode/a/file.txt', isFile), 0o060)
        self.assertEqual(default_rw_mode('/rw_mode/indexador/tools/file', isFile), 0o070)
        self.assertEqual(default_rw_mode('/rw_mode/indexador/jre/bin/file', isFile), 0o070)
        self.assertEqual(default_rw_mode('/rw_mode/indexador/lib/file', isFile), 0o070)
        self.assertEqual(default_rw_mode('/rw_mode/a/file.exe', isFile), 0o070)

    def test_default_ro(self):
        isDir=True
        isFile=False
        self.assertEqual(default_ro_mode('/ro_mode/', isDir), 0o050)
        self.assertEqual(default_ro_mode('/ro_mode/file.txt', isFile), 0o040)
        self.assertEqual(default_ro_mode('/ro_mode/a', isDir), 0o050)
        self.assertEqual(default_ro_mode('/ro_mode/a/file.txt', isFile), 0o040)
        self.assertEqual(default_ro_mode('/ro_mode/indexador/tools/file', isFile), 0o050)
        self.assertEqual(default_ro_mode('/ro_mode/indexador/jre/bin/file', isFile), 0o050)
        self.assertEqual(default_ro_mode('/ro_mode/indexador/lib/file', isFile), 0o050)
        self.assertEqual(default_ro_mode('/ro_mode/a/file.exe', isFile), 0o050)

