#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# Import python libraries
import os
import sys
import io
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

# Posts directory
posts_dir = '../posts'

# Latest 'number_of_post_to_show' post to show
number_of_post_to_show = 4


# Set default encoding
reload(sys)
sys.setdefaultencoding('utf8')


# Template of the blog
def create_html_post(post_title=None, post_date=None, post_category=None, post_body=None):
    """
    This function contains the template of the posts structure
    """
    html_blog_doc_post = """                            <li>
                                <div class="timelineUnit">
                                    <h4>{ptitle}<span class="timelineDate">{pdate}</span></h4>
                                    <h5>Category: {category}</h5>
                                    <p>
                                        {post}
                                    </p>
                                </div>
                            </li>"""

    html_blog_doc_post = html_blog_doc_post.format(ptitle=post_title, pdate=post_date,
                                                   category=post_category, post=post_body)
    # return
    return html_blog_doc_post


# Create string of posts
def string_posts(latest_posts=None):
    """
    This function reads the posts and creats the posts section in html
    """
    # Define variable
    post_string = ''

    # Read the posts
    for item in latest_posts:
        # Read post
        print('Reading post [{}].....'.format(item), log_type='info')
        html_post_file = os.path.join(posts_dir, item)
        with io.open(html_post_file, 'r', encoding='utf8') as post:
            html_post = post.read()
        
        # Create a Beautifulsoup object to parse the html
        print('Parsing HTML.....', log_type='info')
        soup = BeautifulSoup(html_post, 'html.parser')
        ptitle = str(soup.ptitle.string)  # <Ptitle> tag contains the title of the post
        post_body_elements = soup.select('post  p')  # <post> tag holds the main body of the post
        # Join all the paragraph's of the post body
        post = '\n'.join(str(item) for item in post_body_elements)
        category = str(soup.category.string)  # <category> tag contains the post category
        pdate = str(soup.pdate.string)  # <pdate> tag is the date and time the post was written
  
        # Create the posts
        print('Creating post entry for [{}].....'.format(item), log_type='info')
        ret_post = create_html_post(post_title=ptitle, post_date=pdate, post_category=category,
                                    post_body=post)
        post_string += str(ret_post)
        post_string += '\n'
    
    # Return
    return post_string


# Check template files
def check_post_files():
    """
    This function checks permission for the template files

    :return: (list) A python list of files present in posts directory
    """
    
    # Check for files
    print('Checking file permissions for posts.....', log_type='info')
    file_list = os.listdir(posts_dir)

    # Check file permissions
    for item in sorted(file_list):
        current_file = os.path.join(posts_dir, item)
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


# Create a function to generate posts
def generate_post():
    """
    This function genrates posts in the blog section of the website
    It uses text file from posts directory to create posts

    :return: (obj) File oject
    """
    # Make sure there are posts in the posts directory
    post_file_list = check_post_files()
    if len(post_file_list) >= number_of_post_to_show:
        n = number_of_post_to_show
    else:
        n = len(post_file_list)
    print('Selecting [{}] most recent posts.....'.format(n), log_type='info')
    latest_posts = sorted(post_file_list, reverse=True)[:n]

    # Generate post section
    posts = string_posts(latest_posts=latest_posts)

    # Now read the pre_blog template and create blog.html
    input_file = os.path.join(templates_dir, 'pre_blog.html')
    output_file = os.path.join(templates_dir, 'blog.html')
    
    # Read input tamplate and create blog.html file
    print('Creating blog.html file.....', log_type='info')
    replace_dict = {'_posts_': posts}
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
