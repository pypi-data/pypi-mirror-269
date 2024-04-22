# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
# No warranty

"""
Metadata XML generator for Haskell Hpack.

The following attributes are supported:

* Upstream maintainer(s)
* Upstream documentation
* Remote ID
"""

import logging
from pathlib import Path

from gentle.generators import AbstractGenerator
from gentle.metadata import MetadataXML
from gentle.metadata.types import RemoteID
from gentle.metadata.utils import extract_name_email, extract_remote_id

try:
    import yaml
    from yaml import CLoader
    _HAS_PYYAML = True
except ModuleNotFoundError:
    _HAS_PYYAML = False

logger = logging.getLogger("hpack")


class HpackGenerator(AbstractGenerator):
    def __init__(self, srcdir: Path):
        self.package_yaml = srcdir / "package.yaml"

    def update_metadata_xml(self, mxml: MetadataXML) -> None:
        with open(self.package_yaml) as file:
            if (package := yaml.load(file, CLoader)) is None:
                package = {}

        maint_key = "maintainer"
        if maint_key not in package:
            maint_key = "author"

        maintainers = package.get(maint_key, [])
        if isinstance(maintainers, str):
            maintainers = [maintainers]

        for maint in map(extract_name_email, maintainers):
            if maint is None:
                continue
            logger.info("Found upstream maintainer: %s", maint)
            mxml.add_upstream_maintainer(maint)

        if (bugs_to := package.get("bug-reports")) is not None:
            logger.info("Found bug tracker: %s", bugs_to)
            mxml.set_upstream_bugs_to(bugs_to)

        if (homepage := package.get("homepage")) is not None:
            logger.info("Found homepage: %s", homepage)
            if (remote_id := extract_remote_id(homepage)) is not None:
                mxml.add_upstream_remote_id(remote_id)

        if (github := package.get("github")) is not None:
            logger.info("Found GitHub repo: %s", github)
            # strip subdirectory
            github_repo = "/".join(github.split("/")[:2])

            remote_id = RemoteID(attr="github", value=github_repo)
            mxml.add_upstream_remote_id(remote_id)

        if (git := package.get("git")) is not None:
            logger.info("Found Git repo: %s", git)
            if (remote_id := extract_remote_id(git)) is not None:
                mxml.add_upstream_remote_id(remote_id)

    @property
    def active(self) -> bool:
        return _HAS_PYYAML and self.package_yaml.is_file()
