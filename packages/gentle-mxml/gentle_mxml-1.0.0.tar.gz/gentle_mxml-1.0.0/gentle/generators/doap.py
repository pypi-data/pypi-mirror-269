# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2022 Anna <cyber@sysrq.in>
# No warranty

"""
Metadata XML generator for DOAP.

The following attributes are supported:

* Upstream maintainer(s)
* Remote ID
"""

import logging
from pathlib import Path
from xml.sax._exceptions import SAXException

from gentle.generators import AbstractGenerator
from gentle.metadata import MetadataXML
from gentle.metadata.types import Person
from gentle.metadata.utils import extract_remote_id

try:
    import rdflib.exceptions
    from rdflib import Graph
    from rdflib.namespace import DOAP, FOAF
    _HAS_RDFLIB = True
except ModuleNotFoundError:
    _HAS_RDFLIB = False

logger = logging.getLogger("doap")


class DoapGenerator(AbstractGenerator):
    def __init__(self, srcdir: Path):
        self.doap_files = list(srcdir.glob("*.doap"))

    def update_metadata_xml(self, mxml: MetadataXML) -> None:
        project = Graph(base="doap", bind_namespaces="rdflib")
        try:
            project.parse(self.doap_files[0], format="xml")
        except (SAXException, rdflib.exceptions.ParserError):
            return

        maint_key = DOAP.maintainer
        if (None, maint_key, None) not in project:
            maint_key = DOAP.developer

        for maint_obj in project.objects(None, maint_key):
            person = Person()
            maint_name_objs = list(project.objects(maint_obj, FOAF.name))
            maint_email_objs = list(project.objects(maint_obj, FOAF.mbox))

            if len(maint_name_objs) == 1:
                person.name = str(maint_name_objs[0])
            else:
                continue

            if len(maint_email_objs) != 0:
                person.email = str(maint_email_objs[0]).removeprefix("mailto:")

            logger.info("Found upstream maintainer: %s", person)
            mxml.add_upstream_maintainer(person)

        for homepage in project.objects(None, DOAP.homepage):
            logger.info("Found homepage: %s", homepage)
            if (remote_id := extract_remote_id(str(homepage))) is not None:
                mxml.add_upstream_remote_id(remote_id)

    @property
    def active(self) -> bool:
        return _HAS_RDFLIB and len(self.doap_files) == 1
