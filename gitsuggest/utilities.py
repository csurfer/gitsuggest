# -*- coding: utf-8 -*-

"""
gitsuggest.utilities
~~~~~~~~~~~~~~~~~~~~

This module contains utility classes which help in displaying the results.
"""

from os import path
from jinja2 import FileSystemLoader, Environment


class ReposToHTML(object):
    """Class to convert the repository list to HTML page with results."""

    def __init__(self, user, repos):
        """Constructor.

        :param user: User for whom we are fetching the repositories for.
        :param repos: List of github.Repository objects.
        """
        self.user = user
        self.repos = repos

    def get_html(self):
        """Method to convert the repository list to a search results page."""
        here = path.abspath(path.dirname(__file__))

        env = Environment(loader=FileSystemLoader(path.join(here, "res/")))
        suggest = env.get_template("suggest.htm.j2")

        return suggest.render(
            logo=path.join(here, "res/logo.png"),
            user_login=self.user,
            repos=self.repos,
        )

    def to_html(self, write_to):
        """Method to convert the repository list to a search results page and
        write it to a HTML file.

        :param write_to: File/Path to write the html file to.
        """
        page_html = self.get_html()

        with open(write_to, "wb") as writefile:
            writefile.write(page_html.encode("utf-8"))
