#!/usr/bin/python

# begin boilerplate
import sys
import os
scriptName = os.path.basename(sys.argv[0])
scriptPath = os.path.dirname(sys.argv[0])
sharedPath = os.path.join(scriptPath, "../shared-scripts/")
sys.path.append(os.path.abspath(sharedPath))
import GitHelper
import Scripts

#end boilerplate

class Script(Scripts.Script):

    def helpString(self):
        return "lists the current submodules in use by the repo";

    def run(self):
        submodules = GitHelper.submodules();
        for submodule in submodules:
            print submodule;


Script().run();


