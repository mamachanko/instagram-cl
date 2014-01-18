from bisect import bisect
import os
import random

from PIL import Image
import requests


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
