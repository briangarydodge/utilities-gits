#!/usr/bin/env python3

from lib.repositories import *
####################################################
## Summerise all repositories
####################################################
def displayMenu(repositories):

  repositories.loadYamlDocument()

  menuText = "\n\033[95mGITS Repository Management.\n\033[0m" \
           + "  1. Add Repository.\n" \
           + "  2. Remove Repository.\n" \
           + "  3. Clone Repositories.\n" \
           + "  4. List All repositories.\n" \
           + "  5. Repository Summary.\n" \
           + "  6. Raw Git Command."
  userInput = ""
  numericInput = -1
  while userInput.upper() != "Q":
    print(menuText)
    userInput = input('\033[1m' + '\033[92m' + "Select option (1-6 or [q]uit): " + '\033[0m')
    
    try:
      numericInput = int(userInput)
      if (numericInput < 0) or (numericInput > 6):
        print("Invalid request. Try again or quit.")
    except:
      if (userInput.upper() == "Q"):
        print("Exiting...")

    if(numericInput >= 1) and (numericInput <=6):
      menuAction(numericInput, repositories)
    numericInput = 0
####################################################
## Switch between User action requests
####################################################
def menuAction(action, repositories):
  if(action == 1):
    performAdd(repositories)
  if(action == 2):
    performRemove(repositories)
  if(action == 3):
    performClone(repositories)
  if(action == 4):
    performList(repositories)
  if(action == 5):
    performSummary(repositories)
  if(action == 6):
    performGITCommand(repositories)
####################################################
## CLI Add command
####################################################
def performAdd(repositories):
  try:
    repositoryName = input("\033[94mEnter repository name: \033[0m")
    repositoryBranch = input("\033[94mEnter default branch: \033[0m")
    repositoryURL = input("\033[94mEnter url to repository: \033[0m")
    if(input("\033[94mIs this a base for GITS? [Y/N]: \033[0m").upper() == "Y"):
      isGitsBase = True
    if(input("\033[93mAre you sure you wish to add " + repositoryName + "? [Y/N] \033[0m").upper() == "Y"):
      print(repositories.addRepository(str(repositoryName), str(repositoryBranch), str(repositoryURL), isGitsBase))
  except:
    print("\033[91mFailed to successfully add new repository. Please try again.\033[0m")
####################################################
## CLI Remove Command
####################################################
def performRemove(repositories):
  index = 0
  numericInput = -1
  for name in repositories.getRepositoryNames():
    print("" + str(index) + ": " + name)
    index = index + 1
  userInput = input("\033[1m\033[92mSelect which repository you wish to be removed: \033[0m")
  try:
    numericInput = int(userInput)
  except:
    print("\033[91mNot a valid selection. Cancelling operation...\033[0m")
  try:
    if(numericInput != -1) and ( (numericInput >= 0) and (numericInput < len(repositories.getRepositoryNames()))):
      if(input('\033[93m' + "Please confirm you wish to remove: [Y/N] " + '\033[0m').upper() == "Y"):
        selectedName = repositories.getRepositoryNames()[numericInput]
        print("Removing: " + selectedName )
        print(repositories.removeRepository(selectedName))
      else:
        print("Cancelling...")
    else:
      print("Cancelling operation...")
  except:
    print("\033[91mFailed to successfully remove repository. Please try again.\033[0m")
####################################################
## CLI Clone Command
####################################################
def performClone(repositories):
  fullClone = False
  if(input("Do you wish to clone recursively? [Y/N] ").upper() == "Y"):
    fullClone = True
  repositories.cloneAllRepositories(DIR_PATH + "/../", fullClone)
####################################################
## CLI List Command
####################################################
def performList(repositories):
  repositories.listRepositories()
####################################################
## CLI Summary Command
####################################################
def performSummary(repositories):
  repositories.displayRepositorySummary()
####################################################
## CLI Git General Command
####################################################
def performGITCommand(repositories):
  print("\n\033[94mGit command line interface (Type \033[1mclihelp\033[0m \033[94mfor help)\n" + '\033[0m')
  userInput = []
  command = ""
  helpText = "\nUse the standard git command by entering the normal commands in this cli.\n" \
           + "\nCommands: \n" \
           + '\033[1m' + "exit" + '\033[0m' + " to close the git cli\n" \
           + '\033[1m' + "clihelp" + '\033[0m' + " to display this help\n" \
           + '\033[1m' + "help" + '\033[0m' + " to display standard git help\n"
  while command.upper() != "EXIT":  
    userInput = input('\033[92m'+ '\033[1m' + "git [command][*options]$ " + '\033[0m').split()
    if(len(userInput) > 0):
      command = userInput[0]
      options = userInput[1:]
      if(command.upper() == "GIT"):
        command = userInput[1]
        options = userInput[2:]
      if(command.upper() != "EXIT") and (command.upper() != "CLIHELP"):
        repositories.rawGit(command, options)
      if(command.upper() == "CLIHELP"):
        print(helpText)
