# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023-2024 Anna <cyber@sysrq.in>
# No warranty

from pathlib import Path

import pytest

from gentle.metadata import MetadataXML
from gentle.pms.portagepm import parse_mxml


def pytest_addoption(parser):
    parser.addoption("--with-perl", action="store_true",
                     help="run tests that require Perl")
    parser.addoption("--with-ruby", action="store_true",
                     help="run tests that require Ruby")


def pytest_configure(config):
    config.addinivalue_line("markers", "perl: mark test as using Perl")
    config.addinivalue_line("markers", "ruby: mark test as using Ruby")


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--with-perl"):
        skip_perl = pytest.mark.skip(reason="need --with-perl option to run")
        for item in items:
            if "perl" in item.keywords:
                item.add_marker(skip_perl)

    if not config.getoption("--with-ruby"):
        skip_perl = pytest.mark.skip(reason="need --with-ruby option to run")
        for item in items:
            if "ruby" in item.keywords:
                item.add_marker(skip_perl)


@pytest.fixture
def mxml() -> MetadataXML:
    return MetadataXML(Path(__file__).parent / "metadata.xml", parse_mxml)
