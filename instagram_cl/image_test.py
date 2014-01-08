from bisect import bisect
import os
import random

from PIL import Image
import requests


class AsciiImage(object):

    greyscale = [
        " ",
        " ",
        ".,",
        "_ivc=!/|\\~",
        "gjez2]/(YL)t[+T7Vf",
        "mdK4ZGbNDXY5P*Q",
        "W8KMAB",
        "#%$@"
        ]

    # using the bisect class to put luminosity values
    # in various ranges.
    # these are the luminosity cut-off points for each
    # of the 7 tonal levels. At the moment, these are 7 bands
    # of even width, but they could be changed to boost
    # contrast or change gamma, for example.
    zonebounds=[36, 72, 108, 144, 180, 216, 252]

    ratio = 37. / 89.

    def __init__(self, image_path, width=50):
        self.image = Image.open(image_path)
        self.width = width
        self.dimensions = (self.width, int(self.width*self.ratio))

    def __repr__(self):
        return self.as_string

    @property
    def as_string(self):
        try:
            return self._as_string
        except AttributeError:
            self._as_string = '\n'.join(
                ''.join(row) for row in self.as_array)
            return self._as_string

    @property
    def as_array(self):
        try:
            return self._as_array
        except AttributeError:
            image = self.image.resize(self.dimensions, Image.BILINEAR)

            image_array = []
            for y in range(0, image.size[1]):
                image_row = []
                for x in range(0, image.size[0]):
                    pixel = image.getpixel((x, y))
                    brightness = 255 - sum(pixel)/3
                    row = bisect(self.zonebounds, brightness)
                    possibles = self.greyscale[row]
                    image_row.append(possibles[random.randint(0, len(possibles)-1)])
                image_array.append(image_row)
            self._as_array = image_array
            return self._as_array

    def get_pixel(self, x, y):
        return self.as_array[y][x]

    def get_rgb_pixel(self, x, y):
        image = self.image.resize(self.dimensions, Image.BILINEAR)
        def to_hex(decimal_number):
            hex_values = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
            return hex_values[decimal_number/16]
        return map(to_hex, image.getpixel((x, y)))


def render_image(ascii_image):
    import urwid

    def exit_on_q(key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    background_colour = '#aaa'
    palette = [
        # ('banner', '', '', '', '#ffa', '#60d'),
        ('streak', '', '', '', 'g50', background_colour),
        ('background', '', '', '', 'g7', background_colour),]

    palette.extend(get_image_palette(ascii_image))

    placeholder = urwid.SolidFill()
    loop = urwid.MainLoop(placeholder, palette, unhandled_input=exit_on_q)
    loop.screen.set_terminal_properties(colors=256)
    loop.widget = urwid.AttrMap(placeholder, 'background')
    loop.widget.original_widget = urwid.Filler(urwid.Pile([]))

    import string
    import random

    # div = urwid.Divider()
    # outside = urwid.AttrMap(div, 'outside')
    # inside = urwid.AttrMap(div, 'inside')
    image_rows = []
    for row_number, row in enumerate(ascii_image.as_array):
        pixel_row = get_pixel_row(row, row_number)
        text = urwid.Text(pixel_row, align='center')
        row = urwid.AttrMap(text, 'streak')
        image_rows.append(row)
    pile = loop.widget.base_widget
    for row in image_rows:
        pile.contents.append((row, pile.options()))

    loop.run()


def get_image_palette(ascii_image):
    pixel_palette = []
    for x in range(ascii_image.dimensions[0]):
        for y in range(ascii_image.dimensions[1]):
            pixel_rgb_value = ascii_image.get_rgb_pixel(x, y)
            colour = '#%s' % ''.join(pixel_rgb_value)
            # pixel_palette.append(('%s,%s' % (x, y), '', '', '', 'g50', colour))
            pixel_palette.append(('%s,%s' % (x, y), '', '', '', '', colour))
    return pixel_palette


def get_pixel_row(row, row_number):
    pixel_row = []
    for x, char in enumerate(row):
        char = char
        style = '%s,%s' % (x, row_number)
        pixel_row.append((style, char))
    return pixel_row


if __name__ == '__main__':
    image_path = './test/image.jpg'
    ascii_image = AsciiImage(image_path, width=100)
    render_image(ascii_image)
