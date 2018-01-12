#!/bin/bash

echo "Building docs..."
mkdocs build --strict
if [ $? -ne 0 ]; then
    exit 1
fi
echo "Compiling Dictionary..."
aspell --lang=en create master ./tmp <.spell-dict
if [ $? -ne 0 ]; then
    exit 1
fi
echo "Checking spelling..."

let "fails=0"

for file in $(find site/ -type f -name "*.html"); do
    words=$(aspell list --lang=en --mode=html --add-html-skip=code --extra-dicts=./tmp  <$file)
    if [ "$words" ]; then
        uniquewords=$(tr ' ' '\n' <<< "${words[@]}" | sort -u | tr '\n' ' ')
        let "fails++"
        echo "Misspelled words in '$file':"
        echo "-----------------------------------------------------------------"
        for word in ${uniquewords[@]}; do
            echo $word
        done
        echo "-----------------------------------------------------------------"
    fi
done
rm -f ./tmp
rm -rf site

if [ $fails -gt 0 ]; then
    echo "$fails files with misspelled words."
    exit 1
else
    exit 0
fi
