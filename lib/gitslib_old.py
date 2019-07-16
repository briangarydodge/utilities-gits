#!/usr/bin/env python
# ====================================================================
# Gits Multi-module git repository loader and tool.                  |
#                                                                    |
# Updates                                                            |
#                                                                    |
# 25/06/2018 - Added ability to add modules                          |
# ====================================================================
try:
  import subprocess
  from optparse import OptionParser
  from os import chdir, getcwd, path, stat
  from sys import argv, exit
except:
  print "Fatal error!\nPlease check Python Installation.\nExiting."
  exit(0)

try:
  import yaml
except:
  print "Missing pyyaml. Try running command: pip install pyyaml.\nExiting."
  exit(0)

try:
  from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
  from yaml import Loader, Dumper

# ====================================================================
# Store Module information loaded from yaml                          |
#                                                                    |
# ====================================================================
class Module:
  def __init__(self, name, url, branch):
	self.name = name
	self.url = url
	self.branch = branch
# ====================================================================
# Colour Constants for output of text                                |
#                                                                    |
# ====================================================================
class Text_Colours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# -- Globals --------------------------------------------------------

GITS_REGISTER_FILE = 'gits-modules.yaml'
modulelist = []   # Store each repository in collection
SELECTED_MODULE = ''
# Full path required to ensure no IOException when writing /appending to files.
DIR_PATH = path.dirname(path.realpath(__file__))

# -- Error Constants ------------------------------------------------

GIT_OPERATION_EXCEPTION = 2001
YAML_FILE_LOAD_EXCEPTION = 2002
MODULE_DATA_PACKET_EXCEPTION = 2003
YAML_FILE_WRITE_EXCEPTION = 2004
FOLDER_TRANSITION_EXCEPTION = 2005
FILE_WRITE_EXCEPTION = 2006
MODULES_FILE_NOT_FOUND = 2007

# -- End of Globals -------------------------------------------------

# ====================================================================.
# Python wrapper to the Git command                                  |
#                                                                    |
# ====================================================================
def git(action, *options):
  try:
    git_command = ['git', action]
    git_command.extend(options)
    subprocess.call(git_command)
  except:
    print "Error performing git operation."
    exit(GIT_OPERATION_EXCEPTION)

# ====================================================================
# Load .gits-modules.yaml to collection of yaml documents            |
#                                                                    |
# ====================================================================
def loadYamlDocument():
  try:
    documents = yaml.load(file(DIR_PATH + '/../' + GITS_REGISTER_FILE, 'r'), Loader=Loader)

    for document in documents:
      name = documents[document]['name']
      url = documents[document]['url']
      branch = documents[document]['branch']
      modulelist.append(Module(name, url, branch))
  except:
    print "Error parsing modules!\n Check yaml file."
    exit(YAML_FILE_LOAD_EXCEPTION)

# ====================================================================
# Store user provided Module information to .gits-modules.yaml       |
#                                                                    |
# ====================================================================
def appendYamlDocument(name, url, branch):
  try:
    data = { name : {
      "name": name,
      "url" : url,
      "branch" : branch
    }}
  except:
    print "Error creating repo information.\nAborting."
    exit(MODULE_DATA_PACKET_EXCEPTION)

  try:
    with open(DIR_PATH + '/../' + GITS_REGISTER_FILE, 'a') as outfile:
      yaml.dump(data, outfile, default_flow_style=False)
  except:
    print "Unable to serialise to modules file.\nAborting."
    exit(YAML_FILE_WRITE_EXCEPTION)

# ====================================================================
# Iterate to parent folder until gits-module.yaml found              |
#                                                                    |
# ====================================================================
def go_project_root():
  try:
    while not path.exists(GITS_REGISTER_FILE) and getcwd() != '/':
        chdir('..')
  except:
    print "Error occurred while moving up folder structure\n or modules file not found."
    exit(FOLDER_TRANSITION_EXCEPTION)

# ====================================================================
# Basic append text to file - for use with .gitignore                |
#                                                                    |
# ====================================================================
def appendToFile(filename, toIgnore):
  try:
    with open(DIR_PATH + '/' + filename, 'a') as file:
	    file.write(toIgnore + "/\n")
	    file.close()
  except:
    print "Error updating .gitignore file"
    exit(FILE_WRITE_EXCEPTION)

# ====================================================================
# Print basic message to console                                     |
#                                                                    |
# ====================================================================
def info(message):
    print(message)

# ====================================================================
# Retrieve the currently tracked branch of module                    |
#                                                                    |
# ====================================================================
def getBranch(module):
  if path.exists(module):
	  chdir(module)
	  branch = subprocess.Popen(r"git branch | grep \*", shell=True, stdout=subprocess.PIPE).stdout.read()
	  chdir('..')
	  return branch[2:-1]
  else:
	  return "Not Known"

# ====================================================================
# Change the currently tracked branch of module                      |
#                                                                    |
# ====================================================================  
def setBranch(module, branch):
  if path.exists(module):
	  chdir(module)
	  git('checkout', branch)
	  chdir('..')

