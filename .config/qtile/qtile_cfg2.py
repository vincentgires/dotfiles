import re

groups_config = {
    '1. main': {
        'key': 'quotedbl',
        'layout': 'tile'},
    '2. net': {
        'key': 'guillemotleft',
        'layout': 'tile',
        'matches': [{'wm_class': ['firefox']}]},
    '3. dev': {
        'key': 'guillemotright',
        'layout': 'tile',
        'matches': [{'wm_class': ['kdevelop', 'code']}]},
    '4. chat': {
        'key': 'parenleft',
        'layout': 'tile',
        'matches': [{'wm_class': ['element', 'discord']}]},
    '5. media': {
        'key': 'parenright',
        'layout': 'tile'},
    '6. work': {
        'key': 'at',
        'layout': 'tile'},
    '7. maya': {
        'key': 'plus',
        'layout': 'tile',
        'matches': [{'wm_class': ['maya.bin']}]},
    '8. nuke': {
        'key': 'minus',
        'layout': 'tile',
        'matches': [{'wm_class': ['Nuke']}]},
    '9. muster': {
        'key': 'slash',
        'layout': 'tile',
        'matches': [{'wm_class': ['xConsole.bin']}]},
    '0. review': {
        'key': 'asterisk',
        'layout': 'tile'}}
master_match = [
    {'wm_class': [
        'kdevelop',
        'Nuke',
        'Blender',
        'code',
        'Katana']},
    {'wm_class': 'maya.bin',
     'title': re.compile('.*Autodesk Maya.*', re.IGNORECASE)}]
floating_rules = [
    {'wm_instance_class': ['vlc', 'TeamViewer']},
    {'wm_class': 'maya.bin',
     'title': [
         'Script Editor',
         'Node Editor']},
    {'wm_class': 'maya.bin', 'title': re.compile('Render Settings.*')},
    {'wm_class': 'maya.bin', 'title': re.compile('.*Options.*')}
]
font = 'ubuntu'
font_size = 13
wallpaper = '~/wallpaper.png'
bar_size = 25
