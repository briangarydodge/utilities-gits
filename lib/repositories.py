#!/usr/bin/env python3

import yaml
import os
import shutil
from lib.gitwrapper import *
from lib.repository import *
import json

try:
  from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
  from yaml import Loader, Dumper

DIR_PATH = path.dirname(path.realpath(__file__))

class Repositories:
####################################################
## Constructor
####################################################
  def __init__(self, fileLocation, gitsFile):
    self.repositoryList = []
    self.rootPath = fileLocation
    self.fileLocation = fileLocation + '/' + gitsFile
    self.gitIgnore = fileLocation + '/.gitignore'
####################################################
## Load a specified yaml document and create
## a repository collection
####################################################
  def loadYamlDocument(self):
    if os.path.isfile(self.fileLocation):
      with open(self.fileLocation, 'r') as stream:
        documents = yaml.load(stream)
        for document in documents:
          name = documents[document]['name']
          url = documents[document]['url']
          branch = documents[document]['branch']
          isGitsBase = documents[document]['isGitsBase'] if 'isGitsBase' in documents[document] else False
          self.repositoryList.append(Repository(name, url, branch, isGitsBase))
####################################################
## Add a new repository and serialise to yaml
####################################################
  def addRepository(self, name, branch, url, isGitsBase):
    found = False
    for repository in self.repositoryList:
      if repository.name == name:
        found = True
    if found:
      return "Not Added"
    else:
      repository = Repository(name, url, branch, isGitsBase)
      self.repositoryList.append(repository)
      repository.appendToYaml(self.fileLocation)
      self.appendToFile(name)
      return "Success Added"
####################################################
## Remove a repository from collection
####################################################     
  def removeRepository(self, name):
    found = False
    index = 0
    chdir(self.rootPath)
    try:
      os.remove(self.fileLocation)
      if(len(self.repositoryList) != 0):
        for repository in self.repositoryList:
          if repository.name != name:
            repository.appendToYaml(self.fileLocation)
          else:
            foundIndex = index
            found = True
          index = index + 1
        if found:
            del self.repositoryList[foundIndex]
            shutil.rmtree(name, ignore_errors=False, onerror=None)
            self.removeFromFile(name)
            return "'" + name + "' Successfully Removed"
        else:
            return "'" + name + "` not found!"
      else:
        print("No records of sub-modules")
    except Exception as e:
      print(str(e))
####################################################
## List all repositories
####################################################
  def listRepositories(self):
    for repository in self.repositoryList:
      print(json.dumps(str(repository), indent=4, sort_keys=True))
####################################################
## Return collection of all repositories
####################################################
  def getRepositoryNames(self):
    namesList = []
    for repo in self.repositoryList:
      namesList.append(repo.name)
    return namesList
####################################################
## Clone all repositories
####################################################
  def cloneAllRepositories(self, basePath, autoUpdateBase = False): 
    try: 
      for repository in self.repositoryList:
        chdir(basePath)
        repoName = repository.name
        if path.exists(repoName) != True:
          git('clone', repository.url)
          setBranch(repoName, repository.branch)
        else:
          print(repository.name + " already exists! Ignoring...")
        if(repository.isGitsBase) and autoUpdateBase:
          tempRepoList = Repositories(DIR_PATH + "/../" + repoName,  'gits-modules.yaml')
          tempRepoList.loadYamlDocument()
          tempRepoList.cloneAllRepositories(DIR_PATH + "/../" + repoName + "/")
    except Exception as e:
      print('Error: '+ str(e))
####################################################
## Summarise all repositories
####################################################
  def displayRepositorySummary(self, isSub = False):
    if(len(self.repositoryList) == 0):
      print("No records of sub-modules.")
    for repository in self.repositoryList:
      repoName = str(repository.name)
      print(moduleInfo(self.rootPath, repoName, isSub))
      if(repository.isGitsBase):
          tempRepoList = Repositories(DIR_PATH + "/../" + repoName,  'gits-modules.yaml')
          tempRepoList.loadYamlDocument()
          tempRepoList.displayRepositorySummary(True)
####################################################
## Update .gitignore file
####################################################
  def appendToFile(self, toIgnore):
    try:
      with open(self.gitIgnore, 'a') as file:
        file.write(toIgnore + "/\n")
        file.close()
    except:
      print("Error updating .gitignore file")
      exit(0)
####################################################
## Update .gitignore file
####################################################
  def removeFromFile(self, toIgnore):
    try:
      file = open(self.gitIgnore,"r")
      lines = file.readlines()
      file.close()
      file = open(self.gitIgnore,"w")
      for line in lines:
        if line != toIgnore + "/\n":
          file.write(line)
      file.close()
    except:
      print("\033[91mFailed to update .gitignore. Please do manually.\033[0m")
####################################################
## Raw Git Command on all repositories
####################################################
  def rawGit(self, command, options):
    for repo in self.repositoryList:
      chdir(repo.name)
      git(command, *options)
      chdir('..')
####################################################
## Raw Git Command on all repositories
####################################################
  def rawGitModule(self, repo, command, options):
      chdir(repo.name)
      git(command, *options)
      chdir('..')

