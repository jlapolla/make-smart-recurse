lexer grammar MakefileRuleLexer;

EOL : '\n' ;
PIPE : '|' ;
COLON : ':' ;
SEMICOLON : ';' -> pushMode(RECIPE) ;
INITIAL_TAB : '\n\t' -> pushMode(RECIPE) ;
WHITESPACE : [ \t] -> skip ;
COMMENT : '#' ~'\n'* -> skip ;
LINE_CONTINATION : '\\\n' -> skip ;
IDENTIFIER : ~[ |:;#\t\n]+ ;

mode RECIPE;
RECIPE_TEXT : RECIPE_TEXT_BASE* '\n' -> popMode ;
RECIPE_TEXT_MULTI : RECIPE_TEXT_BASE* ('\n\t' | '\\\n' '\t'?) ;
fragment RECIPE_TEXT_BASE : (~[\\\n] | '\\' ~'\n') ;

