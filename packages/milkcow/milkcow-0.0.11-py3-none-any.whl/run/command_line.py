#!/usr/bin/python

import sys
import os
import select
from getopt import getopt, GetoptError
from typing import Optional

from milkcow import milkcat


def main():
    in_file = None
    out_file = None
    skip_confirm = False
    json_out = False
    try:
        opts, args = getopt(sys.argv[1:],
                            'hyji:o:',
                            longopts=[
                                'help',
                                'yes',
                                'to-json',
                                'in=',
                                'out=',
                                ]
                            )
        if len(args) == 1:
            in_file = args[0]

        elif len(args) == 2:
            in_file = args[0]
            out_file = args[1]

        elif len(args) != 0:
            print(args)
            print('unknown', args[2])
            sys.exit(1)

    except GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('we all need help sometimes')
            sys.exit()
        elif opt in ("-y", "--yes"):
            skip_confirm = True
        elif opt in ("-j", "--to-json"):
            json_out = True

        elif opt in ("-i", "--in"):
            in_file = arg
        elif opt in ("-o", "--out"):
            out_file = arg

    if in_file is not None:
        pylist = from_filein(in_file)
    else:
        pylist = from_stdin()
    if pylist is not None:
        read_out(pylist, out_file, json_out, skip_confirm)


def read_out(pylist: list, out_file, json_out, skip_confirm):
    if json_out is True:
        data = milkcat.to_json(pylist)
    else:
        data = milkcat.dump(pylist)

    if out_file is None:
        sys.stdout.write(data)
        return

    if skip_confirm is False:
        if os.path.isfile(out_file):
            pass
    to_fileout(data, out_file)


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


def to_stdout(json_list):
    print(json_list)


if __name__ == "__main__":
    main()
