# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2022 Anna <cyber@sysrq.in>
# No warranty

"""
Metadata XML generator for Apache Maven POM.

The following attributes are supported:

* Upstream maintainer(s)
* Upstream bug tracker
* Remote ID
"""

import logging
from pathlib import Path

import lxml.etree as ET

from gentle.generators import AbstractGenerator
from gentle.metadata import MetadataXML
from gentle.metadata.types import Person
from gentle.metadata.utils import extract_remote_id
from gentle.utils import stringify

logger = logging.getLogger("pom")


class PomGenerator(AbstractGenerator):
    def __init__(self, srcdir: Path):
        self.pom_xml = srcdir / "pom.xml"

    # pylint: disable=too-many-locals
    def update_metadata_xml(self, mxml: MetadataXML) -> None:
        try:
            xml: ET._ElementTree = ET.parse(self.pom_xml)
        except ET.ParseError:
            return

        pom_ns = "http://maven.apache.org/POM/4.0.0"
        ns = {"pom": pom_ns}

        if xml.getroot().tag != f"{{{pom_ns}}}project":
            return

        for dev in xml.findall("pom:developers", ns):
            if dev.tag != f"{{{pom_ns}}}developer":
                continue

            if (dev_name := dev.find("pom:name", ns)) is None:
                continue

            person = Person(stringify(dev_name))
            if (dev_email := dev.find("pom:email", ns)) is not None:
                person.email = stringify(dev_email)

            logger.info("Found upstream maintainer: %s", person)
            mxml.add_upstream_maintainer(person)

        if (issues := xml.find("pom:issueManagement", ns)) is not None:
            if (issues_url := issues.find("pom:url", ns)) is not None:
                issues_url_text = stringify(issues_url)
                logger.info("Found bug tracker: %s", issues_url_text)
                mxml.set_upstream_bugs_to(issues_url_text)

        if (homepage := xml.find("pom:url", ns)) is not None:
            homepage_text = stringify(homepage)
            logger.info("Found homepage: %s", homepage_text)
            if (remote_id := extract_remote_id(homepage_text)) is not None:
                mxml.add_upstream_remote_id(remote_id)

        if (scm := xml.find("pom:scm", ns)) is not None:
            if (scm_url := scm.find("pom:url", ns)) is not None:
                scm_url_text = stringify(scm_url)
                logger.info("Found repository: %s", scm_url_text)
                if (remote_id := extract_remote_id(scm_url_text)) is not None:
                    mxml.add_upstream_remote_id(remote_id)

    @property
    def active(self) -> bool:
        return self.pom_xml.is_file()
