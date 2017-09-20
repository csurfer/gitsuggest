# -*- coding: utf-8 -*-

#    _______ __  _____                             __
#   / ____(_) /_/ ___/__  ______ _____ ____  _____/ /_
#  / / __/ / __/\__ \/ / / / __ `/ __ `/ _ \/ ___/ __/
# / /_/ / / /_ ___/ / /_/ / /_/ / /_/ /  __(__  ) /_
# \____/_/\__//____/\__,_/\__, /\__, /\___/____/\__/
#                        /____//____/

"""
GitSuggest
~~~~~~~~~~

GitSuggest is a library written in Python, to suggest git repositories a user
might be interested in based on user's interests.

:copyright: (c) 2017 by Vishwas B Sharma.
:licence: MIT, see LICENSE for more details.
"""

__title__ = 'gitsuggest'
__version__ = '0.0.9'
__author__ = 'Vishwas B Sharma'
__author_email__ = 'sharma.vishwas88@gmail.com'
__license__ = 'MIT'
__copyright__ = 'Copyright 2017 Vishwas B Sharma'

from .suggest import GitSuggest
from .utilities import ReposToHTML