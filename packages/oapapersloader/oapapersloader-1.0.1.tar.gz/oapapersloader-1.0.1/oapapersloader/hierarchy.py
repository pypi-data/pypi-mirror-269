# -*- coding: UTF-8 -*-
""""
Created on 17.08.22

:author:     Martin Dočekal
"""
import math

from dataclasses import dataclass
from typing import Optional, Union, List, Dict, Any, Generator, Pattern, Callable, Tuple, Sequence, AbstractSet

from oapapersloader.myjson import json_dumps


@dataclass
class RefSpan:
    """
    Referencing span
    """

    __slots__ = ("index", "start", "end")

    index: Optional[int]
    """
    identifier of referenced entity
    it should be index to non_plaintext_content or bibliography
    null means that the source is unknown
    """
    start: int  #: span start offset
    end: int  #: span end offset (not inclusive)

    def asdict(self) -> Dict[str, Any]:
        """
        Converts this data class to dictionary.

        :return: dictionary representation of this data class
        """
        # dataclasses.asdict is too slow
        return {
            "index": self.index,
            "start": self.start,
            "end": self.end
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "RefSpan":
        """
        Creates this data class from dictionary.

        :param d: the dictionary used of instantiation
        :return: create RefSpan
        """
        return RefSpan(
            index=d["index"],
            start=d["start"],
            end=d["end"]
        )


@dataclass
class TextContent:
    """
    Text content of a document.
    """

    __slots__ = ("text", "citations", "references")

    text: str  #: text content of a part
    citations: List[RefSpan]  #: list of citation
    references: List[RefSpan]  #: list of references to images, graphs, tables, ...

    def asdict(self):
        """
        Converts this data class to dictionary.

        :return: dictionary representation of this data class
        """
        # dataclasses.asdict is too slow
        return {
            "text": self.text,
            "citations": [c.asdict() for c in self.citations],
            "references": [r.asdict() for r in self.references]
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "TextContent":
        """
        Creates this data class from dictionary.

        :param d: the dictionary used of instantiation
        :return: create TextContent
        """
        return TextContent(
            text=d["text"],
            citations=[RefSpan.from_dict(c) for c in d["citations"]],
            references=[RefSpan.from_dict(r) for r in d["references"]]
        )


@dataclass
class Hierarchy:
    """
    Representation of a document in form of hierarchy.

    Example of a document with two sections where each section has 2 paragraphs with 2 sentences

    headline    Title of a document
    content
        headline Section 1 headline
        content
            headline None
            content
                headline None
                content First sentence of first paragraph in first section.

                headline None
                content Second sentence of first paragraph in first section.

            headline None
            content
                headline None
                content First sentence of second paragraph in first section.

                headline None
                content Second sentence of second paragraph in first section.

        headline Section 2 headline
        content
            headline None
            content
                headline None
                content First sentence of first paragraph in second section.

                headline None
                content Second sentence of first paragraph in second section.

            headline None
            content
                headline None
                content First sentence of second paragraph in second section.

                headline None
                content Second sentence of second paragraph in second section.
    """
    __slots__ = ("headline", "content")

    headline: Optional[str]  #: headline of a part
    content: Union[List["Hierarchy"], TextContent]  # content of a part could contain another parts or a text content

    def __str__(self):
        return json_dumps(self.asdict())

    def remove(self, path: Sequence[int]):
        """
        Removes a sub-hierarchy from this hierarchy.

        :param path: the path to the sub-hierarchy
        """
        if len(path) == 1:
            del self.content[path[0]]
        else:
            self.content[path[0]].remove(path[1:])

    def asdict(self) -> Dict[str, Any]:
        """
        Converts this data class to dictionary.

        :return: dictionary representation of this data class
        """
        # dataclasses.asdict(self) is too slow
        return {
            "headline": self.headline,
            "content": self.content.asdict() if isinstance(self.content, TextContent) else [h.asdict() for h in self.content]
        }

    @staticmethod
    def from_dict(d: Dict[str, Any], lazy: bool = False, lazy_children: bool = False) -> "Hierarchy":
        """
        Creates this data class from dictionary.

        :param d: the dictionary used of instantiation
        :param lazy: if True, the content is not parsed and instead a lazy hierarchy is created
        :param lazy_children: if True, the children are not parsed and instead lazy hierarchies are created
        :return: create hierarchy
        """
        if lazy:
            return LazyHierarchy(d)

        content_dic = d["content"]

        content = [Hierarchy.from_dict(h, lazy_children) for h in content_dic] \
            if isinstance(content_dic, list) else TextContent.from_dict(content_dic)

        return Hierarchy(
            headline=d["headline"],
            content=content
        )

    def text_content(self, parent_condition: Optional[Callable[["Hierarchy"], bool]] = None) \
            -> Generator[TextContent, None, None]:
        """
        Generates text contents in hierarchy from the left most one to the right most one.

        :param parent_condition: optional filter that allows to set up condition on parent of text content
            True passes
        :return: generator of TextContent
        """

        for h in self.pre_order():
            if isinstance(h.content, TextContent) and (parent_condition is None or parent_condition(h)):
                yield h.content

    def citation_spans(self) -> Generator[RefSpan, None, None]:
        """
        Generation of all citations spans in hierarchy.
        It iterates text content from the left most one to the right most one, but it does not guarantee left to right
        positioning of citation inside a single text content.

        :return: generator of citation spans
        """
        for text in self.text_content():
            for cit in text.citations:
                yield cit

    @property
    def height(self) -> int:
        """
        Height of hierarchy.
        """
        if isinstance(self.content, TextContent) or len(self.content) == 0:
            return 0
        return max(h.height + 1 for h in self.content)

    @property
    def has_text_content(self) -> bool:
        """
        True if in this whole hierarchy is at least one text content with non empty text
        """

        return any(len(t_c.text) > 0 for t_c in self.text_content())

    def sections(self, min_height: int = 2) -> Generator["Hierarchy", None, None]:
        """
        Generates sections in hierarchy. Doesn't generate itself.

        :param min_height: sub-hierarchy is considered as section when it has at least such height
        :return: generator of sections in pre-order fashion
        """

        iterator = iter(self.pre_order())
        next(iterator)  # not interested in itself

        for h in iterator:
            if h.height >= min_height:
                yield h

    def nodes_with_height(self, height: int) -> Generator["Hierarchy", None, None]:
        """
        Generates nodes with given height in pre-order fashion.

        :param height: height of nodes that are supposed to be generated
        :return: generator of nodes with given height
        """

        for n in self.pre_order():
            if n.height == height:
                yield n

    def paths_to_nodes_with_height(self, height: int, on_path: Optional[List["Hierarchy"]] = None) \
            -> Generator[List["Hierarchy"], None, None]:
        """
        Generates paths from root to nodes with given height in pre-order fashion.

        :param height: height of nodes
        :param on_path: path tracing of parents
        :return: generates paths from roots to nodes with given height
             path is represented by sequence of nodes
        """
        self_height = self.height

        act_path = [self] if on_path is None else on_path + [self]

        if self_height == height:
            yield act_path
        elif self_height > height and isinstance(self.content, list):
            for h in self.content:
                yield from h.paths_to_nodes_with_height(height, act_path)

    def pre_order(self) -> Generator["Hierarchy", None, None]:
        """
        Iterates all sub-hierarchies in pre-order like order.

        And yes, it also generates itself.

        :return: generator of sub-hierarchies
        """

        to_process = [self]

        while to_process:
            h = to_process.pop(-1)
            yield h
            if isinstance(h.content, list):
                for sub_hierarchy in reversed(h.content):
                    to_process.append(sub_hierarchy)

    def get_part(self, headline_re: Pattern, max_h: float = math.inf, min_depth: float = 0,
                 max_depth: float = math.inf, return_path: bool = False) -> Union[List["Hierarchy"], List[Tuple[List["Hierarchy"], Tuple[int]]]]:
        """
        Searches in hierarchy for given headline and returns the whole sub-hierarchy associated to it.

        If a hierarchy with matching headline contains sub hierarchy with headline that also matches, it returns just
        the parent hierarchy.

        :param headline_re: compiled regex that will be used for headline matching
        :param max_h: maximal number of matching hierarchies after which the search is stopped
        :param min_depth: minimal depth of a node (root has zero depth)
        :param max_depth: maximal depth of a node
        :param return_path: if True, returns also path to the hierarchy
            path is represented by sequence of indices of sub-hierarchies
        :return: all searched hierarchies.
            If return_path is True, returns also path to the hierarchy
        """
        to_process = [(0, self, ())]

        res = []

        while to_process:
            depth, h, path = to_process.pop(-1)

            if h.headline is not None and depth >= min_depth:
                if headline_re.match(h.headline):
                    res.append((h, path) if return_path else h)
                    if len(res) >= max_h:
                        break
                    continue

            if isinstance(h.content, list) and depth < max_depth:
                for i, sub_hierarchy in zip(range(len(h.content)-1, -1, -1), reversed(h.content)):
                    to_process.append((depth + 1, sub_hierarchy, path + (i,)))

        return res


    def insert(self, pos: Sequence[int], item: "Hierarchy"):
        """
        Inserts the item at the given position.

        :param pos: position where to insert the item
        :param item: item to insert
        """
        if len(pos) == 0:
            raise ValueError("The position cannot be empty.")
        if len(pos) == 1:
            self.content.insert(pos[0], item)
        else:
            self.content[pos[0]].insert(pos[1:], item)

    def get(self, pos: Sequence[int]) -> "Hierarchy":
        """
        Returns the item at the given position.

        :param pos: position of the item
        :return: item at the given position
        """
        if len(pos) == 0:
            raise ValueError("The position cannot be empty.")
        if len(pos) == 1:
            return self.content[pos[0]]
        else:
            return self.content[pos[0]].get(pos[1:])


class LazyHierarchy(Hierarchy):
    """
    The content is loaded only when it is needed.
    """

    def __init__(self, d: Dict):
        """
        :param d: dictionary representation of a hierarchy
        """
        self.d = d
        self._hierarchy = None

    def __getattr__(self, attr):
        if self._hierarchy is None:
            self._hierarchy = Hierarchy.from_dict(self.d, lazy_children=True)
        return getattr(self._hierarchy, attr)
