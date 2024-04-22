# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
# No warranty

"""
Metadata XML generator for Python PEP 643 (PKG-INFO).

The following attributes are supported:

* Upstream maintainer(s)
* Upstream bug tracker
* Upstream changelog
* Upstream documentation
* Remote ID
"""

import logging
from pathlib import Path

from gentle.generators import AbstractGenerator
from gentle.generators.python import (
    BUG_TRACKER_LABELS,
    CHANGELOG_LABELS,
    DOCS_LABELS,
    HOME_REPO_LABELS
)
from gentle.metadata import MetadataXML
from gentle.metadata.utils import extract_name_email, extract_remote_id

try:
    import pkginfo
    _HAS_PKGINFO_LIB = True
except ModuleNotFoundError:
    _HAS_PKGINFO_LIB = False

logger = logging.getLogger("pkg-info")


class PkgInfoGenerator(AbstractGenerator):
    def __init__(self, srcdir: Path):
        self.srcdir = srcdir
        self.pkg_info = srcdir / "PKG-INFO"

    # pylint: disable=too-many-branches
    def update_metadata_xml(self, mxml: MetadataXML) -> None:
        package = pkginfo.UnpackedSDist(str(self.srcdir))

        maint_keys = (package.maintainer, package.maintainer_email)
        if maint_keys == (None, None):
            maint_keys = (package.author, package.author_email)

        maintainers = []
        for maint_key in maint_keys:
            if maint_key is None:
                continue
            maintainers += [entry.strip() for entry in maint_key.split(",")]

        for maint in map(extract_name_email, maintainers):
            if maint is None:
                continue
            logger.info("Found upstream maintainer: %s", maint)
            mxml.add_upstream_maintainer(maint)

        if package.home_page is not None:
            logger.info("Found homepage: %s", package.home_page)
            if (remote_id := extract_remote_id(package.home_page)) is not None:
                mxml.add_upstream_remote_id(remote_id)

        for entry in package.project_urls:
            name, value = [item.strip()
                           for item in entry.split(",", maxsplit=1)]
            logger.info("Found %s: %s", name, value)
            if name.lower() in BUG_TRACKER_LABELS:
                mxml.set_upstream_bugs_to(value)
            elif name.lower() in CHANGELOG_LABELS:
                mxml.set_upstream_changelog(value)
            elif name.lower() in DOCS_LABELS:
                mxml.set_upstream_doc(value)
            elif name.lower() in HOME_REPO_LABELS:
                if (remote_id := extract_remote_id(value)) is not None:
                    mxml.add_upstream_remote_id(remote_id)

    @property
    def active(self) -> bool:
        return _HAS_PKGINFO_LIB and self.pkg_info.is_file()
