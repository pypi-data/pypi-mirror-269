# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2022 Anna <cyber@sysrq.in>
# No warranty

"""
Metadata XML generator for Node.js npm.

The following attributes are supported:

* Upstream maintainer(s)
* Upstream bug tracker
* Remote ID
"""

import json
import logging
from pathlib import Path

from gentle.generators import AbstractGenerator
from gentle.metadata import MetadataXML
from gentle.metadata.types import Person, RemoteID
from gentle.metadata.utils import extract_name_email, extract_remote_id

logger = logging.getLogger("npm")


class NpmGenerator(AbstractGenerator):
    def __init__(self, srcdir: Path):
        self.package_json = srcdir / "package.json"

    def update_metadata_xml(self, mxml: MetadataXML) -> None:
        with open(self.package_json) as file:
            try:
                package = json.load(file)
            except json.decoder.JSONDecodeError:
                return

        if (maint := package.get("author")) is not None:
            logger.info("Found upstream maintainer: %s", maint)
            if isinstance(maint, str):
                person = extract_name_email(maint)
            else:
                person = Person(name=maint.get("name", ""),
                                email=maint.get("email", ""))

            if person is not None and person.name:
                mxml.add_upstream_maintainer(person)

        if (bugs := package.get("bugs")) is not None:
            logger.info("Found bug tracker: %s", bugs)
            if (bugs_url := bugs.get("url")) is not None:
                mxml.set_upstream_bugs_to(bugs_url)
            elif (bugs_email := bugs.get("email")) is not None:
                mxml.set_upstream_bugs_to("mailto:" + bugs_email)

        if (homepage := package.get("homepage")) is not None:
            logger.info("Found homepage: %s", homepage)
            if (remote_id := extract_remote_id(homepage)) is not None:
                mxml.add_upstream_remote_id(remote_id)

        if (repo := package.get("repository")) is not None:
            logger.info("Found repository: %s", repo)
            # TODO: process 'repository' objects
            if isinstance(repo, str):
                *attr, value = repo.split(":")
                match attr:
                    case ["bitbucket"] | ["github"] | ["gitlab"]:
                        remote_id = RemoteID(attr=attr[0], value=value)
                        mxml.add_upstream_remote_id(remote_id)
                    case []:
                        remote_id = RemoteID(attr="github", value=value)
                        mxml.add_upstream_remote_id(remote_id)

    @property
    def active(self) -> bool:
        return self.package_json.is_file()
