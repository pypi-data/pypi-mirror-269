#!/usr/bin/python

import sys
import select
from getopt import getopt, GetoptError
from typing import Optional

from milkcow import milkcat
from milkcow import JqCow


def main():
    print('mlkcw')
    key_on = None
    in_file = None
    out_file = None
    try:
        opts, args = getopt(sys.argv[1:],
                            'hytk:i:o:',
                            longopts=[
                                'help',
                                'yes',
                                'test',
                                'save',
                                'key-on=',
                                'in=',
                                'out=',
                                ]
                            )
        if len(args) == 1:
            key_on = args[0]

        elif len(args) == 2:
            key_on = args[0]
            in_file = args[1]

        elif len(args) == 3:
            key_on = args[0]
            in_file = args[1]
            out_file = args[2]

        elif len(args) != 0:
            print(args)
            print('milkcow:Unknown-args:', args[2])
            sys.exit(1)

    except GetoptError:
        sys.exit(2)

    skip_confirm = False
    just_test = False
    for opt, arg in opts:
        if opt == '-h':
            print('we all need help sometimes')
            sys.exit()
        elif opt in ("-y", "--yes"):
            skip_confirm = True
        elif opt in ("-t", "--test"):
            skip_confirm = True
            just_test = True

        elif opt in ("-k", "--key-on"):
            key_on = arg
        elif opt in ("-i", "--in"):
            in_file = arg
        elif opt in ("-o", "--out"):
            out_file = arg

    if in_file is not None:
        pylist = from_filein(in_file)
    else:
        pylist = from_stdin()

    if pylist is not None:
        if just_test is True:
            test_output_with_input(key_on, pylist)
            sys.exit(0)

        else:
            if out_file is None:
                if skip_confirm is False:
                    print('milkcow:missing-args: out(out file)')
                    print('use -t for testing or -y to use mc.db as output')
                    sys.exit(1)

                out_file = 'mc.db'

            if key_on is None:
                print('milkcow:missing-args: key-on')
                print('just testing? use -t to test output')
                sys.exit(1)

            if skip_confirm is False:
                print('about to save to database or overwrite file at path:')
                input('Ctl-C to not do that:')

            save_with_jc(key_on, pylist, out_file)

        return

    print('no input')
    sys.exit(1)


def test_output_with_input(key_on: Optional[str], pylist: list):
    if key_on is not None:
        data = milkcat.milkcat.map_by_key(key_on, pylist)
        print(data)

    else:
        print(pylist)


def save_with_jc(key_on: str, pylist: list, out_file: str):
    jc = JqCow(key_on)
    jc.connect(out_file)
    jc.push_unkeyed(pylist)


def from_filein(path) -> list:
    if path is not None and path != '':
        try:
            with open(path, 'r') as f:
                data = f.read()
                if data is None:
                    return []

                try:
                    return milkcat.load(data)

                except Exception as e:
                    print(e)
                    sys.exit(1)

        except FileNotFoundError as e:
            print(e)
            sys.exit(1)
    print('you must provide a valid path')
    sys.exit(1)


def from_stdin() -> Optional[list]:
    if select.select([sys.stdin,], [], [], .1)[0]:
        line = sys.stdin.read()
        if line:
            try:
                data = milkcat.load(line)
                return data

            except Exception as e:
                raise e
        else:
            sys.exit(1)


def to_fileout(json_list: str, path: str):
    try:
        with open(path, 'w') as f:
            try:
                f.write(json_list)

            except Exception as e:
                raise e

    except FileNotFoundError as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
