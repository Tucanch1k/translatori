from my_scanner import TokenType
import math


class ParserError(Exception):
    pass


class Parser:
    """
    Грамматика:

    Expr        → Term Expr'
    Expr'       → + Term Expr' | ε

    Term        → Factor Term'
    Term'       → * Factor Term' | ε

    Factor      → NUM
                | POW_FUNC
                | ( Expr )

    POW_FUNC    → pow ( Expr , Expr )
    """

    TOKEN_NAMES = {
        TokenType.NUM: "число",
        TokenType.PLUS: "+",
        TokenType.MULT: "*",
        TokenType.LPAREN: "(",
        TokenType.RPAREN: ")",
        TokenType.COMMA: ",",
        TokenType.POW: "pow",
        TokenType.EOF: "конец выражения"
    }
    

    def __init__(self, scanner):
        self.scanner = scanner
        self.current_token = self.scanner.get_next_token()

    def error(self, message):
        pos = self.current_token.pos
        raise ParserError("Синтаксическая ошибка в позиции {}: {}".format(pos, message))

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.scanner.get_next_token()
        else:
            expected = self.TOKEN_NAMES.get(token_type, str(token_type))
            found = self.TOKEN_NAMES.get(self.current_token.type, str(self.current_token.type))
            self.error("ожидалось {}, получено {}".format(expected, found))


    # Expr → Term Expr'
    def expr(self):
        result = self.term()
        return self.expr_prime(result)

    # Expr' → + Term Expr' | ε
    def expr_prime(self, inherited):
        if self.current_token.type == TokenType.PLUS:
            self.eat(TokenType.PLUS)
            term_value = self.term()
            return self.expr_prime(inherited + term_value)
        return inherited

    # Term → Factor Term'
    def term(self):
        result = self.factor()
        return self.term_prime(result)

    # Term' → * Factor Term' | ε
    def term_prime(self, inherited):
        if self.current_token.type == TokenType.MULT:
            self.eat(TokenType.MULT)
            factor_value = self.factor()
            return self.term_prime(inherited * factor_value)
        return inherited

    # Factor → NUM | POW_FUNC | ( Expr )
    def factor(self):
        token = self.current_token

        if token.type == TokenType.NUM:
            self.eat(TokenType.NUM)
            return token.value

        if token.type == TokenType.POW:
            return self.pow_func()

        if token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            value = self.expr()
            self.eat(TokenType.RPAREN)
            return value

        self.error("ожидалось {}, {} или {}".format(self.TOKEN_NAMES[TokenType.NUM], self.TOKEN_NAMES[TokenType.POW], self.TOKEN_NAMES[TokenType.LPAREN]))


    # POW_FUNC → pow ( Expr , Expr )
    def pow_func(self):
        self.eat(TokenType.POW)
        self.eat(TokenType.LPAREN)
        base = self.expr()
        self.eat(TokenType.COMMA)
        exponent = self.expr()
        self.eat(TokenType.RPAREN)

        return math.pow(base, exponent)

    def parse(self):
        result = self.expr()
        if self.current_token.type != TokenType.EOF:
            self.error("лишние символы после конца выражения")
        return result
