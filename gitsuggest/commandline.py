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
      --deep_dive  If added considers repositories starred by users you follow
                   along with repositories you have starred. Is significantly
                   slower.

    >>> gitsuggest <username>
    # Asks for password input in a secure way to fetch suggested repositories
    # for the authenticated user.
"""
import argparse
import getpass
import webbrowser

import crayons
import github

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

    parser.add_argument('--deep_dive',
                        help=' '.join([
                            'If added considers repositories starred by users',
                            'you follow along with repositories you have',
                            'starred. Is significantly slower.'
                        ]),
                        action='store_true',
                        default=False)

    # Parse command line arguments.
    arguments = parser.parse_args()

    if arguments.username is None:
        parser.print_help()
        return

    print('')
    print(crayons.white(
        'Authentication (with password) have higher rate limits.'))
    print(crayons.white(
        'Skipping password might cause failure due to rate limit.'))
    print('')

    password = getpass.getpass(crayons.blue(
        'Enter password (to skip press enter without entering anything): ',
        bold=True))

    try:
        gs = GitSuggest(username=arguments.username,
                        password=password,
                        token=None,
                        deep_dive=arguments.deep_dive)
    except github.BadCredentialsException:
        print('')
        print(crayons.red(
            'Incorrect password provided, to skip password enter nothing.',
            bold=True))
        exit()

    print('')
    print(crayons.green('Suggestions generated !'))

    repos = list(gs.get_suggested_repositories())
    r2h = ReposToHTML(repos)

    file_name = '/tmp/gitresults.html'
    r2h.to_html(file_name)

    webbrowser.open_new('file://' + file_name)


if __name__ == '__main__':
    main()
