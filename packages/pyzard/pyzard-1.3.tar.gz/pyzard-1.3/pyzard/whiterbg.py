from PIL import Image


def whiterbg(png):
    image1 = png

    imag1_size = image1.size

    background = Image.new("RGB", (imag1_size), (255, 255, 255))
    background.paste(image1, mask=image1.split()[3]) # 3 is the alpha channel
    background.convert('RGB')
    return background