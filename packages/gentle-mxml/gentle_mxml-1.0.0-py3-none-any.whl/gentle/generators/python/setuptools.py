# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
# No warranty

"""
Metadata XML generator for Python Setuptools (setup.cfg).

The following attributes are supported:

* Upstream bug tracker
* Upstream changelog
* Upstream documentation
* Remote ID
"""

import configparser
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
from gentle.metadata.utils import extract_remote_id

logger = logging.getLogger("setuptools")


class SetuptoolsGenerator(AbstractGenerator):
    def __init__(self, srcdir: Path):
        self.setup_cfg = srcdir / "setup.cfg"

    def update_metadata_xml(self, mxml: MetadataXML) -> None:
        cfg = configparser.ConfigParser()
        try:
            cfg.read(self.setup_cfg)
        except configparser.Error:
            return

        if not cfg.has_section("metadata"):
            return
        metadata = cfg["metadata"]

        # Not parsing "author" and "maintainer" because of uncertain format

        if (url := metadata.get("url")) is None:
            url = metadata.get("home-page")

        if url is not None:
            if (remote_id := extract_remote_id(url)) is not None:
                logger.info("Found homepage: %s", url)
                mxml.add_upstream_remote_id(remote_id)

        for key_val in metadata.get("project_urls", "").strip().split("\n"):
            key_val = [item.strip() for item in key_val.split("=", maxsplit=1)]
            if len(key_val) != 2:
                continue

            name = key_val[0].lower()
            value = key_val[1]
            logger.info("Found %s: %s", name, value)
            if name in BUG_TRACKER_LABELS:
                mxml.set_upstream_bugs_to(value)
            elif name in CHANGELOG_LABELS:
                mxml.set_upstream_changelog(value)
            elif name in DOCS_LABELS:
                mxml.set_upstream_doc(value)
            elif name in HOME_REPO_LABELS:
                if (remote_id := extract_remote_id(value)) is not None:
                    mxml.add_upstream_remote_id(remote_id)

    @property
    def active(self) -> bool:
        return self.setup_cfg.is_file()
