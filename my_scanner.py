# scanner.py
# Лексический анализатор (сканер)

import sys
from enum import Enum


class TokenType(Enum):
    NUM = 1
    PLUS = 2
    MULT = 3
    LPAREN = 4 
    RPAREN = 5
    COMMA = 6
    POW = 7
    EOF = 8


class Token:
    def __init__(self, token_type, value=None):
        self.type = token_type
        self.value = value

    def __repr__(self):
        return "Token({}, {})".format(self.type, self.value)


class LexerError(Exception):
    pass


class Scanner:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def identifier(self):
        result = ""
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        return result

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(TokenType.NUM, self.number())

            if self.current_char.isalpha():
                ident = self.identifier()
                if ident == "pow":
                    return Token(TokenType.POW)
                else:
                    raise LexerError("Неизвестный идентификатор: {}".format(ident))

            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS)

            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MULT)

            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN)

            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN)

            if self.current_char == ',':
                self.advance()
                return Token(TokenType.COMMA)

            raise LexerError("Недопустимый символ: {}".format(self.current_char))

        return Token(TokenType.EOF)
