#!/bin/bash

# find the X most recently modified markdown files
files=$(find content -name "*.md" -printf '%T@ %p\n' | ag -v '_index.md|README.md|p8|y0emvc09|_todos.md' | sort -n | tail -10 | cut -f2- -d" ")
files=$(echo "$files" | tac)

# initialize an empty JSON array
json='[]'

# loop over the files
for file in $files; do
    # get the modification time and file name
    #filename=$(basename "$file")
    modtime=$(date -d "$(stat -c %y "$file")" '+%m-%d-%Y %H:%M')
    filename=$(echo $file | sed "s/^content\//\//g" | sed "s/.md$//g")

    # Get title from .md or .md posts
    filetitle=$(cat $file | grep -m 1 '^# ' | sed 's/# //g')
    if [ -z "$filetitle" ]; then
          filetitle=$(cat $file | ag "title.*=" | sed 's/title.*=//' | sed 's/"//g')
    fi

    # Get the category
    category=""
    IFS='/' read -ra array <<< "$filename"
    if [ "${#array[@]}" -ge 3 ]; then
        category="${array[1]}"
    fi

    if [ -z "$filetitle" ]; then
        continue;
    fi
    if [ -z "$category" ]; then
        continue;
    fi

    # add a new JSON object to the array
    json=$(jq -n --arg m "$modtime" --arg f "$filename" --arg t "$filetitle" --arg c "$category" \
      --argjson j "$json" '$j + [{modtime: $m, filename: $f, title: $t, category: $c}]')
done

# write the JSON to the file
echo "$json" > recents.json