# ====================================================================
# Wrapped git clone command                                          |
#                                                                    |
# ==================================================================== 
def clone(name, url, branch):
  if path.exists(name) != True:
    try:
      info('CLONING: ' + name)
      git('clone', url, name)
      setBranch(name, branch)
    except:
      print 'Unable to clone: name. Skipping...\n'
  else:
	  info(name + ' already exists! Skipping...')

# ====================================================================
# Report if repository has any uncommitted changes                   |
#                                                                    |
# ==================================================================== 
def repoIsChanged(repo):
  if path.exists(repo):
    chdir(repo)
    isChanged = subprocess.Popen("git diff-index HEAD", shell=True, stdout=subprocess.PIPE).stdout.read()
    chdir('..')
    if isChanged == "":
      return "false"
    else:
      return "true"
  else:
    return "Not Known"

# ====================================================================
# Print to console summary information for module(s)                 |
#                                                                    |
# ==================================================================== 
def moduleInfo(name):
  if path.exists(name):
	  module_exists = Text_Colours.OKGREEN + "True"  + Text_Colours.ENDC
  else:
	  module_exists = Text_Colours.FAIL + "False"  + Text_Colours.ENDC

  module_branch = getBranch(name)
  module_changed = repoIsChanged(name)

  information = str(Text_Colours.HEADER + "Module:" + Text_Colours.ENDC + " {0:<35} " \
    + Text_Colours.HEADER + "Exists:" + Text_Colours.ENDC + " {1:<15} " \
    + Text_Colours.HEADER + "Branch:" + Text_Colours.ENDC + " {2:<25}" \
    + Text_Colours.HEADER + "Uncommitted Changes:" + Text_Colours.ENDC + " {3:}"
    ).format(name, module_exists, module_branch, module_changed)
  info(information)

# ====================================================================
# Clone each repository referenced by modules file                   |
#                                                                    |
# ====================================================================
def perform_clone():
  for module in modulelist:
    clone(module.name, module.url, module.branch)

# ====================================================================
# Either display info for all or one module                          |
#                                                                    |
# ====================================================================
def perform_info():
  if (SELECTED_MODULE == ''):
    for module in modulelist:
      moduleInfo(module.name)
  else:
    moduleInfo(SELECTED_MODULE)

# ====================================================================
# Perform typical git commands on all or one                         |
#                                                                    |
# ====================================================================
def perform_other(command, options):
  if (SELECTED_MODULE == ''):
    for module in modulelist:
      info('PROCESSING: ' + module.name)
      chdir(module.name)
      git(command, *options)
      chdir('..')
  else:
    info('PROCESSING: ' + SELECTED_MODULE)
    chdir(SELECTED_MODULE)
    git(command, *options)
    chdir('..')

# ====================================================================
# Add new reference to repository in modules file.                   |
#                                                                    |
# ====================================================================
def perform_add():
  project_name = raw_input("Enter project name: ")
  project_url = raw_input("Enter git url: ")
  project_branch = raw_input("Enter default branch: ")

  appendYamlDocument(project_name, project_url, project_branch)

  doAppend = raw_input("Add project to .gitignore file? [y/n]: ")
  if (doAppend == 'y') or (doAppend == 'Y'):
    appendToFile('../.gitignore', project_name)

# ====================================================================
# execute function                                                      |
#                                                                    |
# ====================================================================
def doexecute(argv):
  global GITS_REGISTER_FILE
  go_project_root()

  help_text = "usage: %prog [command..] [options]\n\n" \
	    + "Wrapper for git, used for orchestrating multi-module project.\n" \
	    + "Commands:\n\n" \
      + "  add\t\tAdd a project to the gits-modules file.\n" \
	    + "  clone\t\tClone all modules in to parent directory.\n" \
	    + "  initialise\tClone all modules in to parent directory.\n" \
	    + "  info\t\tDisplay summary information about modules.\n\n" \
	    + "  <other standard git commands>\t\tCheck git documentation."
  
  parser = OptionParser(usage=help_text)
  parser.add_option("-y", "--yaml", dest="yaml_file", type="string", help="Use custom yaml file for modules", metavar="YAML_FILE")
  parser.add_option("-m", "--module", dest="module", type="string", help="Perform action on individual module", metavar="MODULE")
  (options, args) = parser.parse_args()

  if (options.yaml_file is not None):
    GITS_REGISTER_FILE = options.yaml_file

  if (options.module is not None):
    global SELECTED_MODULE
    SELECTED_MODULE = options.module

  

  # parse arguments
  command = args[0] # First Command Line Argument
  options = args[1:] # All Remaining Command Line Arguments

  if (command == 'add'):
    perform_add()
  else:

    if not path.exists(GITS_REGISTER_FILE):
      print(GITS_REGISTER_FILE + ' not found')
      exit(MODULES_FILE_NOT_FOUND)

    if (stat(GITS_REGISTER_FILE).st_size == 0):
      print('The modules file is empty. Please add entry and retry. Exiting')
      exit(MODULES_FILE_NOT_FOUND)

    loadYamlDocument()

    # check arguments
    if len(args) < 1:
      print('Usage: gits <git command>')
      exit(1)

    if (command == 'clone') or (command == 'initialise'):
      perform_clone()
    elif (command == 'info'):
      perform_info()
    else:
      perform_other(command, options)
