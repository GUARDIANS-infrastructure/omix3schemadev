#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
DICT_DIR="$SCRIPT_DIR/../dictionary"

echo "SCRIPT_DIR is: $SCRIPT_DIR"
echo "Source prod_dict path: $DICT_DIR/prod_dict"
echo "Destination path: $DICT_DIR/test_dict"

if [ -d "$DICT_DIR/test_dict" ]; then
    read -p "Are you sure you want to overwrite the test dictionary? (y/N): " confirm
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        echo "Removing existing test_dict at: $DICT_DIR/test_dict"
        rm -r "$DICT_DIR/test_dict"
    else
        echo "Aborting."
        exit 1
    fi
fi

mkdir "$DICT_DIR/test_dict"
echo "Copying $DICT_DIR/prod_dict to $DICT_DIR/test_dict ..."
cp -r "$DICT_DIR/prod_dict/" "$DICT_DIR/test_dict"

echo "Copied prod dictionary to test_dict."
