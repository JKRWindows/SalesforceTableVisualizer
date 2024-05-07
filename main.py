import sys

from Grapher import Dot
from Visualizer import SFVisualizer

outfile = sys.argv[1].split('.')
branch = sys.argv[2] if len(sys.argv) > 2 else 'main'

v = SFVisualizer(branch_name=branch)

filename, extension = '.'.join(outfile[:-1]), outfile[-1]

with Dot(filename, extension) as f:
    f.write(v.to_dot())
