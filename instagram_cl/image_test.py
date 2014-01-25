from bisect import bisect
import os

from PIL import Image
import requests


def render_image(unicode_image):
    import urwid

    def exit_on_q(key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    background_colour = '#aaa'
    palette = [
        ('streak', '', '', '', 'g50', background_colour),
        ('background', '', '', '', 'g7', background_colour)]

    # ('x, y', '', '', '', character_colour, background_colour)
    palette.extend(get_image_palette(unicode_image))

    placeholder = urwid.SolidFill()
    loop = urwid.MainLoop(placeholder, palette, unhandled_input=exit_on_q)
    loop.screen.set_terminal_properties(colors=256)
    loop.widget = urwid.AttrMap(placeholder, 'background')
    loop.widget.original_widget = urwid.Filler(urwid.Pile([]))


    # image_rows = []
    # for row_number, row in enumerate(unicode_image.as_array):
    #     # pixel_row = get_pixel_row(row, row_number)
    #     pixels = map(lambda x: x.character, row)
    #     text = urwid.Text(pixels, align='center')
    #     # row = urwid.AttrMap(text, 'streak')
    #     image_rows.append(text)

    # pile = loop.widget.base_widget
    # for row in image_rows:
    #     pile.contents.append((row, pile.options()))


    pixel_rows = []
    for row_number, pixel_row in enumerate(unicode_image.as_array):
        row = []
        for pixel_number, pixel in enumerate(pixel_row):
            style_name = '{0},{1}'.format(row_number, pixel_number)
            row.append((style_name, pixel.character))
        pixels_text = urwid.Text(row, align='center')
        pixel_rows.append(pixels_text)

    # debug
    import arrow
    pixel_rows.append(urwid.Text(str(arrow.now()), align='center'))

    pile = loop.widget.base_widget
    for row in pixel_rows:
        pile.contents.append((row, pile.options()))

    loop.run()


def get_image_palette(unicode_image):
    pixel_palette = []
    for x in range(unicode_image.array_dimensions[0]):
        for y in range(unicode_image.array_dimensions[1]):
            style_name = '{0},{1}'.format(x, y)
            # pixel_palette.append((style_name, '', '', '', 'g0', 'g100'))
            pixel_palette.append(unicode_image.get_pixel_style(x, y))
    return pixel_palette


if __name__ == '__main__':
    from image import UnicodeImage
    image_filename = './test/image.jpg'
    image = Image.open(image_filename)
    unicode_image = UnicodeImage(image)
    render_image(unicode_image)
