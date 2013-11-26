#!/bin/sh

#  script-installer.sh
#
#  Created by Mike Fullerton on 7/27/13.
#

set -e

MY_PATH="`dirname \"$0\"`"              
MY_PATH="`( cd \"$MY_PATH\" && pwd )`"  

SOURCE_FILES_PATH="$1"
FOLDER_NAME=`basename "$1"`
DEST_PATH="$2/$FOLDER_NAME"

# reset install folder

if [ -d "$DEST_PATH" ]; then
    rm -rd "$DEST_PATH"
fi

mkdir -p "$DEST_PATH"
chmod u+rwx "$DEST_PATH"

# install scripts

# cd "$SOURCE_FILES_PATH"

FILES=`ls $SOURCE_FILES_PATH`
for file in $FILES; do
    src="$SOURCE_FILES_PATH/$file"
    dest="$DEST_PATH/$file"

    echo "src = $src"
    echo "dest = $dest"

    extension=${file##*.}

    if [[ "$extension" == "sh" ]] || [[ "$extension" == "py" ]]; then
        filename_no_extension=`basename "$file" .$extension`
        dest="$DEST_PATH/$filename_no_extension"
    fi

    cp -R "$src" "$dest" || { echo "unable to copy script to: $dest"; exit 1; }
    echo "# installed: \"$dest\""
done

script_dir_file="$DEST_PATH/script-dir"
echo "#!/bin/bash" > "$script_dir_file"
echo "echo \"$DEST_PATH\"" > "$script_dir_file"

chmod -R u+rwx "$DEST_PATH" || { echo "unable to change permissions on: $DEST_PATH"; exit 1; }

# update profile files

function append_path_to_file() {
    local the_file="$1"

    if [ -f "$the_file" ]; then
        # this deletes the line
        sed -i -e "/$FOLDER_NAME/d" "$the_file"
#        echo "$cmd"
    fi

    # this adds the line back
    echo "export PATH=\"\$PATH:$DEST_PATH\"" >> "$the_file"
    echo "# updated: $the_file"
}

# bash
append_path_to_file "$HOME/.bash_profile"

# c and korn
append_path_to_file "$HOME/.login"
append_path_to_file "$HOME/.profile"

echo "# for your copy/paste pleasure: "
echo "open \"$DEST_PATH\""
echo "cd \"$DEST_PATH\""

echo ""
echo "# Note please restart your terminal session (so the PATH variable is updated)"
echo ""


