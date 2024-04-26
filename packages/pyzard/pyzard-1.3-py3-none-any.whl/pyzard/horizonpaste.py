from PIL import Image, ImageDraw, ImageFont
import numpy as np


def horizonpaste(up, down):
    """
    이미지 수직 이어붙이기.
    """
    ux, uy = up.size
    dx, dy = down.size
    roundback = Image.new(
        'RGB', ((ux), (uy+dy)), (255, 255, 255))
    roundback.paste(up, (0, 0))
    roundback.paste(down, (0, uy))
    return roundback
