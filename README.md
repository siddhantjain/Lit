Lit
===

Lost in Translation(Lit) is a compiler created as a part of the course on Programming Languages and Compiler Construction.

# Language Specifications

The specifications for the language can be viewed in the file named Language Specifications.txt

# Lexer

    "src/lexicalanalyser.py"
*       The lexer has been hand-written in python
*       The re module has been extensively used for pattern matching
*       Formed regexes are available in the file data.py
*       The lexical analyser has 0 look-aheads but principal of longest match is satisfied through the order in which the regexes are tested


# Grammar

* The grammar is LL(1) compliant and the rules have been written in the grammar.txt file. The corresponding parse table has been represented in the ParseTable.xslx file. 
Note: The numbers in the parse table refer to the rule numbers as in the grammar.txt file.


       




