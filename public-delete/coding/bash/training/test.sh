#!/bin/bash

hello () {
  yourname=${1:-none}
  echo "-> Hello: ${yourname}"
}
