#!/usr/bin/python
import json
import sys
import os
from lib.configuration import *
from lib.repo_builder import *
from lib.bench_runner import *

# Usage: python benchmark.py <configdir> <resultsdir> <configfile> 

# This is the top level program for configuring, running, and plotting results
# for the SYCL parallel STL, or other products that use ComputeCPP.

# At the highest level, it is run with a configuration file, along with two 
# arguments that specify when results should be written, and where further
# configuration files (which the original file may depend on) can be found.

# On platforms without numpy/pandas support (e.g. minimal headless servers),
# the tool can be run with the "--noplot" option, which ensures that 
# the numpy/pandas libraries are not included/imported. 

# The exact behaviour of the tool depends on the kind and content of the 
# configuration files used.

def main(configfile, icfg, other_args=[]):
  config = parse_config(configfile, icfg)
  print config
  config.run()

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