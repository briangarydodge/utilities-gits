# GITS

---  

Python utility for orchestrating multi-module projects by wrapping the vanilla git command and utilising persistant settings.

## Requirements

As gits is a python script, it will work on linux & mac terminal and the windows command line.

Python 2.7 is a requirement for gits to function, as well as, the pyyaml library (Installed using pip).

## Usage

### Creating a new multi-module project

1. Create a root folder for your project
2. Copy the ```gits``` file and the ```lib``` folder into you new root folder
3. Open a terminal in your root folder (CTRL-ALT-T)
4. Type ```./gits add``` and press Enter
5. Type/Copy in the desired module name
6. Type/Copy in the url to the bitbucket repository (obtained from the clone button in bitbucket)
7. Type in the desired default branch (i.e. develop)
8. Enter whether you wish the module to be listed in the ```.gitignore``` file
9. Repeat steps 4 - 8 for each module you wish to add
10. Create a repository for your project in bitbucket using the same name as your root folder
11. Type ```git init``` and press Enter
12. Type ```git add .``` and press Enter
13. Type ```git commit -m "Initial Commit"```
14. Type ```git remote add origin ssh://git@stash.idsp.dvla.gov.uk:7999/<Project>/<rootfoldername>.git``` and press Enter
15. Type ```git push -u origin master``` and press Enter
16. Type ```./gits clone``` and press Enter *(You may need to be connected to the VPN for this to function correctly)*

### Adding a new module to an existing multi-module project

1. Open terminal in the root folder of your project
2. Type ```./gits add``` and press Enter
3. Type/Copy in the desired module name
4. Type/Copy in the url to the bitbucket repository (obtained from the clone button in bitbucket)
5. Type in the desired default branch (i.e. develop)
6. Enter whether you wish the module to be listed in the ```.gitignore``` file
7. Repeat steps 2 - 6 for each module you wish to add
8. Type ```git add .``` and press Enter
9. Type ```git commit -m "Added repo"``` and press Enter
10. Type ```git push``` and press Enter

### Updating the multi-module project

1. Open terminal in the root folder of your project
2. Type ```git pull``` and press Enter
3. Type ```./gits pull``` and press Enter

### Removing a module from an existing multi-module project

1. Open the root folder of your project
2. Delete the folder of the module you wish to remove
3. Open the ```gits-module.yaml``` file and remove the section from the file
4. Open the ```.gitignore``` file and remove the project line

### Viewing information about your multi-module project

1. Open terminal in the root folder of your project
2. Type ```./gits info``` and press Enter
