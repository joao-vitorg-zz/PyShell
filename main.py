#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gzip
import readline
from itertools import count
from random import choice

from dill import dump, load


def completer(text, state):
    options = [i for i in dir(__builtins__) if i.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None


readline.parse_and_bind("tab: complete")
readline.set_completer(completer)


class PyShell(object):
    def __init__(self):
        with gzip.open('files/banner.gzip', 'rb') as banner:
            print(choice(load(banner)))

        try:
            with gzip.open('files/user_globals.gzip', 'rb') as f:
                self.user_globals = load(f)
        except FileNotFoundError:
            self.user_globals = {}

        self.main_loop()

    def main_loop(self):
        for i in count():
            try:
                user_input = input('\033[32m\nIn [%i]: \033[m' % i)
                self.exec_user_input(user_input, i)
            except (EOFError, KeyboardInterrupt):
                print()
                break
            except Exception as e:
                print('\033[33m%s: %s\033[m' % (e.__class__.__name__, e))

    def dump_user_globals(self):
        self.user_globals.pop('__builtins__')
        with gzip.open('files/user_globals.gzip', 'wb') as f:
            dump(self.user_globals, f)

    def exec_user_input(self, user_input, i):
        try:
            retval = eval(user_input, self.user_globals)
            if retval:
                print('\033[34mOut [%i]:\033[m %s' % (i, retval))
        except SyntaxError:
            exec(user_input, self.user_globals)
            if '=' in user_input:
                self.dump_user_globals()


if __name__ == '__main__':
    PyShell()
