#!/usr/bin/python


import sys
import os
import subprocess
import glob
import fnmatch
import json
import shutil
import shutil, errno
from time import strftime

import sys
import os
scriptName = os.path.basename(sys.argv[0])
scriptPath = os.path.dirname(sys.argv[0])
sharedPath = os.path.join(scriptPath, "../shared-scripts/")
sys.path.append(os.path.abspath(sharedPath))

import Utils
import GitHelper

def pieceFileName():
    return "piece-description.json";

def allPieces():

    fishlamp = absolutePathToPiecesFolder();

    Utils.verbose("found " + fishlamp)

    pieces = [];
    for filename in Utils.findFiles(fishlamp, pieceFileName()):
        Utils.assertPathExists(filename);
        piece = Piece(filename);
        pieces.append(piece);

    return pieces;

def findPieceForName(name):
    for piece in allPieces():
        if piece.name() == name:
            return piece;

def defaultPieces() :
    return [ "fishlamp-templates" ];

def githubReference() :
    return "git@github.com:"

def submoduleURI(name):
    return  + name;

def addPiece(name):
    GitHelper.addSubmodule(githubReference() + "fishlamp", name, folderName());

def folderName() :
    return "Pieces";

def createFishLampFolderIfNeeded() :
    if os.path.exists(folderName()) == False:
        os.makedirs(folderName())

def initFolder() :
    if os.path.exists(folderName()) == False:
        os.makedirs(folderName())

def searchForFishLampFolder(dir) :
    oldDir = Utils.workingDirectory();

    if(oldDir == "/"):
        return None;

    result = None;

    if os.path.exists(folderName()):

        if dir:
            result = os.path.join(dir, folderName());
        else:
            result = folderName();

    else:
        Utils.setWorkingDirectory("..");

        if dir:
            result = searchForFishLampFolder(os.path.join("..", dir));
        else:
            result = searchForFishLampFolder("..");

    Utils.setWorkingDirectory(oldDir);

    return result;

def relativePathToPiecesFolder():
    fishlamp = searchForFishLampFolder(None);

    if fishlamp:
        Utils.assertPathExists(fishlamp);

    return fishlamp

def absolutePathToPiecesFolder():
    fishlamp = relativePathToPiecesFolder();
    if fishlamp:
        fishlamp = os.path.abspath(fishlamp);
        Utils.assertPathExists(fishlamp);

    return fishlamp;

class Piece:
    _piece = 0;
    _pieceName = "";
    _folder = ""
    _filePath = ""

    def addMissing(self, piece) :

        labels = { "version", "pieceName", "createdOn", "codeUrl", "description", "license" }
        lists = { "dependsOn", "contact", "createdBy", "urls", "includes", "platforms", "includes", "tags" }

        for label in labels:
            if label not in piece:
                piece[label] = "";

        for list in lists:
            if list not in piece:
                piece[list] = [""];

    def defaultPiece(self):

        piece = { };

        self.addMissing(piece);

        piece["createdOn"] = strftime("%Y-%m-%d %H:%M:%S");
        piece["pieceName"] = self._pieceName;
        piece["createdBy"] = [ { "name" : GitHelper.userName(), "contact" : "hello@greentongue.com" } ];
        piece["urls"] = ["http://www.fishlamp.com", "https://www.github.com/fishlamp/" + self._pieceName];
        piece["sourceUrl"] = "https://www.github.com/fishlamp/" + self._pieceName.strip("/") + ".git";
        piece["dependsOn"] = [ "FishLamp-Objc-Core" ];
        piece["contact"] = [ "hello@fishlamp.com" ];
        piece["version"] = "v1.0.0";
        piece["includes"] = [ "Classes" ];
        piece["platforms"] = [ { "name" : "OSX", "version" : "10.0.6" }, { "name" : "iOS", "version" : "5.0.0"} ];
        piece["license"] = "MIT";
        piece["tags"] = [ "objc" ]
        return piece;

    def name(self):
        return self._piece['name'];

    def description(self):
        return self._piece['shortDescription']

    def folderPath(self):
        return self._folder;

    def allPaths(self):
        paths = []
        for path in self._piece['importPaths'].split(','):
            paths.append(os.path.join(self.name(), path.strip()));
        return paths;

    def printSelf(self):
        print "Piece Name: " + self.name();
        print "Piece folder: " + self.folderPath();
        print "Description: " + self.description();
        print "Paths: "
        for path in self.allPaths():
            print "  " + path;

    def readFile(self):
        jsonString = Utils.readFileIntoString(filepath);
        self._piece = json.loads(jsonString)

    def fileExists(self):
        return os.path.exists(self._filePath)

    def createIfNeeded(self):

        if not os.path.exists(self._folder):
            os.makedirs(self._folder)

        if not os.path.exists(self._filePath):
            with open(self._filePath, 'w') as outfile:
                json.dump(self._piece, outfile, sort_keys=True, indent=4, separators=(',', ': '))

            print "# wrote " + self._filePath;
        else:
            print "# alread exists: " + self._filePath

    def __init__(self, pieceName, path):
        self._pieceName = pieceName;
        self._filePath = path.strip();
        self._folder = os.path.dirname(self._filePath)
        self._piece = self.defaultPiece();

    def subDirectoryPath(self, relativePathToPiecesFolder) :
        path = os.path.join(self.folderPath(), relativePathToPiecesFolder);
        return Utils.assertPathExists(path);