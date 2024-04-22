from argparse import ArgumentParser
from .config import add_arguments

parser = ArgumentParser()
add_arguments(parser)


# --------- Run ---------
args = parser.parse_args()
args.func(parser)
