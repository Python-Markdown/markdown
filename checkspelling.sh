#!/bin/bash

echo "Building docs..."
python setup.py --quiet build_docs --force
echo "Compiling Dictionary..."
aspell --lang=en create master ./tmp <.spell-dict
echo "Checking spelling...\n"

let "fails=0"

for file in $(find build/docs/ -type f -name "*.html"); do
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
rm -rf build

if [ $fails -gt 0 ]; then
    echo "$fails files with misspelled words."
    exit 1
else
    exit 0
fi
