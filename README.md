Lit
===

Lost in Translation(Lit) is a compiler created as a part of the course Programming Languages and Compiler Construction.

# Language Specifications

The specifications for the language can be viewed in the following gist:
[enter gist link here]


# First sets, Follow sets and parse table

We'll be performing LR(1) parsing for this language. The first sets, follow sets and parse table 
All of these are available in corresponding files in the gist
[again refer to gist]


# Lexer

    "lexicalanalyser.py"
*       The lexer has been hand-written in python
*       The re module has been extensively used for pattern matching
*       Formed regexes are available in the file data.py
*       The lexical analyser has 0 look-aheads but principal of longest match is satisfied through the order in which the regexes are tested
*       




