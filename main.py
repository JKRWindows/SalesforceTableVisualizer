import sys

from Grapher import Dot
from Visualizer import SFVisualizer

write_to_file = False
branch = 'main'

def print_usage():
    print('''Usage: main.py <filename> [Options]
    Options:
        --file | -f: Whether to write the code out to a `dot` file (default: False)
        (--branch | -b) <branch_name>: What branch folder to look in (default: main)
''')

outfile = sys.argv[1].split('.')

args = sys.argv[2:]

while len(args):
    arg = args.pop(0)
    match arg:
        case '--file' | '-f':
            write_to_file = True
        case '--branch' | '-b':
            branch = args.pop(0)
        case _:
            print(f'Unknown argument "{arg}"')
            print_usage()

v = SFVisualizer(branch_name=branch)

filename, extension = '.'.join(outfile[:-1]), outfile[-1]

with Dot(filename, extension, write_to_file) as f:
    f.write(v.to_dot())
