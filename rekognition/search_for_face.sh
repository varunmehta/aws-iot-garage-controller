#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: ./searc_for_face <FILE_NAME>"
fi

aws rekognition search-faces-by-image \
    --image '{"S3Object":{"Bucket":"carpen9000-rekognition","Name":"test/'$1'"}}' \
    --collection-id "CarPen9000"