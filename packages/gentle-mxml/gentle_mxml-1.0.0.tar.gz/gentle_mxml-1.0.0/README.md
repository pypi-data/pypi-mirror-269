<!-- SPDX-FileCopyrightText: 2023-2024 Anna <cyber@sysrq.in> -->
<!-- SPDX-License-Identifier: CC0-1.0 -->

gentle
======

[![Build Status](https://drone.tildegit.org/api/badges/CyberTaIlor/gentle/status.svg)](https://drone.tildegit.org/CyberTaIlor/gentle)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/8269/badge)](https://www.bestpractices.dev/projects/8269)

**Gent**oo **L**azy **E**ntry — a `metadata.xml` generator.

If you need a distro-agnostic solution, try [upstream-ontologist][u-o]!

[u-o]: https://github.com/jelmer/upstream-ontologist


Supported generators
--------------------

* Crystal ([Shards](https://github.com/crystal-lang/shards/blob/master/docs/shard.yml.adoc))
* Dart ([Pub](https://dart.dev/tools/pub/pubspec))
* Haskell ([Hpack](https://github.com/sol/hpack/blob/main/README.md))
* Java ([Maven](https://maven.apache.org/pom.html))
* .NET ([NuGet](https://learn.microsoft.com/en-us/nuget/reference/nuspec))
* Node.js ([npm](https://docs.npmjs.com/files/package.json/), [Bower](https://github.com/bower/spec/blob/master/json.md))
* Perl ([CPAN::Meta::Spec](http://search.cpan.org/perldoc?CPAN::Meta::Spec))
* PHP ([Composer](https://getcomposer.org/doc/04-schema.md), [PEAR/PECL](https://pear.php.net/manual/en/guide.developers.package2.php))
* Python ([PEP 621](https://peps.python.org/pep-0621/), [PEP 643](https://peps.python.org/pep-0643/), [Setuptools](https://setuptools.pypa.io/en/latest/userguide/declarative_config.html))
* Ruby ([Gem metadata](https://guides.rubygems.org/specification-reference/))
* Rust ([Cargo](https://doc.rust-lang.org/cargo/reference/manifest.html))

Language-independent:

* [DOAP](https://github.com/ewilderj/doap/wiki)
* [GNU Autoconf](https://www.gnu.org/savannah-checkouts/gnu/autoconf/manual/autoconf-2.71/html_node/Initializing-configure.html)


Dependencies
------------

* Required:
  * [Portage](https://pypi.org/project/portage/)
  * [lxml](https://lxml.de/)
* Optional:
  * [GNU Autoconf](https://www.gnu.org/software/autoconf/)
  * [pkginfo](https://pypi.org/project/pkginfo/)
  * [PyYAML](https://pyyaml.org/)
  * [rdflib](https://pypi.org/project/rdflib/)
  * [Tomli](https://pypi.org/project/tomli/)


Installing
----------

### Gentoo

```sh
emerge app-portage/gentle
```

### Other systems

`pip install gentle-mxml --user`


Packaging
---------

You can track new releases using an [atom feed][atom] provided by GitHub.

[atom]: https://github.com/cybertailor/gentle/releases.atom


Contributing
------------

Patches and pull requests are welcome. Please use either
[git-send-email(1)][git-send-email] or [git-request-pull(1)][git-request-pull],
addressed to <cyber@sysrq.in>.

If you prefer GitHub-style workflow, use the [mirror repo][gh] to send pull
requests.

Your commit message should conform to the following standard:

```
file/changed: Concice and complete statement of the purpose

This is the body of the commit message.  The line above is the
summary.  The summary should be no more than 72 chars long.  The
body can be more freely formatted, but make it look nice.  Make
sure to reference any bug reports and other contributors.  Make
sure the correct authorship appears.
```

Code style is whatever the almighty linters say, should be at least
[PEP 8][pep8].


[git-send-email]: https://git-send-email.io/
[git-request-pull]: https://git-scm.com/docs/git-request-pull
[gh]: http://github.com/cybertailor/gentle
[pep8]: https://peps.python.org/pep-0008/


IRC
---

You can join the `#gentle` channel either on [Libera Chat][libera] or
[via Matrix][matrix].

[libera]: https://libera.chat/
[matrix]: https://matrix.to/#/#gentle:sysrq.in


License
-------

WTFPL
