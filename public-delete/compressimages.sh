#!/bin/bash

for img in ./i/*; do
  echo -n "."
  if [[ $img == *.jpg ]] || [[ $img == *.png ]] || [[ $img == *.jpeg ]]; then
    dimensions=$(identify -format "%wx%h" "${img}")
    width=$(echo "${dimensions}" | cut -d'x' -f1)
    #height=$(echo $dimensions | cut -d'x' -f2)

    if [ $width -gt 1920 ]; then
      echo "- Resizing ${img}"
      convert "${img}" -resize '1920x>' "${img}"
    fi
  fi
done
