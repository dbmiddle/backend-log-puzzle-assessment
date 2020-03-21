#!/usr/bin/env python2
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"

"""

import os
import re
import sys
import urllib
import argparse


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    puzzle_urls = []
    unique_urls = []
    special_unique_urls = []
    server = 'http://code.google.com'
    with open(filename) as f:
        for line in f:
            matching_url = re.search(r'GET\s(\S+)\sHTTP', line)
            # ending_url = re.search(r'(-w+-w+.jpg)', matching_url.group(1))
            if 'puzzle' in line:
                puzzle_urls.append(server + matching_url.group(1))
            for url in puzzle_urls:
                if url not in unique_urls:
                    unique_urls.append(url)
            # for url in unique_urls:
            #     if url.endswith(ending_url.group())
    sorted_unique_urls = sorted(unique_urls)
    # sorted_special_unique_urls = sorted(special_unique_urls)
    # if filename == 'animal_code.google.com':
    return sorted_unique_urls
    # else:
    #     return sorted_special_unique_urls


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    img_num = 0
    html_images = []
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)
    with open('index.html', 'wb') as f:
        for img_url in img_urls:
            destination = os.path.join(dest_dir, 'img{}'.format(img_num))
            html_images.append('<img src=' + destination + '>')
            urllib.urlretrieve(img_url, destination)
            img_num += 1
            print('Retrieving...')
        markup = '''
        <html>
        <body>
        {}
        </body>
        </html>
        '''.format(''.join(html_images))
        f.write(markup)


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--todir',  help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
