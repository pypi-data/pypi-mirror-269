# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
# No warranty

"""
Metadata XML generator for Python PEP 621 (pyproject.toml).

The following attributes are supported:

* Upstream maintainer(s)
* Upstream bug tracker
* Upstream changelog
* Upstream documentation
* Remote ID
"""

import logging
from pathlib import Path
import tomllib

from gentle.generators import AbstractGenerator
from gentle.generators.python import (
    BUG_TRACKER_LABELS,
    CHANGELOG_LABELS,
    DOCS_LABELS,
    HOME_REPO_LABELS
)
from gentle.metadata import MetadataXML
from gentle.metadata.types import Person
from gentle.metadata.utils import extract_remote_id

logger = logging.getLogger("pyproject")


class PyprojectGenerator(AbstractGenerator):
    def __init__(self, srcdir: Path):
        self.pyproject_toml = srcdir / "pyproject.toml"

    def update_metadata_xml(self, mxml: MetadataXML) -> None:
        with open(self.pyproject_toml, "rb") as file:
            pyproject = tomllib.load(file)

        if (project := pyproject.get("project")) is None:
            return

        maint_key = "maintainers"
        if maint_key not in project:
            maint_key = "authors"

        for maint in project.get(maint_key, {}):
            person = Person(name=maint.get("name", ""), email=maint.get("email", ""))
            logger.info("Found upstream maintainer: %s", person)
            if not person.name:
                continue
            mxml.add_upstream_maintainer(person)

        for name, value in project.get("urls", {}).items():
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
        return self.pyproject_toml.is_file()
