#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
gitsuggest as a command
~~~~~~~~~~~~~~~~~~

Usage:
    >>> pyheat --help
    usage: pyheat [-h] [-o OUT] pyfile
    positional arguments:
    pyfile             Python file to be profiled
    optional arguments:
    -h, --help         show this help message and exit
    -o OUT, --out OUT  Output file
    >>> pyheat <filename>
    # Displays the heatmap for the file.
    >>> pyheat <filename> --out myimage.png
    # Saves the heatmap as an image in file myimage.png
"""

import argparse
import getpass
import webbrowser

from .suggest import GitSuggest
from .utilities import ReposToHTML


def main():
    """Starting point for the program execution."""

    # Create command line parser.
    parser = argparse.ArgumentParser()

    # Adding command line arguments.
    parser.add_argument('username', help='Username', default=None)
    parser.add_argument('-p', '--password', help='Password', default=None)

    # Parse command line arguments.
    arguments = parser.parse_args()

    if arguments.username is None:
        parser.print_help()
        return

    if arguments.password is None:
        arguments.password = getpass.getpass()

    gs = GitSuggest(arguments.username, arguments.password)
    repos = list(gs.get_suggested_repositories())
    r2h = ReposToHTML(repos)

    file_name = '/tmp/gitresults.html'
    r2h.to_html(file_name)

    webbrowser.open_new('file://' + file_name)


if __name__ == '__main__':
    main()
