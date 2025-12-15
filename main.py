from my_scanner import Scanner, LexerError
from my_parser import Parser, ParserError


def main():
    print("Транслятор арифметических выражений")
    print("Поддержка: +, *, pow(a,b), скобки")
    print("Пример: pow(2, pow(3, 4))")
    print("Введите выражение:")

    try:
        text = input("> ")
        scanner = Scanner(text)
        parser = Parser(scanner)
        result = parser.parse()
        print("Результат:", result)

    except LexerError as le:
        print("Лексическая ошибка:", le)

    except ParserError as pe:
        print("Синтаксическая ошибка:", pe)

    except Exception as e:
        print("Ошибка:", e)


if __name__ == "__main__":
    main()
