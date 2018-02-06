#!/usr/bin/env python3
import os
from shutil import copy2
import sys

###############################################################################################
# TODO:
# Moved large chunk of program to main(), hasn't been tested.
# Need to enter some flags. First one will be -e for 'file exists' for the target directory
# Maybe should break up the main() into smaller pieces
###############################################################################################

extensions = []
# not_sortable = True
unsorted = []


def read_input():
    if sys.argv[1][0] == '-':
        flags(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        base = sys.argv[1]
        target = sys.argv[2]
        os.mkdir(target)
        os.mkdir(target + '/unsorted')  # files without clear extension
        main(base, target)


# This will handle flags passed in
def flags(flag, base, target):
    pass


def is_extension(ext, f_name):
    check_at = f_name.find(ext) + len(ext)
    try:
        f_name[check_at]  # this checks that there are no characters at the end of where the extension should be
        return False
    except IndexError:  # if the extension is actually the last piece, there will be an index error
        return True


def main(base, target):
    not_sortable = True
    for subdir, dirs, files in os.walk(base):
        for file_name in files:
            for c in range(len(file_name)):
                if file_name[c] == '.':
                    if file_name[c:] in extensions:
                        pass
                    elif len(file_name[c:]) <= 5:
                        extensions.append(file_name[c:])
                        os.mkdir(target + '/' + file_name[c + 1:])
                        print(file_name[c:])
                        not_sortable = False
            if not_sortable:
                unsorted.append(subdir + '/' + file_name)

    for subdir, dirs, files in os.walk(base):
        for file_name in files:
            for i in extensions:
                if i in file_name:
                    if is_extension(i, file_name):
                        print(subdir + '/' + file_name)
                        copy2(subdir + '/' + file_name, target + '/' + i[1:])

    error_out = []
    for f in unsorted:
        try:
            copy2(f, target + '/unsorted')
            print(f)
        except:
            error_out.append(f)

    print('Error on:')
    print(error_out)
    input('Press Enter to quit')


read_input()
