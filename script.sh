#!/bin/sh

FILE_NAME="$1"
OUTPUT_FILE="$2"

for word in $(cat $FILE_NAME); do
    #Verify if the word is URL
    case "$word" in
    *.*)
      #Prepend http://
      python main.py "http://$word" >> "$OUTPUT_FILE"
      ;;
  esac

done