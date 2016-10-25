from configuration import *
from pushd import *
import git
import os
import os.path
from subprocess import call

# new methods for RepoConfig
def check(self, extrargs=[]):
  print "Checking repository is correct"
  if not os.path.exists(self.path):
    print "Error: cannot find repository, failing!"
    exit(1)

def run(self, extrargs=[]):
  print "Running repository"
  # Check that the repository exists
  self.check()
  # Change directory, into the repo 
  with pushd(self.path) as ctx:
    # Run git commands
    repo = git.cmd.Git(ctx.cwd)
    repo.stash()
    repo.checkout(self.branch)
    # repo.pull()
    if self.git_hash:
      repo.checkout(self.git_hash)
    # Copy the build script in
    print "COPYING BUILD SCRIPT"
    rpbs = self.path + "/" + os.path.basename(self.build_script)
    with tempcopy(self.build_script, rpbs) as tc:
      # Build the repository
      print "BUILDING"
      call(["chmod", "a+x", tc.dst])
      print "Calling: " + rpbs + " with args: " + str([self.ccpp_config.path] + extrargs)
      call([rpbs, self.ccpp_config.path] + extrargs)

def hasrun(self, extrargs=[]):
  pass

RepoConfig.check = check
RepoConfig.run = run
RepoConfig.hasrun = hasrun

