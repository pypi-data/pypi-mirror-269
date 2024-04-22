# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2022-2023 Anna <cyber@sysrq.in>
# No warranty

# pylint: disable=unused-import

import argparse
import importlib.util
import logging
import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import gentle
from gentle.generators import AbstractGenerator, GeneratorClass
from gentle.metadata import MetadataXML

import gentle.generators.autoconf
import gentle.generators.bower
import gentle.generators.cargo
import gentle.generators.composer
import gentle.generators.cpan
import gentle.generators.doap
import gentle.generators.gemspec
import gentle.generators.hpack
import gentle.generators.npm
import gentle.generators.nuspec
import gentle.generators.pear
import gentle.generators.pubspec
import gentle.generators.python.pyproject
import gentle.generators.python.setuptools
import gentle.generators.python.pkg_info
import gentle.generators.python.wheel
import gentle.generators.shards

_HAS_PORTAGE = importlib.util.find_spec("portage") is not None

_HAS_BUILD = importlib.util.find_spec("build") is not None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")


def main() -> None:
    """
    Parse command-line arguments and run the program.
    """

    pm = []
    if _HAS_PORTAGE:
        pm.append("portage")

    if len(pm) == 0:
        raise RuntimeError("No package manager installed. Aborting")

    py_api = ["simple"]
    if _HAS_BUILD:
        py_api.insert(0, "wheel")

    parser = argparse.ArgumentParser("gentle", description=gentle.__doc__)
    parser.add_argument("ebuild", type=Path, help="path to the ebuild file")
    parser.add_argument("--api", "-a", choices=pm, default=pm[0],
                        help="package manager API to use")
    parser.add_argument("--prefix", "-p",
                        help="value of EPREFIX")
    parser.add_argument("--quick", "-q", action="store_true",
                        help="skip slow generators")
    parser.add_argument("-v", action="version", version=gentle.__version__)
    args = parser.parse_args()

    if args.prefix is not None:
        os.environ["PORTAGE_OVERRIDE_EPREFIX"] = args.prefix

    with TemporaryDirectory(prefix="gentle-") as tmpdir:
        # pylint: disable=import-outside-toplevel
        match args.api:
            case "portage":
                from gentle.pms.portagepm import parse_mxml, src_unpack

        mxml_file = args.ebuild.parent / "metadata.xml"
        try:
            mxml = MetadataXML(mxml_file, parse_mxml)
        except FileNotFoundError:
            logger.error("Ebuild's metadata.xml file is missing, create it before running gentle")
            sys.exit(1)

        srcdir = src_unpack(args.ebuild, tmpdir)
        cls: GeneratorClass
        for cls in AbstractGenerator.get_generator_subclasses():
            generator = cls(srcdir)
            if not generator.active:
                continue
            if args.quick and generator.slow:
                continue
            logger.info("Starting %s", cls.__name__)
            generator.update_metadata_xml(mxml)

    if mxml.modified:
        mxml.dump()


if __name__ == "__main__":
    main()
