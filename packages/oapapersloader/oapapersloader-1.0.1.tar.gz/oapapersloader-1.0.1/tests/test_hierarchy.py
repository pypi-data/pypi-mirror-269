# -*- coding: UTF-8 -*-
""""
Created on 17.08.22

:author:     Martin Dočekal
"""
import copy
import re
from unittest import TestCase

from windpyutils.structures.maps import ImmutIntervalMap

from oapapersloader.hierarchy import Hierarchy, TextContent, RefSpan


class TestHierarchy(TestCase):
    def setUp(self) -> None:
        self.hierarchy = Hierarchy(
            "title",
            [
                Hierarchy(
                    "headline1",
                    [
                        Hierarchy(None,
                                  [
                                      Hierarchy(None, TextContent("text0", [], [])),
                                      Hierarchy(None, TextContent("text1", [], []))
                                  ]),
                        Hierarchy(None, TextContent("text2", [RefSpan(1, 10, 100)], []))
                    ]
                ),
                Hierarchy(
                    "headline2",
                    TextContent("text3", [RefSpan(2, 20, 200)], [RefSpan(0, 20, 200)])
                ),
            ]
        )

    def test_height(self):
        self.assertEqual(3, self.hierarchy.height)
        self.assertEqual(0, Hierarchy(None, TextContent("text0", [], [])).height)
        self.assertEqual(0, Hierarchy(None, []).height)
        self.assertEqual(1, Hierarchy(None,
                                      [
                                          Hierarchy(None, TextContent("text0", [], [])),
                                          Hierarchy(None, TextContent("text1", [], []))
                                      ]).height)

    def test_sections(self):
        self.assertSequenceEqual([self.hierarchy.content[0]], list(self.hierarchy.sections()))
        self.assertSequenceEqual([], list(Hierarchy(None, []).sections()))
        self.assertSequenceEqual([
            self.hierarchy.content[0], self.hierarchy.content[0].content[0]
        ], list(self.hierarchy.sections(1)))

    def test_has_text_content(self):
        self.assertTrue(self.hierarchy.has_text_content)
        self.assertTrue(Hierarchy(None, TextContent("text0", [], [])).has_text_content)
        self.assertFalse(Hierarchy(None, []).has_text_content)
        self.assertFalse(Hierarchy(None, [Hierarchy(None, []), Hierarchy(None, [])]).has_text_content)
        self.assertFalse(Hierarchy(None, TextContent("", [], [])).has_text_content)

    def test_nodes_with_height(self):
        self.assertSequenceEqual([
            Hierarchy(None, TextContent("text0", [], [])), Hierarchy(None, TextContent("text1", [], [])),
            Hierarchy(None, TextContent("text2", [RefSpan(1, 10, 100)], [])),
            Hierarchy("headline2", TextContent("text3", [RefSpan(2, 20, 200)], [RefSpan(0, 20, 200)]))
        ], list(self.hierarchy.nodes_with_height(0)))

        res = list(self.hierarchy.nodes_with_height(1))
        self.assertSequenceEqual(self.hierarchy.content[0].content[:1], res)
        self.assertSequenceEqual([self.hierarchy.content[0]], list(self.hierarchy.nodes_with_height(2)))
        self.assertSequenceEqual([], list(self.hierarchy.nodes_with_height(99)))

    def test_paths_to_nodes_with_height(self):
        self.assertSequenceEqual([], list(self.hierarchy.paths_to_nodes_with_height(10)))
        res = list(self.hierarchy.paths_to_nodes_with_height(0))
        self.assertSequenceEqual([
            [self.hierarchy, self.hierarchy.content[0], self.hierarchy.content[0].content[0],
             self.hierarchy.content[0].content[0].content[0]],
            [self.hierarchy, self.hierarchy.content[0], self.hierarchy.content[0].content[0],
             self.hierarchy.content[0].content[0].content[1]],
            [self.hierarchy, self.hierarchy.content[0], self.hierarchy.content[0].content[1]],
            [self.hierarchy, self.hierarchy.content[1]]
        ], res)

    def test_text_content(self):
        self.assertListEqual(
            [
                TextContent("text0", [], []),
                TextContent("text1", [], []),
                TextContent("text2", [RefSpan(1, 10, 100)], []),
                TextContent("text3", [RefSpan(2, 20, 200)], [RefSpan(0, 20, 200)])
            ], list(self.hierarchy.text_content()))

    def test_text_content_parent_condition(self):
        self.assertListEqual(
            [
                TextContent("text3", [RefSpan(2, 20, 200)], [RefSpan(0, 20, 200)])
            ], list(self.hierarchy.text_content(lambda x: x.headline == "headline2")))

    def test_pre_order(self):
        sub_hiers = [
            self.hierarchy,
            self.hierarchy.content[0],
            self.hierarchy.content[0].content[0],
            self.hierarchy.content[0].content[0].content[0], self.hierarchy.content[0].content[0].content[1],
            self.hierarchy.content[0].content[1],
            self.hierarchy.content[1],
        ]
        res = list(self.hierarchy.pre_order())
        self.assertListEqual(sub_hiers, res)

