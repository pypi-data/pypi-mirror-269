# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
# No warranty

"""
Metadata XML generator for PHP Composer.

The following attributes are supported:

* Upstream maintainer(s)
* Upstream bug tracker
* Upstream documentation
* Remote ID
"""

import json
import logging
from pathlib import Path

from gentle.generators import AbstractGenerator
from gentle.metadata import MetadataXML
from gentle.metadata.types import Person
from gentle.metadata.utils import extract_remote_id

logger = logging.getLogger("composer")


class ComposerGenerator(AbstractGenerator):
    def __init__(self, srcdir: Path):
        self.composer_json = srcdir / "composer.json"

    def update_metadata_xml(self, mxml: MetadataXML) -> None:
        with open(self.composer_json) as file:
            try:
                package = json.load(file)
            except json.decoder.JSONDecodeError:
                return

        for maint in package.get("authors", []):
            logger.info("Found upstream maintainer: %s", maint)
            person = Person(name=maint.get("name", ""),
                            email=maint.get("email", ""))
            if person.name:
                mxml.add_upstream_maintainer(person)

        if (support := package.get("support")) is not None:
            if (issues := support.get("issues")) is not None:
                logger.info("Found bug tracker: %s", issues)
                mxml.set_upstream_bugs_to(issues)
            elif (support_email := support.get("email")) is not None:
                logger.info("Found support email: %s", support_email)
                mxml.set_upstream_bugs_to("mailto:" + support_email)

            if (doc := support.get("docs")) is not None:
                logger.info("Found documentation: %s", doc)
                mxml.set_upstream_doc(doc)

            if (source := support.get("source")) is not None:
                logger.info("Found source: %s", source)
                if (remote_id := extract_remote_id(source)) is not None:
                    mxml.add_upstream_remote_id(remote_id)

        if (homepage := package.get("homepage")) is not None:
            logger.info("Found homepage: %s", homepage)
            if (remote_id := extract_remote_id(homepage)) is not None:
                mxml.add_upstream_remote_id(remote_id)

    @property
    def active(self) -> bool:
        return self.composer_json.is_file()
