"""
Lexer for Rmarkdown files that use Pandoc's markdown flavour.

Inline formating
 - italics (_text_ or *text*)
 - bold (__text__ or **text**)
 - subscript (H~2~O)
 - superscript (s^2)
 - code(`print("Hello, World!")`)
 - links ([text](link))
 - images (![alt text](path/to/image))
 - footnote (^[I am a footnote]) TODO
Block-level elements
 - heading (### Heading level 3)
 - unordered list ( - list item 1)
 - ordered list ( 1. list item )
 - code (```Code block```) TODO
 - block quote (> "First line TODO
                  Second line"
                > --- Mark Twain)
Special tokens
 - EOF
 - newline

"""

import re
from enum import Enum


class Token(Enum):
    """Enumerate possible token types."""

    EOF = 0
    ILLEGAL = 1
    NEWLINE = 2
    TEXT = 3
    ITALICS = 4
    STRONG = 5
    BLOCKQUOTE = 6
    SUPERSCRIPT = 7
    SUBSCRIPT = 8
    ULIST = 9
    OLIST = 10
    LINK = 11
    IMAGE = 12
    CODE = 13
    INLINECODE = 14
    HEADER1 = 15
    HEADER2 = 16
    HEADER3 = 17


class NewToken(object):
    """Describes a single token."""

    def __init__(self, _type: Enum,
                 _literal: str = "", _line: int = 1) -> None:
        self.type = _type
        self.literal = _literal
        self.line = _line

    def __repr__(self):
        print(f"Type: {self.type}, line: {self.line}, literal: {self.literal}")

    def __str__(self):
        return f"Type: {self.type}, line: {self.line}, literal: {self.literal}"

    def __eq__(self, o):
        """Define equality as equal type, line and literal."""
        return self.type == o.type and \
            self.line == o.line and \
            self.literal == o.literal


def stripchars(s, chars):
    """Strip `chars` from the beginning of a string s."""
    if len(s) < 1:
        return s
    i = 0
    while s[i] in chars:
        print(s[i])
        i += 1
    return s[i:]

def inlineLexer(input: str) -> str:
    """TODO: Make function to reduce repetition"""
    # Italic
    print(input)
    input = re.sub(r'([\s][*]{1})([^*]+)([*]{1}[\s])',
                   r' <span style="font-style: italic">\2</span> ',
                   input)
    # Bold
    input = re.sub(r'([\s][*]{2})(.*)([*]{2}[\s])',
                   r' <span style="font-weight: bold">\2</span> ',
                   input)
    # Superscript
    input = re.sub(r'([\^]{1})(.*)([\^]{1})',
                   r'<sup>\2</sup> ',
                   input)
    # Subscript
    input = re.sub(r'([\~]{1})(.*)([\~]{1})',
                   r'<sub>\2</sub>',
                   input)
    # Inline code
    input = re.sub(r'([\`]{1})(.*)([\`]{1})',
                   r'<code>\2</code>',
                   input)
    #Image
    input = re.sub(r'([\!][\[]{1})(.*)([\]]{1})([\(]{1})(.*)([\)]{1})',
                   r'<img src="\5" alt="\2" />',
                   input)
    #Link
    input = re.sub(r'([\[]{1})(.*)([\]]{1})([\(]{1})(.*)([\)]{1})',
                   r'<a href="\5">\2</a>',
                   input)
    return input



class Lexer(object):
    """Do lexical analysis of a string and get tokens."""

    def __init__(self, _input: str,
                 linestart: bool = True, position: int = 0,
                 readPosition: int = 0, ch: str = "",
                 startofline: bool = True) -> None:
        """Make Lexer object with string input."""
        self.input = _input
        self.position = position
        self.readPosition = readPosition
        self.line = 1
        self.startofline = startofline
        self.ch = _input[readPosition]

    def nextToken(self) -> Token:
        """Get the next token based on rules."""
        self.readChar()
        res = Token.ILLEGAL
        lit = self.ch
        line = self.line

        la1 = self.peakahead(0)
        la2 = self.peakahead(1)
        la3 = self.peakahead(2)

        if self.ch == "\n":
            res = Token.NEWLINE
            self.line += 1
        elif self.ch == "#":
            if la1 == " ":
                res = Token.HEADER1
                lit = self.get_until_chars(offset=1)
            elif la1 == "#" and la2 == " ":
                res = Token.HEADER2
                lit = self.get_until_chars(offset=2)
            elif la1 == "#" and la2 == "#" and la3 == " ":
                res = Token.HEADER3
                lit = self.get_until_chars(offset=3)
            else:
                res = Token.TEXT
                lit = self.get_until_chars(offset=-1)
        elif self.ch in "0123456789" and la1 == ".":
            res = Token.OLIST
            lit = self.get_until_chars(offset=2)
        elif (self.ch == "-" and la1 != "-") or \
             (self.ch == "*" and la1 != "*"):
            res = Token.ULIST
            lit = self.get_until_chars(offset=1)
        elif self.ch == ">":
            res = Token.BLOCKQUOTE
            lit = self.get_until_chars(offset=1)
            lit = stripchars(lit, [" ", ">"])
        elif self.ch == "\0":
            res = Token.EOF
            lit = "\0"
        elif self.ch == "`":
            mult = 1
            i = self.readPosition + 1
            while self.input[i] == "`":
                mult += 1
                i += 1
            print(f"Found {mult} `")
            res = Token.CODE
            lit = self.get_until_chars(offset=mult, chars="`", multiples=mult)
            self.readChar()
            print("Done", self.ch)
        else:
            res = Token.TEXT
            lit = self.get_until_chars(offset=-1)
        if res == Token.TEXT:
            lit = inlineLexer(lit)
        return NewToken(res, lit.strip(), line)

    def peakahead(self, pos: int = 0):
        """Get a char ahead of readPosition if there is one."""
        if (self.readPosition + pos >= len(self.input)):
            return "\0"
        else:
            return self.input[self.readPosition + pos]

    def get_until_chars(self, offset: int = 0, chars="\n", multiples=1):
        """Give me the rest of the letters until newline. TODO: Cleanup."""
        self.readPosition += offset
        self.position += offset
        res = ""
        self.readChar()
        while self.ch != "\0":
            if self.ch == chars:
                found = 1
                for i in range(multiples - 1):
                    if self.peakahead() == chars:
                        found += 1
                        self.readChar()
                    else:
                        break
                if found == multiples:
                    break
                else:
                    res += chars * found
                    self.readChar()
            else:
                res += self.ch
                self.readChar()
        self.line += res.count("\n")
        if chars == "\n":
            self.line += 1
        return res

    def readChar(self):
        """Read the next character and move positions ahead."""
        if self.readPosition >= len(self.input):
            self.ch = "\0"
        else:
            self.ch = self.input[self.readPosition]
        self.position = self.readPosition
        self.readPosition += 1
