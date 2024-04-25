import unittest
import tempfile
import os

from pyhashers import hash_directory_contents
import hashlib


def hash_directory_contents_with_python(directory):
    directory_hashes = {}
    md5_hash = hashlib.md5()
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                while True:
                    data = f.read(4096)
                    if not data:
                        break
                    md5_hash.update(data)
            directory_hashes[file] = md5_hash.hexdigest()
    return directory_hashes


class TestHashDirectoryContentsPythonEqualsRust(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, 'test_file.txt')
        with open(self.test_file, 'w') as f:
            f.write('Hello, World!')

    def test_hash_directory_contents(self):
        python_result = hash_directory_contents_with_python(self.test_dir)
        rust_result = hash_directory_contents(self.test_dir)
        self.assertEqual(python_result, rust_result)

    def tearDown(self):
        os.remove(self.test_file)
        os.rmdir(self.test_dir)

if __name__ == '__main__':
    unittest.main()