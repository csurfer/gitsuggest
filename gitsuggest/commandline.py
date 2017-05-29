#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
gitsuggest.commandline
~~~~~~~~~~~~~~~~~~~~~~

This module contains code to use the GitSuggest as commandline.

Usage:

    >>> gitsuggest --help
    usage: gitsuggest [-h] username

    positional arguments:
      username    Github Username

    optional arguments:
      -h, --help  show this help message and exit

    >>> gitsuggest <username>
    # Asks for password input in a secure way to fetch suggested repositories
    # for the authenticated user.
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
    parser.add_argument('username',
                        help='Github Username',
                        default=None)

    # Parse command line arguments.
    arguments = parser.parse_args()

    if arguments.username is None:
        parser.print_help()
        return

    print('')
    print('INFO: Authentication (with password) have higher rate limits.')
    print('INFO: Skipping password might cause failure due to rate limit.')
    print('')

    password = getpass.getpass('Password (to skip press enter):')

    print('Generating suggestions...')

    gs = GitSuggest(arguments.username, password)
    repos = list(gs.get_suggested_repositories())
    r2h = ReposToHTML(repos)

    file_name = '/tmp/gitresults.html'
    r2h.to_html(file_name)

    webbrowser.open_new('file://' + file_name)


if __name__ == '__main__':
    main()
