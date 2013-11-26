#!/bin/bash

name="$1"
repo=`pwd`
repo="`basename \"$repo\"`"

echo "$repo"

exists="YES"
remote_path="git@github.com:fishlamp/$repo"

creds=`"$HOME\.github_credentials"`
creds=$(echo $creds)

git ls-remote $remote_path || { exists="NO"; }

if [ $exists == "NO" ]; then

    echo "# adding to github..."

    curl -u "$creds" https://api.github.com/orgs/fishlamp/repos -d "{\"name\": \"$repo\"}" > last-add.txt || { exit 1; }

else
    echo "# $repo already exists on github"
fi

echo "# adding remote host..."
git remote rm origin

git remote add origin git@github.com:fishlamp/$repo.git || { exit 1; }

branch=`git rev-parse --abbrev-ref HEAD` || { exit 1; }

echo "# git push origin $branch"

git push -u origin $branch || { exit 1; }
