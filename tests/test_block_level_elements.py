"""
Python Markdown

A Python implementation of John Gruber's Markdown.

Documentation: https://python-markdown.github.io/
GitHub: https://github.com/Python-Markdown/markdown/
PyPI: https://pypi.org/project/Markdown/

Started by Manfred Stienstra (http://www.dwerg.net/).
Maintained for a few years by Yuri Takhteyev (http://www.freewisdom.org).
Currently maintained by Waylan Limberg (https://github.com/waylan),
Dmitry Shachnev (https://github.com/mitya57) and Isaac Muse (https://github.com/facelessuser).

Copyright 2007-2023 The Python Markdown Project (v. 1.7 and later)
Copyright 2004, 2005, 2006 Yuri Takhteyev (v. 0.2-1.6b)
Copyright 2004 Manfred Stienstra (the original version)

License: BSD (see LICENSE.md for details).

Tests for block level elements.
===============================

Tests specific to the hybrid list/set container for block level elements.
"""

import unittest

from markdown.util import _BlockLevelElements


class TestBlockLevelElements(unittest.TestCase):
    """ Tests for the block level elements container. """

    def test__init__(self):
        ble = _BlockLevelElements([])
        self.assertEqual(ble._list, [])
        self.assertEqual(ble._set, set())

    def test___add__(self):
        ble = _BlockLevelElements(["a", "b", ])
        with self.assertWarns(DeprecationWarning):
            ble2 = ble + ["c", "d"]
        self.assertIsInstance(ble2, list)
        self.assertEqual(ble2, ["a", "b", "c", "d"])

    def test___and__(self):
        ble = _BlockLevelElements(["a", "b"])
        ble2 = ble & {"b", "c"}
        self.assertIsInstance(ble2, set)
        self.assertEqual(ble2, {"b"})

    def test___contains__(self):
        ble = _BlockLevelElements(["a", "b"])
        self.assertIn("a", ble)
        self.assertNotIn("c", ble)

    def test___delitem__(self):
        ble = _BlockLevelElements(["a", "b", "c"])
        with self.assertWarns(DeprecationWarning):
            del ble[0]
        self.assertEqual(ble._list, ["b", "c"])
        self.assertEqual(ble._set, {"b", "c"})
        with self.assertWarns(DeprecationWarning):
            del ble[1]
        self.assertEqual(ble._list, ["b"])
        self.assertEqual(ble._set, {"b"})
        with self.assertWarns(DeprecationWarning):
            self.assertRaises(IndexError, ble.__delitem__, 10)

    def test___getitem__(self):
        ble = _BlockLevelElements(["a", "b", "c"])
        with self.assertWarns(DeprecationWarning):
            self.assertEqual(ble[0], "a")
            self.assertEqual(ble[1], "b")
            self.assertEqual(ble[2], "c")
            self.assertRaises(IndexError, ble.__getitem__, 10)

    def test___iadd__(self):
        ble = _BlockLevelElements(["a", "b"])
        with self.assertWarns(DeprecationWarning):
            ble += ["c", "d"]
        self.assertEqual(ble._list, ["a", "b", "c", "d"])
        self.assertEqual(ble._set, {"a", "b", "c", "d"})

    def test___iand__(self):
        ble = _BlockLevelElements(["a", "b"])
        ble &= {"b", "c"}
        self.assertEqual(ble._list, ["b"])
        self.assertEqual(ble._set, {"b"})

    def test___ior__(self):
        ble = _BlockLevelElements(["a", "b"])
        ble |= {"b", "c"}
        self.assertEqual(ble._list, ["a", "b", "c"])
        self.assertEqual(ble._set, {"a", "b", "c"})

    def test___iter__(self):
        ble = _BlockLevelElements(["a", "b", "c"])
        self.assertEqual(tuple(ble), ("a", "b", "c"))

    def test___len__(self):
        self.assertEqual(len(_BlockLevelElements([])), 0)
        self.assertEqual(len(_BlockLevelElements(["a", "a"])), 2)
        self.assertEqual(len(_BlockLevelElements(["a", "b", "c"])), 3)

    def test___or__(self):
        ble = _BlockLevelElements(["a", "b"])
        ble2 = ble | {"b", "c"}
        self.assertIsInstance(ble2, set)
        self.assertEqual(ble2, {"a", "b", "c"})

    def test___rand__(self):
        ble = _BlockLevelElements(["a", "b"])
        ble2 = {"b", "c"} & ble
        self.assertIsInstance(ble2, set)
        self.assertEqual(ble2, {"b"})

    def test___ror__(self):
        ble = _BlockLevelElements(["a", "b"])
        ble2 = {"b", "c"} | ble
        self.assertIsInstance(ble2, set)
        self.assertEqual(ble2, {"a", "b", "c"})

    def test___rsub__(self):
        ble = _BlockLevelElements(["a", "b"])
        ble2 = {"b", "c"} - ble
        self.assertIsInstance(ble2, set)
        self.assertEqual(ble2, {"c"})

    def test___rxor__(self):
        ble = _BlockLevelElements(["a", "b"])
        ble2 = {"b", "c"} ^ ble
        self.assertIsInstance(ble2, set)
        self.assertEqual(ble2, {"a", "c"})

    def test___sub__(self):
        ble = _BlockLevelElements(["a", "b"])
        ble2 = ble - {"b", "c"}
        self.assertIsInstance(ble2, set)
        self.assertEqual(ble2, {"a"})

    def test___xor__(self):
        ble = _BlockLevelElements(["a", "b"])
        ble2 = ble ^ {"b", "c"}
        self.assertIsInstance(ble2, set)
        self.assertEqual(ble2, {"a", "c"})

    def test___reversed__(self):
        ble = _BlockLevelElements(["a", "b", "c"])
        with self.assertWarns(DeprecationWarning):
            self.assertEqual(tuple(reversed(ble)), ("c", "b", "a"))

    def test___setitem__(self):
        ble = _BlockLevelElements(["a", "b", "c"])
        with self.assertWarns(DeprecationWarning):
            ble[0] = "d"
        self.assertEqual(ble._list, ["d", "b", "c"])
        self.assertEqual(ble._set, {"d", "b", "c"})
        with self.assertWarns(DeprecationWarning):
            ble[1] = "e"
        self.assertEqual(ble._list, ["d", "e", "c"])
        self.assertEqual(ble._set, {"d", "e", "c"})
        with self.assertWarns(DeprecationWarning):
            self.assertRaises(IndexError, ble.__setitem__, 10, "f")

    def test___str__(self):
        ble = _BlockLevelElements(["a"])
        self.assertEqual(str(ble), "{'a'}")

    def test_add(self):
        ble = _BlockLevelElements(["a", "b"])
        ble.add("c")
        self.assertEqual(ble._list, ["a", "b", "c"])
        self.assertEqual(ble._set, {"a", "b", "c"})

    def test_append(self):
        ble = _BlockLevelElements(["a", "b"])
        with self.assertWarns(DeprecationWarning):
            ble.append("c")
        self.assertEqual(ble._list, ["a", "b", "c"])
        self.assertEqual(ble._set, {"a", "b", "c"})

    def test_clear(self):
        ble = _BlockLevelElements(["a", "b"])
        ble.clear()
        self.assertEqual(ble._list, [])
        self.assertEqual(ble._set, set())

    def test_copy(self):
        ble = _BlockLevelElements(["a", "b"])
        ble2 = ble.copy()
        self.assertIsNot(ble2, ble)
        self.assertEqual(ble2._list, ["a", "b"])
        self.assertEqual(ble2._set, {"a", "b"})

    def test_count(self):
        ble = _BlockLevelElements(["a", "b", "a"])
        with self.assertWarns(DeprecationWarning):
            self.assertEqual(ble.count("a"), 2)
            self.assertEqual(ble.count("b"), 1)
            self.assertEqual(ble.count("c"), 0)

    def test_difference(self):
        ble = _BlockLevelElements(["a", "b"])
        ble2 = ble.difference({"b", "c"})
        self.assertIsInstance(ble2, set)
        self.assertEqual(ble2, {"a"})

    def test_difference_update(self):
        ble = _BlockLevelElements(["a", "b"])
        ble.difference_update({"b", "c"})
        self.assertEqual(ble._list, ["a"])
        self.assertEqual(ble._set, {"a"})

    def test_discard(self):
        ble = _BlockLevelElements(["a", "b"])
        ble.discard("b")
        self.assertEqual(ble._list, ["a"])
        self.assertEqual(ble._set, {"a"})

    def test_extend(self):
        ble = _BlockLevelElements(["a", "b"])
        with self.assertWarns(DeprecationWarning):
            ble.extend(["c", "d"])
        self.assertEqual(ble._list, ["a", "b", "c", "d"])
        self.assertEqual(ble._set, {"a", "b", "c", "d"})

    def test_index(self):
        ble = _BlockLevelElements(["a", "b", "c"])
        with self.assertWarns(DeprecationWarning):
            self.assertEqual(ble.index("a"), 0)
            self.assertEqual(ble.index("b"), 1)
            self.assertEqual(ble.index("c"), 2)
            self.assertRaises(ValueError, ble.index, "d")

    def test_insert(self):
        ble = _BlockLevelElements(["a", "b", "c"])
        with self.assertWarns(DeprecationWarning):
            ble.insert(1, "d")
        self.assertEqual(ble._list, ["a", "d", "b", "c"])
        self.assertEqual(ble._set, {"a", "b", "c", "d"})
        with self.assertWarns(DeprecationWarning):
            ble.insert(100, "e")
        self.assertIn("e", ble)

    def test_intersection(self):
        ble = _BlockLevelElements(["a", "b"])
        ble2 = ble.intersection({"b", "c"})
        self.assertIsInstance(ble2, set)
        self.assertEqual(ble2, {"b"})

    def test_intersection_update(self):
        ble = _BlockLevelElements(["a", "b"])
        ble.intersection_update({"b", "c"})
        self.assertEqual(ble._list, ["b"])
        self.assertEqual(ble._set, {"b"})

    def test_isdisjoint(self):
        ble = _BlockLevelElements(["a", "b"])
        self.assertFalse(ble.isdisjoint({"b", "c"}))
        self.assertTrue(ble.isdisjoint({"c", "d"}))

    def test_issubset(self):
        ble = _BlockLevelElements(["a", "b"])
        self.assertTrue(ble.issubset({"a", "b", "c"}))
        self.assertFalse(ble.issubset({"a", "c"}))

    def test_issuperset(self):
        ble = _BlockLevelElements(["a", "b"])
        self.assertTrue(ble.issuperset({"a"}))
        self.assertTrue(ble.issuperset({"a", "b"}))
        self.assertFalse(ble.issuperset({"a", "c"}))

    def test_pop(self):
        ble = _BlockLevelElements(["a", "b", "c"])
        self.assertEqual(ble.pop(), "c")
        self.assertEqual(ble._list, ["a", "b"])
        self.assertEqual(ble._set, {"a", "b"})
        self.assertEqual(ble.pop(0), "a")
        self.assertEqual(ble._list, ["b"])
        self.assertEqual(ble._set, {"b"})
        self.assertRaises(IndexError, ble.pop, 10)

    def test_remove(self):
        ble = _BlockLevelElements(["a", "b", "c"])
        ble.remove("b")
        self.assertEqual(ble._list, ["a", "c"])
        self.assertEqual(ble._set, {"a", "c"})
        self.assertRaises(ValueError, ble.remove, "d")

    def test_reverse(self):
        ble = _BlockLevelElements(["a", "b", "c"])
        with self.assertWarns(DeprecationWarning):
            ble.reverse()
        self.assertEqual(ble._list, ["c", "b", "a"])
        self.assertEqual(ble._set, {"a", "b", "c"})

    def test_sort(self):
        ble = _BlockLevelElements(["c", "a", "b"])
        with self.assertWarns(DeprecationWarning):
            ble.sort()
        self.assertEqual(ble._list, ["a", "b", "c"])
        self.assertEqual(ble._set, {"a", "b", "c"})

    def test_symmetric_difference(self):
        ble = _BlockLevelElements(["a", "b"])
        ble2 = ble.symmetric_difference({"b", "c"})
        self.assertIsInstance(ble2, set)
        self.assertEqual(ble2, {"a", "c"})

    def test_symmetric_difference_update(self):
        ble = _BlockLevelElements(["a", "b"])
        ble.symmetric_difference_update({"b", "c"})
        self.assertEqual(ble._list, ["a", "c"])
        self.assertEqual(ble._set, {"a", "c"})

    def test_union(self):
        ble = _BlockLevelElements(["a", "b"])
        ble2 = ble.union({"b", "c"})
        self.assertIsInstance(ble2, set)
        self.assertEqual(ble2, {"a", "b", "c"})

    def test_update(self):
        ble = _BlockLevelElements(["a", "b"])
        ble.update({"b", "c"})
        self.assertEqual(ble._list, ["a", "b", "c"])
        self.assertEqual(ble._set, {"a", "b", "c"})