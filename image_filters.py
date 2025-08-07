import numpy as np
from PIL import Image
from io import BytesIO
from PyQt6.QtGui import QPixmap

def filter(type, image):
    if type == "grayscale":
        return filter_grayscale(image)
    if type == "sepia":
        return filter_sepia(image)
    if type == "invert":
        return filter_invert(image)
    # Add other filter types as needed
    return image

def filter_grayscale(image):
    img = Image.open(image)
    grayscale_img = img.convert("L")
    buf = BytesIO()
    grayscale_img.save(buf, format="JPEG")
    buf.seek(0)
    print(f"Grayscale image saved to {buf}")
    return buf

def filter_sepia(image):
    img = Image.open(image)
    np_img = np.array(img)
    pixels = img.load()  # Create the pixel map

    sepia_matrix = np.array([[0.393, 0.769, 0.189],
                       [0.349, 0.686, 0.168],
                       [0.272, 0.534, 0.131]])

    sepia_img = np_img @ sepia_matrix.T
    sepia_img = np.clip(sepia_img, 0, 255).astype(np.uint8)
    
    sepia_pil = Image.fromarray(sepia_img)
    buf = BytesIO()
    sepia_pil.save(buf, format="JPEG")
    buf.seek(0)
    print(f"Sepia image saved to {buf}")
    return buf

def filter_invert(image):
    img = Image.open(image)
    inverted_img = Image.fromarray(255 - np.array(img))
    buf = BytesIO()
    inverted_img.save(buf, format="JPEG")
    buf.seek(0)
    print(f"Inverted image saved to {buf}")
    return buf

def applyAndShowFilter(self, filter_type, image_path):
    buf = filter(filter_type, image_path)
    pixmap = QPixmap()
    pixmap.loadFromData(buf.getvalue())
    self.image_label.setPixmap(pixmap)
    return buf
