# Copyright (c) 2022 Dane Freeman.
# Distributed under the terms of the Modified BSD License.


import subprocess
import sys

from ._base import NODE, STATIC


def main():
    args = [NODE, STATIC / "stardog-graphql-language-server/dist/cli.js", *sys.argv[1:]]
    str_args = [*map(str, args)]
    proc = subprocess.Popen(str_args, stdin=sys.stdin, stdout=sys.stdout)
    return proc.wait()


if __name__ == "__main__":
    main()
