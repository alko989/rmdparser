from rmdparser.lexer import Lexer, NewToken, Token

def test_bold():
    input = "This is just text, while **this here** is bold text"
    expected = [
        NewToken(Token.TEXT, "This is just text, while "
                 '<span style="font-weight: bold">this here</span> is bold text', 1)
    ]

    lex = Lexer(input)

    for i, ex in enumerate(expected):
        tok = lex.nextToken()
        print(f"is {tok.type} expected: {ex.type}")
        assert tok.type == ex.type
        assert tok.literal == ex.literal
        assert tok.line == ex.line

def test_italic():
    input = "This is just text, while **this here** is bold text, while " \
        "*this here* is italics"
    expected = [
        NewToken(Token.TEXT,
                 'This is just text, while <span style="font-weight: bold">'
                 'this here</span> is bold text,'
                 ' while <span style="font-style: italic">this here</span> '
                 "is italics", 1)
    ]

    lex = Lexer(input)

    for i, ex in enumerate(expected):
        tok = lex.nextToken()
        print(f"is {tok.type} expected: {ex.type}")
        assert tok.type == ex.type
        assert tok.literal == ex.literal
        assert tok.line == ex.line


def test_italic_short_long():
    input = "This is just text, while **t** is bold text, while " \
        "*this long string here* is italics"
    expected = [
        NewToken(Token.TEXT,
                 'This is just text, while <span style="font-weight: bold">'
                 't</span> is bold text,'
                 ' while <span style="font-style: italic">this long string here</span> '
                 "is italics", 1)
    ]

    lex = Lexer(input)

    for i, ex in enumerate(expected):
        tok = lex.nextToken()
        print(f"is {tok.type} expected: {ex.type}")
        assert tok.type == ex.type
        assert tok.literal == ex.literal
        assert tok.line == ex.line


def test_supsub():
    input = "This is just text, while **this here** is bold text, while " \
        "*this here* is italics, H~2~O, E = mc^2^"
    expected = [
        NewToken(Token.TEXT,
                 'This is just text, while <span style="font-weight: bold">'
                 'this here</span> is bold text,'
                 ' while <span style="font-style: italic">this here</span> '
                 "is italics, H<sub>2</sub>O, E = mc<sup>2</sup>", 1)
    ]

    lex = Lexer(input)

    for i, ex in enumerate(expected):
        tok = lex.nextToken()
        print(f"is {tok.type} expected: {ex.type}")
        assert tok.type == ex.type
        assert tok.literal == ex.literal
        assert tok.line == ex.line


def test_inlinecode():
    input = "Here comes some code in R: `This is some code`"
    expected = [
        NewToken(Token.TEXT,
                 'Here comes some code in R: <code>This is some code</code>', 1)
    ]

    lex = Lexer(input)

    for i, ex in enumerate(expected):
        tok = lex.nextToken()
        print(f"is {tok.type} expected: {ex.type}")
        assert tok.type == ex.type
        assert tok.literal == ex.literal
        assert tok.line == ex.line


def test_link_img():
    input = "You can find it [here](https://example.com/), ![alt text](test.png)"
    expected = [
        NewToken(Token.TEXT,
                 'You can find it <a href="https://example.com/">here</a>, '
                 '<img src="test.png" alt="alt text" />', 1)
    ]

    lex = Lexer(input)

    for i, ex in enumerate(expected):
        tok = lex.nextToken()
        print(f"is {tok.type} expected: {ex.type}")
        assert tok.type == ex.type
        assert tok.literal == ex.literal
        assert tok.line == ex.line
