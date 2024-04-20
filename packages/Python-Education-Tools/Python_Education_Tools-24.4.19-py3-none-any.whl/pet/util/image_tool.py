from PIL import Image
import numpy as np
def img_to_ndarray(filename):
    return np.array(Image.open(filename))

def img_info(filename):
    image = Image.open(filename)
    info=dict(format=image.format,size=image.size,mode=image.mode)
    return info
def file_to_img(filename):
    return Image.open(filename)
def ndarray_to_img(ndar):
    return Image.fromarray(ndar)
def save(img,out_filename):
    img.save(out_filename)

