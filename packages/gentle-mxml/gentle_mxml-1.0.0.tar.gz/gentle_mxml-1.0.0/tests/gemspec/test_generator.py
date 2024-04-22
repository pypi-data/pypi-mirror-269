# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
# No warranty

from copy import deepcopy
from pathlib import Path

import pytest

from gentle.generators.gemspec import GemspecGenerator
from gentle.metadata import MetadataXML
from tests.utils import compare_mxml


def test_pkg_none(mxml: MetadataXML):
    gen = GemspecGenerator(Path(__file__).parent / "pkg_none")
    assert not gen.active


def test_pkg_empty(mxml: MetadataXML):
    gen = GemspecGenerator(Path(__file__).parent / "pkg_empty")
    assert gen.active

    mxml_old = deepcopy(mxml)
    gen.update_metadata_xml(mxml)
    assert compare_mxml(mxml_old, mxml) == ""


@pytest.mark.parametrize("dirname", ["rails"])
def test_pkg(mxml: MetadataXML, dirname: str):
    gen = GemspecGenerator(Path(__file__).parent / dirname)
    assert gen.active

    gen.update_metadata_xml(mxml)
    with open(Path(__file__).parent / dirname / "metadata.xml") as file:
        assert mxml.dumps() == file.read().rstrip()

    mxml_prev = deepcopy(mxml)
    gen.update_metadata_xml(mxml)
    assert compare_mxml(mxml_prev, mxml) == ""


@pytest.mark.ruby
def test_pkg_spec_empty(mxml: MetadataXML):
    gen = GemspecGenerator(Path(__file__).parent / "pkg_spec" / "pkg_empty")
    assert gen.active

    mxml_old = deepcopy(mxml)
    gen.update_metadata_xml(mxml)
    assert compare_mxml(mxml_old, mxml) == ""


@pytest.mark.ruby
@pytest.mark.parametrize("dirname", ["rubygems"])
def test_pkg_spec(mxml: MetadataXML, dirname: str):
    directory = Path(__file__).parent / "pkg_spec" / dirname

    gen = GemspecGenerator(directory)
    assert gen.active

    gen.update_metadata_xml(mxml)
    with open(directory / "metadata.xml") as file:
        assert mxml.dumps() == file.read().rstrip()

    mxml_prev = deepcopy(mxml)
    gen.update_metadata_xml(mxml)
    assert compare_mxml(mxml_prev, mxml) == ""
