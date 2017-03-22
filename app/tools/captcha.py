# coding:utf-8
from PIL import Image, ImageDraw, ImageFont
import random
import string


class RandomChr(object):
    code = string.uppercase + string.lowercase + string.digits

    @classmethod
    def random_string(cls, digits=8):
        return random.sample(cls.code, digits)

    @classmethod
    def random_letter(cls):
        return random.choice(cls.code)

    # todo:random chinese words
    @classmethod
    def random_chinese(cls):
        pass


class ImageChar(RandomChr):
    """
    step 1: initial Image attributes
    step 2: draw one letter or number from random_string
    step 3: rotate image randomly
    step 4: add jitter to image
    step 5: merger all texts
    """
    font = ImageFont.truetype('msyh.ttc', 36) or ImageFont.truetype('consolas.ttc', 36)
    words = 8

    def __init__(self, mode="RGB", size=(480, 60), font_color=(0, 0, 0), bg_color=(255, 255, 255)):
        self.size = size
        self.weight, self.height = self.size
        self.fontColor = font_color
        self.bgColor = bg_color
        self.mode = mode
        self.image = Image.new(mode=self.mode, size=self.size, color=self.fontColor)

    @staticmethod
    def bg_color():
        return random.randint(64, 255), random.randint(64, 255), random.randint(64, 255)

    @staticmethod
    def font_color():
        return random.randint(32, 127), random.randint(32, 127), random.randint(32, 127)

    def draw(self):
        draw = ImageDraw.Draw(self.image)
        draw.text(xy=(8, 16), text=self.random_letter())
        del draw

    def rotate(self):
        pass

    def jitter(self, draw):
        """
        draw random lines as jitter
        :param draw:
        :return:
        """
        size1 = random.randint(0, self.weight), random.randint(0, self.height)
        size2 = random.randint(0, self.weight), random.randint(0, self.height)
        draw.line(size1 + size2, fill=128)
        del draw

    def merge(self):
        pass

    def captcha(self):
        l = ''
        draw = ImageDraw.Draw(self.image)

        weight, height = self.image.size
        for x in range(weight):
            for y in range(height):
                draw.point((x, y), fill=self.bg_color())

        for t in range(self.words):
            letter = self.random_letter()
            l += letter
            draw.text((60 * t + 10, 10), letter, font=self.font, fill=self.font_color())
            # todo：after draw text we need to rotate and jitter
            self.jitter(draw=draw)

        # print("captcha:", l)
        # self.image.show()
        return l, self.image


if __name__ == '__main__':
    print(ImageChar().captcha())