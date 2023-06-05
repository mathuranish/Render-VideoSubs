#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
# installing ccextractor
sudo apt-get install -y libglew-dev libglfw3-dev cmake gcc libcurl4-gnutls-dev tesseract-ocr libtesseract-dev libleptonica-dev clang libclang-dev
cd ccextractor/linux

# Build ccextractor
./build
cd..
cd..

python manage.py collectstatic --no-input
python manage.py migrate