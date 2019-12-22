import json
import os
from PIL import ImageFont, Image


def loadConfig(path):
    with open(path, 'r') as jsonConfig:
        data = json.load(jsonConfig)
        return data


def _makeFont(name, size):
    font_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            'fonts',
            name
        )
    )
    return ImageFont.truetype(font_path, size)


def makeFonts():
    font = _makeFont("Dot Matrix Regular.ttf", 10)
    fontBold = _makeFont("Dot Matrix Bold.ttf", 10)
    fontBoldTall = _makeFont("Dot Matrix Bold Tall.ttf", 10)
    fontBoldLarge = _makeFont("Dot Matrix Bold.ttf", 20)
    return {
        "font": font,
        "fontBold": fontBold,
        "fontBoldTall": fontBoldTall,
        "fontBoldLarge": fontBoldLarge
    }
