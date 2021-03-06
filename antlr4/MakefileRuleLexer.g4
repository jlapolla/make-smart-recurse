lexer grammar MakefileRuleLexer;
options { superClass=autorecurse.lib.antlr4.custom.CustomLexer; }

EOL : '\n';
PIPE : '|' ;
COLON : ':' ;
SEMICOLON : ';' -> pushMode(RECIPE), skip ;
INITIAL_TAB : '\n\t' -> pushMode(RECIPE), skip ;
WHITESPACE : [ \t] -> skip ;
COMMENT : '#' ~'\n'* -> skip ;
LINE_CONTINATION : '\\\n' -> skip ;
IDENTIFIER : (~[ \\|:;#\t\n] | '\\' ~'\n')+ ;

mode RECIPE;
RECIPE_LINE_WITH_TERMINATION : RECIPE_TEXT_BASE* '\n' -> type(RECIPE_LINE), popMode ;
RECIPE_LINE : RECIPE_TEXT_BASE* ('\n\t' | '\\\n' '\t'?) ;
fragment RECIPE_TEXT_BASE : (~[\\\n] | '\\' ~'\n') ;

