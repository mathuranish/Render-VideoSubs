#!/bin/bash
# Installing dependencies
# sudo apt-get install -y libglew-dev libglfw3-dev cmake gcc libcurl4-gnutls-dev tesseract-ocr libtesseract-dev libleptonica-dev clang libclang-dev

# Change directory to ccextractor/linux
cd ccextractor/linux

# Build ccextractor
# ./build

# Run ccextractor with the provided file name
./ccextractor "$1"