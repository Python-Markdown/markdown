#!/bin/bash

echo "Checking links in documentation..."

# List of files in docs dir
docs=$(find . -path './docs/*.md')
# List of files in project root (README, etc)
extras=$(find . -maxdepth 1 -name '*.md')
# Combined list of files to check
files=("${docs[@]}" "${extras[@]}")

let "fails=0"
let "count=0"

for file in ${files[@]}; do
    let "count++"
    markdown-link-check -q "$file"
    if [ $? -ne 0 ]; then
        let "fails++"
    fi
done

echo -e "\n\033[0;33m$count files checked."

if [ $fails -gt 0 ]; then
    echo -e "\033[0;31mERROR: $fails files with dead links found!"
    exit 1
else
    echo -e "\033[0;32mCongratulations! No dead links found."
    exit 0
fi
