# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
# No warranty

""" Metadata routines """

import logging
from pathlib import Path
from typing import Callable

import lxml.etree as ET

from gentle.metadata.types import Person, RemoteID, Upstream

logger = logging.getLogger("metadata")


class MetadataXML:
    """ Modify :file:`metadata.xml` files """

    def __init__(self, xmlfile: Path, parser: Callable[[Path], Upstream]):
        """
        :param xmlfile: Path to the :file:`metadata.xml` file
        :param upstream: Pre-parsed :class:`Upstream` object
        """
        self.xmlfile: Path = xmlfile
        self.xml: ET._ElementTree = ET.parse(self.xmlfile)

        self.upstream: Upstream = parser(xmlfile)
        self.modified: bool = False

        self._whitespace_map = {
            " ": "%20",
            "\n": "%0D",
            "\t": "%09",
        }

    def _encode_whitespace(self, url: str) -> str:
        for char, code in self._whitespace_map.items():
            url = url.replace(char, code)
        return url

    def dump(self) -> None:
        """ Write :file:`metadata.xml` file """
        logger.info("Writing metadata.xml")
        ET.indent(self.xml, space="\t", level=0)
        self.xml.write(self.xmlfile,
                       xml_declaration=True,
                       pretty_print=True,
                       encoding="UTF-8")

    def dumps(self) -> str:
        """ Convert the object to text """
        ET.indent(self.xml, space="\t", level=0)
        return ET.tostring(self.xml.getroot(), encoding="unicode")

    def add_upstream_maintainer(self, person: Person) -> None:
        """ Add a person to the list of upstream maintainers """
        if person in self.upstream.maintainers:
            return

        logger.info("Adding upstream maintainer: %s", person)
        self.upstream.maintainers.append(person)
        upstream = self._make_upstream_element()
        upstream.append(person.to_xml())

        self.modified = True

    def add_upstream_remote_id(self, remote_id: RemoteID) -> None:
        """ Add an item to the list of remote ids """
        for old_remote_id in self.upstream.remote_ids:
            if remote_id.attr == old_remote_id.attr:
                return

        logger.info("Adding remote id: %s", remote_id)
        self.upstream.remote_ids.append(remote_id)
        upstream = self._make_upstream_element()
        upstream.append(remote_id.to_xml())

        self.modified = True

    def set_upstream_bugs_to(self, url: str) -> None:
        """ Set upstream bugs-to URL """
        url = self._encode_whitespace(url)
        if self.upstream.bugs_to:
            return

        logger.info("Setting upstream bug tracker to %s", url)
        self.upstream.bugs_to = url

        upstream = self._make_upstream_element()
        bugs_to = ET.SubElement(upstream, "bugs-to")
        bugs_to.text = url

        self.modified = True

    def set_upstream_changelog(self, url: str) -> None:
        """ Set upstream changelog URL """
        url = self._encode_whitespace(url)
        if self.upstream.changelog:
            return

        logger.info("Setting upstream changelog to %s", url)
        self.upstream.changelog = url

        upstream = self._make_upstream_element()
        changelog = ET.SubElement(upstream, "changelog")
        changelog.text = url

        self.modified = True

    def set_upstream_doc(self, url: str) -> None:
        """ Set upstream documentation URL """
        url = self._encode_whitespace(url)
        if self.upstream.doc:
            return

        logger.info("Setting upstream documentation to %s", url)
        self.upstream.doc = url

        upstream = self._make_upstream_element()
        doc = ET.SubElement(upstream, "doc")
        doc.text = url

        self.modified = True

    def _make_upstream_element(self) -> ET._Element:
        if (upstream := self.xml.find("upstream")) is None:
            pkgmetadata = self.xml.getroot()
            upstream = ET.SubElement(pkgmetadata, "upstream")
        return upstream
