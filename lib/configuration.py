import json
from pushd import *
import os
# get a key, or else another value, from a dictionary
# if other is a function/callable, call it - as it might be error handling, 
# or giving more information to the user
def getelse(d, key, other):
  try:
    return d[key]
  except KeyError, k:
    if(callable(other)):
      return other((d, key, k))
    else:
      return other    

# wrapper function to build a callable function for getelse, that provides
# a more detailed error message than a raw exception, yet still throws 
# a KeyError exception 
def require_key(error_message):
  def throw(tpl):
    d = tpl[0]
    key = tpl[1]
    kerr = tpl[2]
    print error_message
    print "Key " + key + " required, failing."
    raise kerr
  return throw

# given a dictionary entry, and a type to, either cast from a dictionary into 
# that type, or if a string, parse the config file at that path and convert
# into the type specified
def parse_or_inline(entry, ty, icfg):
  if isinstance(entry, dict):
    return ty.fromdict(entry, icfg)
  elif isinstance(entry, str) or isinstance(entry, unicode):
    c = parse_config(icfg.cfd_replace(entry), icfg)
    if not isinstance(c, ty):
      print "Error - config file parses into an unexpected type!"
      print "Got type: " + str(type(c)) + ", expected " + str(ty)
      exit(1)
    else:
      return c
  else:
    print "Error, cannot load a config from an entry of type " + str(type(entry))
    print "Expected a dictionary convertible to a type " + str(ty) + " or a path to a config"
    exit(1)

# A configuration for a particular instance call of the program,
class InstanceConfig:
  def __init__(self, configdir, resultsdir, plotdir):
    self.configdir = configdir
    self.resultsdir = resultsdir
    self.plotdir = plotdir

  def cfd_replace(self, fname):
    return fname.replace("$CONFIGDIR", self.configdir)

  def rsd_replace(self, fname):
    return fname.replace("$RESULTSDIR", self.resultsdir)

  def pld_replace(self, fname):
    return fname.replace("$PLOTDIR", self.plotdir)

# Base class for configurations which are in some way "runnable"
class RunnableConfig:
  # check that a runnable config has been set up properly, and can therefore
  # be run
  def check(self, extrargs):
    print "Error: this function (check) must be overloaded to be used, failing."
    exit(2)

  # run a runnable config - e.g. build the parallel stl, or execute
  # a benchmark configuration
  def run(self, extrargs):
    print "Error: this function (run) must be overloaded to be used, failing."
    exit(2)

  # check to see if the given configuration has already been run, and if so, 
  # just use that.
  def hasrun(self, extrargs):
    print "Error: this function (hasrun) must be overloaded to be used, failing."
    exit(2)

# A ComputeCPP configuration
class ComputeCppConfig(RunnableConfig):
  def __init__(self, version, path):
    self.version = version
    self.path = path 

  @classmethod
  def fromdict(cls, jsondict, icfg):
    version = jsondict["version"]
    path = icfg.cfd_replace(jsondict["path"])
    return cls(version, path)

  def check(self):
    if not os.path.exits(self.path):
      print "ComputeCPP directory doesn't exist"
      print "Path: " + self.path
      exit(1)

# A repository configuration, for something depending on ComputeCPP (e.g. PSTL)
class RepoConfig(RunnableConfig):
  def __init__(self, path, branch, git_hash, build_script, copy_script, 
    run_script, ccpp_config):
    self.path = path
    self.branch = branch
    self.git_hash = git_hash
    self.build_script = build_script
    self.copy_script = copy_script
    self.run_script = run_script
    self.ccpp_config = ccpp_config

  @classmethod
  def fromdict(cls, jsondict, icfg):
    path = getelse(jsondict, "path", "SyclParallelSTL")
    branch = getelse(jsondict, "branch", "master")
    git_hash = getelse(jsondict, "hash", None)

    build_script_error = require_key(("A build script must be specified in order"
                                      "to configure & build the repository."))
    build_script = icfg.cfd_replace(
      getelse(jsondict, "buildscript", build_script_error))

    copy_script_error = require_key(("A copy script must be specified in order"
                                     "to copy artefacts from the repository."))
    copy_script = icfg.cfd_replace(
      getelse(jsondict, "copyscript", copy_script_error))

    run_script_error = require_key(("A run script must be specified in order"
                                     "to run artefacts and get results."))
    run_script = icfg.cfd_replace(
      getelse(jsondict, "runscript", run_script_error))

    ccpp_config_error = require_key(("The repository must be configured "
                                     "with a specific ComputeCPP "
                                     "configuration."))
    ccpp_config = parse_or_inline(getelse(jsondict, 
      "ccpp_config", ccpp_config_error), ComputeCppConfig, icfg)
    return cls(path, branch, git_hash, 
      build_script, copy_script, run_script, ccpp_config)

