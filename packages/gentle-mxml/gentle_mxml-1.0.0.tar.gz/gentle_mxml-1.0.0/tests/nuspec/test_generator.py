# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
# No warranty

from copy import deepcopy
from pathlib import Path

from gentle.generators.nuspec import NuspecGenerator
from gentle.metadata import MetadataXML
from tests.utils import compare_mxml


def test_pkg_none(mxml: MetadataXML):
    gen = NuspecGenerator(Path(__file__).parent / "pkg_none")
    assert not gen.active


def test_pkg_multiple(mxml: MetadataXML):
    gen = NuspecGenerator(Path(__file__).parent / "pkg_multiple")
    assert not gen.active


def test_pkg_empty(mxml: MetadataXML):
    gen = NuspecGenerator(Path(__file__).parent / "pkg_empty")
    assert gen.active

    mxml_old = deepcopy(mxml)
    gen.update_metadata_xml(mxml)
    assert compare_mxml(mxml_old, mxml) == ""
