from PIL import Image, ImageOps
from tesserocr import PyTessBaseAPI, RIL
from enum import Enum


class HOCRParser():
    def __init__(self):
        self.api = PyTessBaseAPI()


    def load_image(self, image):
        self.api.SetImage(image)


    def get_all_with_tag(self, tag):
        convert = {
            'block' : RIL.BLOCK,
            'para' : RIL.PARA,
            'line' : RIL.TEXTLINE,
            'word' : RIL.WORD,
            'char' : RIL.SYMBOL
        }
        boxes = self.api.GetComponentImages(convert[tag], True, raw_image=True, raw_padding=5)

        for (im, box, _, _) in boxes:
            # im is a PIL image object
            # box is a dict with x, y, w and h keys
            self.api.SetRectangle(box['x'], box['y'], box['w'], box['h'])
            ocrResult = self.api.GetUTF8Text()
            conf = self.api.MeanTextConf()

            """attempts = 0
            while conf < 80 and attempts < 2:
                attempts += 1

                im = ImageOps.invert(im)
                self.api.SetImage(im)

                ocrResult = self.api.GetUTF8Text()
                conf = self.api.MeanTextConf()"""
            yield [box, ocrResult, im]

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.api.End()


if __name__ == "__main__":
    
    image = Image.open(r'/Users/jasorein/Documents/Autogreener/data/input/ss.png')

    hocr = HOCRParser()

    hocr.load_image(image)

    paras = hocr.get_all_with_tag('line')

    boxes, text, images = list(zip(*paras))
    
    # Debug print result
    [print(f'{b}, {r}') for b,r in zip(boxes, text)]
    print(f'Total: {len(boxes)} results')
