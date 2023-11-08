from rmdparser.lexer import NewToken, Token, Lexer


def test_Token():
    tok = NewToken(Token.HEADER2, "Hello, World!", 313)
    assert tok.type == Token.HEADER2
    assert tok.line == 313
    assert tok.literal == "Hello, World!"


def test_Header1():
    input = "This is just text\n\n# This is a heading level one"
    expected = [
        NewToken(Token.TEXT, "This is just text", 1),
        NewToken(Token.NEWLINE, "", 2),
        NewToken(Token.HEADER1, "This is a heading level one", 3)
    ]

    lex = Lexer(input)

    for i, ex in enumerate(expected):
        tok = lex.nextToken()
        print(tok.type)
        print(ex.type)
        assert tok.type == ex.type
        assert tok.literal == ex.literal
        assert tok.line == ex.line


def test_Blockquote():
    input = "> This is a blqt\n\n# This is a heading level one"
    expected = [
        NewToken(Token.BLOCKQUOTE, "This is a blqt", 1),
        NewToken(Token.NEWLINE, "", 2),
        NewToken(Token.HEADER1, "This is a heading level one", 3)
    ]

    lex = Lexer(input)

    for i, ex in enumerate(expected):
        tok = lex.nextToken()
        print(tok.type)
        print(ex.type)
        assert tok.type == ex.type
        assert tok.literal == ex.literal
        assert tok.line == ex.line


def test_FakeBlockquote():
    input = "> \n >\n>> sadsad\n# This is a heading level one"
    expected = [
        NewToken(Token.BLOCKQUOTE, "", 1),
        NewToken(Token.TEXT, ">", 2),
        NewToken(Token.BLOCKQUOTE, "sadsad", 3),
        NewToken(Token.HEADER1, "This is a heading level one", 4)
    ]

    lex = Lexer(input)

    for i, ex in enumerate(expected):
        tok = lex.nextToken()
        print(tok.type)
        print(ex.type)
        assert tok.type == ex.type
        assert tok.literal == ex.literal
        assert tok.line == ex.line


def test_MixHeaders():
    input = "This is just text\n\n# This is a heading level one\n" \
        "## This is level 2\n\n\n" \
        "This is a small text\nThis is just text## This is not 2" \
        "\nThis is text\n\n### And this is level 3"
    expected = [
        NewToken(Token.TEXT, "This is just text", 1),
        NewToken(Token.NEWLINE, "", 2),
        NewToken(Token.HEADER1, "This is a heading level one", 3),
        NewToken(Token.HEADER2, "This is level 2", 4),
        NewToken(Token.NEWLINE, "", 5),
        NewToken(Token.NEWLINE, "", 6),
        NewToken(Token.TEXT, "This is a small text", 7),
        NewToken(Token.TEXT, "This is just text## This is not 2", 8),
        NewToken(Token.TEXT, "This is text", 9),
        NewToken(Token.NEWLINE, "", 10),
        NewToken(Token.HEADER3, "And this is level 3", 11)
    ]

    lex = Lexer(input)

    for i, ex in enumerate(expected):
        tok = lex.nextToken()
        print(f"is {tok.type} expected: {ex.type}")
        assert tok.type == ex.type
        assert tok.literal == ex.literal
        assert tok.line == ex.line


def test_Newline():
    input = "\n\n\n"
    expected = [
        NewToken(Token.NEWLINE, "", 1),
        NewToken(Token.NEWLINE, "", 2),
        NewToken(Token.NEWLINE, "", 3)
    ]

    lex = Lexer(input)

    for i, ex in enumerate(expected):
        tok = lex.nextToken()
        assert tok.type == ex.type
        assert tok.literal == ex.literal
        assert tok.line == ex.line


def test_olist():
    input = "1. first\n2. second\n3. third"
    expected = [
        NewToken(Token.OLIST, "first", 1),
        NewToken(Token.OLIST, "second", 2),
        NewToken(Token.OLIST, "third", 3)
    ]

    lex = Lexer(input)
    for i, ex in enumerate(expected):
        tok = lex.nextToken()
        assert tok.type == ex.type
        assert tok.literal == ex.literal
        assert tok.line == ex.line


def test_ulist():
    input = "- first\n- second\n- third"
    expected = [
        NewToken(Token.ULIST, "first", 1),
        NewToken(Token.ULIST, "second", 2),
        NewToken(Token.ULIST, "third", 3)
    ]

    lex = Lexer(input)
    for i, ex in enumerate(expected):
        tok = lex.nextToken()
        assert tok.type == ex.type
        assert tok.literal == ex.literal
        assert tok.line == ex.line


def test_ulist2():
    input = "* first\n- second\n* third\n- fourth"
    expected = [
        NewToken(Token.ULIST, "first", 1),
        NewToken(Token.ULIST, "second", 2),
        NewToken(Token.ULIST, "third", 3),
        NewToken(Token.ULIST, "fourth", 4)
    ]

    lex = Lexer(input)
    for i, ex in enumerate(expected):
        tok = lex.nextToken()
        assert tok.type == ex.type
        assert tok.literal == ex.literal
        assert tok.line == ex.line


def test_blockcode():
    input = "```def get_stuff(arg1: int = 0, arg2: str = 'asd'):\n" \
        "    print(arg1)\n" \
        "    print(arg2)```\n# Heading 1"
    expected = [
        NewToken(Token.CODE, "def get_stuff(arg1: int = 0, "
                 "arg2: str = 'asd'):\n"
                 "    print(arg1)\n    print(arg2)", 1),
        NewToken(Token.NEWLINE, "", 3),
        NewToken(Token.HEADER1, "Heading 1", 4)
    ]

    lex = Lexer(input)
    for i, ex in enumerate(expected):
        tok = lex.nextToken()
        print(tok)
        print(ex)
        assert tok.type == ex.type
        assert tok.literal == ex.literal
        assert tok.line == ex.line


def test_blockcode5():
    input = "`````def get_stuff(arg1: int = 0, arg2: str = 'asd'):\n" \
        "    print(arg1)\n" \
        "    print(arg2)`````\n# Heading 1"
    expected = [
        NewToken(Token.CODE, "def get_stuff(arg1: int = 0, "
                 "arg2: str = 'asd'):\n"
                 "    print(arg1)\n    print(arg2)", 1),
        NewToken(Token.NEWLINE, "", 3),
        NewToken(Token.HEADER1, "Heading 1", 4)
    ]

    lex = Lexer(input)
    for i, ex in enumerate(expected):
        tok = lex.nextToken()
        print(tok)
        print(ex)
        assert tok.type == ex.type
        assert tok.literal == ex.literal
        assert tok.line == ex.line

def test_blockcode_with__inside__backticks():
    input = "```def get_stuff(arg1: int = 0, arg2: str = 'asd'):\n" \
        "    print(arg1)\n" \
        "    print(`arg2`)```\n# Heading 1"
    expected = [
        NewToken(Token.CODE, "def get_stuff(arg1: int = 0, "
                 "arg2: str = 'asd'):\n"
                 "    print(arg1)\n    print(`arg2`)", 1),
        NewToken(Token.NEWLINE, "", 3),
        NewToken(Token.HEADER1, "Heading 1", 4)
    ]
    lex = Lexer(input)
    toks = lex.parse()
    for i, ex in enumerate(expected):
        tok = toks[i]
        print(tok)
        print(ex)
        assert tok.type == ex.type
        assert tok.literal == ex.literal
        assert tok.line == ex.line
