#!/bin/bash

MY_PATH="`dirname \"$0\"`"              
MY_PATH="`( cd \"$MY_PATH\" && pwd )`"  

cd "$MY_PATH"

source "scripts/installer-config/destination.sh"

if [ -d "$DEST" ]; then
    rm -rd "$DEST"
fi

mkdir -p "$DEST"

cp -R "scripts/shared-scripts" "$DEST/shared-scripts" || { echo "unable to copy script to: $DEST"; exit 1; }

for dir in scripts/commands/*/
do
    dir=${dir%*/}
    echo "# will install: ${dir##*/}"
done

for dir in scripts/commands/*/
do
    dir=${dir%*/}
#    echo ${dir##*/}

    bash "scripts/installer/script-installer.sh" "`pwd`/$dir" "$DEST"

done

#bash "sh/script-installer.sh" "`pwd`/scripts/pieces" "$DEST"
#bash "SharedScripts/script-installer.sh" "`pwd`/scripts/fek" "$DEST"
#bash "SharedScripts/script-installer.sh" "`pwd`/scripts/utils" "$DEST"

