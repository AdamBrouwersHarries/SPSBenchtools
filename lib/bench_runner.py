from configuration import *
from repo_builder import *
import platform
import os
# for BenchConfiguration

def check(self, extrargs=[]):
  print "Checking benchmark configuration"
  if self.hostname != platform.uname()[1]:
    print "Error: hostname does not match config hostname."
    print "\tExpected: " + self.hostname
    print "\tGot: " + platform.uname()[1]
    exit(1)



def run(self, extrargs=[]):
  print "Running benchmark configuration"
  self.check(extrargs)
  # should we really be checking?
  # if not self.hasrun(extrargs=[]):

  # setup and build the repository
  self.repo_config.run(extrargs)
  
  if not os.path.exists(self.results_folder):
    os.makedirs(self.results_folder)
    
  # call the copy script, with some arguments
  rpcs = self.repo_config.copy_script
  call([rpcs, self.repo_config.path, self.results_folder] + extrargs)

  # call the script to run the benchmarks
  rprs = self.repo_config.run_script
  call([rprs, self.results_folder, self.device] + extrargs)


def hasrun(self, extrargs=[]):
  print "Has the benchmark configuration run?"
  return False

BenchConfiguration.check = check
BenchConfiguration.run = run
BenchConfiguration.hasrun = hasrun