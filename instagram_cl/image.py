import math
import sys

from PIL import Image, ImageOps


class UnicodePixel(object):

    def __init__(self, character, background_colour, character_colour):
        self.character = character
        self.background_colour = background_colour
        self.character_colour = character_colour

    @property
    def ansii_sequence(self):
        return '\033[48;5;{0}m\033[38;5;{1}m{2}\033[0m'.format(
            self.background_colour,
            self.character_colour,
            self.character)

    def __repr__(self):
        return self.ansii_sequence


class UnicodeImage(object):
    XTERM_GRAY_OFFSET = 232
    ADJUST_FACTOR = 1.5
    SCALE = 256/24.

    def __init__(self, image, width=150):
        self.original_image = image
        self.ratio = .75 / .9
        self.dimensions = (width, int(width * self.ratio))
        self.width, self.height = self.dimensions
        image = self.original_image.resize(self.dimensions, Image.BILINEAR)
        self.image = ImageOps.grayscale(image)
        self.pixels = self.image.load()

    def __repr__(self):
        return '\n'.join(''.join(map(str, row)) for row in self.as_array)

    def get_pixel(self, x, y):
        return self.as_array[x][y]

    @property
    def array_dimensions(self):
        image_array = self.as_array
        return len(image_array), len(image_array[0])

    @property
    def as_array(self):
        try:
            return self._image_array
        except AttributeError:
            self._image_array = self._as_array()
            return self._image_array

    def _as_array(self):
        pixel_values = []
        image_array = []
        for y in range(self.height/4):
            row = []
            braille_char_row = []
            background_colour_before, text_colour_before = None, None
            for x in range(self.width/2):

                pixel_octet = []
                for i in range(8):
                    a = x * 2 + ((i & 4) >> 2)
                    b = y * 4 + (i & 3)
                    pixel = self.pixels[a, b]
                    pixel_values.append(pixel)
                    pixel_octet.append(pixel)

                pixel_octet_values = self.get_values_for_pixel_octet(
                    pixel_octet)
                background_color, text_color, braille_char = pixel_octet_values
                row.append(UnicodePixel(braille_char,
                                        background_color,
                                        text_color))

            image_array.append(row)

        return image_array


    def get_braille_chars(self):
        pass

    def extract_gray_values(self, pixel_octet):
        lower_bound = self.encode_gray_value(min(pixel_octet))
        upper_bound = self.encode_gray_value(max(pixel_octet), ceil=True)

        return lower_bound, upper_bound

    def distance(self, v1, v2):
        return abs(v1 - v2)

    def encode_gray_value(self, gray_value, ceil=False):
        gray_value /= self.SCALE
        if ceil:
            gray_offset = int(math.ceil(gray_value))
        else:
            gray_offset = int(math.floor(gray_value))
        return self.XTERM_GRAY_OFFSET + gray_offset

    def decode_gray_value(self, gary_value):
        return int((gary_value - self.XTERM_GRAY_OFFSET) * self.SCALE)

    def get_values_for_pixel_octet(self, pixel_octet):
        background_color, maximum_gray = self.extract_gray_values(pixel_octet)

        gray_window = self.distance(maximum_gray, background_color)
        gray_value = gray_window * self.ADJUST_FACTOR
        text_color_offset = int(
            background_color + gray_value) - self.XTERM_GRAY_OFFSET
        text_color_offset = max(0, min(23, text_color_offset))
        text_color = self.XTERM_GRAY_OFFSET + text_color_offset

        braille_char = self.get_braille_char(pixel_octet,
                                             background_color,
                                             maximum_gray)

        return background_color, text_color, braille_char

    def get_braille_char(self, pixel_octet, background_color, maximum_gray):

        def make_dots(current, next):
            is_set = self.is_dot_set(pixel_octet[next],
                                     background_color,
                                     maximum_gray)
            return current | (is_set << next)

        braille_char = reduce(make_dots, range(8), 0)
        braille_char = self.dot(braille_char)

        return braille_char.encode('utf8')

    def is_dot_set(self, gray_value, background_color, maximum_gray):
        background_color = self.decode_gray_value(background_color)
        maximum_gray = self.decode_gray_value(maximum_gray)

        if self.distance(background_color, maximum_gray) == 0:
            return True

        gray_window = self.distance(background_color, maximum_gray)
        gray_value_offset = self.distance(gray_value, background_color)
        gray_ratio = float(gray_value_offset) / gray_window
        x = math.exp(-gray_window * (gray_ratio - 0.5))
        normalised_distance = 1. / (x + 1)

        return .5 < normalised_distance

    def dot(self, bits):
        bits = bits & 0b111 | (bits & 112) >> 0b1 | (bits & 0b1000) << 0b11 | bits & 0b10000000
        return unichr(0x2800 + bits)


class UrwidImage(UnicodeImage):

    def get_pixel_style(self, x, y):
        unicode_pixel = self.get_pixel(x, y)
        style_name = '{0},{1}'.format(x, y)
        foreground_colour = int(round((unicode_pixel.character_colour - 231) * (100/24.)))
        background_colour = int(round((unicode_pixel.background_colour - 231) * (100/24.)))
        return (style_name,
                '', '', '',
                'g{}'.format(foreground_colour),
                'g{}'.format(background_colour))

    def get_palette(self):
        palette = []
        height, width = self.array_dimensions
        for x in range(height):
            for y in range(width):
                palette.append(self.get_pixel_style(x, y))
        return palette


if __name__ == "__main__":
    if len(sys.argv) > 1:
        image_filename = sys.argv[1]
    else:
        image_filename = './test/image.jpg'

    image = Image.open(image_filename)
    unicode_image = UnicodeImage(image)
    print unicode_image
