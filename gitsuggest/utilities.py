# -*- coding: utf-8 -*-

"""
gitsuggest.utilities
~~~~~~~~~~~~~~~~~~~~

This module contains utility classes which help in displaying the results.
"""

from os import path
from string import Template


class ReposToHTML(object):
    """Class to convert the repository list to HTML page with results."""

    GITHUB_URL = 'https://github.com/'

    def __init__(self, repositories):
        """Constructor.

        :param repositories: List of github.Repository objects.
        """
        self.repositories = repositories

    def get_html(self):
        """Method to convert the repository list to a search results page."""
        here = path.abspath(path.dirname(__file__))

        result_template = ""
        with open(path.join(here, 'res/result.template')) as readfile:
            result_template = readfile.read()

        page_template = ""
        with open(path.join(here, 'res/page.template')) as readfile:
            page_template = readfile.read()

        results = list()
        for repo in self.repositories:
            substitutions = {
                'link': ReposToHTML.GITHUB_URL + repo.full_name,
                'title': repo.full_name,
                'description': repo.description
            }
            results.append(Template(result_template).substitute(substitutions))

        result_html = '\n'.join(results)
        substitutions = {
            'results': result_html
        }
        page_html = Template(page_template).substitute(substitutions)

        return page_html

    def to_html(self, write_to):
        """Method to convert the repository list to a search results page and
        write it to a HTML file.

        :param write_to: File/Path to write the html file to.
        """
        page_html = self.get_html()

        with open(write_to, 'wb') as writefile:
            writefile.write(page_html.encode('utf-8'))
