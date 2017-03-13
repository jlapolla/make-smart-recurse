from autorecurse.app.lib.makefile import *
from autorecurse.app.antlr.grammar import *
from antlr4 import *
from antlr4.error.Errors import ParseCancellationException
import unittest


class TestMakefileTarget(unittest.TestCase):

    def test_basic_operation(self):
        string = """\\backslash\\target\\:: source\\ |\t\\back\tslash\\ 
\t  Hurray:|;#\t it works\\quite\\well\\
  And this is still recipe text \\
\tAnd this tab is removed # Not a comment!
# Interspersed comment

\t  More recipe (trailing spaces)  
next/target : next\\ source\\
another-source\\
\t and-another-source;|:recipes!!;; # Oh\tboy!
\t :#I can't wait...
# Still in the recipe
\t ...until this recipe is over!
# New line with lone tab
\t
a b c: d | e"""

        input_ = InputStream(string)
        lexer = MakefileRuleLexer(input_)
        token_stream = CommonTokenStream(lexer)
        parser = MakefileRuleParser(token_stream)

        ctx = parser.makefileRule()
        self.assertIsNone(ctx.exception)
        target = MakefileTarget.make_from_parse_context(ctx, 0)
        self.assertEqual(target.path, '\\backslash\\target\\:')
        it = target.prerequisites
        it.move_to_next()
        self.assertEqual(it.current_item, 'source\\ ')
        it.move_to_next()
        self.assertIs(it.is_at_end, True)
        it = target.order_only_prerequisites
        it.move_to_next()
        self.assertEqual(it.current_item, '\\back')
        it.move_to_next()
        self.assertEqual(it.current_item, 'slash\\ ')
        it.move_to_next()
        self.assertIs(it.is_at_end, True)

        ctx = parser.makefileRule()
        self.assertIsNone(ctx.exception)
        target = MakefileTarget.make_from_parse_context(ctx, 0)
        self.assertEqual(target.path, 'next/target')
        it = target.prerequisites
        it.move_to_next()
        self.assertEqual(it.current_item, 'next\\ source')
        it.move_to_next()
        self.assertEqual(it.current_item, 'another-source')
        it.move_to_next()
        self.assertEqual(it.current_item, 'and-another-source')
        it.move_to_next()
        self.assertIs(it.is_at_end, True)
        it = target.order_only_prerequisites
        it.move_to_next()
        self.assertIs(it.is_at_end, True)

        ctx = parser.makefileRule()
        self.assertIsNone(ctx.exception)
        target = MakefileTarget.make_from_parse_context(ctx, 0)
        self.assertEqual(target.path, 'a')
        it = target.prerequisites
        it.move_to_next()
        self.assertEqual(it.current_item, 'd')
        it.move_to_next()
        self.assertIs(it.is_at_end, True)
        it = target.order_only_prerequisites
        it.move_to_next()
        self.assertEqual(it.current_item, 'e')
        it.move_to_next()
        self.assertIs(it.is_at_end, True)
        target = MakefileTarget.make_from_parse_context(ctx, 1)
        self.assertEqual(target.path, 'b')
        it = target.prerequisites
        it.move_to_next()
        self.assertEqual(it.current_item, 'd')
        it.move_to_next()
        self.assertIs(it.is_at_end, True)
        it = target.order_only_prerequisites
        it.move_to_next()
        self.assertEqual(it.current_item, 'e')
        it.move_to_next()
        self.assertIs(it.is_at_end, True)
        target = MakefileTarget.make_from_parse_context(ctx, 2)
        self.assertEqual(target.path, 'c')
        it = target.prerequisites
        it.move_to_next()
        self.assertEqual(it.current_item, 'd')
        it.move_to_next()
        self.assertIs(it.is_at_end, True)
        it = target.order_only_prerequisites
        it.move_to_next()
        self.assertEqual(it.current_item, 'e')
        it.move_to_next()
        self.assertIs(it.is_at_end, True)


class TestPriorityListDirectoryMakefileLocator(unittest.TestCase):

    def test_with_result_1(self):
        locator = PriorityListDirectoryMakefileLocator.make(['does_not_exist.py', 'gnumake.py', 'makefile.py'])
        with locator.makefile_iterator('autorecurse/app/lib') as it:
            self.assertIs(it.is_at_start, True)
            it.move_to_next()
            makefile = it.current_item
            self.assertEqual(makefile.exec_path, 'autorecurse/app/lib')
            self.assertEqual(makefile.file_path, 'gnumake.py')
            it.move_to_next()
            self.assertIs(it.is_at_end, True)

    def test_with_result_2(self):
        locator = PriorityListDirectoryMakefileLocator.make(['does_not_exist.py', 'makefile.py', 'gnumake.py'])
        with locator.makefile_iterator('autorecurse/app/lib') as it:
            self.assertIs(it.is_at_start, True)
            it.move_to_next()
            makefile = it.current_item
            self.assertEqual(makefile.exec_path, 'autorecurse/app/lib')
            self.assertEqual(makefile.file_path, 'makefile.py')
            it.move_to_next()
            self.assertIs(it.is_at_end, True)

    def test_without_result_1(self):
        locator = PriorityListDirectoryMakefileLocator.make(['does_not_exist.py'])
        with locator.makefile_iterator('autorecurse/app/lib') as it:
            self.assertIs(it.is_at_start, True)
            it.move_to_next()
            self.assertIs(it.is_at_end, True)

    def test_without_result_2(self):
        locator = PriorityListDirectoryMakefileLocator.make([])
        with locator.makefile_iterator('autorecurse/app/lib') as it:
            self.assertIs(it.is_at_start, True)
            it.move_to_next()
            self.assertIs(it.is_at_end, True)


class TestRecursiveDirectoryMakefileLocator(unittest.TestCase):

    def test_without_excluded_directories(self):
        sub_locator = PriorityListDirectoryMakefileLocator.make(['Makefile', 'bar.c', 'baz.c'])
        locator = RecursiveDirectoryMakefileLocator.make(sub_locator)
        with locator.makefile_iterator('test_sample/gnu') as it:
            self.assertIs(it.is_at_start, True)
            it.move_to_next()
            makefile = it.current_item
            self.assertEqual(makefile.exec_path, 'test_sample/gnu/project')
            self.assertEqual(makefile.file_path, 'Makefile')
            it.move_to_next()
            makefile = it.current_item
            self.assertEqual(makefile.exec_path, 'test_sample/gnu/project/src')
            self.assertEqual(makefile.file_path, 'bar.c')
            it.move_to_next()
            self.assertIs(it.is_at_end, True)

    def test_with_excluded_directories(self):
        sub_locator = PriorityListDirectoryMakefileLocator.make(['Makefile', 'bar.c', 'baz.c'])
        locator = RecursiveDirectoryMakefileLocator.make(sub_locator)
        locator.exclude_directory_name('src')
        with locator.makefile_iterator('test_sample/gnu') as it:
            self.assertIs(it.is_at_start, True)
            it.move_to_next()
            makefile = it.current_item
            self.assertEqual(makefile.exec_path, 'test_sample/gnu/project')
            self.assertEqual(makefile.file_path, 'Makefile')
            it.move_to_next()
            self.assertIs(it.is_at_end, True)


