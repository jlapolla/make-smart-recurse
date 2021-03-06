from autorecurse.gnumake.grammar import MakefileRuleLexer
from antlr4.InputStream import InputStream
from antlr4 import Token
import unittest


class TestMakefileRuleLexer(unittest.TestCase):

    def test_basic_operation(self):
        string = """# A comment
\\backslash\\target\\:: source\\ |\t\\back\tslash\\ 
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
all:|;

\t
\t\\
and here is the recipe finally
clean:;
dist:;
\t
"""
        input_ = InputStream(string)
        lexer = MakefileRuleLexer(input_)
        #token = lexer.nextToken()
        #self.assertEqual(token.text, '# A comment')
        #self.assertEqual(token.type, MakefileRuleLexer.COMMENT)
        token = lexer.nextToken()
        self.assertEqual(token.text, '\n')
        self.assertEqual(token.type, MakefileRuleLexer.EOL)
        token = lexer.nextToken()
        self.assertEqual(token.text, '\\backslash\\target\\:')
        self.assertEqual(token.type, MakefileRuleLexer.IDENTIFIER)
        token = lexer.nextToken()
        self.assertEqual(token.text, ':')
        self.assertEqual(token.type, MakefileRuleLexer.COLON)
        token = lexer.nextToken()
        self.assertEqual(token.text, 'source\\ ')
        self.assertEqual(token.type, MakefileRuleLexer.IDENTIFIER)
        token = lexer.nextToken()
        self.assertEqual(token.text, '|')
        self.assertEqual(token.type, MakefileRuleLexer.PIPE)
        token = lexer.nextToken()
        self.assertEqual(token.text, '\\back')
        self.assertEqual(token.type, MakefileRuleLexer.IDENTIFIER)
        token = lexer.nextToken()
        self.assertEqual(token.text, 'slash\\ ')
        self.assertEqual(token.type, MakefileRuleLexer.IDENTIFIER)
        #token = lexer.nextToken()
        #self.assertEqual(token.text, '\n\t')
        #self.assertEqual(token.type, MakefileRuleLexer.INITIAL_TAB)
        token = lexer.nextToken()
        self.assertEqual(token.text, '  Hurray:|;#\t it works\\quite\\well\\\n')
        self.assertEqual(token.type, MakefileRuleLexer.RECIPE_LINE)
        token = lexer.nextToken()
        self.assertEqual(token.text, '  And this is still recipe text \\\n\t')
        self.assertEqual(token.type, MakefileRuleLexer.RECIPE_LINE)
        token = lexer.nextToken()
        self.assertEqual(token.text, 'And this tab is removed # Not a comment!\n')
        self.assertEqual(token.type, MakefileRuleLexer.RECIPE_LINE)
        #token = lexer.nextToken()
        #self.assertEqual(token.text, '# Interspersed comment')
        #self.assertEqual(token.type, MakefileRuleLexer.COMMENT)
        token = lexer.nextToken()
        self.assertEqual(token.text, '\n')
        self.assertEqual(token.type, MakefileRuleLexer.EOL)
        #token = lexer.nextToken()
        #self.assertEqual(token.text, '\n\t')
        #self.assertEqual(token.type, MakefileRuleLexer.INITIAL_TAB)
        token = lexer.nextToken()
        self.assertEqual(token.text, '  More recipe (trailing spaces)  \n')
        self.assertEqual(token.type, MakefileRuleLexer.RECIPE_LINE)
        token = lexer.nextToken()
        self.assertEqual(token.text, 'next/target')
        self.assertEqual(token.type, MakefileRuleLexer.IDENTIFIER)
        token = lexer.nextToken()
        self.assertEqual(token.text, ':')
        self.assertEqual(token.type, MakefileRuleLexer.COLON)
        token = lexer.nextToken()
        self.assertEqual(token.text, 'next\\ source')
        self.assertEqual(token.type, MakefileRuleLexer.IDENTIFIER)
        token = lexer.nextToken()
        self.assertEqual(token.text, 'another-source')
        self.assertEqual(token.type, MakefileRuleLexer.IDENTIFIER)
        token = lexer.nextToken()
        self.assertEqual(token.text, 'and-another-source')
        self.assertEqual(token.type, MakefileRuleLexer.IDENTIFIER)
        #token = lexer.nextToken()
        #self.assertEqual(token.text, ';')
        #self.assertEqual(token.type, MakefileRuleLexer.SEMICOLON)
        token = lexer.nextToken()
        self.assertEqual(token.text, '|:recipes!!;; # Oh\tboy!\n\t')
        self.assertEqual(token.type, MakefileRuleLexer.RECIPE_LINE)
        token = lexer.nextToken()
        self.assertEqual(token.text, ' :#I can\'t wait...\n')
        self.assertEqual(token.type, MakefileRuleLexer.RECIPE_LINE)
        #token = lexer.nextToken()
        #self.assertEqual(token.text, '# Still in the recipe')
        #self.assertEqual(token.type, MakefileRuleLexer.COMMENT)
        #token = lexer.nextToken()
        #self.assertEqual(token.text, '\n\t')
        #self.assertEqual(token.type, MakefileRuleLexer.INITIAL_TAB)
        token = lexer.nextToken()
        self.assertEqual(token.text, ' ...until this recipe is over!\n')
        self.assertEqual(token.type, MakefileRuleLexer.RECIPE_LINE)
        #token = lexer.nextToken()
        #self.assertEqual(token.text, '\n\t')
        #self.assertEqual(token.type, MakefileRuleLexer.INITIAL_TAB)
        token = lexer.nextToken()
        self.assertEqual(token.text, '\n')
        self.assertEqual(token.type, MakefileRuleLexer.RECIPE_LINE)
        token = lexer.nextToken()
        self.assertEqual(token.text, 'all')
        self.assertEqual(token.type, MakefileRuleLexer.IDENTIFIER)
        token = lexer.nextToken()
        self.assertEqual(token.text, ':')
        self.assertEqual(token.type, MakefileRuleLexer.COLON)
        token = lexer.nextToken()
        self.assertEqual(token.text, '|')
        self.assertEqual(token.type, MakefileRuleLexer.PIPE)
        #token = lexer.nextToken()
        #self.assertEqual(token.text, ';')
        #self.assertEqual(token.type, MakefileRuleLexer.SEMICOLON)
        token = lexer.nextToken()
        self.assertEqual(token.text, '\n')
        self.assertEqual(token.type, MakefileRuleLexer.RECIPE_LINE)
        #token = lexer.nextToken()
        #self.assertEqual(token.text, '\n\t')
        #self.assertEqual(token.type, MakefileRuleLexer.INITIAL_TAB)
        token = lexer.nextToken()
        self.assertEqual(token.text, '\n\t')
        self.assertEqual(token.type, MakefileRuleLexer.RECIPE_LINE)
        token = lexer.nextToken()
        self.assertEqual(token.text, '\\\n')
        self.assertEqual(token.type, MakefileRuleLexer.RECIPE_LINE)
        token = lexer.nextToken()
        self.assertEqual(token.text, 'and here is the recipe finally\n')
        self.assertEqual(token.type, MakefileRuleLexer.RECIPE_LINE)
        token = lexer.nextToken()
        self.assertEqual(token.text, 'clean')
        self.assertEqual(token.type, MakefileRuleLexer.IDENTIFIER)
        token = lexer.nextToken()
        self.assertEqual(token.text, ':')
        self.assertEqual(token.type, MakefileRuleLexer.COLON)
        #token = lexer.nextToken()
        #self.assertEqual(token.text, ';')
        #self.assertEqual(token.type, MakefileRuleLexer.SEMICOLON)
        token = lexer.nextToken()
        self.assertEqual(token.text, '\n')
        self.assertEqual(token.type, MakefileRuleLexer.RECIPE_LINE)
        token = lexer.nextToken()
        self.assertEqual(token.text, 'dist')
        self.assertEqual(token.type, MakefileRuleLexer.IDENTIFIER)
        token = lexer.nextToken()
        self.assertEqual(token.text, ':')
        self.assertEqual(token.type, MakefileRuleLexer.COLON)
        #token = lexer.nextToken()
        #self.assertEqual(token.text, ';')
        #self.assertEqual(token.type, MakefileRuleLexer.SEMICOLON)
        token = lexer.nextToken()
        self.assertEqual(token.text, '\n\t')
        self.assertEqual(token.type, MakefileRuleLexer.RECIPE_LINE)
        token = lexer.nextToken()
        self.assertEqual(token.text, '\n')
        self.assertEqual(token.type, MakefileRuleLexer.RECIPE_LINE)
        token = lexer.nextToken()
        self.assertEqual(token.text, '<EOF>')
        self.assertEqual(token.type, Token.EOF)


