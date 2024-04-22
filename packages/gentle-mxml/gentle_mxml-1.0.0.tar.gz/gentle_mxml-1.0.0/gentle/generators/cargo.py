# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2022 Anna <cyber@sysrq.in>
# No warranty

"""
Metadata XML generator for Cargo.

The following attributes are supported:

* Upstream maintainer(s)
* Upstream documentation
* Remote ID
"""

import logging
import tomllib
from pathlib import Path

from gentle.generators import AbstractGenerator
from gentle.metadata import MetadataXML
from gentle.metadata.utils import extract_name_email, extract_remote_id

logger = logging.getLogger("cargo")


class CargoGenerator(AbstractGenerator):
    def __init__(self, srcdir: Path):
        self.srcdir = srcdir
        self.cargo_toml = srcdir / "Cargo.toml"

    def process_metadata(self, package: dict, mxml: MetadataXML) -> None:
        if isinstance(authors := package.get("authors"), list):
            for author in map(extract_name_email, authors):
                if author is None:
                    continue
                logger.info("Found upstream maintainer: %s", author)
                mxml.add_upstream_maintainer(author)

        if isinstance(doc := package.get("documentation"), str):
            logger.info("Found documentation: %s", doc)
            mxml.set_upstream_doc(doc)

        if isinstance(homepage := package.get("homepage"), str):
            logger.info("Found homepage: %s", homepage)
            if (remote_id := extract_remote_id(homepage)) is not None:
                mxml.add_upstream_remote_id(remote_id)

        if isinstance(repo := package.get("repository"), str):
            logger.info("Found repository: %s", repo)
            if (remote_id := extract_remote_id(repo)) is not None:
                mxml.add_upstream_remote_id(remote_id)

    def update_metadata_xml(self, mxml: MetadataXML) -> None:
        with open(self.cargo_toml, "rb") as file:
            crate = tomllib.load(file)

        if (package := crate.get("package")):
            self.process_metadata(package, mxml)

        if (workspace := crate.get("workspace")) is not None:
            if (workspace_package := workspace.get("package")) is not None:
                self.process_metadata(workspace_package, mxml)

            members = set(workspace.get("members", []))
            members -= frozenset(workspace.get("exclude", []))
            for member in members:
                logger.info("Processing workspace member: %s", member)
                member_toml = self.srcdir / member / "Cargo.toml"
                try:
                    with open(member_toml, "rb") as file:
                        member_crate = tomllib.load(file)
                except OSError:
                    continue

                if (member_package := member_crate.get("package")) is not None:
                    self.process_metadata(member_package, mxml)

    @property
    def active(self) -> bool:
        return self.cargo_toml.is_file()
