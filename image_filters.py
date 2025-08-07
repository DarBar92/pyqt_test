import os
import numpy as np
from PIL import Image, ImageFilter
from io import BytesIO
from PyQt6.QtGui import QPixmap

def filter(type, image):
    filter_map = {
        "none": lambda img: img,
        "grayscale": filter_grayscale,
        "sepia": filter_sepia,
        "invert": filter_invert,
        "blur": filter_blur,
        "sharpen": filter_sharpen,
        "cartoon": filter_cartoon,
        "emboss": filter_emboss,
        "edge_enhance": filter_edge_enhance
    }
    func = filter_map.get(type)
    if func:
        return func(image)
    return image
    
def filter_grayscale(image):
    img = Image.open(image)
    grayscale_img = img.convert("L")
    img_format = get_image_format(image)
    buf = BytesIO()
    grayscale_img.save(buf, format=img_format)
    buf.seek(0)
    print(f"Grayscale image saved to {buf}")
    return buf

def filter_sepia(image):
    img = Image.open(image).convert("RGB")
    np_img = np.array(img)
    img_format = get_image_format(image)
    sepia_matrix = np.array([[0.393, 0.769, 0.189],
                       [0.349, 0.686, 0.168],
                       [0.272, 0.534, 0.131]])

    sepia_img = np_img @ sepia_matrix.T
    sepia_img = np.clip(sepia_img, 0, 255).astype(np.uint8)
    
    sepia_pil = Image.fromarray(sepia_img)
    buf = BytesIO()
    sepia_pil.save(buf, format=img_format)
    buf.seek(0)
    print(f"Sepia image saved to {buf}")
    return buf

def filter_invert(image):
    img = Image.open(image).convert("RGB")
    img_format = get_image_format(image)
    inverted_img = Image.fromarray(255 - np.array(img))
    buf = BytesIO()
    inverted_img.save(buf, format=img_format)
    buf.seek(0)
    print(f"Inverted image saved to {buf}")
    return buf

def filter_blur(image):
    img = Image.open(image).convert("RGB")
    img_format = get_image_format(image)
    blurred_img = img.filter(ImageFilter.BLUR)
    buf = BytesIO()
    blurred_img.save(buf, format=img_format)
    buf.seek(0)
    print(f"Blurred image saved to {buf}")
    return buf

def filter_sharpen(image):
    img = Image.open(image).convert("RGB")
    img_format = get_image_format(image)
    sharpened_img = img.filter(ImageFilter.SHARPEN)
    buf = BytesIO()
    sharpened_img.save(buf, format=img_format)
    buf.seek(0)
    print(f"Sharpened image saved to {buf}")
    return buf

def filter_cartoon(image):
    img = Image.open(image).convert("RGB")
    img_format = get_image_format(image)

    # Step 1: Reduce colors (posterize)
    # You can adjust 'bits' for more/less quantization
    posterized_img = img.convert("P", palette=Image.ADAPTIVE, colors=16).convert("RGB")

    # Step 2: Edge detection
    edges = img.filter(ImageFilter.FIND_EDGES)
    edges = edges.convert("L").point(lambda x: 0 if x < 80 else 255, '1')
    edges = edges.filter(ImageFilter.MaxFilter(3))  # Thicken edges

    # Step 3: Combine posterized image and edges
    cartoon_img = Image.composite(posterized_img, Image.new("RGB", img.size, "white"), edges)

    buf = BytesIO()
    cartoon_img.save(buf, format=img_format)
    buf.seek(0)
    print(f"Cartoon image saved to {buf}")
    return buf

def filter_emboss(image):
    img = Image.open(image).convert("RGB")
    img_format = get_image_format(image)
    embossed_img = img.filter(ImageFilter.EMBOSS)
    buf = BytesIO()
    embossed_img.save(buf, format=img_format)
    buf.seek(0)
    print(f"Embossed image saved to {buf}")
    return buf

def filter_edge_enhance(image):
    img = Image.open(image).convert("RGB")
    img_format = get_image_format(image)
    enhanced_img = img.filter(ImageFilter.EDGE_ENHANCE)
    buf = BytesIO()
    enhanced_img.save(buf, format=img_format)
    buf.seek(0)
    print(f"Edge enhanced image saved to {buf}")
    return buf

def applyAndShowFilter(self, filter_type, image_path):
    buf = filter(filter_type, image_path)
    pixmap = QPixmap()
    pixmap.loadFromData(buf.getvalue())
    self.image_label.setPixmap(pixmap)
    return buf

def get_image_format(image_path):
    ext = os.path.splitext(image_path)[1].lower().replace('.', '')
    format_map = {
        'jpg': 'JPEG',
        'jpeg': 'JPEG',
        'png': 'PNG',
        'bmp': 'BMP',
        'gif': 'GIF'
    }
    return format_map.get(ext, 'JPEG')