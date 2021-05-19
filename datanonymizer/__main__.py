#!/usr/bin/env python3
import sys
import argparse
import yaml
import csv

from .parser import parse_file
from .generators import Generators


DESCRIPTION = """
Receives a CSV file from standard input and writes an anonymized version on the output.

Example:

    cat input.csv | python -m datanonymizer >output.csv

In this case, the output will be equal to the input as no conversions were applied.
"""


def gen_random_seed(size=6):
    import string
    import random

    chars = string.ascii_uppercase + string.digits
    return "".join(random.choice(chars) for _ in range(size))


def main():
    parser = argparse.ArgumentParser(
        prog="anonimizator",
        description=DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-l", "--language", default="pt-br", help="Language used by the Generator"
    )
    parser.add_argument("-di", "--delimiter_input", default=",", help="CSV delimiter")
    parser.add_argument("-do", "--delimiter_output", default=",", help="CSV delimiter")
    parser.add_argument(
        "-i",
        "--ignore_errors",
        action="store_true",
        default=False,
        help="Continue on errors",
    )
    parser.add_argument(
        "--head", default=None, type=int, help="Outputs only the first <head> lines"
    )

    gen_choices = Generators.choices()
    parser.add_argument(
        "-g",
        "--generator",
        default=gen_choices[0],
        choices=gen_choices,
        help="Generator library to be used for fake data",
    )
    parser.add_argument(
        "--seed",
        default=gen_random_seed,
        type=str,
        help="Seed for the pseudo random generator providers",
    )
    parser.add_argument(
        "--config",
        default=None,
        type=str,
        help="Configuration file",
    )
    args = parser.parse_args()

    if args.config:
        with open(args.config) as f:
            args.config = yaml.load(f, Loader=yaml.FullLoader)

    args.generic = Generators.get(
        args.generator, language=args.language, seed=args.seed
    )

    reader = csv.reader(sys.stdin, delimiter=args.delimiter_input)
    writer = csv.writer(sys.stdout, delimiter=args.delimiter_output)

    parse_file(reader, writer.writerow, args)


if __name__ == "__main__":
    main()
