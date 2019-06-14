#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import readline
from configparser import ConfigParser
from itertools import count
from json import load
from random import choice


class PyShell:
    def __init__(self):
        with open('files/banner.json') as banner:
            print(choice(load(banner)))

        self._user_globals = ConfigParser()
        self._user_globals.read('files/user_globals.ini')
        if not self._user_globals.has_section('USER_GLOBALS'):
            self._user_globals.add_section('USER_GLOBALS')

        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.completer)

        self.main_loop()

    @property
    def user_globals(self):
        return dict(self._user_globals['USER_GLOBALS'])

    @user_globals.setter
    def user_globals(self, l):
        pass

    @staticmethod
    def completer(text, state):
        options = [i for i in dir(__builtins__) if i.startswith(text)]
        if state < len(options):
            return options[state]
        else:
            return None

    def main_loop(self):
        for i in count():
            try:
                user_input = input('\033[32m\nIn [{}]: \033[m'.format(i))
                self.exec_user_input(user_input)
            except (EOFError, KeyboardInterrupt):
                print()
                break
            except Exception as e:
                print('\033[33m{}: {}\033[m'.format(e.__class__.__name__, e))

    def exec_user_input(self, user_input):
        try:
            retval = eval(user_input, self.user_globals)
            if retval:
                print('\033[34mOut [{}]:\033[m {}'.format(i, retval))
        except SyntaxError:
            exec(user_input, self.user_globals)
            if '=' in user_input:
                for key, value in self.user_globals.items():
                    if key[0] != '_' and isinstance(value, (list, dict, str, int, float, bool)):
                        self._user_globals.set('USER_GLOBALS', key, str(value))

                with open('files/user_globals.ini', 'w') as f:
                    self._user_globals.write(f)


if __name__ == '__main__':
    PyShell()
