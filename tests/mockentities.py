#!/usr/bin/python
# -*- coding: utf-8 -*-

"""File with mock classes."""


class MockRepo(object):
    """MockClass to represent a GitRepository."""

    def __init__(self, full_name, description):
        """Constructor.

        :param full_name: Name of the repository.
        :param description: Description of the repository.
        """
        self.full_name = full_name
        self.description = description

    def __eq__(self, other):
        return self.full_name == other.full_name and \
            self.description == other.description
