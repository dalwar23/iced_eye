#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# Import python libraries
import os
import sys
import io
from datetime import datetime
from pyrainbowterm import *
try:
    from bs4 import BeautifulSoup
except ImportError as e:
    print('Can not import BeautifulSoup', log_type='error', color='red')

# Source code meta data
__author__ = 'Dalwar Hossain'
__email__ = 'dalwar.hossain@protonmail.com'

# Templates directory
templates_dir = '../templates'


# Set default encoding
reload(sys)
sys.setdefaultencoding('utf8')

# Create a function to generate posts
def generate_post():
    """
    This function genrates posts in the blog section of the website
    It uses text file from posts directory to create posts

    :return: (obj) File oject
    """
    # Read post
    print('Reading post.....', log_type='info')
    html_post_file = os.path.join(templates_dir, 'latest_post.html')
    with io.open(html_post_file, 'r', encoding='utf8') as post:
        html_post = post.read()
    # Create a Beautifulsoup object to parse the html
    print('Parsing HTML.....', log_type='info')
    soup = BeautifulSoup(html_post, 'html.parser')
    post_title = soup.title.string
    post_body_elements = soup.select('body  p')
    # Join all the paragraph's of the post body
    post_body = '\n'.join(str(item) for item in post_body_elements)
    post_category = soup.category.string
    post_date = datetime.now().strftime('%A, %B %d, %Y @ %H:%M')
    # Now read the pre_blog template and create blog.html
    input_file = os.path.join(templates_dir, 'pre_blog.html')
    output_file = os.path.join(templates_dir, 'blog.html')
    # Read input tamplate and create blog.html file
    print('Creating blog.html file.....', log_type='info')
    replace_dict = {'_post_title_' : post_title, '_post_body_' : post_body,
                    '_post_date_time_' : post_date, '_post_category_' : post_category}
    with io.open(input_file, 'r', encoding='utf8') as infile, io.open(output_file, 'w', encoding='utf8') as outfile:
        for line in infile:
            for source, target in replace_dict.iteritems():
                line = line.replace(source, target)
            outfile.write(line)
    # HTML file creation complete
    print('HTML file creation complete!', log_type='info')


# Boiler plate to run this program
if __name__ == '__main__':
    generate_post()
