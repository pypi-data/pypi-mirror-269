# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
# No warranty

"""
Metadata XML generator for Dart Pub.

The following attributes are supported:

* Upstream maintainer(s)
* Upstream bug tracker
* Upstream documentation
* Remote ID
"""

import logging
from pathlib import Path

from gentle.generators import AbstractGenerator
from gentle.metadata import MetadataXML
from gentle.metadata.utils import extract_remote_id

try:
    import yaml
    from yaml import CLoader
    _HAS_PYYAML = True
except ModuleNotFoundError:
    _HAS_PYYAML = False

logger = logging.getLogger("pubspec")


class PubspecGenerator(AbstractGenerator):
    def __init__(self, srcdir: Path):
        self.pubspec_yml = srcdir / "pubspec.yaml"

    def update_metadata_xml(self, mxml: MetadataXML) -> None:
        with open(self.pubspec_yml) as file:
            if (pubspec := yaml.load(file, CLoader)) is None:
                return

        if (issues := pubspec.get("issue_tracker")) is not None:
            logger.info("Found bug tracker: %s", issues)
            mxml.set_upstream_bugs_to(issues)

        if (doc := pubspec.get("documentation")) is not None:
            logger.info("Found documentation: %s", doc)
            mxml.set_upstream_doc(doc)

        if (homepage := pubspec.get("homepage")) is not None:
            logger.info("Found homepage: %s", homepage)
            if (remote_id := extract_remote_id(homepage)) is not None:
                mxml.add_upstream_remote_id(remote_id)

        if (repo := pubspec.get("repository")) is not None:
            logger.info("Found repository: %s", repo)
            if (remote_id := extract_remote_id(repo)) is not None:
                mxml.add_upstream_remote_id(remote_id)

    @property
    def active(self) -> bool:
        return _HAS_PYYAML and self.pubspec_yml.is_file()
