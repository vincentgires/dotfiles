import os
import shutil
from libqtile import bar, layout, widget, hook
from libqtile.config import (
    Click, Drag, Group, Key, Screen, ScratchPad, DropDown)
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
# import psutil

wmname = 'Qtile'
keys = []
mod = 'mod4'
alt = 'mod1'
# altgr = 'mod5'
# terminal = guess_terminal()
terminal = (
    shutil.which('alacritty')
    or shutil.which('st')
    or shutil.which('xfce4-terminal'))
browser = shutil.which('qutebrowser') or shutil.which('firefox')
audioplayer = (
    shutil.which('audacious')
    or shutil.which('deadbeef')
    or shutil.which('vlc'))
filemanager = shutil.which('thunar')


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
    ([mod], 'v', lazy.layout.maximize(), 'Maximize'),
    ([mod], 'f', lazy.window.toggle_fullscreen(), 'Toggle fullscreen'),
    # MonadTall specific
    ([mod], 'd', [lazy.layout.shrink(), lazy.layout.decrease_nmaster()],
        'Shrink window (MonadTall), decrease number in master pane (Tile)'),
    ([mod], 'l', [lazy.layout.grow(), lazy.layout.increase_nmaster()],
        'Expand window (MonadTall), increase number in master pane (Tile)'),
    ([mod, 'control'], 'f', lazy.window.toggle_floating(), 'Toggle Floating'),
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
    ([mod], ['c', 'eacute'], lazy.window.kill(), 'Close focused window'),
    ([alt], 'F4', lazy.window.kill(), 'Close focused window'),

    # Qtile session
    ([mod, 'control'], 'o', lazy.restart(), 'Restart qtile'),
    ([mod, 'control'], 'q', lazy.shutdown(), 'Shutdown qtile'),

    # Run prompt
    # ([mod], 'x', lazy.spawncmd(),
    #     'Spawn a command using a prompt widget'),
    ([alt], 'space', lazy.spawn('dmenu_run -p Run: -l 5 -sb dimgrey'),
        'Spawn a command using dmenu'),

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
    ([mod], 'dollar', lazy.spawn(filemanager), ''),

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
    'work': 'work'}
group_assignation = [
    (group_names['main'], 'quotedbl', {'layout': 'monadtall'}),
    (group_names['net'], 'guillemotleft',
        {'layout': 'monadtall', 'matches': [Match(wm_class=['firefox'])]}),
    (group_names['dev'], 'guillemotright', {'layout': 'monadtall'}),
    (group_names['chat'], 'parenleft', {'layout': 'monadtall'}),
    (group_names['music'], 'parenright', {'layout': 'monadtall'}),
    (group_names['work'], 'at', {'layout': 'max'}),
    # ('7', 'plus'),
    # ('8', 'minus'),
    # ('9', 'slash'),
    # ('0', 'asterisk')
]

groups = [Group(name, **kwargs) for name, _, kwargs in group_assignation]
for name, key, _ in group_assignation:
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

active_color = '555555'
inactive_color = '404040'

layout_theme = {
    'border_width': 1,
    'margin': 6,
    'border_focus': 'dimgrey',
    'border_normal': '313131'}

layouts = [
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
    layout.MonadTall(new_at_current=True, **layout_theme),
    layout.Bsp(**layout_theme),
    layout.Tile(shift_windows=True, **layout_theme, master_length=3),
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
                # widget.Sep(),
                # widget.TaskList(
                #     border=active_color,
                #     borderwidth=1,
                #     highlight_method='block',
                #     max_title_width=250),
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
            ],
            25,
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


# Swallow feature borrowed from https://github.com/qtile/qtile/issues/1771
# @hook.subscribe.client_new
# def _swallow(window):
#     pid = window.window.get_net_wm_pid()
#     ppid = psutil.Process(pid).ppid()
#     cpids = {
#         c.window.get_net_wm_pid(): wid
#         for wid, c in window.qtile.windows_map.items()}
#     for i in range(5):
#         if not ppid:
#             return
#         if ppid in cpids:
#             parent = window.qtile.windows_map.get(cpids[ppid])
#             parent.minimized = True
#             window.parent = parent
#             return
#         ppid = psutil.Process(ppid).ppid()


# @hook.subscribe.client_killed
# def _unswallow(window):
#     if hasattr(window, 'parent'):
#         window.parent.minimized = False
