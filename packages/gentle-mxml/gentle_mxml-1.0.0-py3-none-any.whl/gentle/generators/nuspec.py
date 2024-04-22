# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
# No warranty

"""
Metadata XML generator for NuGet.

The following attributes are supported:

* Remote ID
"""

import logging
from pathlib import Path

import lxml.etree as ET

from gentle.generators import AbstractGenerator
from gentle.metadata import MetadataXML
from gentle.metadata.utils import extract_remote_id
from gentle.utils import stringify

logger = logging.getLogger("nuget")


class NuspecGenerator(AbstractGenerator):
    def __init__(self, srcdir: Path):
        self.nuspec_files = list(srcdir.glob("*.nuspec"))

    def update_metadata_xml(self, mxml: MetadataXML) -> None:
        try:
            xml: ET._ElementTree = ET.parse(self.nuspec_files[0])
        except ET.ParseError:
            return

        nuspec_ns = "http://schemas.microsoft.com/packaging/2010/07/nuspec.xsd"
        ns = {"nuspec": nuspec_ns}

        if xml.getroot().tag != f"{{{nuspec_ns}}}package":
            return

        if (homepage := xml.find("nuspec:projectUrl", ns)) is not None:
            hp_url = stringify(homepage)
            if (remote_id := extract_remote_id(hp_url)) is not None:
                mxml.add_upstream_remote_id(remote_id)

        if (repo := xml.find("nuspec:repository", ns)) is not None:
            if (repo_url := repo.get("url")) is not None:
                if (remote_id := extract_remote_id(repo_url)) is not None:
                    mxml.add_upstream_remote_id(remote_id)

    @property
    def active(self) -> bool:
        return len(self.nuspec_files) == 1
