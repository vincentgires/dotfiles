import os
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

wmname = 'Qtile'
keys = []
mod = 'mod4'
alt = 'mod1'


def assign_multiple_keys(keys, modifiers, key, *commands, desc=''):
    for k in key:
        keys.append(Key(modifiers, k, *commands, desc=desc))


# This config assume bépo layout is used
# Run the xev utility to see the key code
keys_assignation = [
    # Switch between windows
    ([mod], ['s', 'Down'], lazy.layout.down(),
        'Move focus down in stack pane'),
    ([mod], ['r', 'Up'], lazy.layout.up(),
        'Move focus up in stack pane'),
    # ([mod], ['t', 'Left'], lazy.layout.left(),
    #     'Move focus left in stack pane'),
    # ([mod], ['n', 'Right'], lazy.layout.right(),
    #     'Move focus right in stack pane'),

    # Move windows
    ([mod, 'shift'], ['s', 'Down'], lazy.layout.shuffle_down(),
        'Move window down in current stack'),
    ([mod, 'shift'], ['r', 'Up'], lazy.layout.shuffle_up(),
        'Move window up in current stack'),
    # ([mod, 'shift'], ['t', 'Left'], lazy.layout.shuffle_left(),
    #     'Move window left in current stack'),
    # ([mod, 'shift'], ['n', 'Right'], lazy.layout.shuffle_right(),
    #     'Move window right in current stack'),

    # ([mod, 'control', 'shift'], ['s', 'Down'],
    #     lazy.window.move_floating(0, 15),
    #     'Move floating window down'),
    # ([mod, 'control', 'shift'], ['r', 'Up'],
    #     lazy.window.move_floating(0, -15),
    #     'Move floating window up'),
    # ([mod, 'control', 'shift'], ['t', 'Left'],
    #     lazy.window.move_floating(-15, 0),
    #     'Move floating window left'),
    # ([mod, 'control', 'shift'], ['n', 'Right'],
    #     lazy.window.move_floating(15, 0),
    #     'Move floating window right'),

    # Flip
    ([mod], 'q', lazy.layout.flip(),
        'Flip pane'),

    # Windows geometry
    ([mod], 'f', lazy.window.toggle_fullscreen(), 'Toggle fullscreen'),
    ([mod], 'm', lazy.window.toggle_maximize(), 'Maximize'),
    ([mod, 'control'], 'f', lazy.window.toggle_floating(), 'Toggle Floating'),
    # MonadTall and Tile specific
    ([mod], 'd', [lazy.layout.shrink(), lazy.layout.decrease_nmaster()],
        'Shrink window (MonadTall), decrease number in master pane (Tile)'),
    ([mod], 'l', [lazy.layout.grow(), lazy.layout.increase_nmaster()],
        'Expand window (MonadTall), increase number in master pane (Tile)'),
    # Tile specific
    ([mod], 'v', lazy.layout.decrease_ratio(),
        'Decrease ratio (Tile)'),
    ([mod], 'j', lazy.layout.increase_ratio(),
        'Increase ratio (Tile)'),
    # Bsp specific
    # ([mod], 'd', lazy.layout.grow_down(), 'Grow down'),
    # ([mod], 'l', lazy.layout.grow_up(), 'Grow up'),
    # ([mod], 'v', lazy.layout.grow_left(), 'Grow left'),
    # ([mod], 'j', lazy.layout.grow_right(), 'Grow right'),

    # Switch window focus to other pane(s) of stack
    ([mod], 'space', lazy.layout.next(),
        'Switch window focus to other pane(s) of stack'),

    # Swap panes of split stack
    ([mod, 'shift'], 'space', lazy.layout.rotate(),
        'Swap panes of split stack'),

    # Toggle between different layouts
    ([mod], 'Tab', lazy.next_layout(), 'Toggle between layouts'),
    ([mod, 'shift'], 'Tab', lazy.prev_layout(), 'Toggle between layouts'),

    # Close window
    ([mod], ['c', 'eacute'], lazy.window.kill(), 'Close focused window'),
    ([alt], 'F4', lazy.window.kill(), 'Close focused window'),

    # Qtile session
    ([mod, 'control'], 'o', lazy.restart(), 'Restart qtile'),
    ([mod, 'control'], 'q', lazy.shutdown(), 'Shutdown qtile'),

    # Run prompt
    # ([mod], 'x', lazy.spawncmd(),
    #     'Spawn a command using a prompt widget'),

    # Switch between groups
    ([mod], ['t'], lazy.screen.prev_group(),
        'Move to the group on the left'),
    ([mod, 'control'], 'Left', lazy.screen.prev_group(),
        'Move to the group on the left'),
    ([mod], ['n'], lazy.screen.next_group(),
        'Move to the group on the right'),
    ([mod, 'control'], 'Right', lazy.screen.next_group(),
        'Move to the group on the right'),
    ([alt], 'Tab', lazy.screen.toggle_group(),
        'Move to the last visited group'),

    # Screens
    # Switch focus of monitors
    ([mod, 'control'], 'quotedbl', lazy.to_screen(0),
        'Set focus to monitor 1'),
    ([mod, 'control'], 'guillemotleft', lazy.to_screen(1),
        'Set focus to monitor 2'),
    ([mod], 'g', lazy.next_screen(), 'Set focus to next monitor'),
    ([mod], 'h', lazy.prev_screen(), 'Set focus to prev monitor'),
    # Move to specific monitor
    ([mod, 'control', 'shift'], 'quotedbl',
        [lazy.window.toscreen(0),
         lazy.to_screen(0)],
        'Move to monitor 1'),
    ([mod, 'control', 'shift'], 'guillemotleft',
        [lazy.window.toscreen(1),
         lazy.to_screen(1)],
        'Move to monitor 2'),
]

