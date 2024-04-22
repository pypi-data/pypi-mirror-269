# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2022 Anna <cyber@sysrq.in>
# No warranty

"""
Metadata XML generator for Ruby Gems.

The following attributes are supported:

* Upstream bug tracker
* Upstream changelog
* Upstream documentation
* Remote ID
"""

import logging
import shutil
import subprocess
from pathlib import Path

from gentle.generators import AbstractGenerator
from gentle.metadata import MetadataXML
from gentle.metadata.utils import extract_remote_id

try:
    import yaml
    from yaml import Loader
    _HAS_PYYAML = True

    class VersionTag(yaml.YAMLObject):
        """ Dummy version tag """
        yaml_tag = "!ruby/object:Gem::Version"

    class RequirementTag(yaml.YAMLObject):
        """ Dummy requirement tag """
        yaml_tag = "!ruby/object:Gem::Requirement"

    class DependencyTag(yaml.YAMLObject):
        """ Dummy dependency tag """
        yaml_tag = "!ruby/object:Gem::Dependency"

    class SpecificationTag(yaml.YAMLObject):
        """ Dummy specification tag """
        yaml_tag = "!ruby/object:Gem::Specification"
except ModuleNotFoundError:
    _HAS_PYYAML = False

logger = logging.getLogger("gemspec")


class GemspecGenerator(AbstractGenerator):
    def __init__(self, srcdir: Path):
        self.srcdir = srcdir

        self.gemspec_files = list(srcdir.glob("*.gemspec"))
        self.metadata_yml = srcdir / "all" / "metadata"

        self.ruby = shutil.which("ruby")

    def update_metadata_xml(self, mxml: MetadataXML) -> None:
        if self.metadata_yml.is_file():
            with open(self.metadata_yml, "rb") as file:
                data = file.read()
        else:
            gemspec = self.gemspec_files[0]
            code = "print Gem::Specification.load(gets.chomp).to_yaml"
            data = subprocess.run([str(self.ruby), "-e", code],
                                  input=str(gemspec).encode(),
                                  cwd=self.srcdir,
                                  check=False,
                                  capture_output=True).stdout

        if (metadata := yaml.load(data, Loader)) is None:
            return

        if metadata.homepage:
            logger.info("Found homepage: %s", metadata.homepage)
            if (remote_id := extract_remote_id(metadata.homepage)) is not None:
                mxml.add_upstream_remote_id(remote_id)

        for name, value in metadata.metadata.items():
            if not isinstance(value, str):
                continue

            logger.info("Found %s: %s", name, value)
            match name:
                case "bug_tracker_uri":
                    mxml.set_upstream_bugs_to(value)
                case "changelog_uri":
                    mxml.set_upstream_changelog(value)
                case "documentation_uri":
                    mxml.set_upstream_doc(value)
                case "homepage_uri" | "source_code_uri":
                    if (remote_id := extract_remote_id(value)) is not None:
                        mxml.add_upstream_remote_id(remote_id)

    @property
    def active(self) -> bool:
        return (
            _HAS_PYYAML
            and (
                self.metadata_yml.is_file()
                or (
                    len(self.gemspec_files) == 1
                    and self.ruby is not None
                )
            )
        )
