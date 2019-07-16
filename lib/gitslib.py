#!/usr/bin/env python3
# ====================================================================
# Gits Multi-module git repository loader and tool.                  |
#                                                                    |
# Updates                                                            |
#                                                                    |
# 25/06/2018 - Added ability to add modules                          |
# ====================================================================
from lib.repositories import *
from lib.gitscli import displayMenu

try:
  import subprocess
  from optparse import OptionParser
  from sys import argv, exit
except Exception as e:
  print("Fatal error!\nPlease check Python Installation.\nExiting.")
  print("Error: " + str(e))
  exit(0)

DIR_PATH = path.dirname(path.realpath(__file__))

####################################################
## CLI Add command
####################################################
def performAdd(repositories):
  try:
    repositoryName = input("\033[94mEnter repository name: \033[0m")
    repositoryBranch = input("\033[94mEnter default branch: \033[0m")
    repositoryURL = input("\033[94mEnter url to repository: \033[0m")
    if(input("\033[93mAre you sure you wish to add " + repositoryName + "? [Y/N] \033[0m").upper() == "Y"):
      print(repositories.addRepository(str(repositoryName), str(repositoryBranch), str(repositoryURL), False))
  except:
    print("\033[91mFailed to successfully add new repository. Please try again.\033[0m")
####################################################
## Clone Command
####################################################
def performClone(repositories):
  repositories.cloneAllRepositories(DIR_PATH + "/../")
####################################################
## Summary Command
####################################################
def performSummary(repositories):
  repositories.displayRepositorySummary()
####################################################
## Summary Command
####################################################
def performOther(repositories, command, options):
  repositories.rawGit(command, options)
# ====================================================================
# execute function                                                   |
#                                                                    |
# ====================================================================
def doexecute(argv):

  help_text = "usage: %prog [command..] [options]\n\n" \
	    + "\033[92mWrapper for git, used for orchestrating multi-module project.\n\033[0m" \
	    + "\033[1mCommands:\033[0m\n\n" \
            + "  \033[1mcli\033[0m\t\t\033[94mStart the GITS command Line Interface.\n\033[0m" \
            + "  \033[1mgui\033[0m\t\t\033[94mStart the GITS Graphical User Interface.\n\033[0m" \
            + "  \033[1madd\033[0m\t\t\033[94mAdd a project to the gits-modules file.\n\033[0m" \
	    + "  \033[1mclone\033[0m\t\t\033[94mClone all modules in to parent directory.\n\033[0m" \
	    + "  \033[1minitialise\033[0m\t\033[94mClone all modules in to parent directory.\n\033[0m" \
	    + "  \033[1minfo\033[0m\t\t\033[94mDisplay summary information about modules.\n\n\033[0m" \
	    + "  \033[1m<other standard git commands>\033[0m\t\t\033[94mCheck git documentation.\033[0m"
  
  parser = OptionParser(usage=help_text)
  parser.add_option("-m", "--module", dest="module", type="string", help="Perform action on individual module", metavar="MODULE")
  (options, args) = parser.parse_args()

  # parse arguments
  command = args[0] # First Command Line Argument
  options = args[1:] # All Remaining Command Line Arguments

  repositories = Repositories(DIR_PATH + "/../",  'gits-modules.yaml')

  if(command.upper() == "CLI"):
    displayMenu(repositories)
    exit(0)

  if(command.upper() == "GUI"):
    print("Not yet implemented!")
    exit(0)

  repositories.loadYamlDocument()

  if (command.upper() == 'ADD'):
    performAdd(repositories)
    exit(0)

  # check arguments
  if len(args) < 1:
    print('Usage: gits <git command>')
    exit(1)

  if (command.upper() == 'CLONE') or (command.upper() == 'INITIALISE'):
    performClone(repositories)
  elif (command.upper() == 'INFO'):
    performSummary(repositories)
  else:
    performOther(repositories, command, options)
