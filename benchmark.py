#!/usr/bin/python
import json
import sys
import os
from lib.configuration import *
from lib.repo_builder import *
from lib.bench_runner import *

def main(configfile, icfg, other_args=[]):
  config = parse_config(configfile, icfg)
  print config
  config.run()

# Usage: python benchmark.py <configdir> <resultsdir> <configfile> 
if __name__ == '__main__':
  if len(sys.argv) < 4:
    print "Error: expected more arguments!"
    print "Usage:"
    print "\tpython benchmark.py <configdir> <resultsdir> <plotsdir> <configfile>"
  else:
    cfdir = sys.argv[1]
    rsdir = sys.argv[2]
    pdir = sys.argv[3] 
    configfile = sys.argv[4] 
    icfg = None
    if pdir == "--noplot":
      print "running without plotting"
      icfg = InstanceConfig(cfdir, rsdir, "None")
    else:
      print "running with plotting"
      from lib.plot_runner import *
      icfg = InstanceConfig(cfdir, rsdir, pdir)
    main(configfile, icfg)