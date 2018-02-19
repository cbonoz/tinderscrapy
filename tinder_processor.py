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

class TinderProcessor:

    def __init__(self, tinder_file='./tinder.csv'):
        self.tinder_file = tinder_file
        self.data = pd.read_csv(tinder_file, header=0)
        print(self.data.info())

    def parse_text_from_image(self, frame):
        pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
        screen_text = pytesseract.image_to_string(frame)
        return screen_text

    def get_image(self, image_url):
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

    def process_image_url(self, url):
        image = self.get_image(url)
        # width = image.size[0]
        # height = image.size[1]
        return self.parse_text_from_image(image)

    def process_texts(self, texts):
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

    def run(self):
        images = list(self.data['url'])
        processed = []
        for i, url in enumerate(images[:]):
            print('Processing Image #%d: %s' % (i, url))
            screen_text = self.process_image_url(url)
            screen_text = screen_text.split('\n')
            print('screen text: %s' % screen_text)
            try:
                texts = self.process_texts(screen_text)
            except Exception as e:
                print('error processing screen text', url, e)
                continue
            conversation = ' '.join(texts)
            print(url, conversation)
            processed.append({"url": url, "conversation": conversation})

        convs = pd.DataFrame(processed)
        output_file = None
        if '_' in self.tinder_file:
            # ex: tinder_1519057231.csv -> 1519057231
            ts = self.tinder_file.split('_')[1].split('.')[0]
            output_file = './conversations_%s.csv' % ts
        else:
            output_file = './conversations.csv'

        convs.to_csv(output_file)

if __name__ == '__main__':
    tinder_file = '/Users/cbuonocore/personal/python/tinderspider/tinder_1519057231.csv'
    tp = TinderProcessor(tinder_file)
    tp.run()