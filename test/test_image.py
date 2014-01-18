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
        ansii_sequence = unicode_pixel.ansii_sequence
        assert u'\033[48;5;0m\033[38;5;24m\u0041\033[0m' == ansii_sequence


class TestUnicodeImage:

    def test_print(self):
        image_filename = './test/image.jpg'
        image = Image.open(image_filename)
        unicode_image = UnicodeImage(image)
        print unicode_image

    def test_get_pixel(self):
        image_filename = './test/image.jpg'
        image = Image.open(image_filename)
        unicode_image = UnicodeImage(image)
        assert isinstance(unicode_image.get_pixel(0, 0), UnicodePixel)

        height, width = unicode_image.array_dimensions
        assert isinstance(unicode_image.get_pixel(0, 0), UnicodePixel)
        assert isinstance(unicode_image.get_pixel(height-1, width-1),
                          UnicodePixel)
