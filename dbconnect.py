#!/usr/bin/env python3

"""
Script for Accessing sqlite databases
"""

import sqlite3
import pathlib
import readline

# Stolen from here
# https://stackoverflow.com/a/69349450
def complete_path(text, state):
    incomplete_path = pathlib.Path(text)
    if incomplete_path.is_dir():
        completions = [p.as_posix() for p in incomplete_path.iterdir()]
    elif incomplete_path.exists():
        completions = [incomplete_path]
    else:
        exists_parts = pathlib.Path('.')
        for part in incomplete_path.parts:
            test_next_part = exists_parts / part
            if test_next_part.exists():
                exists_parts = test_next_part
        completions = []
        for p in exists_parts.iterdir():
            p_str = p.as_posix()
            if p_str.startswith(text):
                completions.append(p_str)
    return completions[state]

readline.set_completer_delims(" \t\n;")
readline.parse_and_bind("tab: complete")
readline.set_completer(complete_path)

try:
    filename = str(input("Enter Database Filename : "))
    readline.parse_and_bind('set disable-completion on')
    con = sqlite3.connect(filename)
    con.close()

except Exception as e:
    print(f"ERROR : {e}")
    input("ERROR : Cannot Connect to Database (Check Filename Spelling?)")
    exit()

command = None
while command != "exit":
    command = input("SQL://> ")
    con = sqlite3.connect(filename)
    cur = con.cursor()

    try:
        res = cur.execute(command)
        for record in res.fetchall():
            print(record)
    except Exception as e:
        print(f"Syntax Error : {e}")
    con.commit()
    con.close()
