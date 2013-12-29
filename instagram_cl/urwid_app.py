import arrow
import urwid

instagram_blue = '#04a'
palette = [('banner', '', '', '', '#ffa', instagram_blue),
           ('streak', '', '', '', 'g50', instagram_blue),
           ('inside', '', '', '', 'g38', instagram_blue),
           ('bg', '', '', '', 'g7', '#ccc'),]


def exit_on_q(key):
    if key.lower() == 'q':
        raise urwid.ExitMainLoop()


placeholder = urwid.SolidFill()
loop = urwid.MainLoop(placeholder, palette, unhandled_input=exit_on_q)
loop.screen.set_terminal_properties(colors=256)
loop.widget = urwid.AttrMap(placeholder, 'bg')
loop.widget.original_widget = urwid.Filler(urwid.Pile([]))

divider = urwid.Divider()
inside = urwid.AttrMap(divider, 'inside')
text = urwid.Text(('banner', 'Instagram-CL'), align='center')
streak = urwid.AttrMap(text, 'streak')
pile = loop.widget.base_widget
for item in [inside, streak, inside]:
    pile.contents.append((item, pile.options()))

loop.run()
