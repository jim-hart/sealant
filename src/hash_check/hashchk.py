# ----------------------------Compatibility Imports----------------------------
from __future__ import print_function
from six.moves import range

import sys
import hashlib
if sys.version_info < (3, 6):
    import sha3
# -----------------------------------------------------------------------------

import os
import hmac  # Python 2.7 and 3.3+

# TODO: Implement hash method choices

class HashCheck(object):
    """Class for comparing, processing, and generating hash digests."""

    @staticmethod
    def process_digest(digest):
        """Determines if source of digest is stored in a text file, or if it's a
        string provided by user.
        
        Args:
            digest (str): filename or string containing digest to be processed
        
        Returns:
            str: hash digest stipped of leading and trailing whitespace
        """

        if os.path.isfile(digest):
            with open(digest, 'r') as f:
                return f.read().split(' ')[0]
        else:
            return digest.strip()

    @staticmethod
    def generate_digest(filename):
        """Returns hexadecimal digest generated from filename
        
        Args:
            filename (str): filename of binary file
        
        Returns:
            str: hash digest generated from binary file
        """

        buffer_size = 65536  # Buffer used to cut down on memory for large files.
        blocks = (os.path.getsize(filename) // buffer_size) + 1

        hash_digest = hashlib.sha256()

        with open(filename, 'rb') as f:
            # generator expression used for reading file in chunks
            generator = (f.read(buffer_size) for _ in range(blocks))
            for data in generator:
                hash_digest.update(data)

        return hash_digest.hexdigest()

    @staticmethod
    def compare_digests(digest_1, digest_2):
        """Returns result of equality comparison betwen digest_1 and digest_2
        
        Args:
            digest_1 (str): digest to be compared against digest_2
            digest_2 (str): digest to be compared against digest_1
        
        Returns:
            bool: result of comparison of digest_1 and digest_2
        """

        return hmac.compare_digest(digest_1, digest_2)


