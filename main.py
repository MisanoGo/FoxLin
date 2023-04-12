import os
import sys

from foxlin.fox import FoxLin, Schema, BASIC_BOX
from foxlin.box import CreateJsonDB, DBDump, JsonBox


BASE_DIR = os.path.realpath(os.path.dirname(__file__))


def main():
    args = sys.argv
    if args[1] == "test":
        os.system("pytest")


if __name__ == "__main__":
    main()
