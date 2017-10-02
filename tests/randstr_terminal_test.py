"""unit-tests for sealant's randstr_terminal classes and functions"""

import os
import sys
import io
import shutil

import unittest
import tempfile
import string
import random

import pyperclip

sys.path.insert(0, os.path.abspath('../sealant/randstr'))  # shhh
import randstr_terminal


class RandstrParserTests(unittest.TestCase):
    """Tests for Randstr's argparse methods"""

    def setUp(self):
        """Sets up parser object to be used for argparse.parse_args calls"""
        self.parser = randstr_terminal.RandstrParser().parser
        self.str_len = str(random.randint(10, 100))
        self.reference_char_set = (
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVW"
            "XYZ0123456789!\"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~ ")

    def test_undefined_length(self):
        """Verify passing empty arguments causes system exit"""

        with self.assertRaises(SystemExit) as _:
            self.parser.parse_args()

    def test_length_argument(self):
        """Tests length value and type correctly set"""

        args = self.parser.parse_args([self.str_len])
        self.assertEqual(int(self.str_len), args.len)

    def test_character_set_argument(self):
        """Tests that when an alternate character set is provided, that set
        contains all provided characters in their original index positions."""

        user_char_set = ''.join(random.sample(
            self.reference_char_set, random.randint(10, 90)))

        args = self.parser.parse_args(
            [self.str_len, '--character-set', user_char_set])

        self.assertEqual(user_char_set, args.characters)

    def test_switch_combinations(self):
        """Verifies all available switches accepted as an argument"""

        switches = ['-p', '--print', '-cp', '--copy', '-f', '--file', '-ro',
                    '--raw-output', '-s', '--shuffle', '-rl', '--remove-limit',
                    ('-cs', ''), ('--character-set', '')]

        # Sets up switches with required length argument
        args = (('1',) + i if isinstance(i, tuple) else ('1', i) for i in switches)

        for arg in args:
            with self.subTest(arg=arg):
                self.assertIsNot(self.parser.parse_args(arg), None)

    def test_boolean_switches(self):
        """Sub-tests for simple switches that store as True when included as an
        argument."""
        switches = {'print': ['-p', '--print'],
                    'copy': ['-cp', '--copy'],
                    'shuffle': ['-s', '--shuffle'],
                    'raw_output': ['-ro', '--raw-output'],
                    'remove_limit': ['-rl', '--remove-limit']}

        for dest, switches in switches.items():
            for switch in switches:
                with self.subTest(switch=switch):
                    args = self.parser.parse_args([self.str_len, switch])
                    self.assertTrue(getattr(args, dest))


class RandstrOutputFiles(unittest.TestCase):
    """Test cases for randstr_terminal.randstr_output() file related
    operations."""

    def setUp(self):
        """Sets up default parser and test directories used during tests"""

        self.test_dir = os.path.abspath(tempfile.mkdtemp())
        os.chdir(self.test_dir)

        self.randstr_output = randstr_terminal.RandstrOutput
        self.parser = randstr_terminal.RandstrParser().parser
        self.str_len = str(random.randint(10, 100))

        sys.stdout = io.StringIO()

    def tearDown(self):
        """Removes any files/directories created during file write test
        procedures and resets sys.stdout back to its default value"""

        os.chdir(os.path.abspath(os.path.dirname(__file__)))
        shutil.rmtree(self.test_dir)

        sys.stdout = sys.__stdout__

    def test_no_filename_extension(self):
        """Tests that providing a filename without an extension defaults the
        extension to .txt"""

        expected_filename = os.path.join(self.test_dir, 'test_file.txt')
        returned_filename = randstr_terminal._write_file('', 'test_file')

        self.assertEqual(expected_filename, returned_filename)

    def test_filename_with_extension(self):
        """Tests that providing a filename extension doesn't add an additional
        extension"""

        expected_filename = os.path.join(self.test_dir, 'test_file.txt')
        returned_filename = randstr_terminal._write_file('', 'test_file.txt')

        self.assertEqual(expected_filename, returned_filename)

    def test_file_write(self):
        """Test that randomized string correctly writes to file"""

        args = self.parser.parse_args([self.str_len, '--file', '--raw-output'])

        self.randstr_output(args).process_parsed_args()
        output = sys.stdout.getvalue()

        filename = os.path.join(self.test_dir, args.file)
        with open(filename, 'r') as f:
            random_string = f.read()

        self.assertIn(random_string, output)

    def test_default_filename_iteration(self):
        """Verifies that generated filenames created when --file is provided
        without a user-defined filename are unique in respect to
        other filenames in CWD."""

        for file_number in range(1, 11):
            filename = 'randstr_{}.txt'.format(file_number)
            with open(filename, 'w') as f:
                f.flush()

        parser = randstr_terminal.RandstrParser().parser
        args = parser.parse_args([self.str_len, '--file'])
        self.randstr_output(args).process_parsed_args()

        expected_filename = 'randstr_11.txt'
        self.assertTrue(os.path.exists(expected_filename))

    def test_user_defined_filename(self):
        """Tests that user defined filename overrides default filename for
        --file switch"""

        char_set = '{s.ascii_letters}{s.digits}'.format(s=string)
        random_name = ''.join(
            random.choice(char_set) for _ in range(0, random.randint(10, 50)))

        user_filename = "{}.txt".format(random_name)

        args = self.parser.parse_args([self.str_len, '-f', user_filename, '-ro'])
        self.randstr_output(args).process_parsed_args()
        output = sys.stdout.getvalue()

        with open(user_filename, 'r') as f:
            contents = f.read()

        self.assertEqual(contents, output)


