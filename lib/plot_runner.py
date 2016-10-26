from configuration import *
from bench_runner import *
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
import socket
import math 

# for PlotConfiguration

def newest_subdir(path):
  directories = [path + d for d in os.listdir(path) if os.path.isdir(path+d)]
  most_recent_subdir = max(directories, key=os.path.getmtime)
  return most_recent_subdir + "/"

def parse_result_file(fname):
  print "Parsing "+fname
  dat = []
  with open(fname) as f:
    for l in f:
      if "ComputeCpp" not in l and l.rstrip() != "":
        try:
          bench,duff,size,time = l.rstrip().split(" ")
          dat.append((size, time))
        except Exception, e:
          if "terminate" in l or "what()" in l:
            print "Found error, finishing parse."
            break
          else:
            print "Failed to parse " + l
            raise e
  if dat == []:
    print "Failed to parse any data from file: " + fname
    exit(1)
  return dat

class DataSet(object):
  def __init__(self, tup):
    super(DataSet, self).__init__()
    self.config = tup[0]
    self.benchmark = tup[1]
    self.name = tup[2] 
    # find the most recent subdirectory, and then 
    # get the results folder from the config + director, 
    # and get the result file
    dfname = newest_subdir(self.config.results_folder) + self.benchmark
    # parse the data from the results file - discard the raw stuff
    raw_data = parse_result_file(dfname)
    # turn it into a dataframe
    self.data = pd.DataFrame.from_records(raw_data, columns=["size", "time"]
      ).astype(float)



# Given a filename, and extension, 
def get_unique_filename(filename):
  # split the file into name + extension
  name, ext = os.path.splitext(filename)
  # given the name of a file, find the next name_n.ext file available
  if not os.path.exists(filename):
    # if the file doesn't exist yet, just write to it...
    return filename
  # start with name_1.ext
  n = 1
  # build a subsitution string
  nname = name+"_%s."+ext
  # keep trying to substitute it with higher numbers while it exists
  while os.path.exists(nname % n):
    n = n + 1
  # return the only one that doesn't exist
  return (nname % n)



def check(self, extrargs=[]):
  print "Checking plot configuration"

def run(self, extrargs=[]):
  print "running plotrunner"
  datasets = [DataSet(c) for c in self.bench_configs] 
  for c in datasets:
    print c
  print self.fname
  print self.options
  print "Starting plotting"
  sns.set_style("darkgrid")
  plt.figure()
  for d in datasets:
    if "transforms" in self.options:
      for key, value in self.options["transforms"].iteritems():
        fn = eval(value)
        d.data[key] = d.data[key].apply(fn)
    d.data.plot(x="size", y="time", label=d.name)
  plt.legend(loc="upper left")
  plt.title(getelse(self.options, "title", "defulat title"))
  plt.yscale(getelse(self.options, "yscale", "linear"))
  plt.xscale(getelse(self.options, "yscale", "linear"))
  plt.ylabel(getelse(self.options, "ylabel", "time"))
  plt.xlabel(getelse(self.options, "xlabel", "size"))

  ofname = get_unique_filename(self.fname)
  plt.savefig(ofname, bbox_inches = "tight")


def hasrun(self, extrargs=[]):
  print "Has the plot configuration run?"

PlotConfiguration.check = check
PlotConfiguration.run = run
PlotConfiguration.hasrun = hasrun