.. SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
.. SPDX-License-Identifier: WTFPL
.. No warranty.

Installation
============

Prerequisites
-------------

The only hard dependencies are `Portage`_ and `lxml`_.

All other dependencies are optional, you can find them in the
:file:`pyproject.toml` file.

.. _Portage: https://pypi.org/project/portage/
.. _lxml: https://lxml.de/

Gentoo
------

gentle is packaged in the Gentoo repository.

.. prompt:: bash #

   emerge app-portage/gentle

Manual installation
-------------------

.. prompt:: bash

   pip install gentle-mxml --user
