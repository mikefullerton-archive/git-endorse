#!/usr/bin/python


import sys
import os
import subprocess
import glob
import fnmatch
import json
import shutil
import shutil, errno

import sys
import os
scriptName = os.path.basename(sys.argv[0])
scriptPath = os.path.dirname(sys.argv[0])
sharedPath = os.path.join(scriptPath, "../shared-scripts/")
sys.path.append(os.path.abspath(sharedPath))

import Utils

def scriptsPath() :
    path = subprocess.check_output(["fishlamp", "scripts-path"]).strip();
    Utils.assertPathExists(path);
    return path;

def templatePath(subDir) :
    return Utils.assertPathExists(os.path.join(os.path.join(scriptsPath(), "templates"), subDir));

def executeCommand(name, args) :

    newargs = []
    newargs.append("fishlamp");
    newargs.append(name);

    for arg in args:
        newargs.append(arg);

    return subprocess.check_output(newargs).strip();

class Script :

    def __init__(self):
        self.checkParams();

    def scriptName(self):
        return os.path.basename(sys.argv[0]);

    def scriptPath(self):
        return os.path.dirname(sys.argv[0]);

    def checkForHelp(self):
        for str in sys.argv:
            if str == "--help":
                print self.helpString()
                sys.exit(0);
            elif (str == "--usage" or str == "-u"):
                self.printUsage()
                sys.exit(0);
            elif (str == "-v" or str == "--verbose"):
                Utils.enableVerbose();

    def printUsage(self):
        print self.usageString();

    def usageString(self):
        return "usage TBD";

    def helpString(self):
        return "help TBD";

    def checkParams(self):
        self.checkForHelp();

    def run(self):
        Utils.printError("override this");

    def hasParameterAtIndex(self, index):
        if len(sys.argv) > index:
            return True;
        return False;

    def parameterAtIndex(self, index, errorString):

        parm = None;
        if len(sys.argv) > index:
            parm = sys.argv[index];
            Utils.assertNotNone(parm, "parameter at Index: " );
#            + index
        else:
            Utils.printError(errorString);
            sys.exit(1)

        return parm;

    def scriptArguments(self) :
        args = [];
        i = 0;
        for arg in sys.argv:
            if i > 0:
                args.append(arg);
            i += 1;
        return args;

    def scriptArgumentsAsString(self):
        str = "";
        i = 0;
        for arg in sys.argv:
            if i > 0:
                if str:
                    str = " " + str;
                else:
                    str = arg;
            i += 1;
        return str;


    def hasParameter(self, p) :
        for arg in sys.argv:
            if p == arg:
                return True;
        return False;

class ParseInput :

    def __init__(self, arguments):
        self.arguments = arguments;
        self.parseArguments();

    def handleFailure(self, msg) :
            print "##! " + msg;
            sys.exit(0);

    def validateResults(self, results) :

#        print "results needing validation: " + str(results);

        newResults = dict()

        for key in results:

            arg = results[key];

            validator = arg.validator;

            while validator != None:
                if not validator.validate(arg):
                    self.handleFailure(validator.failedMessage(arg));
                    return None;
                else:
                    validator = validator.nextValidator;

            newResults[ arg.key ] = arg;

        return newResults;

    def badParam(self, val):
        print '##! argument not understood: "{val}"'.format(**locals());
        print '##! available parameters:'
        for arg in self.arguments:
            print "##! " + arg.description()

        sys.exit(0);

    def getInvokedArguments(self) :
        inputArray = sys.argv;
        inputArray.pop(0);

        results = dict();

        while(len(inputArray)):

            found = False;
            for arg in self.arguments:
                lastCount = len(inputArray);
                inputArray = arg.handleInput(inputArray);

                if len(inputArray) < lastCount:
                    found = True;
                    results[ arg.key ] = arg;

#                    print "found result: " + arg.key;
#                    print "results: " + str(results);
                    break;

            if not found:
                self.badParam(inputArray[0]);
                break;

        return results

    def parseArguments(self) :
        self.results = self.validateResults(self.getInvokedArguments());

    def getArgumentHandler(self, key) :
        if key in self.arguments:
            return self.arguments[key];
        else:
            return None;

class ArgumentValidator :

    def __init__(self, message = None, nextValidator = None):
        self.nextValidator = nextValidator;
        self.message = message;

    def validate(self, argument) :
        return True;

    def failedMessage(self) :
        return self.message;

    def description(self) :
        return "";

    def mutate(self, argument) :
        return argument;

class RequiredArgument(ArgumentValidator) :

    def failedMessage(self, argument) :
        return 'missing required argument: ' + argument.key

    def validate(self, argument) :
        return argument.wasInvoked;

    def description(self) :
        return "this argument is required";

class FilePathValidator(ArgumentValidator) :

    def failedMessage(self, arg) :
        path = arg.value;
        msg = ArgumentValidator.failedMessage(self);
        return 'Can\'t find path: "{path}" ({msg})"'.format(**locals())

    def validate(self, argument) :
        if argument.value:
            path = argument.value;
            return os.path.exists(path);

        return True;

    def mutate(self, argument) :
        return os.path.abspath(argument);

    def description(self) :
        return "path must exist"

class OptionalArgument(ArgumentValidator) :

    def description(self) :
        return "this argument is optional";

class Argument :

    def __init__(self, key, validator = None):
        self.key = key;
        self.value = None;
        self.validator = validator;
        self.wasInvoked = False;

    def handleInput(self, inputArray) :
        if self.key == inputArray[0] :
            inputArray.pop(0);
            self.wasInvoked = True;

            # TODO add better handling of bad params
            if self.validator:
                if len(inputArray):
                    result = inputArray[0];
                    inputArray.pop(0);

                    validator = self.validator;
                    while validator != None:
                        result = validator.mutate(result);
                        validator = validator.nextValidator;

                    self.value = result;

        return inputArray;

    def description(self) :

        validator = self.validator;
        outString = self.key;

        validators = None;

        while validator:

            if validators:
                validators += ", " + validator.description();
            else:
                validators = validator.description();

            validator = validator.nextValidator;

        if validators:
            outString += " (" + validators + ")"

        return outString;

    def __repr__(self):
        return "<Argument %s=\"%s\">" % (self.key, self.value);

    def __str__(self):
        return "<Argument %s=\"%s\">" % (self.key, self.value);

