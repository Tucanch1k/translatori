import unittest

from my_scanner import Scanner, LexerError
from my_parser import Parser, ParserError


def evaluate(expr):
    """
    Выполняет полный цикл трансляции:
    строка -> токены -> синтаксический разбор -> вычисление
    """
    print("\n----------------------------------")
    print("Входное выражение: {}".format(expr))

    scanner = Scanner(expr)
    parser = Parser(scanner)
    result = parser.parse()

    print("Результат: {}".format(result))
    return result


def evaluate_with_error(expr, error_type):
    """
    Проверяет, что при обработке выражения возникает ожидаемая ошибка
    """
    print("\n----------------------------------")
    print("Входное выражение: {}".format(expr))
    print("Ожидаемая ошибка: {}".format(error_type.__name__))

    with unittest.TestCase().assertRaises(error_type):
        scanner = Scanner(expr)
        parser = Parser(scanner)
        parser.parse()

    print("Ошибка корректно обнаружена")


class TestCorrectExpressions(unittest.TestCase):
    """Корректные выражения"""

    def test_single_number(self):
        self.assertEqual(evaluate("5"), 5)

    def test_simple_addition(self):
        self.assertEqual(evaluate("2+3"), 5)

    def test_simple_multiplication(self):
        self.assertEqual(evaluate("2*3"), 6)

    def test_operator_priority(self):
        self.assertEqual(evaluate("2+3*4"), 14)

    def test_parentheses(self):
        self.assertEqual(evaluate("(2+3)*4"), 20)

    def test_simple_pow(self):
        self.assertEqual(evaluate("pow(2,3)"), 8)

    def test_nested_pow(self):
        self.assertEqual(evaluate("pow(2,pow(3,2))"), 512)

    def test_complex_expression(self):
        self.assertEqual(
            evaluate("2 + pow(2,3) * (1 + 1)"),
            18
        )


class TestLexerErrors(unittest.TestCase):
    """Лексические ошибки"""

    def test_unknown_symbol(self):
        evaluate_with_error("2 & 3", LexerError)

    def test_unknown_identifier(self):
        evaluate_with_error("foo(2,3)", LexerError)

    def test_invalid_character(self):
        evaluate_with_error("@", LexerError)

    def test_mixed_invalid(self):
        evaluate_with_error("2 + #", LexerError)


class TestParserErrors(unittest.TestCase):
    """Синтаксические ошибки"""

    def test_missing_right_parenthesis(self):
        evaluate_with_error("(2+3", ParserError)

    def test_extra_right_parenthesis(self):
        evaluate_with_error("2+3)", ParserError)

    def test_missing_operand(self):
        evaluate_with_error("2+", ParserError)

    def test_double_operator(self):
        evaluate_with_error("2++3", ParserError)

    def test_missing_comma_in_pow(self):
        evaluate_with_error("pow(2 3)", ParserError)

    def test_missing_second_argument_pow(self):
        evaluate_with_error("pow(2,)", ParserError)

    def test_missing_first_argument_pow(self):
        evaluate_with_error("pow(,3)", ParserError)

    def test_empty_pow(self):
        evaluate_with_error("pow()", ParserError)


class TestEdgeCases(unittest.TestCase):
    """Граничные случаи"""

    def test_whitespace(self):
        self.assertEqual(evaluate("   2   +   3   "), 5)

    def test_large_numbers(self):
        self.assertEqual(evaluate("pow(10,2)"), 100)

    def test_nested_parentheses(self):
        self.assertEqual(evaluate("((2))"), 2)

    def test_only_parentheses(self):
        evaluate_with_error("()", ParserError)

    def test_empty_input(self):
        evaluate_with_error("", ParserError)


if __name__ == "__main__":
    unittest.main(exit=False)
