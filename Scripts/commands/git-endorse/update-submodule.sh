#!/bin/sh

#  fishlamp-update-submodule.sh
#  fishlamp-install
#
#  Created by Mike Fullerton on 7/27/13.
#

function usage() {
    echo "either adds or updates a submodule"
}

if [ "$1" == "--help" ]; then
    usage
    exit 0;
fi


the_module="$1"
the_relative_path="Pieces/$the_module"

has_module=0

if [ -f .gitmodules ]; then

    search_result=`grep \"$the_relative_path\" .gitmodules`

    if [[ "$search_result" != "" ]]; then
        has_module=1
    fi
fi

if [ $has_module == 0 ]; then
    git submodule add git@github.com:fishlamp/$the_module.git "$the_relative_path"
fi

cd "$the_relative_path"
branch=`git rev-parse --abbrev-ref HEAD`

if [ "$branch" != "master" ]; then
    git checkout master

    if [ $has_module == 1]; then
        git pull origin master
    fi
fi