# A benchmark configuration
class BenchConfiguration(RunnableConfig):
  def __init__(self, hostname, device, repo_config, icfg):
    self.hostname = hostname
    self.device = device
    self.repo_config = repo_config
    self.icfg = icfg 
    # setup a results directory based on various configuration patterns
    self.results_folder = self.icfg.resultsdir + "/" + \
      self.hostname + "/" + \
      self.device + "/" + \
      self.repo_config.ccpp_config.version + "/" + \
      os.path.basename(self.repo_config.path) + "/" + \
      self.repo_config.branch + "/" + \
      self.repo_config.git_hash + "/" 
    self.results_folder = self.results_folder.replace(" ","_")

  @classmethod
  def fromdict(cls, jsondict, icfg):
    hostname = jsondict["hostname"]
    device = jsondict["device"]
    repo_config_error = require_key(("A benchmark must be configured "
                                     "with a specific repository "
                                     "configuration."))
    repo_config = parse_or_inline(getelse(jsondict, 
      "repo_config", repo_config_error), RepoConfig, icfg)
    return cls(hostname, device, repo_config, icfg)

# A plot configuration
class PlotConfiguration(RunnableConfig): 
  def __init__(self, bench_configs, fname, options):
    self.bench_configs = bench_configs
    self.fname = fname
    self.options = options


  @classmethod
  def fromdict(cls, jsondict, icfg):
    configlist_error = require_key(("A plot configuration must include "
                                    "a list of benchmark configurations")) 
    def bcparse(subdict):
      cf_err = require_key(("Benchmark configuration must specify a file/json "
                           "configuration for the benchmark to run."))
      bm_err = require_key(("Benchmark configuration must specify a specific "
                           "benchmark to plot the result of."))
      nm_err = require_key(("Benchmark configuration must specify a name "
                            "to refer to the line in the plot."))
      cf = parse_or_inline(getelse(subdict, "config", cf_err), 
        BenchConfiguration, icfg)
      bm = getelse(subdict,"benchmark", bm_err)
      nm = getelse(subdict,"name", nm_err)
      return (cf, bm, nm)


    bench_configs = [bcparse(cf) for cf in 
      getelse(jsondict, "bench_configs", configlist_error)]

    fname_error = require_key(("A plot configuration must include a filename "
                             "to write to. "))
    fname = icfg.pld_replace(getelse(jsondict, "fname", fname_error))

    options_error = require_key(("A plot configuration should specify a "
                                     "set of plotoptions to configure the "
                                     "title, axes and transforms of the plot."))
    options = getelse(jsondict, "plotoptions", options_error)
    
    return cls(bench_configs, fname, options)

# parse_config :: String -> 
#   Union[ComputeCppConfig, RepoConfig, BenchConfiguration, PlotConfiguration]
def parse_config(jsonf, icfg):
  # Load the config file, from json.
  try:
    with open(jsonf) as jf:
      jd = json.load(jf)
      return {
        "computecpp" : ComputeCppConfig,
        "repo" : RepoConfig,
        "benchmark" : BenchConfiguration,
        "plot" : PlotConfiguration
      }[jd["configtype"]].fromdict(jd, icfg)
  except Exception, e:
    raise e