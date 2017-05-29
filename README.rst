gitsuggest
===========

|Licence|

A tool to suggest github repositories based on the repositories you have shown
interest in.

|Demo|

Whats happening here?
---------------------

``Programs must be written for people to read, and only incidentally for
machines to execute. ~ Hal Abelson``

One quick way to become a better programmer is by reading code written by smart
people. Github makes finding such code/repositories easy. At the end of the day
we all are interested in our own specific areas and we express this interest by
"starring" repositories and/or "following" people who contribute to such
repositories.

This is a tool which uses the repositories you have starred and the repositories
that people you follow have starred to help you discover repositories which
might be of interest to you.

How fast is it?
---------------

It totally depends on the number of repositories you have, and people you follow
have starred. Based on this number it might take anywhere between a minute to
two minutes to give you the list of suggested repositories.

Setup
-----

Using pip
~~~~~~~~~

.. code:: bash

    pip install gitsuggest

Directly from the repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    git clone --recursive https://github.com/csurfer/gitsuggest.git
    python gitsuggest/setup.py install

Post setup
----------

If you see a stopwords error, it means that you do not have the corpus
`stopwords` downloaded from NLTK. You can download it using command below.

.. code:: bash

    python -c "import nltk; nltk.download('stopwords')"

Usage
-----

As a command
~~~~~~~~~~~~

.. code:: bash

    # For help with usage
    gitsuggest --help

    # With just username in command to provide password secretly
    gitsuggest <username>

    # Password can be skipped which means you chose to go the unauthenticated
    # way which may raise RateLimitExceeded exception.

    # NOTE: Using it this way generates a static html page with the search
    # results. This gets opened it in your default browser.

As a module
~~~~~~~~~~~

.. code:: python

    from gitsuggest import GitSuggest

    gs = GitSuggest(<username>, <password>)
    # To use without authenticating
    # gs = GitSuggest(<username>)

    # To get an iterator over suggested repositories.
    gs.get_suggested_repositories()

FAQ
---

**Why do we need to authenticate (with password) to get suggestions, I browse
gihub all the time without authenticating?**

You don't. From `v0.0.4` you can choose to procure suggestions without actually
authenticating with a password, but know that **access to github through API is
highly rate limited** and it is much lesser for unauthenticated requests when
compared to authenticated ones. More details about `ratelimits`_.

What this means is that when used without a password (unauthenticated) it may
fail with `RateLimitExceeded` exception.

Contributing
------------

Bug Reports and Feature Requests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Please use `issue tracker`_ for reporting bugs or feature requests.

Development
~~~~~~~~~~~

Pull requests are most welcome.

.. _issue tracker: https://github.com/csurfer/gitsuggest/issues

.. |Licence| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://raw.githubusercontent.com/csurfer/gitsuggest/master/LICENSE

.. |Demo| image:: http://i.imgur.com/5j5YnLR.gif

.. _ratelimits: https://developer.github.com/v3/search/#rate-limit