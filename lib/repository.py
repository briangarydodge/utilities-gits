import yaml
# Library Imports ****Start****
try:
  from lib.gitwrapper import *
except ImportError:
  print("Unable to find gitwrapper. Exiting...")
  exit(1)

try:
  from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
  try:
   from yaml import Loader, Dumper
  except ImportError:
    print("Fatal error loading yaml dependencies. Exiting...")
    exit(1)
# Library Imports ****End***

# ***********************************************************
# Repository Class                                          *
# ***********************************************************
# Properties:                                               *
#   name - Display name for git repo                        *
#   url - repository location                               *
#   branch - stored current branch                          *
#   isGitsBase - flag indicating further gits level         *
# ***********************************************************
class Repository:

  def __repr__(self):
    return "Repository()"

  def __str__(self):
    return str(self.data)

  def __init__(self, name, url, branch, isGitsBase, path=None, parent=None):
    self.name = name
    self.url = url
    self.branch = branch
    self.isGitsBase = isGitsBase
    self.path = path
    self.parent = parent
    self.data = { self.name : {
      "name": self.name,
      "url": self.url,
      "branch": self.branch,
      "isGitsBase": self.isGitsBase,
      "path": self.path
    }}

  # *******************************************************
  # Serialize Repo Information to file                    *
  # *******************************************************
  def appendToYaml(self, fileLocation):
    self.fileLocation = fileLocation  
    with open(self.fileLocation, 'a') as outfile:
      yaml.dump(self.data, outfile, default_flow_style=False)
  # *******************************************************
  # Clone project repo locally                            *
  # *******************************************************
  def cloneRepo(self):
    print("Cloning Repo %s" % self.name)
    if self.url is not None:
      git("clone", self.url)
    else:
      print("Repository url not defined, Aborting...")
  # *******************************************************
  # Change local repo to branch                           *
  # *******************************************************
  def changeBranch(self, branch):
    print("Changing branch from %s to %s" % (self.branch, branch))
    self.branch = branch
    git("checkout", branch)
  # *******************************************************
  # Check if local repo is in changed state               *
  # *******************************************************
  def repoIsChanged(self):
    print("Dunno! :)")
  # *******************************************************
  # Perform a standard git command                        *
  # *******************************************************
  def pureGit(self, command, options):
    git(command, options)
  # *******************************************************
  # Print repo details                                    *
  # *******************************************************
  def printItemSummary(self):
    print("Name: %s, Branch: %s" % (self.name, self.branch))


