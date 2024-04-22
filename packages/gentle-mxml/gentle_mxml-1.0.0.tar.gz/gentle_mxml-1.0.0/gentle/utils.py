# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
# No warranty

""" Misc utilities """

import lxml.etree as ET


def stringify(element: ET._Element) -> str:
    return "".join(
        (text for text in element.itertext() if isinstance(text, str))
    )
