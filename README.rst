Everbug - Debugger for Django projects
======================================

The Everbug is a lightweight Django middleware for Chrome extension with easy install. One of the advantages: the response body of target page remains clean
and unchanged.

Special summary:
* Database queries with explains (Multiple database support)
* Context variables
* Profiles functions (cProfile through decorator)
* Support ajax requests


Installing
-----------------

For Django:

::

   Run "pip install everbug".
   Add "everbug" to your INSTALLED_APPS in settings.py.
   Append "everbug.middleware.Tracer" to MIDDLEWARE or MIDDLEWARE_CLASSES in settings.py.

For Chrome: _chrome_ext_
For Firefox: _firefox_ext_

Usage
-----------------

“Context” works for any view which has a “context_data”. “Queries” works
as-is for all databases in “DATABASES” section. “Profile” works through
decorator (based on builtin cProfile). By default, profile output is
truncated to 20 lines.

Example usage:

::

   from everbug.shortcuts import profile

   @profile
   def sample_method():
       // some code here ...  

Call @profile with argument for full view, for example:

::

   @profile(short=False)
   def sample_method():
       // some code here ...  

Running the tests
-----------------

::

   docker-compose  up -d 
   docker exec -it everbug tox

Requirements
-----------------

| Python >= 3.5
| Django >= 1.11

License
-----------------

This project is licensed under the MIT License - see the `LICENSE`_ file
for details

.. _chrome_ext: https://chrome.google.com/webstore/search/everbug
.. _firefox_ext: https://addons.mozilla.org/ru/firefox/addon/everbug
.. _LICENSE: LICENSE