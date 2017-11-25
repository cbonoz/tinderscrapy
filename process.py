import numpy as np
import pandas as pd
import pytesseract
import re
import os
import requests
import os.path

try:
    import Image
except ImportError:
    from PIL import Image

data = pd.read_csv('./tinder.csv', header=0)
print(data.info())

def parse_text_from_image(frame):
    pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
    screen_text = pytesseract.image_to_string(frame)
    return screen_text

def get_image(image_url):
    img_extension = image_url.split('/')[-1]
    img_file = './images/%s' % img_extension

    if not os.path.isfile(img_file):
        # Retrieve and save the file.
        img_data = requests.get(image_url).content
        with open(img_file, 'wb') as handler:
            handler.write(img_data)
    else:
        print('using cached image', img_file)

    return Image.open(img_file)

def process_image_url(url):
    image = get_image(url)
    width = image.size[0]
    height = image.size[1]
    return parse_text_from_image(image)

def process_texts(texts):
    texts = list(filter(lambda x: x and (not x.isspace()) and ('PM' not in x) and ('AM' not in x) and ('Type a message' not in x), texts))
    start = 0
    for i, text in enumerate(texts):
        if 'you ma' in text.lower():
            start = i
            break
    if start + 1 < len(texts):
        texts = texts[start+1:]
    if 'sent' in texts[-1]:
        texts = texts[:-1]
    return texts

def main():
    images = list(data['url'])
    processed = []
    for i, url in enumerate(images[:]):
        print('Processing Image #%d: %s' % (i, url))
        screen_text = process_image_url(url)
        screen_text = screen_text.split('\n')
        print('screen text: %s' % screen_text)
        try:
            texts = process_texts(screen_text)
        except Exception as e:
            print('error processing screen text', url, e)
            continue
        conversation = ' '.join(texts)
        print(url, conversation)
        processed.append({"url": url, "conversation": conversation})

    convs = pd.DataFrame(processed)
    convs.to_csv('./conversations.csv')

if __name__ == '__main__':
    main()