from configparser import ConfigParser
from itertools import count
from json import load
from random import choice


class PyShell:
    def __init__(self):
        with open('files/banner.json') as banner:
            print(choice(load(banner)))

        self.user_globals = ConfigParser()
        self.user_globals.read('files/user_globals.ini')
        if not self.user_globals.has_section('USER_GLOBALS'):
            self.user_globals.add_section('USER_GLOBALS')

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
        globals = dict(self.user_globals['USER_GLOBALS'])

        try:
            retval = eval(user_input, globals)
            if retval:
                print(f'\033[34mOut [{i}]:\033[m {retval}')
        except SyntaxError:
            exec(user_input, globals)
            if '=' in user_input:
                for key, value in globals.items():
                    if key[0] != '_' and isinstance(value, (list, dict, str, int, float, bool)):
                        self.user_globals.set('USER_GLOBALS', key, str(value))

                with open('files/user_globals.ini', 'w') as f:
                    self.user_globals.write(f)


if __name__ == '__main__':
    PyShell()
