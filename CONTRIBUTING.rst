============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

Bug reports
===========

When `reporting a bug`_ please include:

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

The best way to send feedback is to file an issue at `cdpyr issues`_.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that code contributions are welcome :)

Development
===========

**Note** this project uses the `GitLab flow`_ branching model.

To set up CDPyR_ for local development:

1. Fork cdpyr_ (look for the "Fork" button).
#. Clone your fork locally:

   .. code-block:: bash

      $ git clone https://gitlab.com/<your-username>/cdpyr.git

#. Set up your local development environment by installing tox, creating the dev environment, and setting up git flow

   .. code-block:: bash

      $ pip install tox
      $ tox -e dev

#. Activate the python environment:

   1. Windows:

   .. code-block:: powershell

      > .venv\Scripts\activate.bat

   2. Unix:

   .. code-block:: shell

      $ . .venv/bin/activate

#. Create a branch for local development to make your changes locally:

   .. code-block:: shell
   
      $ git checkout -b your-branch-name-should-explain-the-changes
      
#. When you're done making changes, run all the checks, doc builder and spell checker with `tox <https://tox.readthedocs.io/en/latest/install.html>`_ one command:

   .. code-block:: shell

      $ tox

#. Commit your changes and push your branch to your repository:

   .. code-block:: shell

      $ git add .
      $ git commit -m "Your detailed description of your changes."
      $ git push origin your-branch-name-should-explain-the-changes

#. `Submit a merge request`_ through the GitLab website.

If your change requires changes to the dependencies of :code:`cdpyr`, then add these in :code:`setup.py` under :code:`install_requires`.
However, if you make changes to the dependencies of tests or the development environment, then add these dependencies in :code:`tox.ini` in the :code:`deps` of either the :code:`[testenv]` or :code:`[testenv:dev]` section.

Pull Request Guidelines
-----------------------

If you need some code review or feedback while you're developing the code just make the pull request.

For merging, you should:

1. Include passing tests (run :code:`tox`) [#ci-footnote]_.
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


.. [#ci-footnote] If you don't have all the necessary python versions available locally you can rely on GitLab CI - it will `run the tests <https://gitlab.com/cable-robots/cdpyr/-/pipelines>`_ for each change you add in the pull request. It will be slower though ...


.. _cdpyr: https://gitlab.com/cable-robots/cdpyr/
.. _`Submit a merge request`: https://gitlab.com/cable-robots/cdpyr/-/merge_requests
.. _`reporting a bug`: https://gitlab.com/cable-robots/cdpyr/-/issues/
.. _`cdpyr issues`: https://gitlab.com/cable-robots/cdpyr/-/issues/
.. _`GitLab flow`: https://docs.gitlab.com/ee/topics/gitlab_flow.html
