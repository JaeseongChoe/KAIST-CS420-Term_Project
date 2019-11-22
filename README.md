# ARTIDE (Naming is Needed!)

ARTIDE is A Really Tiny Integrated Delopment Enviroment for the mini-C programming language which provide only compiler and debugger. ARTIDE written in Python. ARTIDE was originally start from a term project of compiler design course in KAIST.

## Tentative schedule
|Week|Description|
|---|---|
|week9|~~Presentation (management plan)~~|
|week10|~~Design internal data structure~~|
|week11|~~Implement lexical and syntax analyzer~~|
|week12|~~Report (internal data structure)~~, implement semantic analyzer|
|week13|Implement intermediate code generator|
|week14|Implement interpreter/debugger and code generator|
|week15|Final presentation|
|week16|Final report|

## mini-C

mini-C specification from TA.

## mini-C compiler

### Front end

The front end of the mini-C compiler consist of three different parts, namely, lexical, syntax, and semantic analyzer. The lexical and syntax analyzer implemented by using [PLY (Python Lex-Yacc)](https://github.com/dabeaz/ply) library (PLY-3.11). The PLY libary has two modules Lex and Yacc.

#### Lexical analyzer

The lexical analyzer uses Lex module of the PLY library. Token specification of mini-C can be found in [`lexical_analyzer.py`](https://github.com/JaeseongChoe/KAIST-CS420-Term_Project/tree/master/src/lexical_analyzer.py). It can covers all the tokens of ANSI C (C89/C90).

#### Syntax analyzer

The syntax anlayzer uses Yacc module of the PLY library. Context free grammer within BNF can be found in [`syntax_analyzer.py`](https://github.com/JaeseongChoe/KAIST-CS420-Term_Project/tree/master/src/syntax_analyzer.py). The parsing mechnism of generated syntax analyzer is LALR(1).

#### Semantic analyzer

### Middle end

Intermediate language generation.

### Back end

Back end of mini-C compiler in ARTIDE has only code generator.

#### Code Generator

Code generator of mini-C compiler in ARTIDE supports only x86 ISA with AT&T syntax.

## mini-C debuger

#### Syntax Handling

#### Run-time error handling

#### Interpretation

#### printf function

#### next command

#### print command

#### trace command

#### Code generation

## License

**[MIT](LICENSE)**
