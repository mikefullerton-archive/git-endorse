#!/usr/bin/python


import sys
import os
import subprocess
import glob
import fnmatch
import json
import shutil
import shutil, errno

# this doesn't work
gVerbose = False

def verbose(str):
    if gVerbose == True:
        print str

def enableVerbose():
    gVerbose = True;
    print "--Verbose"

def printError(str):
    print "##! " + str;

def assertPathExists(path):
    if os.path.exists(path):
        verbose("Found path:" + path)
        return path;
    else:
        printError("Path not found: " + path);
        sys.exit(1);

def assertNotNone(item, msg):
    if item is None:
        printError("unexpected None value: " + msg);
        sys.exit(1);
    return item;

def deleteDirectory(path) :
    path = path.strip();
    FishLamp.assertNotNone(path, "path is empty");
    
    if len(path) > 1 and os.path.exists(path):
        shutil.rmtree(path)

def copyFileOrDirectory(src, dst) :
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

def readFileIntoString(path):
    assertPathExists(path);

    with open (path, "r") as myfile:
        data=myfile.read().replace('\n', '')
    return data;

def workingDirectory():
    return os.getcwd();

def setWorkingDirectory(dir):
    prev = os.getcwd();
    os.chdir(dir);
    return prev;

def runInDirectory(dir, func):
    prev = setWorkingDirectory(dir);
    func(args);
    setWorkingDirectory(prev);

def findFiles(directory, pattern):
    directory = directory.strip();

    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename);
                yield filename;



def depthFirstFindByName(name):
    outList = [];
    for root, dirs, files in os.walk(os.getcwd()):
        for dir in dirs:
            if name in dir:
                outList.append(os.path.join(root, dir));

        for file in files:
            if name in file:
                outList.append(os.path.join(root, file));

    sort_key = lambda s: (-len(s), s)
    outList.sort(key=sort_key)

    return outList;

def executeCommandWithPath(pathToCommand, args) :
    cmd = pathToCommand;
    for arg in args:
        cmd += " ";
        if(arg.find(" ") > 0):
            cmd += ("\"" + arg + "\"");
        else:
            cmd += arg;

    pr = subprocess.Popen(cmd, cwd = os.getcwd(), shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE )

    (out, error) = pr.communicate()

    if out:
        out = out.strip();
        if len(out) == 0:
            out = None;

    if error:
        error = error.strip();

        if len(error) == 0:
            error = None;

    return (out, error);

def curl(args) :
    return executeCommandWithPath("/usr/bin/curl", args);


