#!/bin/bash
cd "$( cd "$( dirname "$0" )"; pwd )"

mkdir -p output
poetry run python -m tolino_notes \
--input-file tests/resources/notes.txt \
--output-dir output

find output -type f -iname "*.md" |while read f
do
    md5_left=$( md5 ${f} |awk '{print $4}' )
    md5_right=$( md5 ${f}.org |awk '{print $4}' )
    ident=$( if [ "$md5_left" == "$md5_right" ]; then echo "YES"; else echo "NO"; fi )
    echo $ident $md5_left $md5_right
done
