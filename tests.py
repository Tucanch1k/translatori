import unittest
from my_scanner import Scanner, LexerError
from my_parser import Parser, ParserError


def evaluate(expr):
    print("\n----------------------------------")
    print("Входное выражение: {}".format(expr))
    try:
        scanner = Scanner(expr)
        parser = Parser(scanner)
        result = parser.parse()
        print("Результат: {}".format(result))
        return result
    except (LexerError, ParserError) as e:
        print(e)
        raise


def evaluate_with_error(expr, error_type):
    print("\n----------------------------------")
    print("Входное выражение: {}".format(expr))
    print("Ожидаемая ошибка: {}".format(error_type.__name__))
    try:
        scanner = Scanner(expr)
        parser = Parser(scanner)
        parser.parse()
    except error_type as e:
        print("Ошибка корректно обнаружена: {}".format(e))
        return
    except Exception as e:
        # Любая другая ошибка
        print("Обнаружена неожиданная ошибка: {}".format(e))
        raise
    # Если ошибка не произошла
    raise AssertionError("Ожидаемая ошибка {} не произошла".format(error_type.__name__))


# ---------- Тесты ----------

class TestCorrectExpressions(unittest.TestCase):
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
        self.assertEqual(evaluate("2 + pow(2,3) * (1 + 1)"), 18)

    def test_negative_number(self):
        self.assertEqual(evaluate("-5 + 3"), -2)

    def test_negative_in_pow(self):
        self.assertEqual(evaluate("pow(-2,3)"), -8)


class TestLexerErrors(unittest.TestCase):
    def test_unknown_symbol(self):
        evaluate_with_error("2 & 3", LexerError)

    def test_unknown_identifier(self):
        evaluate_with_error("foo(2,3)", LexerError)

    def test_invalid_character(self):
        evaluate_with_error("@", LexerError)

    def test_mixed_invalid(self):
        evaluate_with_error("2 + #", LexerError)


class TestParserErrors(unittest.TestCase):
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
