#!/usr/bin/env python3

class Text_Colours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

import subprocess
from os import chdir, getcwd, path, stat

def git(action, *options):
  try:
    git_command = ['git', action]
    git_command.extend(options)
    subprocess.call(git_command)
  except:
    print("Error performing git operation.")

def getBranch(rootLocation):
  if path.exists(rootLocation):
    chdir(rootLocation)
    branch = subprocess.Popen(r"git branch | grep \*", shell=True, stdout=subprocess.PIPE).stdout.read()
    chdir('..')
    return branch[2:-1]
  else:
    return "Not Known"

def setBranch(module, branch):
  if path.exists(module):
    chdir(module)
    git('checkout', branch)
    chdir('..')

# ====================================================================
# Report if repository has any uncommitted changes                   |
#                                                                    |
# ==================================================================== 
def repoIsChanged(repo):
  if path.exists(repo):
    chdir(repo)
    isChanged = subprocess.Popen("git diff-index HEAD", shell=True, stdout=subprocess.PIPE).stdout.read()
    chdir('..')
    if str(isChanged.decode("utf-8")) == "":
      return "false"
    else:
      return "true"
  else:
    return "Not Known"

# ====================================================================
# Print to console summary information for module(s)                 |
#                                                                    |
# ==================================================================== 
def moduleInfo(rootPath, name, gitRoot = False):
  rootLocation = rootPath + "/" + name
  if path.exists(rootLocation):
    module_exists = Text_Colours.OKGREEN + "True"  + Text_Colours.ENDC
  else:
    module_exists = Text_Colours.FAIL + "False"  + Text_Colours.ENDC
  module_branch = getBranch(rootLocation).decode("utf-8") if getBranch(rootLocation) != "Not Known" else getBranch(rootLocation)
  module_changed = repoIsChanged(rootLocation)
  
  moduleType = "  - Submodule:" if gitRoot else "Module:"

  information = str(Text_Colours.HEADER + moduleType + Text_Colours.ENDC + " {0:<35} " \
    + Text_Colours.HEADER + "Exists:" + Text_Colours.ENDC + " {1:<15} " \
    + Text_Colours.HEADER + "Branch:" + Text_Colours.ENDC + " {2:<25}" \
    + Text_Colours.HEADER + "Uncommitted Changes:" + Text_Colours.ENDC + " {3:}"
    ).format(name, module_exists, module_branch, module_changed)
  return information
