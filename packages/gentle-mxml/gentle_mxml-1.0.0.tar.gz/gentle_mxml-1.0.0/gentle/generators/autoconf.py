# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
# No warranty

"""
Metadata XML generator for GNU Autoconf.

The following attributes are supported:

* Upstream bug tracker
* Remote ID
"""

import logging
import re
import shutil
import subprocess
from email.utils import parseaddr
from pathlib import Path

from gentle.generators import AbstractGenerator
from gentle.metadata import MetadataXML
from gentle.metadata.utils import extract_remote_id

logger = logging.getLogger("autoconf")


class AutoconfGenerator(AbstractGenerator):
    def __init__(self, srcdir: Path):
        self.srcdir = srcdir

        self.conf_sh = srcdir / "configure"
        self.conf_ac = srcdir / "configure.ac"

        self.autoconf = shutil.which("autoconf")

    def update_metadata_xml(self, mxml: MetadataXML) -> None:
        if not self.conf_sh.is_file() and self.conf_ac.is_file():
            subprocess.run([str(self.autoconf)], cwd=self.srcdir, check=False)

        if not self.conf_sh.is_file():
            return

        bugs_re = re.compile("^PACKAGE_BUGREPORT='(?P<val>.+)'$")
        url_re = re.compile("^PACKAGE_URL='(?P<val>.+)'$")

        with open(self.conf_sh) as file:
            for line in file:
                if (bugs_to := bugs_re.match(line)) is not None:
                    value = bugs_to.group("val")
                    logger.info("Found bug tracker: %s", value)

                    if "@" in parseaddr(value)[1]:
                        value = f"mailto:{value}"
                    mxml.set_upstream_bugs_to(value)
                elif (url := url_re.match(line)) is not None:
                    value = url.group("val")
                    logger.info("Found homepage: %s", value)
                    if (remote_id := extract_remote_id(value)) is not None:
                        mxml.add_upstream_remote_id(remote_id)

    @property
    def active(self) -> bool:
        return (
            self.conf_sh.is_file()
            or (
                self.conf_ac.is_file() and self.autoconf is not None
            )
        )

    @property
    def slow(self) -> bool:
        return not self.conf_sh.is_file()
