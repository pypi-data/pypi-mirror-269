# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
# No warranty

from copy import deepcopy
from pathlib import Path

import pytest

from gentle.generators.shards import ShardsGenerator
from gentle.metadata import MetadataXML
from tests.utils import compare_mxml


def test_pkg_none(mxml: MetadataXML):
    gen = ShardsGenerator(Path(__file__).parent / "pkg_none")
    assert not gen.active


def test_pkg_empty(mxml: MetadataXML):
    gen = ShardsGenerator(Path(__file__).parent / "pkg_empty")
    assert gen.active

    mxml_old = deepcopy(mxml)
    gen.update_metadata_xml(mxml)
    assert compare_mxml(mxml_old, mxml) == ""


@pytest.mark.parametrize("dirname", ["athena-spec", "exception_page"])
def test_pkg(mxml: MetadataXML, dirname: str):
    gen = ShardsGenerator(Path(__file__).parent / dirname)
    assert gen.active

    gen.update_metadata_xml(mxml)
    with open(Path(__file__).parent / dirname / "metadata.xml") as file:
        assert mxml.dumps() == file.read().rstrip()

    mxml_prev = deepcopy(mxml)
    gen.update_metadata_xml(mxml)
    assert compare_mxml(mxml_prev, mxml) == ""
