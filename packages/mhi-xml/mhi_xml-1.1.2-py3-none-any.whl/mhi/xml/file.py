"""
MHI's XML File
"""

#===============================================================================
# Imports
#===============================================================================

from __future__ import annotations

from pathlib import Path
from random import randint
from typing import cast, Optional, Protocol, Union

from lxml import etree as ET

from mhi.xml.node import RootNode


#===============================================================================
# Exports
#===============================================================================

__all__ = ['File', 'FileProtocol', ]


#===============================================================================
# XML File object
#===============================================================================

class File:
    """
    Base-class for various XML files
    """

    _path: Optional[Path]
    _doc: ET._ElementTree
    _root: RootNode
    _modified: bool


    def __init__(self, parser: ET.XMLParser):

        self._parser = parser
        self._modified = False


    def _parse(self, xml_str: str) -> ET._Element:

        return ET.fromstring(xml_str, self._parser)


    def _read(self, path: Path):

        self._doc = ET.parse(path, self._parser)
        self._root = cast(RootNode, self._doc.getroot())
        self._path = path
        self._modified = False

        self._root._file_ref = self         # pylint: disable=protected-access


    def _load(self, xml_str: str):

        self._root = cast(RootNode, self._parse(xml_str))
        self._doc = self._root.getroottree()
        self._path = None
        self.set_modified()

        self._root._file_ref = self         # pylint: disable=protected-access


    def set_modified(self):
        """
        Flag the XML document as modified
        """

        self._modified = True


    @property
    def modified(self) -> bool:
        """
        Return the modified status of the XML document (read-only)
        """

        return self._modified


    @property
    def path(self) -> Optional[Path]:
        """
        The path of the XML document (read-only)

        .. note::

            The path is `None` if it has not been read from an actual file.
        """

        return self._path


    def save(self):
        """
        Write the updated XML document back to the file it was read from.
        """

        if self._path is None:
            raise ValueError("This XML document does not have a path.")

        self._save_as(self._path)
        self._modified = False


    def save_as(self, path: Union[Path, str]):
        """
        Write the XML document to a file.
        """

        path = Path(path)

        self._save_as(path)
        self._path = path
        self._modified = False


    def _save_as(self, path: Path):

        self._doc.write(path, encoding='utf-8')


    def id_exists(self, id_: int) -> bool:
        """
        Test whether an `<element id='#'/>` exists in the document
        """

        node = self._root.find(f'.//*[@id="{id_}"]')

        return node is not None


    def make_id(self) -> int:
        """
        Create a new (and unused) ID number
        """

        new_id = randint(100_000_000, 1_000_000_000)
        while self.id_exists(new_id):
            new_id = randint(100_000_000, 1_000_000_000)

        return new_id

    @property
    def root(self):
        """
        Fetch root node of file
        """

        return self._root


#===============================================================================

class FileProtocol(Protocol):           # pylint: disable=too-few-public-methods
    """
    Mix-in Protocol for retrieving the `mhi.xml.File` from an object
    """

    @property
    def _file(self) -> File: ...
