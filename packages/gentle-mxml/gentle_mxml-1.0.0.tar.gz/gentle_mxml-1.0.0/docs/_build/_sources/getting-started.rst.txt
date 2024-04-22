.. SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
.. SPDX-License-Identifier: WTFPL
.. No warranty.

Getting Started
===============

.. note::
   The :file:`metadata.xml` file must exist before running gentle.

To update your :file:`metadata.xml` file, just point ``gentle`` at the ebuild:

.. prompt:: bash

   metagen -m  # create metadata.xml
   gentle foo-0.1.ebuild

The command will unpack the sources and process supported upstream file.
