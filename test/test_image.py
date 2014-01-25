from PIL import Image
import pytest

from instagram_cl.image import UnicodeImage, UnicodePixel, UrwidImage


def get_test_image():
    image_filename = './test/image.jpg'
    return Image.open(image_filename)


@pytest.fixture
def unicode_image():
    return UnicodeImage(get_test_image())


@pytest.fixture
def urwid_image():
    return UrwidImage(get_test_image())


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

    def test_print(self, unicode_image):
        print unicode_image

    def test_get_pixel(self, unicode_image):
        assert isinstance(unicode_image.get_pixel(0, 0), UnicodePixel)

        height, width = unicode_image.array_dimensions
        assert isinstance(unicode_image.get_pixel(0, 0), UnicodePixel)
        assert isinstance(unicode_image.get_pixel(height-1, width-1),
                          UnicodePixel)


class TestUrwidImage:

    def test_heritage(self, urwid_image):
        assert isinstance(urwid_image, UnicodeImage)

    def test_format_pixel_colours(self, urwid_image):
        assert ('g46', 'g42') == urwid_image.format_pixel_colours(0, 0)

    def test_get_pixel_style_topleft(self, urwid_image):
        pixel_style = urwid_image.get_pixel_style(0, 0)
        assert ('0,0', '', '', '', 'g46', 'g42') == pixel_style

    def test_get_pixel_style_bottomright(self, urwid_image):
        height, width = urwid_image.array_dimensions
        pixel_style = urwid_image.get_pixel_style(height-1, width-1)
        assert ('30,74', '', '', '', 'g25', 'g8') == pixel_style

    def test_get_palette(self, urwid_image):
        height, width = urwid_image.array_dimensions
        palette = urwid_image.get_palette()
        assert len(palette) == width * height
        for x in range(height):
            for y in range(width):
                pixel_style = urwid_image.get_pixel_style(x, y)
                assert pixel_style in palette

    def test_get_pixel_row(self, urwid_image):
        height, width = urwid_image.array_dimensions
        for x in range(height):
            pixel_row = urwid_image.get_pixel_row(x)
            assert width == len(pixel_row)
