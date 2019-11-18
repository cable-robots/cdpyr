============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

Bug reports
===========

When `reporting a bug <https://github.com/cable-robots/cdpyr/issues>`_ please include:

    * Your operating system name and version.
    * Any details about your local setup that might be helpful in troubleshooting.
    * Detailed steps to reproduce the bug.

Documentation improvements
==========================

CDPyR could always use more documentation, whether as part of the
official CDPyR docs, in docstrings, or even on the web in blog posts,
articles, and such.

Feature requests and feedback
=============================

The best way to send feedback is to file an issue at https://github.com/cable-robots/cdpyr/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that code contributions are welcome :)

Development
===========

To set up `cdpyr` for local development:

1. Fork `cdpyr <https://github.com/cable-robots/cdpyr>`_ (look for the "Fork" button).
#. Clone your fork locally:

   .. code-block:: bash

      $ git clone git@github.com:cable-robots/cdpyr.git

#. Set up your local development environment by installing tox and creating the dev environment:

   .. code-block:: bash

      $ pip install tox
      $ tox -e dev

#. Activate the environment:

   1. Windows:

   .. code-block:: powershell

      > .tox\dev\Scripts\activate

   2. Unix:

   .. code-block:: shell

      $ source .tox/dev/bin/activate

#. Create a branch for local development to make your changes locally:

   .. code-block:: shell

      $ git checkout -b name-of-your-bugfix-or-feature

#. When you're done making changes, run all the checks, doc builder and spell checker with `tox <https://tox.readthedocs.io/en/latest/install.html>`_ one command:

   .. code-block:: shell

      $ tox

#. Commit your changes and push your branch to GitHub:

   .. code-block:: shell

      $ git add .
      $ git commit -m "Your detailed description of your changes."
      $ git push origin name-of-your-bugfix-or-feature

#. Submit a pull request through the GitHub website.

If your change requires changes to the dependencies of ``cdpyr``, then add these in ``setup.py`` under ``install_requires``.
However, if you make changes to the dependencies of tests or the development environment, then add these dependencies in ``tox.ini`` in either ``deps`` of either the ``[testenv]`` or ``[testenv:dev]`` section.

Pull Request Guidelines
-----------------------

If you need some code review or feedback while you're developing the code just make the pull request.

For merging, you should:

1. Include passing tests (run ``tox``) [1]_.
#. Update documentation when there's new API, functionality etc.
#. Add a note to ``CHANGELOG.rst`` about the changes.
#. Add yourself to ``AUTHORS.rst``.

.. [1] If you don't have all the necessary python versions available locally you can rely on Travis - it will
       `run the tests <https://travis-ci.org/cable-robots/cdpyr/pull_requests>`_ for each change you add in the pull request.

       It will be slower though ...

Tips
----

To run a subset of tests:

.. code-block:: shell

   tox -e envname -- pytest -k test_myfeature

To run all the test environments in *parallel* (you need to ``pip install detox``):

.. code-block:: shell

   detox

To build the docs locally to ``dist/docs``:

.. code-block:: shell

   tox -e docs
