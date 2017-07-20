import random
import time
import sys
import string
import os
from functools import wraps


def benchmark(function):
    """Decorator Function for benchmarking string creation time"""
    @wraps(function)
    def function_wrapper(*args, **kwargs):

        print("Function : {}()".format(function.__name__))
        print("Benchmark: ", end='')
        sys.stdout.flush()

        start = time.time()
        result = function(*args, **kwargs)
        print("{:4.3f}s\n".format(time.time()-start))

        return result
    return function_wrapper

@benchmark
def shuffle(character_list):
    """Shuffles character_list 3-5 times.  Shuffle count value is randomly chosen."""

    shuffle_count = secrets.choice(list(range(3, 6)))
    for _ in range(0, shuffle_count):
        random.shuffle(character_list)
    return character_list

@benchmark
def get_random(char_set=None, length=None, shuffle=False, output_file=False):
    """Returns a randomized string of either pre-set, or user-defined length.

    Args:
        length (int) -- defines length of randomized string. If not provided,
                        function will default length to the length of
                        character_list
        char_set (list[str]) -- list containing single string elements.  If not
                                provided, ASCII upper, lower, punction, and
                                whitespace (single) characters will comrpise
                                sample population for the randomization process
        shuffle (bool) -- If True, character list is sent to shuffle() function
        output_file (bool) -- If True, string is output to text file instead of
                              printed to screen. Useful for larger sequences.
    """
    character_list = char_set or (list(string.ascii_letters+' '+string.punctuation))
    length = length or len(character_list)

    if shuffle:
        character_list = shuffle(character_list)

    randomized_string = "".join([random.choice(character_list) for _ in range(0, length)])

    if output_file:
        filename = 'randomized_string.txt'
        with open(filename, 'w') as f:
            f.write(randomized_string)
        return "Output string written to: {}".format(os.path.abspath(sys.argv[0]))

    return "Output: {}\nLength: {}\n".format(randomized_string, len(randomized_string))


if __name__ == '__main__':
    print(get_random(length=10000, output_file=True))