"""unittests for sealant's randstr modules

Todo: *setUp and tearDown methods

"""

import unittest
import string
import random
import sys
import os

sys.path.insert(0, os.path.abspath('../sealant/randstr'))  # Ughh
from randstr import RandomString
from randstr_terminal import RandstrParser


class RandomStringGeneration(unittest.TestCase):
    """Tests for RandomString methods"""

    def setUp(self):
        """Defines object instance used for test cases"""
        rand_length = random.randint(10, 100)
        self.randstr_generator = RandomString(length=rand_length)

        self.default_char_set = self.randstr_generator.default_char_set
        self.randstr_length = self.randstr_generator.length
        self.original_chars = self.randstr_generator.char_set

    def test_generated_length(self):
        """Tests that randomly generated strength matches length parameter"""
        self.assertEqual(self.randstr_length, len(self.randstr_generator()))

    def test_default_char_set(self):
        """Verify correct default character set used"""
        char_set = ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVW"
                    "XYZ0123456789!\"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~ ")

        self.assertEqual(self.default_char_set, char_set)

    def test_user_char_set_generation(self):
        """Verify only user defined characters populate randomly generated
        string"""

        self.randstr_generator.char_set = user_set = "abcDEF123,.;"
        for char_len in range(10, 101, 10):
            return_str = self.randstr_generator()

            with self.subTest(return_str=return_str, user_set=user_set):
                self.assertTrue(set(user_set).issuperset(set(return_str)))

    def test_character_shuffle(self):
        """Tests that character set is shuffled when shuffle=True argument
        provided to RandomString()"""
        self.randstr_generator.shuffle_characters()
        shuffled_set = self.randstr_generator.char_set
        original_set = self.default_char_set

        self.assertNotEqual(original_set, shuffled_set)

    def test_char_set_post_shuffle(self):
        """Test that shuffle process only modifies indices and all original
        characters are still present (use default character set as baseline
        variable)"""
        self.randstr_generator.shuffle_characters()
        shuffled_set = self.randstr_generator.char_set

        # noinspection PyCompatibility
        self.assertCountEqual(shuffled_set, self.original_chars)

    def test_undefined_length(self):
        """Test that value of None is returned when no length is provided to
        RandomString()"""

        # Simulates default RandomString argument assignment
        self.randstr_generator.length = None
        self.assertIsNone(self.randstr_generator())


if __name__ == '__main__':
    unittest.main()
