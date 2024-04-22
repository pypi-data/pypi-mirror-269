# Qrscanner
A simple python repo for scanning Qr code from images and writing its EAN code to a text file.
## How to use
For ubuntu the command to run the code is:
`python /path/to/readbc.py /path/to/barcodes eancodes.txt`
## Create Docker
Use `sudo docker image build -t python:0.0.1` in Qrscanner folder to create docker image.
## Run docker
Use `sudo docker run python:0.0.1` 
