import unittest

from skeletonize.parser import SkeletonParser
from skeletonize.skeleton import Skeleton, Blank, Given


class ParserTest(unittest.TestCase):
    def test_just_skeleton(self):
        self.assertEqual(
            SkeletonParser().parse("<<<hi hi hi>>>"), Skeleton([Blank("hi hi hi")])
        )
        self.assertEqual(
            SkeletonParser().parse("<<<can contain >> character>>>"),
            Skeleton([Blank("can contain >> character")]),
        )
        # can be empty
        self.assertEqual(SkeletonParser().parse("<<<>>>"), Skeleton([Blank("")]))
        self.assertEqual(
            SkeletonParser().parse("<<<multi\nline>>>"),
            Skeleton([Blank("multi\nline")]),
        )
        self.assertEqual(
            SkeletonParser(end="}}}").parse("<<<customizable}}}"),
            Skeleton([Blank("customizable")]),
        )

    def test_no_skeleton(self):
        self.assertEqual(
            SkeletonParser().parse("hi hi hi"), Skeleton([Given("hi hi hi")])
        )
        self.assertEqual(
            SkeletonParser().parse("new\nline"), Skeleton([Given("new\nline")])
        )
        self.assertEqual(
            SkeletonParser().parse("can have << these >> characters"),
            Skeleton([Given("can have << these >> characters")]),
        )

    def test_blank_surrounded_by_given(self):
        self.assertEqual(
            SkeletonParser().parse("hi <<<hi>>> hi"),
            Skeleton([Given("hi "), Blank("hi"), Given(" hi")]),
        )
        self.assertEqual(
            SkeletonParser().parse("hi <<<hi>>>"),
            Skeleton([Given("hi "), Blank("hi")]),
        )
        self.assertEqual(
            SkeletonParser().parse("hi <<<hi>>>\n"),
            Skeleton([Given("hi "), Blank("hi"), Given("\n")]),
        )
        self.assertEqual(
            SkeletonParser().parse("hi <<<hi>>> "),
            Skeleton([Given("hi "), Blank("hi"), Given(" ")]),
        )

    def test_multiple_blanks(self):
        self.assertEqual(
            SkeletonParser().parse("<<<hi>>> * <<<bye>>>"),
            Skeleton([Blank("hi"), Given(" * "), Blank("bye")]),
        )
        self.assertEqual(
            SkeletonParser().parse("<<<adjacent>>><<<blanks>>>"),
            Skeleton([Blank("adjacent"), Blank("blanks")]),
        )
