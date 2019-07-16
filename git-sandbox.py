#!/usr/bin/env python3

from lib.repositories import *
from lib.gitscli import displayMenu
from os import chdir, getcwd, path, stat
import sys


DIR_PATH = path.dirname(path.realpath(__file__))

def main():

  print("Python version", sys.version)
  
  repositories = Repositories(DIR_PATH,  '/gits-modules.yaml')
  #repositories.loadYamlDocument()
  #print(repositories.addRepository("enq-drivers-etl-service","develop","ssh://git@stash.idsp.dvla.gov.uk:7999/enq/enq-drivers-etl-service.git",False))
  #repositories.cloneAllRepositories()
  #repositories.listRepositories()
  #print("Remove Repository: " + repositories.removeRepository("enq-drivers-etl-service") + "\n")
  #repositories.listRepositories()
  #repositories.displayRepositorySummary()
  #repositories.cloneAllRepositories()

  displayMenu(repositories)


  exit(0)


if __name__ == '__main__':
  main()
