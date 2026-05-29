from Lexer import *
from Parser import *

files = [
    "test_cases/good/input01.txt",
    "test_cases/good/input02.txt",
    "test_cases/bad/input03.txt",
    "test_cases/bad/input04.txt",
]

if __name__ == '__main__':
    for filepath in files:
        print(f"\n--- {filepath} ---")
        try:
            parser = Parser(filepath)
            parser.analize()
        except Exception as e:
            print(f"ERROR: {e}")
