from nbtlib import parse_nbt
import os
from PIL import Image, ImageOps


pattern = {"b": "base",
         "bo": "borber",
         "bri": "bricks",
         "mc": "circle",
         "cre": "creeper",
         "cr": "cross",
         "cbo": "curly_border",
         "ld": "diagonal_left",
         "rud": "diagonal_right",
         "lud": "diagonal_up_left",
         "rd": "diagonal_up_right",
         "flo": "flower",
         "glb": "globe",
         "gra": "gradient",
         "gru": "gradient_up",
         "hh": "half_horizontal",
         "hhb": "half_horizontal_bottom",
         "vh": "half_vertical",
         "vhr": "half_vertical_right",
         "moj": "mojang",
         "pig": "piglin",
         "mr": "rhombus",
         "sku": "skull",
         "ss": "small_stripes",
         "bl": "square_bottom_left",
         "br": "square_bottom_right",
         "tl": "square_top_left",
         "tr": "square_top_right",
         "sc": "straight_cross",
         "bs": "stripe_bottom",
         "cs": "stripe_center",
         "dls": "stripe_down_left",
         "drs":  "stripe_down_right",
         "ls": "stripe_left",
         "ms":  "stripe_middle",
         "rs":  "stripe_right",
         "ts": "stripe_top",
         "bt": "triangle_bottom",
        "tt": "triangle_top",
        "bts": "triangles_bottom",
        "tts": "triangles_top"}

def createImg(layers: dict, name: str):
    new_image = Image.new('RGB', (20, 40), (250, 250, 250))

    for key in layers.keys():
        if 'b' not in layers:
            img = Image.open(f'./MineBannerLib/samples/base.png')
            new_image.paste(img, (0, 0))

        img = Image.open(f'./MineBannerLib/samples/{pattern[key]}.png')
        imgcol = ImageOps.colorize(img, white='red', black="black")
        new_image.paste(imgcol, (0, 0))

    if not os.path.exists('./buildbanner/'):
        os.mkdir('./buildbanner')
    new_image.save(f'./buildbanner/{name}.jpg', "JPEG")


def getPartsFlag(nbts):
    comp = parse_nbt(nbts)
    tags = dict()
    for i in comp['BlockEntityTag']['Patterns']:
        tags[i['Pattern']] = i['Color']
    return (tags)


def create_banner(name: str, json: str):
    createImg(getPartsFlag(json), name)

create_banner('test', '{BlockEntityTag:{Patterns:[{Color:14,Pattern:"cre"},{Color:4,Pattern:"sku"}]}}')
