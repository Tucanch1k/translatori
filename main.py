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

    except (LexerError, ParserError) as e:
        # Сообщение уже содержит тип и позицию ошибки
        print(e)

    except Exception as e:
        print("Внутренняя ошибка:", e)


if __name__ == "__main__":
    main()
