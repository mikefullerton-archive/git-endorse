#!/usr/bin/python

# begin boilerplate
import sys
import os
scriptName = os.path.basename(sys.argv[0])
scriptPath = os.path.dirname(sys.argv[0])
sharedPath = os.path.join(scriptPath, "../shared-scripts")
sys.path.append(os.path.abspath(sharedPath))
import GitHelper
import Scripts

import subprocess


class Script(Scripts.Script):

    def helpString(self):
        return "Fek is a helper for git";

    def check(self, folders):
        dirty = [];
        clean = [];

        for folder in folders:

            dir = os.getcwd();
            os.chdir(folder);
            (out, error) = GitHelper.executeSilent(["status"]);
            os.chdir(dir);

            if out.find("nothing to commit") >= 0:
                clean.append(folder);
            else:
                dirty.append(folder);

#                if quick == False:
#                    print "#### " + folder + " ####";
#                    print out;
#                    print "#### " + folder + " ####";


        print "# " + str(len(clean)) + " clean repos:"
#        for f in clean:
#            print "  " + os.path.relpath(f);

        if len(dirty) == 0:
            print "# all clear!"
        else:
            print "# " + str(len(dirty)) + " dirty repos:"
            for f in dirty:
                print "  " + os.path.abspath(f);

    def run(self):

        print "# fekking..."

        folders = GitHelper.findGitFolders();

        if self.hasParameter("check"):
            self.check(folders)
        else:
            for folder in folders:

                f = os.path.abspath(folder)

                dir = os.getcwd();
                os.chdir(folder);

                args = self.scriptArgumentsAsString();
                if not args:
                    args = "";

                print ""
                print "# dir: " + f
                print "# cmd: git " + args;

                (out, error) = GitHelper.execute(self.scriptArguments());
                os.chdir(dir);
#                print f

Script().run();
