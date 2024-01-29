from pyzbar.pyzbar import decode
from PIL import Image

import pytesseract


def get_text_from_image(image_path):
    extracted_text = pytesseract.image_to_string(image_path)
    # Write the extracted text to a file
    image_path = image_path.split('/')[1].split('.')[0]
    with open(f'content/{image_path}.txt', 'w') as f:
        f.write(extracted_text)

    return extracted_text


def get_barcode_from_image(image_path):
    # Load the image
    image = Image.open(image_path)

    # Decode barcodes in the image
    barcodes = decode(image)
    if len(barcodes) == 0:
        return "No barcode detected"
    else:
        return barcodes[0].data.decode('utf-8')
