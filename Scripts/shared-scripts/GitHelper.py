#!/usr/bin/python

import sys
import os
import subprocess
import glob

import sys
import os
scriptName = os.path.basename(sys.argv[0])
scriptPath = os.path.dirname(sys.argv[0])
sharedPath = os.path.join(scriptPath, "../shared-scripts/")
sys.path.append(os.path.abspath(sharedPath))

import Utils
import re

def _print(str) :
    if str:
        str = str.strip();
        if len(str):
            print str;

def executeSilent(args) :

    print "# current dir: " + os.getcwd();

    git = [ "/usr/bin/git", "/usr/local/git/bin/git" ];

# TODO:
# type -a git

    cmd = None;
    for p in git:
        if os.path.exists(p):
            cmd = p;

    if not cmd:
        print "Can't find git"
        sys.exit(1)
        return;

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


def execute(args) :
    (out, error) = executeSilent(args);
    if len(out):
        print out;

    if len(error):
        print error;
    
    return (out, error);

def init():
    return execute(["init"]);

def status():
    return execute(["status"])

def isGitRepo():
    return os.path.exists(os.path.join(os.getcwd(),".git"));

def confirmGitRoot() :
    if isGitRepo() == False :
        Utils.printError("git not found - please run in root of your repository.");
        sys.exit(1)

def hasSubmodule(name):
    file = gitmodulesFile();
    return file.find(name) >= 0;

# addSubmodule("git@github.com:fishlamp", "FishLampCore", "FishLamp"
def addSubmodule(moduleURL, inFolder):
    confirmGitRoot();

    moduleName = os.path.basename(moduleURL);
    moduleName = os.path.splitext(moduleName)[0]

    if inFolder == None:
        inFolder = "";

    dest = os.path.join(inFolder, moduleName)

    if hasSubmodule(moduleName) == False:
        print "git submodule add " + moduleURL + " " + dest;
        execute(["submodule", "add", moduleURL, dest]);
    else:
        print moduleURL + " already exists"

def branch() :
    return execute(["rev-parse", "--abbreve-ref", "HEAD"]);

def gitmodulesPath() :
    return os.path.join(os.getcwd(),".gitmodules")

def gitmodulesFile() :
    confirmGitRoot();
    if os.path.exists(gitmodulesPath()):
        fileContents = Utils.readFileIntoString(gitmodulesPath());
        return fileContents;

    return "";

def submodules() :
    confirmGitRoot();

    if os.path.exists(gitmodulesPath()) == False:
        return [];

    repos = [];
    with open(gitmodulesPath()) as f:
        for line in f:
            line = line.strip();
            if line.find("submodule") >= 0:
                match = re.search("\"(.+)\"",line);
                if(match):
                    repo = match.string[match.start() + 1 :match.end() - 1]
                    repos.append(repo);

    return repos;

def findGitFolders():
    folders = [];
    for root, dirs, files in os.walk(os.getcwd()):
        for basename in dirs:
            if basename == ".git":
                folders.append(os.path.dirname(os.path.join(root, basename)));

        for basename in files:
            if basename == ".git":
                folders.append(os.path.dirname(os.path.join(root, basename)));

    sort_key = lambda s: (-len(s), s)
    folders.sort(key=sort_key)

    return folders;

def getGitHubCredentials():
    path=os.path.join(os.getenv("HOME"), ".github_credentials");

    if os.path.exists(path) == False:
        print path + " file not found";
        sys.exit(1);

    creds = "";

    with open (path, "r") as myfile:
        creds=myfile.read()

    creds = creds.replace('\n', '')
    creds = creds.replace(' ', '')
    return creds;


def runCommand(str):
    return execute(str.split(" "))

def userName() :
    (out, error) = runCommand("config --get user.name");
    return out;

def updateSubmodules() :
    confirmGitRoot();
    return runCommand("submodule update --init --recursive");

