import os
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

keys = []
mod = 'mod4'
alt = 'mod1'
# terminal = guess_terminal()
terminal = 'st -f hack:size=12'
browser = 'qutebrowser'


def assign_multiple_keys(keys, modifiers, key, *commands, desc=''):
    for k in key:
        keys.append(Key(modifiers, k, *commands, desc=desc))


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
        'Move window down in current stack '),
    ([mod, 'shift'], ['r', 'Up'], lazy.layout.shuffle_up(),
        'Move window up in current stack '),
    ([mod, 'shift'], ['t', 'Left'], lazy.layout.shuffle_left(),
        'Move window left in current stack '),
    ([mod, 'shift'], ['n', 'Right'], lazy.layout.shuffle_right(),
        'Move window right in current stack '),

    # Windows geometry
    ([mod], 'd', [lazy.layout.shrink(), lazy.layout.decrease_nmaster()],
        'Shrink window (MonadTall), decrease number in master pane (Tile)'),
    ([mod], 'l', [lazy.layout.grow(), lazy.layout.increase_nmaster()],
        'Expand window (MonadTall), increase number in master pane (Tile)'),
    ([mod], 'v', lazy.layout.maximize(), 'Maximize'),
    ([mod], 'f', lazy.window.toggle_fullscreen(), 'Toggle fullscreen'),

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
    ([mod, 'control'], 'r', lazy.restart(), 'Restart qtile'),
    ([mod, 'control'], 'q', lazy.shutdown(), 'Shutdown qtile'),

    # Run prompt
    # ([alt], 'space', lazy.spawncmd(),
    #     'Spawn a command using a prompt widget'),
    ([alt], 'space', lazy.spawn('dmenu_run -p Run: -l 5 -sb dimgrey'),
        'Spawn a command using a prompt widget'),

    # Switch between groups
    ([alt, 'control'], 'Left', lazy.screen.prev_group(),
        'Move to the group on the left'),
    ([alt, 'control'], 'Right', lazy.screen.next_group(),
        'Move to the group on the right'),
    ([mod, alt], ['Left', 't', 'r'], lazy.screen.prev_group(),
        'Move to the group on the left'),
    ([mod, alt], ['Right', 'n', 's'], lazy.screen.next_group(),
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
    'main': '1: main',
    'net': '2: net',
    'dev': '3: dev',
    'chat': '4: chat',
    'music': '5: music'}
group_assignation = [
    (group_names['main'], 'quotedbl'),
    (group_names['net'], 'guillemotleft'),
    (group_names['dev'], 'guillemotright'),
    (group_names['chat'], 'parenleft'),
    (group_names['music'], 'parenright'),
    # ('6', 'at'),
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
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        wallpaper='~/Pictures/wallpaper_vignetting_noise.png',
        wallpaper_mode='fill',
        top=bar.Bar(
            [
                widget.GroupBox(),
                widget.Sep(),
                widget.CurrentLayout(),
                # widget.Sep(),
                # widget.Prompt(),
                widget.Sep(),
                widget.WindowName(),
                widget.Systray(),
                # widget.KeyboardLayout(),
                widget.Sep(),
                widget.Clock(format='%Y-%m-%d %H:%M'),
                # widget.Sep(),
                # widget.Backlight(),
                widget.Sep(),
                widget.Volume(),
                widget.Sep(),
                widget.QuickExit()
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


@hook.subscribe.client_new
def agroup(client):
    # Run xprop to find wm_class
    apps = {
        'Navigator': group_names['net'],
        'qutebrowser': group_names['net'],
        'kdevelop': group_names['dev'],
        'element': group_names['chat']}
    wm_class = client.window.get_wm_class()[0]
    group = apps.get(wm_class, None)
    if group:
        client.togroup(group, switch_group=True)
