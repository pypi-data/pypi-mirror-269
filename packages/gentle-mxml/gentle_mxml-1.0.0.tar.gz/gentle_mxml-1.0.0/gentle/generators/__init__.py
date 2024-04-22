# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
# No warranty

""" Generic generator routines """

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Type

from gentle.metadata import MetadataXML


class AbstractGenerator(ABC):
    """ Generic class for metadata generators. """
    _subclasses: "list[GeneratorClass]" = []

    @classmethod
    def get_generator_subclasses(cls) -> "list[GeneratorClass]":
        return cls._subclasses.copy()

    @abstractmethod
    def __init__(self, srcdir: Path):
        ...

    def __init_subclass__(cls: "GeneratorClass", **kwargs: dict) -> None:
        super().__init_subclass__(**kwargs)
        AbstractGenerator._subclasses.append(cls)

    @abstractmethod
    def update_metadata_xml(self, mxml: MetadataXML) -> None:
        ...

    @property
    @abstractmethod
    def active(self) -> bool:
        ...

    @property
    def slow(self) -> bool:
        return False


GeneratorClass = Type[AbstractGenerator]