class RandstrOutputStandard(unittest.TestCase):
    """Tests non file related operations in randstr_terminal.randstr_output()"""

    def setUp(self):
        """Initialize common test attributes"""

        # Saves clipboard as --copy switch will overwrite it's contents
        self.clipboard_contents = pyperclip.paste()
        self.randstr_output = randstr_terminal.RandstrOutput

        self.parser = randstr_terminal.RandstrParser().parser
        self.str_len = str(random.randint(10, 100))

        sys.stdout = io.StringIO()

    def tearDown(self):
        """Restores clipboard and resets sys.stdout back to its default value"""

        pyperclip.copy(self.clipboard_contents)
        sys.stdout = sys.__stdout__

    def test_raw_output(self):
        """Tests that --raw-output limits output only to generated string"""

        args = self.parser.parse_args([self.str_len, '--raw-output'])
        self.randstr_output(args).process_parsed_args()

        output = sys.stdout.getvalue()
        self.assertEqual(int(self.str_len), len(output))

    def test_copy_operation(self):
        """Test that use of '--copy' switch copies string to clipboard"""

        args = self.parser.parse_args([self.str_len, '--raw-output', '--copy'])
        self.randstr_output(args).process_parsed_args()

        output = sys.stdout.getvalue()
        clipboard_contents = pyperclip.paste()
        self.assertEqual(clipboard_contents, output)

    def test_print_operation(self):
        """Tests that --print switch prints string to terminal"""
        args = self.parser.parse_args(['10', '--print', '--copy'])
        self.randstr_output(args).process_parsed_args()

        output = sys.stdout.getvalue()
        clipboard_contents = pyperclip.paste()
        self.assertIn(clipboard_contents, output)

    def test_set_length(self):
        """Tests that generated string matches user defined length value.  Test
        is for lengths under the default 1000 character limit"""

        args = self.parser.parse_args([self.str_len, '--raw-output'])
        self.randstr_output(args).process_parsed_args()

        output = sys.stdout.getvalue()
        self.assertEqual(int(self.str_len), len(output))

    def test_default_length_limit(self):
        """Tests that length defaults to 1000 when value exceeding 1000 provided
        without the --remove-limit switch."""

        args = self.parser.parse_args(['1500', '--raw-output'])
        self.randstr_output(args).process_parsed_args()

        output = sys.stdout.getvalue()
        self.assertEqual(1000, len(output))

    def test_length_limit_override(self):
        """Tests that providing --remove-limit switch allows strings exceeding
        1000 characters to be generated."""

        args = self.parser.parse_args(['1500', '--remove-limit', '--raw-output'])
        self.randstr_output(args).process_parsed_args()

        output = sys.stdout.getvalue()
        self.assertEqual(1500, len(output))


if __name__ == '__main__':
    print("Testing randstr_terminal Methods and Functions\n")
    unittest.main(buffer=True)
