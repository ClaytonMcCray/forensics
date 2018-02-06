#!/usr/bin/env python3
Author = 'Clayton McCray'
Version = 2.1

import os
from shutil import copy2
import sys

###############################################################################################
# TODO:
###############################################################################################

extensions = []
unsorted = []


def read_input():
    try:
        if sys.argv[1][0] == '-':
            base, target = flags(sys.argv[1], sys.argv[2], sys.argv[3])
        else:
            base = sys.argv[1]
            target = sys.argv[2]
            os.mkdir(target)
        try:
            os.mkdir(target + '/unsorted')  # files without clear extension
            main(base, target)
        except FileExistsError:
            print('Error! Does the target exist? Try [-e].')
    except IndexError:
        flags('-h', '', '')


# This will handle flags passed in
def flags(flag, base, target):
    HELP = 'datasort ' + str(Version) + \
           '\nAuthor: ' + Author + '' \
           '\ndatasort [-option] /path/to/base /path/to/target' \
           '\n\nNote that flags should be compounded, i.e. -tb instead of -t -b' \
           '\n-e\t\tTarget file \'e\'xists; do not overwrite (default is to overwrite target)' \
           '\n-b\t\tBase path is abbreviated; it begins in the pwd. Do not lead with / if in pwd' \
           '\n-t\t\tTarget path is abbreviated; it beings in the pwd. Do not lead with / if in pwd' \
           '\n-h\t\tDisplay this menu'

    if 'h' in flag:
        print(HELP)
    if 'b' in flag:
        base = os.getcwd() + '/' + base
    if 't' in flag:
        target = os.getcwd() + '/' + target
    if 'e' in flag:  # -e for 'exists'
        if target[len(target)-1] == '/':
            target = target[:len(target)-1]  # this will strip / if the user includes it for the directory
    return base, target



def is_extension(ext, f_name):
    check_at = f_name.find(ext) + len(ext)  # this basically finds what should be the character after the
    try:                                        # the extension if it's correct; if it's not correct it errors
        f_name[check_at]  # this checks that there are no characters at the end of where the extension should be
        return False
    except IndexError:  # if the extension is actually the last piece, there will be an index error
        return True


# this function moves the files listed in no_ext into the /unsorted directory
def group_unsorted(no_ext, target):
    error = []
    for f in no_ext:
        try:
            copy2(f, target + '/unsorted')
            print(f)
        except:
            error.append(f)
    return error


def main(base, target):
    # not_sortable = True
    MAX_EXT_LEN = 6  # this is just an intelligent guess for a max length of extensions. Change at will/need
    # walk the base to learn extensions and create the directories to house them
    for subdir, dirs, files in os.walk(base):
        for file_name in files:
            not_sortable = True  # check if each file is sortable # causes a problem with everything going to unsorted
            for c in range(len(file_name)):
                if file_name[c] == '.':
                    if file_name[c:].lower() in extensions:
                        not_sortable = False
                    elif len(file_name[c:]) <= MAX_EXT_LEN:
                        extensions.append(file_name[c:].lower())
                        os.mkdir(target + '/' + file_name[c + 1:].lower())  # +1 so that the directory isn't a dotfile
                        print(file_name[c:].lower())
                        not_sortable = False  # this file WAS sorted
            if not_sortable:
                unsorted.append(subdir + '/' + file_name)

    for subdir, dirs, files in os.walk(base):
        for file_name in files:
            if subdir + '/' + file_name in unsorted:  # don't do all the other stuff if the file has been determined
                pass                                    # to not have a sortable extension
            else:
                for i in extensions:  # check every extension in the file_name until success
                    if i in file_name:
                        if is_extension(i, file_name):
                            print(subdir + '/' + file_name)
                            copy2(subdir + '/' + file_name, target + '/' + i[1:])
                            break  # break one level -- we can stop checking extensions after success of is_extension

    error_out = group_unsorted(unsorted, target)  # attempt to move unsorted

    if len(error_out) > 0:
        print('Error on:')
        print(error_out)
    input('Press Enter to quit')

read_input()
