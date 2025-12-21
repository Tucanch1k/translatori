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
    def __init__(self, token_type, value=None, pos=None):
        self.type = token_type
        self.value = value
        self.pos = pos

    def __repr__(self):
        return "Token({}, {}, pos={}).format(self.type, self.value, self.pos)"


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

    # num -> [-]digit+
    def number(self):
        start_pos = self.pos
        sign = 1

        if self.current_char == '-':
            sign = -1
            self.advance()
            if self.current_char is None or not self.current_char.isdigit():
                raise LexerError("Лексическая ошибка в позиции {}: '-' не является числом".format(start_pos))

        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        return sign * int(result), start_pos

    def identifier(self):
        start_pos = self.pos
        result = ""
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        return result, start_pos

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit() or self.current_char == '-':
                value, pos = self.number()
                return Token(TokenType.NUM, value, pos)

            if self.current_char.isalpha():
                ident, pos = self.identifier()
                if ident == "pow":
                    return Token(TokenType.POW, ident, pos)
                else:
                    raise LexerError("Лексическая ошибка в позиции {}: недопустимый символ '{}'".format(pos, ident))

            if self.current_char == '+':
                pos = self.pos
                self.advance()
                return Token(TokenType.PLUS, '+', pos)

            if self.current_char == '*':
                pos = self.pos
                self.advance()
                return Token(TokenType.MULT, '*', pos)

            if self.current_char == '(':
                pos = self.pos
                self.advance()
                return Token(TokenType.LPAREN, '(', pos)

            if self.current_char == ')':
                pos = self.pos
                self.advance()
                return Token(TokenType.RPAREN, ')', pos)

            if self.current_char == ',':
                pos = self.pos
                self.advance()
                return Token(TokenType.COMMA, ',', pos)

            raise LexerError("Лексическая ошибка в позиции {}: недопустимый символ '{}'".format(self.pos, self.current_char))

        return Token(TokenType.EOF, None, self.pos)
