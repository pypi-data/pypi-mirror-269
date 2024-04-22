# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
# No warranty

"""
Metadata XML generator for Bower.

The following attributes are supported:

* Upstream maintainer(s)
* Remote ID
"""

import json
import logging
from pathlib import Path

from gentle.generators import AbstractGenerator
from gentle.metadata import MetadataXML
from gentle.metadata.types import Person
from gentle.metadata.utils import extract_name_email, extract_remote_id

logger = logging.getLogger("bower")


class BowerGenerator(AbstractGenerator):
    def __init__(self, srcdir: Path):
        self.bower_json = srcdir / "bower.json"

    def update_metadata_xml(self, mxml: MetadataXML) -> None:
        with open(self.bower_json) as file:
            try:
                package = json.load(file)
            except json.decoder.JSONDecodeError:
                return

        for maint in package.get("authors", []):
            logger.info("Found upstream maintainer: %s", maint)
            if isinstance(maint, str):
                person = extract_name_email(maint)
            else:
                person = Person(name=maint.get("name", ""),
                                email=maint.get("email", ""))

            if person is not None and person.name:
                mxml.add_upstream_maintainer(person)

        if (homepage := package.get("homepage")) is not None:
            logger.info("Found homepage: %s", homepage)
            if (remote_id := extract_remote_id(homepage)) is not None:
                mxml.add_upstream_remote_id(remote_id)

    @property
    def active(self) -> bool:
        return self.bower_json.is_file()
