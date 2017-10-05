v0.0.13
-------
* Better error message for 2FA authentication.
* Cleaner UI to display the repositories.
* More information about the repositories like the language and number of stars.
* Making the UI same as UI for http://www.gitsuggest.com
* Using Jinja2 for templating.

v0.0.12
-------
* 0 stars exception fix.

v0.0.11
-------
* Use sets instead of lists for speedup.

v0.0.10
-------
* Removing dependency on pyenchant and using nltk instead for english words.
* Adding nltk corpus downloads as post installation tasks in setup.py.

v0.0.9
------
* `--deep_dive` flag to to provide user with control over accuracy vs time.
* Access token based authentication for procuring repository reccomendations.
* Prettier command line display.

v0.0.8
------
* Fixes to setup script to ensure package data is copied over.

v0.0.7
------
* Fixes to ensure proper packaging of resources instead of relying on
  submodules.

v0.0.4, v0.0.5, v0.0.6 (Unstable)
---------------------------------
* Smart pagination usage for much faster response times.
* py3 bug fixes to make it more stable.
* Provision of a way to get suggestions without password. Even though it is
  contingent on the rate limit that is applied.

v0.0.3
------
* Removal of password from command line for better security.

v0.0.2
------
* Some major bug fixes causing slowdown.


v0.0.1
------
* Long time itch to code an idea.
* First release.