for modifiers, key, commands, desc in keys_assignation:
    if not isinstance(commands, (tuple, list)):
        commands = [commands]
    if isinstance(key, (tuple, list)):
        assign_multiple_keys(keys, modifiers, key, *commands, desc='')
    else:
        keys.append(Key(modifiers, key, *commands, desc=desc))

group_names = {
    'main': 'main',
    'net': 'net',
    'dev': 'dev',
    'chat': 'chat',
    'music': 'music',
    'work': 'work',
    'lighting': 'lighting',
    'compositing': 'compositing',
    'farm': 'farm',
    'review': 'review'}
group_assignation = [
    (group_names['main'], 'quotedbl', {'layout': 'tile'}),
    (group_names['net'], 'guillemotleft',
        {'layout': 'tile', 'matches': [Match(wm_class=['Firefox'])]}),
    (group_names['dev'], 'guillemotright',
        {'layout': 'tile', 'matches': [Match(wm_class=['kdevelop'])]}),
    (group_names['chat'], 'parenleft',
        {'matches': [Match(wm_class=['discord'])],
         'layout': 'tile'}),
    (group_names['music'], 'parenright', {'layout': 'tile'}),
    (group_names['work'], 'at', {'layout': 'max'}),
    (group_names['lighting'], 'plus',
        {'matches': [Match(wm_class=['maya.bin'])],
         'layout': 'tile'}),
    (group_names['compositing'], 'minus',
        {'matches': [Match(wm_class=['Nuke'])],
         'layout': 'tile'}),
    (group_names['farm'], 'slash',
        {'layout': 'tile',
         'matches': [Match(wm_class=['xConsole.bin'])]}),
    (group_names['review'], 'asterisk', {'layout': 'tile'})
]

groups = [Group(name, **kwargs) for name, _, kwargs in group_assignation]
for name, key, _ in group_assignation:
    keys.extend([
        # Switch to group
        Key([mod], key, lazy.group[name].toscreen(),
            desc='Switch to group {}'.format(name)),
        # Send current window to another group
        Key([mod, 'shift'], key,
            lazy.window.togroup(name, switch_group=False),
            desc='Switch and move focused window to group {}'.format(name))])

active_color = '555555'
inactive_color = '404040'

layout_theme = {
    'border_width': 1,
    'margin': 6,
    'border_focus': 'dimgrey',
    'border_normal': '313131'}

layouts = [
    layout.Tile(
        shift_windows=True,
        master_match=Match(
            wm_class=['kdevelop', 'Nuke', 'maya.bin', 'Blender']),
        **layout_theme),
    layout.MonadTall(
        new_client_position='after_current',
        ratio=0.65, **layout_theme),
    layout.Max(**layout_theme),
    layout.TreeTab(
        **layout_theme,
        fontsize=12,
        sections=['tab'],
        section_fontsize=12,
        bg_color='131313',
        active_bg=active_color,
        active_fg='ffffff',
        inactive_bg='131313',
        inactive_fg=inactive_color,
        panel_width=150),
    layout.Floating(**layout_theme)]

widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3)
extension_defaults = widget_defaults.copy()

graph_theme = {
    'border_color': '333333',
    'border_width': 1,
    'graph_color': '333333',
    'line_width': 1,
    'fill_color': active_color}


def create_groupbox():
    return widget.GroupBox(
        borderwidth=2,
        highlight_method='line',
        highlight_color=['000000', '000000'],
        this_current_screen_border=active_color,
        inactive=inactive_color)


screens = [
    Screen(
        wallpaper='~/wallpaper.png',
        wallpaper_mode='fill',
        top=bar.Bar(
            [
                create_groupbox(),
                widget.Sep(),
                widget.CurrentLayout(),
                # widget.Sep(),
                # widget.Prompt(),
                widget.Sep(),
                widget.WindowName(),
                widget.Sep(),
                widget.TaskList(
                    border=active_color,
                    borderwidth=1,
                    highlight_method='block',
                    max_title_width=250),
                widget.Sep(),
                widget.Systray(),
                # widget.KeyboardLayout(),
                # widget.Sep(),
                # widget.Backlight(),
                widget.Sep(),
                widget.CPUGraph(**graph_theme),
                widget.MemoryGraph(**graph_theme),
                widget.SwapGraph(**graph_theme),
                widget.Sep(),
                widget.TextBox(text='🔊'),
                widget.Volume(),
                widget.Sep(),
                widget.Clock(format='%Y-%m-%d %H:%M'),
                widget.Sep(),
                widget.QuickExit()
            ],
            25,
            background='131313'
        ),
    ),
    Screen(
        wallpaper='~/wallpaper.png',
        wallpaper_mode='fill',
        top=bar.Bar(
            [
                create_groupbox(),
                widget.Sep(),
                widget.CurrentLayout(),
                widget.Sep(),
                widget.WindowName(),
                widget.Sep(),
                widget.TaskList(
                    border=active_color,
                    borderwidth=1,
                    highlight_method='block',
                    max_title_width=250)
            ],
            25,
        ),
    ),
]

mouse = [
    Drag([mod], 'Button1', lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], 'Button3', lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], 'Button2', lazy.window.bring_to_front()),
    Click([mod, 'control'], 'Button1', lazy.window.toggle_floating())
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry')],  # GPG key password entry
    **layout_theme)
auto_fullscreen = True
focus_on_window_activation = 'smart'
reconfigure_screens = True
auto_minimize = True

