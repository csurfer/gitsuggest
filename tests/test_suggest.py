#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
gitsuggest.suggest test
~~~~~~~~~~

Usage from git root:

    >>> python setup.py test
"""

import unittest

from gitsuggest import GitSuggest

from .mockentities import MockRepo


class GitSuggestTest(unittest.TestCase):
    """Class to test :class:`GitSuggest` functionality."""

    def test_get_unique_repositories(self):
        """Tests to validate get_unique_repositories()."""

        repo_list = [MockRepo('userA/proA', 'A Desc'),
                     MockRepo('userB/proB', 'B Desc'),
                     MockRepo('userA/proA', 'A Desc'),
                     MockRepo('userB/proB', 'B Desc'),
                     MockRepo('userC/proC', 'C Desc')]
        expected_unique = [MockRepo('userA/proA', 'A Desc'),
                           MockRepo('userB/proB', 'B Desc'),
                           MockRepo('userC/proC', 'C Desc')]

        unique = GitSuggest.get_unique_repositories(repo_list)

        self.assertEqual(len(expected_unique), len(unique))
        self.assertEqual(expected_unique, unique)

    def test_minus(self):
        """Tests to validate minus()."""

        repo_list_a = [MockRepo('userA/proA', 'A Desc'),
                       MockRepo('userB/proB', 'B Desc'),
                       MockRepo('userC/proC', 'C Desc'),
                       MockRepo('userD/proD', 'D Desc')]
        repo_list_b = [MockRepo('userB/proB', 'B Desc'),
                       MockRepo('userD/proD', 'D Desc')]
        expected_a_minus_b = [MockRepo('userA/proA', 'A Desc'),
                              MockRepo('userC/proC', 'C Desc')]

        a_minus_b = GitSuggest.minus(repo_list_a, repo_list_b)

        self.assertEqual(len(expected_a_minus_b), len(a_minus_b))
        self.assertEqual(expected_a_minus_b, a_minus_b)


if __name__ == '__main__':
    unittest.main()
