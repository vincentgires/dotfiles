import os
import shutil
from libqtile import bar, layout, widget, hook
from libqtile.config import (
    Click, Drag, Group, Key, Screen, ScratchPad, DropDown)
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

keys = []
mod = 'mod4'
alt = 'mod1'
# altgr = 'mod5'
# terminal = guess_terminal()
terminal = 'alacritty'
browser = shutil.which('qutebrowser') or shutil.which('firefox')
audioplayer = (
    shutil.which('audacious')
    or shutil.which('deadbeef')
    or shutil.which('vlc'))


def assign_multiple_keys(keys, modifiers, key, *commands, desc=''):
    for k in key:
        keys.append(Key(modifiers, k, *commands, desc=desc))


# Run the xev utility to see the key code
keys_assignation = [
    # Switch between windows
    ([mod], ['s', 'Down'], lazy.layout.down(),
        'Move focus down in stack pane'),
    ([mod], ['r', 'Up'], lazy.layout.up(),
        'Move focus up in stack pane'),
    ([mod], ['t', 'Left'], lazy.layout.left(),
        'Move focus left in stack pane'),
    ([mod], ['n', 'Right'], lazy.layout.right(),
        'Move focus right in stack pane'),

    # Move windows
    ([mod, 'shift'], ['s', 'Down'], lazy.layout.shuffle_down(),
        'Move window down in current stack'),
    ([mod, 'shift'], ['r', 'Up'], lazy.layout.shuffle_up(),
        'Move window up in current stack'),
    ([mod, 'shift'], ['t', 'Left'], lazy.layout.shuffle_left(),
        'Move window left in current stack'),
    ([mod, 'shift'], ['n', 'Right'], lazy.layout.shuffle_right(),
        'Move window right in current stack'),

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
    ([mod], 'd', [lazy.layout.shrink(), lazy.layout.decrease_nmaster()],
        'Shrink window (MonadTall), decrease number in master pane (Tile)'),
    ([mod], 'l', [lazy.layout.grow(), lazy.layout.increase_nmaster()],
        'Expand window (MonadTall), increase number in master pane (Tile)'),
    ([mod], 'v', lazy.layout.maximize(), 'Maximize'),
    ([mod], 'f', lazy.window.toggle_fullscreen(), 'Toggle fullscreen'),
    ([mod, 'control'], 'f', lazy.window.toggle_floating(), 'Toggle Floating'),

    # Switch window focus to other pane(s) of stack
    ([mod], 'space', lazy.layout.next(),
        'Switch window focus to other pane(s) of stack'),

    # Swap panes of split stack
    ([mod, 'shift'], 'space', lazy.layout.rotate(),
        'Swap panes of split stack'),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    ([mod, 'shift'], 'Return', lazy.layout.toggle_split(),
        'Toggle between split and unsplit sides of stack'),
    ([mod], 'Return', lazy.spawn(terminal), 'Launch terminal'),

    # Toggle between different layouts
    ([mod], 'Tab', lazy.next_layout(), 'Toggle between layouts'),

    # Close window
    ([mod], 'c', lazy.window.kill(), 'Close focused window'),
    ([alt], 'F4', lazy.window.kill(), 'Close focused window'),

    # Qtile session
    ([mod, 'control'], 'o', lazy.restart(), 'Restart qtile'),
    ([mod, 'control'], 'q', lazy.shutdown(), 'Shutdown qtile'),

    # Run prompt
    # ([alt], 'space', lazy.spawncmd(),
    #     'Spawn a command using a prompt widget'),
    ([alt], 'space', lazy.spawn('dmenu_run -p Run: -l 5 -sb dimgrey'),
        'Spawn a command using a prompt widget'),

    # Switch between groups
    ([mod, 'control'], ['Left', 't', 'r'], lazy.screen.prev_group(),
        'Move to the group on the left'),
    ([mod, 'control'], ['Right', 'n', 's'], lazy.screen.next_group(),
        'Move to the group on the right'),

    # Sound
    ([], 'XF86AudioMute', lazy.spawn('amixer -q set Master toggle'), ''),
    ([], 'XF86AudioLowerVolume',
        lazy.spawn('amixer -c 0 sset Master 1- unmute'), ''),
    ([], 'XF86AudioRaiseVolume',
        lazy.spawn('amixer -c 0 sset Master 1+ unmute'), ''),

    # Brightness
    ([], 'XF86MonBrightnessDown', lazy.spawn('xbacklight -dec 15'), ''),
    ([], 'XF86MonBrightnessUp', lazy.spawn('xbacklight -inc 15'), ''),

    # Applications
    ([mod], 'b', lazy.spawn(browser), ''),
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
    'work': 'work'}
group_assignation = [
    (group_names['main'], 'quotedbl'),
    (group_names['net'], 'guillemotleft'),
    (group_names['dev'], 'guillemotright'),
    (group_names['chat'], 'parenleft'),
    (group_names['music'], 'parenright'),
    (group_names['work'], 'at'),
    # ('7', 'plus'),
    # ('8', 'minus'),
    # ('9', 'slash'),
    # ('0', 'asterisk')
]

groups = [Group(i[0], layout='monadtall') for i in group_assignation]
for name, key in group_assignation:
    keys.extend([
        # Switch to group
        Key([mod], key, lazy.group[name].toscreen(),
            desc='Switch to group {}'.format(name)),
        # Send current window to another group
        Key([mod, 'shift'], key,
            lazy.window.togroup(name, switch_group=True),
            desc='Switch and move focused window to group {}'.format(name)),
    ])

# Dropdown
groups.extend([
    ScratchPad('scratchpad', [
        DropDown('terminal', terminal),
        DropDown('audioplayer', audioplayer)])
])
keys.extend([
  Key([], 'F11', lazy.group['scratchpad'].dropdown_toggle('terminal')),
  Key([], 'F10', lazy.group['scratchpad'].dropdown_toggle('audioplayer')),
])

layout_theme = {
    'border_width': 1,
    'margin': 6,
    'border_focus': 'dimgrey',
    'border_normal': '313131'}

layouts = [
    layout.Max(**layout_theme),
    layout.TreeTab(**layout_theme),
    layout.MonadTall(new_at_current=True, **layout_theme),
    layout.Tile(shift_windows=True, **layout_theme),
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
    'fill_color': '555555'}

screens = [
    Screen(
        wallpaper='~/wallpaper.png',
        wallpaper_mode='fill',
        top=bar.Bar(
            [
                widget.GroupBox(
                    borderwidth=2,
                    highlight_method='line',
                    # rounded=False,
                    highlight_color=['000000', '000000'],
                    this_current_screen_border='555555'),
                widget.Sep(),
                widget.CurrentLayout(),
                # widget.Sep(),
                # widget.Prompt(),
                widget.Sep(),
                widget.WindowName(),
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
                widget.QuickExit(default_text='🗙', countdown_format='{}'),
            ],
            24,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], 'Button1', lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], 'Button3', lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], 'Button2', lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the xprop utility to see the wm_class and name of an X client
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = 'smart'


@hook.subscribe.startup_once
def autostart():
    # Set keyboard layout with bépo
    os.system('setxkbmap fr bepo')


# @hook.subscribe.client_new
# def agroup(client):
#     # Run xprop to find wm_class
#     apps = {
#         'Navigator': group_names['net'],
#         'qutebrowser': group_names['net'],
#         'kdevelop': group_names['dev'],
#         'element': group_names['chat']}
#     wm_class = client.window.get_wm_class()[0]
#     group = apps.get(wm_class, None)
#     if group:
#         client.togroup(group, switch_group=True)
