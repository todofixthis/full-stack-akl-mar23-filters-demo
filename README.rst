Full Stack AKL March 2023 Meetup - Filters Demo
===============================================

Companion repo for https://go.phx.ph/fsa-mar23-slides/ showing how to use the
`Filters library`_ to make validating complex JSON payloads a snap 😺

The most interesting code is in `importer/views.py <./importer/views.py>`_ and
`importer/filters.py <./importer/filters.py>`_.

Setup
-----
Make sure you've got Python v3.9 or later.

.. code-block::

   # Install dependencies:
   pip install -e .

   # Set up database:
   python manage.py migrate
   python manage.py loaddata demo.yaml

The database is created as `db.sqlite3` in the same directory as this README.

Starting the Server
-------------------

.. code-block::

   gunicorn --reload demo_app.wsgi:application

Try It Out
----------

There's a handy Insomnia design doc you can use with some sample requests you
can send to the app to see how it works.

Follow the instructions from the Insomnia docs to `Clone an Existing Remote
Repository`_, and use the following GitHub URI:

https://github.com/todofixthis/full-stack-auckland-mar23-filters-insomnia.git

Once Insomnia loads the document, click to the DEBUG tab in the top navigation,
and you'll see 4 different requests you can play with.

.. _Clone an Existing Remote Repository: https://docs.insomnia.rest/insomnia/git-sync#clone-an-existing-remote-repository
.. _Filters library: https://pypi.org/project/phx-filters/
