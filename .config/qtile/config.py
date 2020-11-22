import os
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = 'mod4'
alt = 'mod1'
# terminal = guess_terminal()
terminal = 'st -f hack:size=12'

keys = [
    # Switch between windows in current stack pane
    Key([mod], 's', lazy.layout.down(),
        desc='Move focus down in stack pane'),
    Key([mod], 'r', lazy.layout.up(),
        desc='Move focus up in stack pane'),
    Key([mod], 't', lazy.layout.left(),
        desc='Move focus left in stack pane'),
    Key([mod], 'n', lazy.layout.right(),
        desc='Move focus right in stack pane'),

    # Move windows up or down in current stack
    Key([mod, 'shift'], 's', lazy.layout.shuffle_down(),
        desc='Move window down in current stack '),
    Key([mod, 'shift'], 'r', lazy.layout.shuffle_up(),
        desc='Move window up in current stack '),
    Key([mod, 'shift'], 't', lazy.layout.shuffle_left(),
        desc='Move window left in current stack '),
    Key([mod, 'shift'], 'n', lazy.layout.shuffle_right(),
        desc='Move window right in current stack '),

    Key([mod], 'd',
        lazy.layout.shrink(),
        lazy.layout.decrease_nmaster(),
        desc=(
            'Shrink window (MonadTall), '
            'decrease number in master pane (Tile)')),
    Key([mod], 'l',
        lazy.layout.grow(),
        lazy.layout.increase_nmaster(),
        desc=(
            'Expand window (MonadTall), '
            'increase number in master pane (Tile)')),

    Key([mod], 'v', lazy.layout.maximize(), desc='Maximize'),
    Key([mod], 'f', lazy.window.toggle_fullscreen(), desc='Toggle fullscreen'),

    # Switch window focus to other pane(s) of stack
    Key([mod], 'space', lazy.layout.next(),
        desc='Switch window focus to other pane(s) of stack'),

    # Swap panes of split stack
    Key([mod, 'shift'], 'space', lazy.layout.rotate(),
        desc='Swap panes of split stack'),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, 'shift'], 'Return', lazy.layout.toggle_split(),
        desc='Toggle between split and unsplit sides of stack'),
    Key([mod], 'Return', lazy.spawn(terminal), desc='Launch terminal'),

    # Toggle between different layouts as defined below
    Key([mod], 'Tab', lazy.next_layout(), desc='Toggle between layouts'),
    Key([mod], 'w', lazy.window.kill(), desc='Kill focused window'),

    Key([mod, 'control'], 'r', lazy.restart(), desc='Restart qtile'),
    Key([mod, 'control'], 'q', lazy.shutdown(), desc='Shutdown qtile'),

    # Key([alt], 'space', lazy.spawncmd(),
    #     desc='Spawn a command using a prompt widget'),
    Key([alt], 'space', lazy.spawn('dmenu_run -p Run: -l 5 -sb dimgrey'),
        desc='Spawn a command using a prompt widget'),

    # Switch between groups
    Key([alt, 'control'], 'Left', lazy.screen.prev_group(),
        desc='Move to the group on the left'),
    Key([alt, 'control'], 'Right', lazy.screen.next_group(),
        desc='Move to the group on the right'),

    # Sound
    Key([], 'XF86AudioMute', lazy.spawn('amixer -q set Master toggle')),
    Key([], 'XF86AudioLowerVolume',
        lazy.spawn('amixer -c 0 sset Master 1- unmute')),
    Key([], 'XF86AudioRaiseVolume',
        lazy.spawn('amixer -c 0 sset Master 1+ unmute')),

    # Brightness
    Key([], 'XF86MonBrightnessDown', lazy.spawn('xbacklight -dec 15')),
    Key([], 'XF86MonBrightnessUp', lazy.spawn('xbacklight -inc 15')),
]

groups = [Group(i, layout='monadtall') for i in '123456789']
for i, group in enumerate(groups):
    keys.extend([
        # Switch to group
        # TODO use correct key with bépo (str(i) can't work)
        Key([mod], str(i), lazy.group[group.name].toscreen(),
            desc='Switch to group {}'.format(group.name)),

        # Send current window to another group
        Key([mod, 'shift'], str(i),
            lazy.window.togroup(group.name, switch_group=True),
            desc='Switch and move focused window to group {}'.format(
                group.name)),
    ])

layouts = [
    layout.Max(),
    layout.Columns(),
    layout.MonadTall(),
    layout.RatioTile(),
    layout.Tile()]

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
                widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.Systray(),
                # widget.KeyboardLayout(),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
                # widget.Backlight(),
                widget.Volume(),
                widget.QuickExit(),
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
    # Run the utility of `xprop` to see the wm class and name of an X client.
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
