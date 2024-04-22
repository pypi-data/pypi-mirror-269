# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
# No warranty

""" Utilities for metadata generators """

import re

from gentle.metadata import Person, RemoteID

author_re = re.compile(r"(?P<name>.+?)\s*<(?P<email>.+?@.+?)>")

remote_ids = {
    "bitbucket":
        re.compile(r"^https?://bitbucket.org/(?P<v>[^\s/]+?/[^\s/]+?)([.]git)?(/.*)?$"),
    "cpan":
        re.compile(r"^https?://metacpan.org/dist/(?P<v>[^\s/]+?)(/.*)?$"),
    "cpan-module":
        re.compile(r"^https?://metacpan.org/pod/(?P<v>[^\s/]+?)(/.*)?$"),
    "cran":
        re.compile(r"^https?://cran.r-project.org/web/packages/(?P<v>\S+?)(/.*)?$"),
    "ctan":
        re.compile(r"^https?://ctan.org/pkg/(?P<v>\S+?)(/.*)?$"),
    "freedesktop-gitlab":
        re.compile(r"^https?://gitlab.freedesktop.org/(?P<v>[^\s/]+?/[^\s/]+?)([.]git)?(/.*)?$"),
    "gentoo":
        re.compile(r"^https?://gitweb.gentoo.org/(?P<v>\S+?)[.]git(/.*)?$"),
    "github":
        re.compile(r"^https?://github.com/(?P<v>[^\s/]+?/[^\s/]+?)([.]git)?(/.*)?$"),
    "gitlab":
        re.compile(r"^https?://gitlab.com/(?P<v>[^\s/]+?/[^\s/]+?)([.]git)?(/.*)?$"),
    "gnome-gitlab":
        re.compile(r"^https?://gitlab.gnome.org/(?P<v>[^\s/]+?/[^\s/]+?)([.]git)?(/.*)?$"),
    "google-code":
        re.compile(r"^https?://code.google.com/archive/p/(?P<v>\S+)(/.*)?$"),
    "hackage":
        re.compile(r"^https?://hackage.haskell.org/package/(?P<v>\S+)(/.*)?$"),
    "heptapod":
        re.compile(r"^https?://foss.heptapod.net/(?P<v>[^\s/]+?/[^\s/]+?)([.]git)?(/.*)?$"),
    "kde-invent":
        re.compile(r"^https?://invent.kde.org/(?P<v>[^\s/]+?/[^\s/]+?)([.]git)?(/.*)?$"),
    "launchpad":
        re.compile(r"^https?://launchpad.net/(?P<v>\S+)(/.*)?$"),
    "osdn":
        re.compile(r"^https?://osdn.net/projects/(?P<v>\S+)(/.*)?$"),
    "pear":
        re.compile(r"^https?://pear.php.net/package/(?P<v>\S+)(/.*)?$"),
    "pecl":
        re.compile(r"^https?://pecl.php.net/package/(?P<v>\S+)(/.*)?$"),
    "pypi":
        re.compile(r"^https?://pypi.org/project/(?P<v>\S+)(/.*)?$"),
    "rubygems":
        re.compile(r"^https?://rubygems.org/gems/(?P<v>\S+)(/.*)?$"),
    "savannah":
        re.compile(r"^https?://savannah.gnu.org/projects/(?P<v>\S+)(/.*)?$"),
    "savannah-nongnu":
        re.compile(r"^https?://savannah.nongnu.org/projects/(?P<v>\S+)(/.*)?$"),
    "sourceforge":
        re.compile(r"^https?://(?P<v>\S+?).sourceforge.(net|io)(/.*)?$"),
    "sourcehut":
        re.compile(r"^https?://(git[.])?sr.ht/(?P<v>\[^\s/]+?/\[^\s/]+?)([.]git)?(/.*)?$"),
    "vim":
        re.compile(r"^https?://www.vim.org/scripts/script.php?script_id=(?P<v>\d+?)$")
}


def extract_name_email(author: str) -> Person | None:
    """
    Make a :class:`Person` object from a string.

    :param author: string in the ``name <email>`` format

    >>> extract_name_email("Foo Bar <foobar@example.com>")
    Person(name='Foo Bar', email='foobar@example.com', status=<MaintainerStatus.NONE: 1>)
    >>> extract_name_email("Foo Bar") is None
    True
    """
    if (match := author_re.match(author)) is None:
        return None
    return Person(match.group("name"), match.group("email"))


def extract_remote_id(url: str) -> RemoteID | None:
    """
    Make a :class:`RemoteID` object from a string.

    :param url: project's source repository

    >>> extract_remote_id("https://pypi.org/project/foo-bar")
    RemoteID(attr='pypi', value='foo-bar')
    >>> extract_remote_id("https://example.com") is None
    True
    """
    for attr, template in remote_ids.items():
        if (match := template.match(url)) is not None:
            return RemoteID(attr, match.group("v"))
    return None
