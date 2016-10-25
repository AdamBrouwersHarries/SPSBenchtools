# SYCL Parallel STL Benchmarking Tools

Tools for configuring, benchmarking and reporting performance for the SYCL Parallel STL.

_Note: This tool is primarily intended for internal (i.e. to Codeplay Software) use. Because of this, it is provided without various configuration files, and other resources which may invoke confidentiality issues. By using this software, you acknowledge that it is provided as-is, without any expectation of functionality or support._ 

## Rationale

The SYCL Parallel STL ships with a number of benchmark applications for the various algorithms provided, as well as benchmark applications for their sequential CPU equivalents. Although the benchmakrs are invaluable for providing performance information about specific instances of the PSTL, it would also be desirable to be able to compare between (say) different versions of ComputeCPP, or specific algorithm implementations, to avoid performance regressions and to help tune the Parallel STL's implementation.

## Usage

The tools in this repository are designed to be used to 1) configure and build the Parallel STL (or other library that depends on ComputeCPP), 2) Run a benchmark set from said library, and then 3) Plot performance results gathered in step 2. This repository does not include the configuration scripts required to specify what/how to run the process, but some examples are given below.

Configuration files can specify paths with one of three run-specific variables:

$CONFIGDIR = argument 1 - the path to the directory containing configuration files
$RESULTSDIR = argument 2 - the folder to store results from running the benchmark programs
$PLOTDIR = argument 3 - the folder to store generated plots

## Example Configuration files

ComputeCPP config file - used to specify a computecpp installation that the SYCL Parallel STL depends on.

  {
    "configtype":"computecpp",
    "version":"<human readable version name>",
    "path":"<path to ComputeCPP install>"
  }

Parallel STL config file - used to checkout, build and test a copy of the SYCL Parallel STL, or some other git based project that depends on ComputeCPP.

  {
    "configtype":"repo",
    "path":"<path to repository>",
    "branch":"<branch>",
    "hash":"<git hash for commit>",
    "buildscript":"<script to build parallel stl>",
    "copyscript":"<script to copy benchmark excecutables>",
    "runscript":"<script to run benchmark excecutables>",
    "ccpp_config":"<configuration file for a ComputeCPP install>"
  }

Benchmark config file - used to run a set of benchmarks from a repository (e.g. the SYCL PSTL) on a specific machine/device.

  {
    "configtype":"benchmark",
    "hostname":"<hostname of the machine the benchmark should be run on>",
    "device":"<device to run the benchmark on, e.g. intel:cpu>",
    "repo_config":"<path to a parallel stl repository configuration>"
  }

Plotting configuration file - used to aggregate performance results from a 

  {
    "configtype":"plot",
    "fname":"$PLOTDIR/<filename to save to>",
    "plotoptions": {
      "title":"<title for plot>",
      "ylabel":"<label for y axis>",
      "xlabel":"<label for x axis>",
      "xscale":"<scale for x axis, default 'linear', can be 'log'>",
      "yscale":"<scale for y axis, default 'linear', can be 'log'>",
      "transforms":
      {
        "<datapoint dimension, e.g. time>":"<optional python lambda to apply to datapoints>"
      }
    },  
    "bench_configs": [
      {
        "config":"<path to benchmark config file>", 
        "benchmark":"<name for benchmark program, the results of which to plot>",
        "name":"<human readable name for key on plot>"
      }
      <more configurations...>
    ]
  }
