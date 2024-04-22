# import the necessary packages
import os
import sys
import cv2
from pyzbar.pyzbar import decode

# Function to load image from the folder


def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = os.path.join(folder, filename)
        if img is not None:
            images.append(img)
    return images

# Function to detect barcode from the file


def BarcodeReader(image):

    img = cv2.imread(image)

    if img is None:
        print(f"Error: Image at {image} could not be read.")
        return None, None

    detectedBarcodes = decode(img)

    if not detectedBarcodes:
        return None, None
    else:
        for barcode in detectedBarcodes:
            if barcode.data != "":
                return barcode.data, barcode.type


def write_text_file(path, file, barcode, type):
    if barcode is not None and type is not None:
        newline = path + ',' + '' + str(type) + ':' + str(barcode) + '\n'
        file.write(newline)


def main():
    folder = sys.argv[1]
    eancode = sys.argv[2]

    images = load_images_from_folder(folder)
    file = open(eancode, 'w')

    for image in images:
        path = os.path.basename(os.path.normpath(image))
        barcode, type = BarcodeReader(image)
        write_text_file(path, file, barcode, type)

    file.close()


if __name__ == "__main__":
    main()
