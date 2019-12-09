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

**Note** this project uses the `git flow`_ branching model.

To set up CDPyR_ for local development:

1. Fork cdpyr_ (look for the "Fork" button).
#. Clone your fork locally:

   .. code-block:: bash

      $ git clone git@github.com:your-username-or-organization/cdpyr.git

#. Set up your local development environment by installing tox, creating the dev environment, and setting up git flow

   .. code-block:: bash

      $ pip install tox
      $ tox -e dev
      $ git flow init

#. Activate the python environment:

   1. Windows:

   .. code-block:: powershell

      > .tox\dev\Scripts\activate

   2. Unix:

   .. code-block:: shell

      $ source .tox/dev/bin/activate

#. Create a branch for local development to make your changes locally:

   1. For new features:

   .. code-block:: shell

      $ git flow feature start name-of-your-feature

   2. For hotfixes:

   .. code-block:: shell

      $ git flow hotfix start name-of-your-hotfix

#. When you're done making changes, run all the checks, doc builder and spell checker with `tox <https://tox.readthedocs.io/en/latest/install.html>`_ one command:

   .. code-block:: shell

      $ tox

#. Commit your changes and push your branch to GitHub:

   .. code-block:: shell

      $ git add .
      $ git commit -m "Your detailed description of your changes."
      $ git push origin name-of-your-hotfix-or-feature

#. Submit a pull request through the GitHub website.

If your change requires changes to the dependencies of :code:`cdpyr`, then add these in :code:`setup.py` under :code:`install_requires`.
However, if you make changes to the dependencies of tests or the development environment, then add these dependencies in :code:`tox.ini` in the :code:`deps` of either the :code:`[testenv]` or :code:`[testenv:dev]` section.

Git Flow Configuration
----------------------

* Branch name for production releases: :code:`master`
* Branch name for "next release" development: :code:`develop`
* Feature branch prefix: :code:`feature/`
* Bugfix branch prefix: :code:`bugfix/`
* Release branch prefix: :code:`release/`
* Hotfix branch prefix: :code:`hotfix/`
* Support branch prefix: :code:`support/`
* Version tag prefix: :code:`v`

Pull Request Guidelines
-----------------------

If you need some code review or feedback while you're developing the code just make the pull request.

For merging, you should:

1. Include passing tests (run :code:`tox`) [1]_.
#. Update documentation when there's new API, functionality etc.
#. Add a note to :code:`CHANGELOG.rst` about the changes.
#. Add yourself to :code:`AUTHORS.rst`.

Tips
----

To run a subset of tests:

.. code-block:: shell

   tox -e envname -- pytest -k test_myfeature

To run all the test environments in *parallel* (you need to :code:`pip install detox`):

.. code-block:: shell

   detox

To build the docs locally to :code:`dist/docs`:

.. code-block:: shell

   tox -e docs


.. [1] If you don't have all the necessary python versions available locally you can rely on Travis - it will `run the tests <https://travis-ci.org/cable-robots/cdpyr/pull_requests>`_ for each change you add in the pull request.

       It will be slower though ...


.. _cdpyr: https://github.com/cable-robots/cdpyr
.. _`git flow`: https://nvie.com/posts/a-successful-git-branching-model/
