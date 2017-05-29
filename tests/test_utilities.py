#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
gitsuggest.utilities test
~~~~~~~~~~

Usage from git root:

    >>> python setup.py test
"""

import unittest

from gitsuggest import ReposToHTML

from .mockentities import MockRepo


class ReposToHTMLTest(unittest.TestCase):
    """Class to test :class:`ReposToHTML` functionality."""

    def test_get_html(self):
        """Tests convertion of repository object list to HTML page."""

        repo_list = [MockRepo('userA/proA', 'A Desc'),
                     MockRepo('userB/proB', 'B Desc'),
                     MockRepo('userC/proC', 'C Desc')]

        r2h = ReposToHTML(repo_list)
        page = r2h.get_html()

        # Assert structure of HTML page.
        self.assertTrue(page.startswith('<html>'))
        self.assertTrue(page.endswith('</html>'))
        self.assertEqual(page.count('section class'), len(repo_list))

        # Assert contents of HTML page.
        for repo in repo_list:
            title = repo.full_name
            description = repo.description
            link = ReposToHTML.GITHUB_URL + title
            self.assertEqual(page.count(title), 1 + 2)  # Title + Links
            self.assertEqual(page.count(description), 1)  # Description
            self.assertEqual(page.count(link), 2)  # Links


if __name__ == '__main__':
    unittest.main()
