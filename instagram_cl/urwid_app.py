import urwid

instagram_blue = '#04a'
palette = [('banner', '', '', '', '#ffa', instagram_blue),
           ('streak', '', '', '', 'g50', instagram_blue),
           ('control_bar', '', '', '', 'g38', instagram_blue),
           ('controls', '', '', '', 'g50', instagram_blue),
           ('background', '', '', '', 'g7', '#ccc')]


def exit_on_q(key):
    if key.lower() == 'q':
        raise urwid.ExitMainLoop()


placeholder = urwid.SolidFill()

loop = urwid.MainLoop(placeholder, palette, unhandled_input=exit_on_q)
loop.screen.set_terminal_properties(colors=256)
loop.widget = urwid.AttrMap(placeholder, 'background')
loop.widget.original_widget = urwid.Filler(urwid.Pile([]), 'top')

controls = urwid.Text(('banner', '(r)efresh  (u)ser  (q)uit'), 'right')
control_bar = urwid.AttrMap(controls, 'control_bar')
text = urwid.Text(('banner', 'Instagram-CL'), align='center')
streak = urwid.AttrMap(text, 'streak')
pile = loop.widget.base_widget
for item in [streak, control_bar]:
    pile.contents.append((item, pile.options()))

loop.run()
