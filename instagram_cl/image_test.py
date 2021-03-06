from PIL import Image

from image import UrwidImage


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
            pixel_palette.append(unicode_image.get_pixel_style(x, y))
    return pixel_palette


if __name__ == '__main__':
    image_filename = './test/image.jpg'
    image = Image.open(image_filename)
    render_image(UrwidImage(image))
