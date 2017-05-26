gitsuggest
===========

|Licence|

A tool to suggest github repositories based on the repositories you have shown
interest in.

|Demo|

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

    # With both username and password in command
    gitsuggest <username> --password <password>

    # With just username in command to provide password secretly
    gitsuggest <username>

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

.. |Demo| image:: http://i.imgur.com/WSWseQN.gif