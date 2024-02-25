#!/usr/bin/python
# -*- coding:utf-8 -*-

from waveshare_epd import epd7in5bc

from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont
from wand.image import Image as WandImage

import io
import time
import urllib.request


api_key = ""
if (api_key == ""):
    print("Please provide a valid OpenAI API key.")
    exit()

client = OpenAI(api_key=api_key)
generation_prompt = "A turned over ink bottle. The ink is spilling from it and the puddle has the shape of a cat."

# images can only be drawn on the display if their 
# resolution exactly matches the size of the display
display_width = 640
display_height = 384

def dalle_img():
    print("generating the image with dall-e")
    response = client.images.generate(
        model="dall-e-3",
        prompt=generation_prompt,
        size="1792x1024",
        quality="hd",
        n=1
    )

    image_url = response.data[0].url

    date = time.strftime('%Y.%m.%d-%H:%M:%S')
    img_filename = f"img/image-{date}.png"

    print("downloading the image")
    urllib.request.urlretrieve(image_url, img_filename)

    return img_filename


def convert_image(filename):
    red_image = None
    black_image = None

    try:
        with WandImage(filename=filename) as img:
            print("resizing the image to match the display size")
            img.resize(display_width, display_height)

            print("remapping image colors")
            with WandImage() as palette:
                with WandImage(width = 1, height = 1, pseudo ="xc:red") as red:
                    palette.sequence.append(red)
                with WandImage(width = 1, height = 1, pseudo ="xc:black") as black:
                    palette.sequence.append(black)
                with WandImage(width = 1, height = 1, pseudo ="xc:white") as white:
                    palette.sequence.append(white)
                palette.concat()
                img.remap(affinity=palette, method='floyd_steinberg')
                
                print("generating red and black bitmaps")
                red = img.clone()
                black = img.clone()
                red.opaque_paint(target='black', fill='white') # replace red pixels with white, so only the blacks remain
                black.opaque_paint(target='red', fill='white') # replace black pixels with white, so only the reds remain
                
                red_image = Image.open(io.BytesIO(red.make_blob("bmp")))
                black_image = Image.open(io.BytesIO(black.make_blob("bmp")))

    except Exception:
        print("Exception in convert_image, exiting.")
        exit()

    return (red_image, black_image)


try:
    img_filename = dalle_img()
    red_image, black_image = convert_image(img_filename)

    print("initializing the display")
    epd = epd7in5bc.EPD()
    epd.init()
    epd.Clear()

    time.sleep(1)

    print("displaying the final image")
    epd.display(epd.getbuffer(black_image), epd.getbuffer(red_image))

except KeyboardInterrupt:    
    epd7in5bc.epdconfig.module_exit(cleanup=True)
    exit()
