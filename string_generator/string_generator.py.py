import random
import time
import locale


def file_processing(get_sample_set=False, write_string=False, random_str=None):
    """Handles retrieving and writing of files used in this program
    
    Args:
        get_sample_set (bool) -- If True, returns string containing character set.
        write_string  (bool) -- If True, writes random_str to .txt file
        random_str (str) -- Contains randomized string; must be provided if
                            write_string=True provided

    """
    bench = time.time

    if get_sample_set:
        filename = 'character_sample.txt'
        with open(filename) as f_obj:
            letters = f_obj.read()
        return list(set(letters))

    if write_string and random_str:
        filename = 'string_dump.txt'

        start = bench()
        with open(filename, 'w') as f_obj:
            f_obj.write(random_str)
        return bench() - start


def shuffle(character_list):

    bench = time.time
 
    start = bench()
    for n in range(0, 3):
        random.shuffle(character_list)
    shuffle_time = bench() - start

    return 


def get_random(character_list, shuff_time, length=None):
    """Returns a randomized string of variable length

    Args:
        length (int) -- defines length of randomized string. If not provided,
                        function will default length to the length of character_set
        character_list (list[str]) -- list containing single string elements
    """

    # aliases
    bench = time.time
    suffule_time = shuff_time

    if not length:
        length = len(character_list)

  
    long_string = []
    start = bench()
    for x in range(0, length):
        long_string += random.choice(character_list)
    construction_time = bench() - start

    return long_string, shuffle_time, construction_time


if __name__ == '__main__':
    sample_set = file_processing(get_sample_set=True)
    rand_str, shuf_time, construc_time = get_random(sample_set, length=10 ** 8)

    #write_time = file_processing(write_string=True, random_str=rand_str)

    # metric conversion
    SI = {'ms': 1000, 's': 1}
    shuf_time *= SI['ms']
    construc_time *= SI['s']
    write_time *= SI['ms']

    # printouts
    print("Shuff Time: {:12.8f}ms".format(shuf_time))
    print("Build Time: {:12.8f}ms".format(construc_time))
    print("Write Time: {:12.8f}ms".format(write_time))

    print("\nString Len: {:>6,}".format(len(rand_str)))
