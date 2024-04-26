from PIL import Image, ImageDraw, ImageFont
import numpy as np


def alpacomposite(bigone, smallone, locate):
    """
    bigone이미지에 smallone 이미지를 붙여넣는 함수.
    """
    tagetx, targety = locate

    onex, oney = bigone.size
    background = Image.new('RGBA', (onex, oney), (255, 255, 255, 0))

    background.paste(smallone, (tagetx, targety))
    final = Image.alpha_composite(bigone, background)
    return final
