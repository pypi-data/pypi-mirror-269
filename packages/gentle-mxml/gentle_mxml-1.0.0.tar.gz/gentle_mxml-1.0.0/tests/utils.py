# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
# No warranty

from xmldiff.formatting import DiffFormatter
from xmldiff.main import diff_trees

from gentle.metadata import MetadataXML


def compare_mxml(old: MetadataXML, new: MetadataXML) -> str:
    return diff_trees(old.xml, new.xml, formatter=DiffFormatter())
