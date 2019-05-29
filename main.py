from itertools import count
from json import dump, load, decoder
from random import choice

"""
\033[31m  =  Red
\033[32m  =  Green
\033[34m  =  Blue
\033[m    =  Remove
"""


class PyShell:
    def __init__(self):
        with open('files/names.json', 'r') as names:
            print(choice(load(names)))

        self.user_globals = self.load_user_globals()
        self.user_input()

    def user_input(self):
        for i in count():
            try:
                self.exec_user_input(i)

            except EOFError:
                print()
                break

            except Exception as e:
                print(f'\033[31m{e.__class__.__name__}: {e}\033[m')

    def exec_user_input(self, i):
        user_input = input(f'\033[32m\nIn [{i}]: \033[m')
        try:
            retval = eval(user_input, self.user_globals)
            if retval:
                print(f'\033[34mOut [{i}]:\033[m {retval}')

        except SyntaxError:
            exec(user_input, self.user_globals)
            if '=' in user_input:
                self.save_user_globals()

    def save_user_globals(self):
        user_globals = self.user_globals.copy()
        user_globals.pop('__builtins__')
        user_globals = dict(
            item for item in user_globals.items() if isinstance(item[1], (list, dict, str, int, float, bool)))
        with open('files/user_globals.json', 'w') as file:
            dump(user_globals, file, indent=2, sort_keys=True)

    @staticmethod
    def load_user_globals():
        try:
            with open('files/user_globals.json', 'r') as file:
                return load(file)
        except decoder.JSONDecodeError:
            return {}


if __name__ == '__main__':
    PyShell()
