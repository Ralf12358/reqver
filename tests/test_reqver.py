import os
import shutil
import tempfile
import unittest
from pathlib import Path
from click.testing import CliRunner
from reqver.cli import main

class TestReqver(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        
        # Copy the test data to the temporary directory
        src = Path(__file__).parent / 'testdata'
        dst = Path(self.test_dir) / 'testdata'
        shutil.copytree(src, dst)

    def tearDown(self):
        # Remove the temporary directory after the test
        shutil.rmtree(self.test_dir)

    def test_reqver_no_args(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            # Copy requirements.txt to the current directory
            shutil.copy(Path(self.test_dir) / 'testdata' / 'requirements.txt', 'requirements.txt')
            
            result = runner.invoke(main)
            self.assertEqual(result.exit_code, 0)
            
            # Check if the file was updated
            with open('requirements.txt', 'r') as f:
                content = f.read()
                self.assertIn('click==', content)
                self.assertIn('pip==21.1.3', content)

    def test_reqver_with_file(self):
        runner = CliRunner()
        result = runner.invoke(main, [str(Path(self.test_dir) / 'testdata' / 'requirements.txt')])
        self.assertEqual(result.exit_code, 0)
        
        # Check if the file was updated
        with open(Path(self.test_dir) / 'testdata' / 'requirements.txt', 'r') as f:
            content = f.read()
            self.assertIn('click==', content)
            self.assertIn('pip==21.1.3', content)

    def test_reqver_force(self):
        runner = CliRunner()
        result = runner.invoke(main, ['--force', str(Path(self.test_dir) / 'testdata' / 'requirements.txt')])
        self.assertEqual(result.exit_code, 0)
        
        # Check if the file was updated
        with open(Path(self.test_dir) / 'testdata' / 'requirements.txt', 'r') as f:
            content = f.read()
            self.assertIn('click==', content)
            self.assertIn('pip==', content)  # pip version should be updated

    def test_reqver_no_backups(self):
        runner = CliRunner()
        result = runner.invoke(main, ['--no-backups', str(Path(self.test_dir) / 'testdata' / 'requirements.txt')])
        self.assertEqual(result.exit_code, 0)
        
        # Check if backup file was not created
        self.assertFalse(os.path.exists(Path(self.test_dir) / 'testdata' / 'requirements.txt.bak'))

if __name__ == '__main__':
    unittest.main()
