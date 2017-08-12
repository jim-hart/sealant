# ----------------------------Compatibility Imports----------------------------
from __future__ import print_function
from six.moves import range
# -----------------------------------------------------------------------------

import hashlib
import os
import hmac  # Python 2.7 and 3.3+


# TODO: Implement hash method choices
# TODO: Repent for not adding doc-strings, then add the doc-strings

class HashCheck(object):
    """Class for comparing, processing, and generating hash digests"""

    @staticmethod
    def process_digest(digest):
        """Either returns digest read from file, or returns digest with
        leading/trailing whitespace stripped.  Process action based on digest
        source."""

        if os.path.isfile(digest):
            with open(digest, 'r') as f:
                return f.read().split(' ')[0]
        else:
            return digest.strip()

    @staticmethod
    def generate_digest(filename):
        """Returns hexadecimal digest generated from filename"""

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
        """Returns True if digest_1 == digest_2"""

        return hmac.compare_digest(digest_1, digest_2)
