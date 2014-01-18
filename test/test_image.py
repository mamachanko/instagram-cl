from PIL import Image

from instagram_cl.image import UnicodeImage, UnicodePixel


class TestUnicodePixel:

    def test_instantiation(self):
        unicode_pixel = UnicodePixel(u'\u0041',
                                     background_colour=0,
                                     character_colour=24)
        assert unicode_pixel.character == u'\u0041'
        assert unicode_pixel.background_colour == 0
        assert unicode_pixel.character_colour == 24

    def test_as_ansii_seq(self):
        unicode_pixel = UnicodePixel(u'\u0041',
                                     background_colour=0,
                                     character_colour=24)
        # assert u'\033[48;5;{0}m\033[38;5;{1}m{2}\033[0m'
        assert u'\033[48;5;0m\033[38;5;24m\u0041\033[0m' == unicode_pixel.ansii_sequence


class TestUnicodeImage:

    def test_fail(self):
        image_filename = './test/image.jpg'
        image = Image.open(image_filename)
        unicode_image = UnicodeImage(image)
