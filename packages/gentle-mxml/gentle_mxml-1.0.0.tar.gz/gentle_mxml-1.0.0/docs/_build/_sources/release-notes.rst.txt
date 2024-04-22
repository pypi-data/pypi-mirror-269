.. SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
.. SPDX-License-Identifier: WTFPL
.. No warranty.

Release Notes
=============

0.5.0
-----

* New generator: Perl CPAN::Meta::Spec
* New generator: Ruby Gem
* Add command-line flags to control tests selection

0.4.0
-----
* New generator: Apache Maven POM
* New generator: Dart Pubspec
* New generator: GNU Autoconf
* New generator: NuGet
* New generator: PEAR/PECL
* New generator: Python Setuptools
* New generator: Python Wheel
* New CLI option to skip slow generators
* Add ``kde-invent`` remote-id
* Trim ".git" suffix when extracting remote-id
* Switch to the ``lxml`` library
* Don't write :file:`metadata.xml` if there are no changes

0.3.1
-----

* Replace NIH metadata parser with Portage API-based parser
* Replace use of ``os.getlogin`` with a more reliable implementation
* Support setting ``EPREFIX`` via cli
