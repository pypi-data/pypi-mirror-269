# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
# No warranty

"""
Metadata XML generator for Perl CPAN::Meta::Spec.

The following attributes are supported:

* Upstream maintainer(s)
* Upstream bug tracker
* Remote ID
"""

import json
import logging
import shutil
import subprocess
from pathlib import Path

from gentle.generators import AbstractGenerator
from gentle.metadata import MetadataXML
from gentle.metadata.utils import extract_name_email, extract_remote_id

logger = logging.getLogger("cpan")


class CpanGenerator(AbstractGenerator):
    def __init__(self, srcdir: Path):
        self.srcdir = srcdir

        self.meta_json = srcdir / "META.json"
        self.makefile_pl = srcdir / "Makefile.PL"

        self.perl = shutil.which("perl")

    # pylint: disable=too-many-branches
    def update_metadata_xml(self, mxml: MetadataXML) -> None:
        meta_json = self.meta_json
        if not self.meta_json.is_file() and self.makefile_pl.is_file():
            cmd = [str(self.perl), str(self.makefile_pl)]
            subprocess.run(cmd, cwd=self.srcdir, check=False)

            meta_json = self.srcdir / "MYMETA.json"

        if not meta_json.is_file():
            return

        with open(meta_json) as file:
            try:
                meta = json.load(file)
            except json.decoder.JSONDecodeError:
                return

        # Support Spec 2 only
        if not (
            "meta-spec" in meta
            and isinstance(meta["meta-spec"], dict)
            and str(meta["meta-spec"].get("version")) == "2"
        ):
            return

        for author in map(extract_name_email, meta.get("author", [])):
            if author is None:
                continue
            logger.info("Found upstream maintainer: %s", author)
            mxml.add_upstream_maintainer(author)

        for name, value in meta.get("resources", {}).items():
            match name:
                case "homepage":
                    if not isinstance(value, str):
                        continue

                    logger.info("Found homepage: %s", value)
                    if (remote_id := extract_remote_id(value)) is not None:
                        mxml.add_upstream_remote_id(remote_id)
                case "bugtracker":
                    if not isinstance(value, dict):
                        continue

                    if "web" in value:
                        bugs_to = value["web"]
                    elif "mailto" in value:
                        bugs_to = "mailto:" + value["mailto"]
                    else:
                        continue
                    logger.info("Found bug tracker: %s", bugs_to)
                    mxml.set_upstream_bugs_to(bugs_to)
                case "repository":
                    if not isinstance(value, dict):
                        continue

                    if (repo := value.get("web")) is None:
                        continue
                    logger.info("Found repository: %s", repo)
                    if (remote_id := extract_remote_id(repo)) is not None:
                        mxml.add_upstream_remote_id(remote_id)
                case _:
                    if not isinstance(value, str):
                        continue

                    logger.info("Found %s: %s", name, value)
                    if (remote_id := extract_remote_id(value)) is not None:
                        mxml.add_upstream_remote_id(remote_id)

    @property
    def active(self) -> bool:
        return (
            self.meta_json.is_file()
            or (
                self.perl is not None
                and self.makefile_pl.is_file()
            )
        )

    @property
    def slow(self) -> bool:
        return not self.meta_json.is_file()
