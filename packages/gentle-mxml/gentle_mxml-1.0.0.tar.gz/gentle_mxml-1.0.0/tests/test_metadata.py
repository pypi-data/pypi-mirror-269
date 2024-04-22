# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
# No warranty

import lxml.etree as ET

from gentle.metadata.types import Person, RemoteID


def test_person_to_xml():
    person = Person(name="Larry the Cow", email="larry@gentoo.org")
    assert (
        ET.tostring(person.to_xml(), encoding="unicode") == (
            '<maintainer>'
            '<name>Larry the Cow</name>'
            '<email>larry@gentoo.org</email>'
            '</maintainer>'
        )
    )

    person = Person(name="Larry the Cow")
    assert (
        ET.tostring(person.to_xml(), encoding="unicode") == (
            '<maintainer>'
            '<name>Larry the Cow</name>'
            '</maintainer>'
        )
    )

    person = Person(email="larry@gentoo.org")
    assert (
        ET.tostring(person.to_xml(), encoding="unicode") == (
            '<maintainer>'
            '<email>larry@gentoo.org</email>'
            '</maintainer>'
        )
    )


def test_remote_id_to_xml():
    remote_id = RemoteID(attr="github", value="gentoo/gentoo")
    assert (
        ET.tostring(remote_id.to_xml(), encoding="unicode") == (
            '<remote-id type="github">gentoo/gentoo</remote-id>'
        )
    )
