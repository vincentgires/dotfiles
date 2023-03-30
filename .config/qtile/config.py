import os
import subprocess
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from qtile_cfg import (
    groups_config, master_match, font, font_size, wallpaper, bar_size,
    floating_rules)

wmname = 'Qtile'
groups = []
keys = []
screens = []
_mod = 'mod4'
_alt = 'mod1'
_moving_floating = 15
_ratio = 0.65
_font_color = 'c3c3c3'
_active_color = '353535'
_inactive_color = '454545'
_layout_theme = {
    'border_width': 1,
    'margin': 5,
    'border_focus': 'dimgrey',
    'border_normal': '313131'}
_keys_assignation = [
    # Switch between windows
    ([_mod], ['s', 'Down'], lazy.layout.down(),
        'Move focus down in stack pane'),
    ([_mod], ['r', 'Up'], lazy.layout.up(),
        'Move focus up in stack pane'),
    # ([_mod], ['t', 'Left'], lazy.layout.left(),
    #     'Move focus left in stack pane'),
    # ([_mod], ['n', 'Right'], lazy.layout.right(),
    #     'Move focus right in stack pane'),

    # Move windows
    ([_mod, 'shift'], ['s', 'Down'], lazy.layout.shuffle_down(),
        'Move window down in current stack'),
    ([_mod, 'shift'], ['r', 'Up'], lazy.layout.shuffle_up(),
        'Move window up in current stack'),
    # ([_mod, 'shift'], ['t', 'Left'], lazy.layout.shuffle_left(),
    #     'Move window left in current stack'),
    # ([_mod, 'shift'], ['n', 'Right'], lazy.layout.shuffle_right(),
    #     'Move window right in current stack'),

    ([_mod, 'control'], ['s', 'Down'],
        lazy.window.move_floating(0, _moving_floating),
        'Move floating window down'),
    ([_mod, 'control'], ['r', 'Up'],
        lazy.window.move_floating(0, -_moving_floating),
        'Move floating window up'),
    ([_mod, 'control'], ['t', 'Left'],
        lazy.window.move_floating(-_moving_floating, 0),
        'Move floating window left'),
    ([_mod, 'control'], ['n', 'Right'],
        lazy.window.move_floating(_moving_floating, 0),
        'Move floating window right'),

    # Flip
    ([_mod], 'q', lazy.layout.flip(), 'Flip pane'),

    # Windows geometry
    ([_mod], 'f', lazy.window.toggle_fullscreen(), 'Toggle fullscreen'),
    ([_mod], 'm', lazy.window.toggle_maximize(), 'Maximize'),
    ([_mod, 'control'], 'f', lazy.window.toggle_floating(), 'Toggle Floating'),
    # MonadTall and Tile specific
    ([_mod], 'd', [lazy.layout.shrink(), lazy.layout.decrease_nmaster()],
        'Shrink window (MonadTall), decrease number in master pane (Tile)'),
    ([_mod], 'l', [lazy.layout.grow(), lazy.layout.increase_nmaster()],
        'Expand window (MonadTall), increase number in master pane (Tile)'),
    # Tile specific
    ([_mod], 'v', lazy.layout.decrease_ratio(),
        'Decrease ratio (Tile)'),
    ([_mod], 'j', lazy.layout.increase_ratio(),
        'Increase ratio (Tile)'),

    # Switch window focus to other pane(s) of stack
    ([_mod], 'space', lazy.layout.next(),
        'Switch window focus to other pane(s) of stack'),

    # Swap panes of split stack
    ([_mod, 'shift'], 'space', lazy.layout.rotate(),
        'Swap panes of split stack'),

    # Toggle between different layouts
    ([_mod], 'Tab', lazy.next_layout(), 'Toggle between layouts'),
    ([_mod, 'shift'], 'Tab', lazy.prev_layout(), 'Toggle between layouts'),

    # Close window
    ([_mod], ['c', 'eacute'], lazy.window.kill(), 'Close focused window'),
    ([_alt], 'F4', lazy.window.kill(), 'Close focused window'),

    # Qtile session
    ([_mod, 'control'], 'o', lazy.restart(), 'Restart qtile'),
    ([_mod, 'control'], 'q', lazy.shutdown(), 'Shutdown qtile'),

    # Run prompt
    ([_mod], 'x', lazy.spawncmd(), 'Spawn a command using a prompt widget'),

    # Switch between groups
    ([_mod], ['t'], lazy.screen.prev_group(),
        'Move to the group on the left'),
    ([_mod, 'control'], 'Left', lazy.screen.prev_group(),
        'Move to the group on the left'),
    ([_mod], ['n'], lazy.screen.next_group(),
        'Move to the group on the right'),
    ([_mod, 'control'], 'Right', lazy.screen.next_group(),
        'Move to the group on the right'),
    ([_alt], 'Tab', lazy.screen.toggle_group(),
        'Move to the last visited group'),

    # Screens
    # Switch focus of monitors
    ([_mod, 'control'], 'quotedbl', lazy.to_screen(0),
        'Set focus to monitor 1'),
    ([_mod, 'control'], 'guillemotleft', lazy.to_screen(1),
        'Set focus to monitor 2'),
    ([_mod], 'g', lazy.next_screen(), 'Set focus to next monitor'),
    ([_mod], 'h', lazy.prev_screen(), 'Set focus to prev monitor'),
    # Move to specific monitor
    ([_mod, 'control', 'shift'], 'quotedbl',
        [lazy.window.toscreen(0),
         lazy.to_screen(0)],
        'Move to monitor 1'),
    ([_mod, 'control', 'shift'], 'guillemotleft',
        [lazy.window.toscreen(1),
         lazy.to_screen(1)],
        'Move to monitor 2')]


