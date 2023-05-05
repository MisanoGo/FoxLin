#!/usr/bin/python3
import argparse
from handlers.handler import system_handler


def main():
    parser = argparse.ArgumentParser(
        prog='main.py',
        description="a client for running foxlin tools.",
        usage="""
python main.py -run [pytest|make_docs]
    or
./main.py -run [pytest|docs]
        """
    )
    parser.add_argument('-run', type=str)
    args = parser.parse_args()

    if args.run == "pytest":
        system_handler.check_command_handlers()
    elif args.run == "docs":
        system_handler.make_docs()
    else:
        system_handler.check_command_handlers()


if __name__ == "__main__":
    main()
