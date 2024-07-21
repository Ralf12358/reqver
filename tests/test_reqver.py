import unittest
import tempfile
import shutil
from pathlib import Path
from click.testing import CliRunner
from reqver.cli import main, get_package_version

class TestReqver(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

        # remove the backup file from the previous test
        (Path(self.test_dir) / 'requirements.txt.bak').unlink(missing_ok=True)


        # Copy the testdata to the temporary directory
        self.testdata_dir = Path(__file__).parent / 'testdata'
        shutil.copytree(self.testdata_dir, self.test_dir, dirs_exist_ok=True)

        # Set up the CLI runner
        self.runner = CliRunner()

    def tearDown(self):
        # Remove the temporary directory after the test
        shutil.rmtree(self.test_dir)

    def test_basic_functionality(self):
        result = self.runner.invoke(main, [str(Path(self.test_dir) / 'requirements.txt')])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Processing", result.output)
        self.assertIn("Updated", result.output)

        # Check if backup file was created
        self.assertTrue((Path(self.test_dir) / 'requirements.txt.bak').exists())

        # Check if versions were updated
        with open(Path(self.test_dir) / 'requirements.txt', 'r') as f:
            content = f.read()
            self.assertIn('click>=8.0.1', content)  # This should not change without --force
            self.assertIn('pip==21.1.3', content)  # This should not change without --force
            self.assertIn(f'packaging=={get_package_version("packaging")}', content)

    def test_force_option(self):
        result = self.runner.invoke(main, ['--force', str(Path(self.test_dir) / 'requirements.txt')])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Processing", result.output)
        self.assertIn("Updated", result.output)

        # Check if versions were updated, including pip
        with open(Path(self.test_dir) / 'requirements.txt', 'r') as f:
            content = f.read()
            self.assertRegex(content, r'click>=\d+\.\d+\.\d+')
            self.assertIn(f'pip=={get_package_version("pip")}', content)
            self.assertIn(f'packaging=={get_package_version("packaging")}', content)

    def test_no_backups_option(self):
        result = self.runner.invoke(main, ['--no-backups', str(Path(self.test_dir) / 'requirements.txt')])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Processing", result.output)
        self.assertIn("Updated", result.output)

        # Check that no backup file was created
        self.assertFalse((Path(self.test_dir) / 'requirements.txt.bak').exists())

        # Check if versions were updated correctly
        with open(Path(self.test_dir) / 'requirements.txt', 'r') as f:
            content = f.read()
            self.assertIn('click>=8.0.1', content)  # This should not change without --force
            self.assertIn('pip==21.1.3', content)  # This should not change without --force
            self.assertIn(f'packaging=={get_package_version("packaging")}', content)

        # Run the command again to ensure no backup is created on subsequent runs
        result = self.runner.invoke(main, ['--no-backups', str(Path(self.test_dir) / 'requirements.txt')])
        self.assertEqual(result.exit_code, 0)
        self.assertFalse((Path(self.test_dir) / 'requirements.txt.bak').exists())

    def test_multiple_files(self):
        # Create a second requirements file
        shutil.copy(Path(self.test_dir) / 'requirements.txt', Path(self.test_dir) / 'requirements2.txt')

        result = self.runner.invoke(main, [str(Path(self.test_dir) / 'requirements.txt'),
                                           str(Path(self.test_dir) / 'requirements2.txt')])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Processing", result.output)
        self.assertIn("Updated", result.output)

        # Check if both files were processed
        self.assertIn("requirements.txt", result.output)
        self.assertIn("requirements2.txt", result.output)

    def test_no_changes_needed(self):
        # First, update the requirements file
        self.runner.invoke(main, [str(Path(self.test_dir) / 'requirements.txt')])

        # Then run again, no changes should be needed
        result = self.runner.invoke(main, [str(Path(self.test_dir) / 'requirements.txt')])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("No changes were necessary", result.output)

    def test_file_not_found(self):
        result = self.runner.invoke(main, ['nonexistent_file.txt'])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Error", result.output)

if __name__ == '__main__':
    unittest.main()
