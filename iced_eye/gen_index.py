#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# Import python libraries
import os
import sys
from pyrainbowterm import *

# Source code meta data
__author__ = 'Dalwar Hossain'
__email__ = 'dalwar.hossain@protonmail.com'

# Templates directory
templates_dir = '../templates' 

# Check template files
def check_template_files():
    """
    This function checks permission for the template files

    :return: (list) A python list of files present in templates directory
    """
    
    # Check for files
    print('Checking file permissions.....', log_type='info')
    file_list = os.listdir(templates_dir)
    # Check file permissions
    for item in sorted(file_list):
        current_file = os.path.join(templates_dir, item)
        if os.access(current_file, os.F_OK):
            # print('{} file found!'.format(current_file), log_type='info')
            if os.access(current_file, os.R_OK):
                print('{} ............... '.format(item), log_type='info', end='')
                print('OK', color='green')
            else:
                print('{} ............... ', log_type='error', end='')
                print('NOT OK', color='red')
                sys.exit(1)
        else:
            print('Can not access files!', log_type='error', color='red')
            sys.exit(1)
    # Return
    return file_list


# Check if all expected files are available or not
def is_all_expected_files_available(files_in_template_dir=None, expected_files_list=None):
    """
    This fucntion checks if all the expected files are available or nto

    :return: (boolean) True, if all expected files are available, False, Otherwiese
    """

    return all(x in files_in_template_dir for x in expected_files_list)


# Generate index html
def generate_indexhtml():
    """
    This function generates a merged file called index.html from
    given templates and sequence

    :return: <>
    """
    # Check file existance and permissions
    currently_available_files = check_template_files()

    # Check if all the necessary files are present or not
    expected_files = ['header.html', 'profile.html', 'menu.html', 'resume.html',
                      'research.html', 'projects.html', 'blog.html', 'footer.html']
    all_files_available = is_all_expected_files_available(files_in_template_dir=currently_available_files,
                                                          expected_files_list=expected_files)
    if all_files_available:
        print('All expected files available', log_type='info')
        # All the files are available, read all of them and create index.html
        print('Creating index.html file.....', log_type='info')
        try:
            with open('../output/index.html', 'w') as output_file:
                for item in expected_files:
                    fname = os.path.join(templates_dir, item)
                    with open(fname) as segmented_file:
                        output_file.write(segmented_file.read())
            print('index.html file creation complete!', log_type='info')
        except Exception as e:
            print('ERROR: {}'.format(e), log_type='error', color='red')
            sys.exit(1)
        
    else:
        missing_files = list(set(expected_files).difference(currently_available_files))
        print('Missing files: {}'.format(missing_files), log_type='info')
        sys.exit(1)
    pass


# Boiler plate to run this program
if __name__ == '__main__':
    generate_indexhtml()
