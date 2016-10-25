#!/usr/bin/python
import json
import sys
import os
from lib.configuration import *
from lib.repo_builder import *
from lib.bench_runner import *
from lib.plot_runner import *


def main(configfile, icfg, other_args=[]):
  config = parse_config(configfile, icfg)
  config.run()

# Usage: python benchmark.py <configdir> <resultsdir> <configfile> 
if __name__ == '__main__':
  if len(sys.argv) < 4:
    print "Error: expected more arguments!"
    print "Usage:"
    print "\tpython benchmark.py <configdir> <resultsdir> <plotsdir> <configfile>"
  else:
    icfg = InstanceConfig(sys.argv[1], sys.argv[2], sys.argv[3])
    configfile = sys.argv[4]
    main(configfile, icfg)