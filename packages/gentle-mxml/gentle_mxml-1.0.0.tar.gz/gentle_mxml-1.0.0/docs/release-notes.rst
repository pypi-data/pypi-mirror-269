.. SPDX-FileCopyrightText: 2023-2024 Anna <cyber@sysrq.in>
.. SPDX-License-Identifier: WTFPL
.. No warranty.

Release Notes
=============

1.0.0
-----

* Drop support for Python 3.10.
* Fix metadata schema violation for URLs with whitespace in them
* [Ruby Gem] Support extracting metadata from Gemspec files, not just Gems

0.4.1
-----

* New generator: Perl CPAN::Meta::Spec
* New generator: Ruby Gem
* [Docs] Fix Sphinx documentation
* [Tests] Add command-line flags to control tests selection

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
