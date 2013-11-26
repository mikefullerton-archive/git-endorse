#!/bin/bash


files=`ls`

for f in $files; do
    if [ -d "$f" ]; then
        cd "$f"
        echo ""
        echo "#### ADDING: $f"
        create-gh-repo "mikefullerton" || { exit 1; }
        cd ".."
    fi
done

echo "#### All done!!"