def _assign_multiple_keys(keys, modifiers, key, *commands, desc=''):
    for k in key:
        keys.append(Key(modifiers, k, *commands, desc=desc))


for modifiers, key, commands, desc in _keys_assignation:
    if not isinstance(commands, (tuple, list)):
        commands = [commands]
    if isinstance(key, (tuple, list)):
        _assign_multiple_keys(keys, modifiers, key, *commands, desc='')
    else:
        keys.append(Key(modifiers, key, *commands, desc=desc))

for name, data in groups_config.items():
    # Create group
    matches = data.get('matches')
    if matches is not None:
        matches = [Match(**x) for x in matches]
    groups.append(Group(name, layout=data.get('layout'), matches=matches))
    # Bind key
    keys.extend([
        # Switch to group
        Key([_mod], data['key'], lazy.group[name].toscreen(),
            desc=f'Switch to group {name}'),
        # Send current window to another group
        Key([_mod, 'shift'], data['key'],
            lazy.window.togroup(name, switch_group=False),
            desc=f'Switch and move focused window to group {name}')])

layouts = [
    layout.Tile(
        shift_windows=True,
        master_match=[Match(**match) for match in master_match],
        ratio=_ratio, **_layout_theme),
    layout.MonadTall(
        new_client_position='after_current',
        ratio=_ratio, **_layout_theme),
    layout.Max(**_layout_theme),
    layout.TreeTab(
        **_layout_theme,
        fontsize=12,
        sections=['tab1', 'tab2'],
        section_fontsize=12,
        bg_color='131313',
        active_bg=_active_color,
        active_fg='ffffff',
        inactive_bg='131313',
        inactive_fg=_inactive_color,
        panel_width=150),
    layout.Floating(**_layout_theme)]

widget_defaults = dict(
    font=font,
    fontsize=font_size,
    padding=3,
    foreground=_font_color)
extension_defaults = widget_defaults.copy()


def _get_monitors():
    xr = subprocess.check_output(
        'xrandr --query | grep " connected"', shell=True).decode().split('\n')
    monitors = len(xr) - 1 if len(xr) > 2 else len(xr)
    return monitors


# _graph_theme = {
#     'border_color': '333333',
#     'border_width': 1,
#     'graph_color': '333333',
#     'line_width': 1,
#     'fill_color': _active_color}


def _create_groupbox():
    return widget.GroupBox(
        borderwidth=1,
        highlight_method='line',
        highlight_color=['252525'] * 2,
        active=_font_color,
        inactive=_inactive_color,
        disable_drag=True,
        this_current_screen_border='787878',
        this_screen_border='787878')


def _create_tasklist():
    return widget.TaskList(
        border=_active_color,
        borderwidth=1,
        highlight_method='block',
        markup_floating='f',
        markup_focused='',
        markup_maximized='m',
        markup_minimized='_',
        markup_normal='')


_sep = widget.Sep(size_percent=70, foreground=_inactive_color)

for monitor in range(_get_monitors()):
    if monitor == 0:
        screens.append(
            Screen(
                wallpaper=wallpaper,
                wallpaper_mode='fill',
                top=bar.Bar([
                    _create_groupbox(),
                    _create_tasklist(),
                    widget.Prompt(),
                    widget.CPU(format='cpu: {load_percent}%'),
                    widget.Memory(
                        format=(
                            'mem: {MemPercent:.1f}% '
                            'swap: {SwapPercent:.1f}%'),
                        measure_mem='G',
                        measure_swap='G'),
                    # widget.CPUGraph(**_graph_theme),
                    # widget.MemoryGraph(**_graph_theme),
                    # widget.SwapGraph(**_graph_theme),
                    _sep,
                    widget.CurrentLayout(),
                    _sep,
                    widget.Systray(),
                    widget.TextBox(text='🔊'),
                    widget.Volume(),
                    _sep,
                    widget.Clock(format='%Y-%m-%d %H:%M'),
                    _sep,
                    widget.QuickExit()],
                    bar_size,
                    background='171717')))
    else:
        screens.append(
            Screen(
                wallpaper=wallpaper,
                wallpaper_mode='fill',
                top=bar.Bar([
                    _create_groupbox(),
                    _create_tasklist(),
                    widget.CurrentLayout()],
                    bar_size,
                    background='171717')))

mouse = [
    Drag([_mod], 'Button1', lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([_mod], 'Button3', lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([_mod], 'Button2', lazy.window.bring_to_front()),
    Click([_mod, 'control'], 'Button1', lazy.window.toggle_floating())]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    *layout.Floating.default_float_rules,
    *[Match(**i) for i in floating_rules],
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry')],  # GPG key password entry
    **_layout_theme)
auto_fullscreen = True
focus_on_window_activation = 'smart'
reconfigure_screens = True
auto_minimize = True
