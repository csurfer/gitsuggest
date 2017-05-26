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

    git clone https://github.com/csurfer/gitsuggest.git
    python gitsuggest/setup.py install

Usage
-----

As a command
~~~~~~~~~~~~

.. code:: bash

    # For help with usage
    gitsuggest --help

    # With just username in command to provide password secretly
    gitsuggest <username>

    # NOTE: Using it this way generates a static html page with the search
    # results. This gets opened it in your default browser.

As a module
~~~~~~~~~~~

.. code:: python

    from gitsuggest import GitSuggest

    gs = GitSuggest(<username>, <password>)

    # To get an iterator over suggested repositories.
    gs.get_suggested_repositories()

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