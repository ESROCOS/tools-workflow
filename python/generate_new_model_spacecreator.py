#!/usr/bin/env python3

# H2020 ESROCOS Project
# Company: GMV Aerospace & Defence S.A.U.
# Licence: GPLv2

import sys
import getopt
import errno
import os
import shutil

from mako.template import Template
from mako.runtime import Context
from newmodelspacecreator import packageGenerators


def main():
    # Parse arguments and create a new model in autoproj
    print ('Generating a new ESROCOS component')

    while True:
        component_name = input ("Please enter the component name:\n ")
        words = component_name.split('/')
        if (len(words) != 2):
            print('The component name is wrong. the format should be [package_type]/[project_name]')
        else:
            break    
    project_name=words[len(words)-1]
    #Check if it is correct
    package_set_name = input ("Please enter the package set that you desire to include the new component:\n") 

    stop = 0
    dependencies = []
    while stop==0:
        d = input("Please enter the dependecies or pulse \"s\" to finish :\n")
        if d == "s":
            stop = 1
            break
        else: #Check depenedies
            if(packageGenerators.check_dependency(d)):
                dependencies.append(d)
            else:
                print("This dependency is not installed in ESROCOS environment")
    # Create autoproj package structures
    #To check this
    packageGenerators.create_component(component_name,project_name, package_set_name, dependencies) #check
    

if __name__ == "__main__":
    main()
