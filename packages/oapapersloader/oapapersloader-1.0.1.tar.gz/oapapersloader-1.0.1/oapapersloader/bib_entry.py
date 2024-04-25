# -*- coding: UTF-8 -*-
""""
Created on 05.09.22

:author:     Martin Dočekal
"""
from dataclasses import dataclass
from typing import Optional, Tuple, Dict, Any


@dataclass
class BibEntry:
    __slots__ = ("id", "title", "year", "authors")

    id: Optional[int]  # this is id of document in dataset may be None if this document is not in it
    title: str
    year: Optional[int]
    authors: Tuple[str, ...]

    def asdict(self) -> Dict[str, Any]:
        """
        Converts this data class to dictionary.

        :return: dictionary representation of this data class
        """
        # dataclasses.asdict is too slow
        return {
            "id": self.id,
            "title": self.title,
            "year": self.year,
            "authors": self.authors
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "BibEntry":
        """
        Creates this data class from dictionary.

        :param d: the dictionary used of instantiation
        :return: bib entry
        """
        return cls(d["id"], d["title"], d["year"], tuple(d["authors"]))

