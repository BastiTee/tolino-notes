#!/bin/bash
cd "$( cd "$( dirname "$0" )"; pwd )"
set -eof pipefail

mkdir -p output

poetry run python -m tolino_notes \
--input-file ~/Downloads/notes.txt \
--output-dir ~/Downloads/notes-output \
--verbose

poetry run python -m tolino_notes \
--input-file ~/Downloads/notes.txt \
--output-dir ~/Downloads/notes-output \
--format json \
--verbose

find ~/Downloads/notes-output -type f -iname "*.md" |while read f
do
    md5_left=$( md5 ${f} |awk '{print $4}' )
    md5_right=$( md5 ${f}.org |awk '{print $4}' )
    ident=$( if [ "$md5_left" == "$md5_right" ]; then echo "YES"; else echo "NO"; fi )
    echo $ident $md5_left $md5_right
done
