import yaml

try:
  from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
  from yaml import Loader, Dumper

class Repository:

  def __repr__(self):
    return "Repository()"

  def __str__(self):
    return str(self.data)

  def __init__(self, name, url, branch, isGitsBase):
    self.name = name
    self.url = url
    self.branch = branch
    self.isGitsBase = isGitsBase
    self.data = { self.name : {
      "name": self.name,
      "url": self.url,
      "branch": self.branch,
      "isGitsBase": self.isGitsBase
    }}

  def appendToYaml(self, fileLocation):
    self.fileLocation = fileLocation  
    with open(self.fileLocation, 'a') as outfile:
      yaml.dump(self.data, outfile, default_flow_style=False)


