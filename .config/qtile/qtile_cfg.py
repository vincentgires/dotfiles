import re

groups_config = {
    'main': {
        'key': 'quotedbl',
        'layout': 'tile'},
    'net': {
        'key': 'guillemotleft',
        'layout': 'tile',
        'matches': [{'wm_class': ['firefox']}]},
    'dev': {
        'key': 'guillemotright',
        'layout': 'tile',
        'matches': [{'wm_class': ['kdevelop']}]},
    'chat': {
        'key': 'parenleft',
        'layout': 'tile',
        'matches': [{'wm_class': ['element', 'discord']}]},
    'media': {
        'key': 'parenright',
        'layout': 'tile'},
    'work': {
        'key': 'at',
        'layout': 'tile'},
    'lighting': {
        'key': 'plus',
        'layout': 'tile',
        'matches': [{'wm_class': ['maya.bin']}]},
    'compositing': {
        'key': 'minus',
        'layout': 'tile',
        'matches': [{'wm_class': ['Nuke']}]},
    'farm': {
        'key': 'slash',
        'layout': 'tile',
        'matches': [{'wm_class': ['xConsole.bin']}]},
    'review': {
        'key': 'asterisk',
        'layout': 'tile'}}
master_match = [
    {'wm_class': ['kdevelop', 'Nuke', 'Blender']},
    {'wm_class': 'maya.bin', 'title': re.compile('.*Autodesk Maya.*')}]
floating_rules = [
    {'wm_instance_class': ['vlc', 'TeamViewer']},
    {'wm_class': 'maya.bin',
     'title': [
         'Script Editor', 'Node Editor', 'Final pre-check', 'Batch render',
         'nWave Fenix4Maya']},
    {'wm_class': 'maya.bin', 'title': re.compile('Render Settings.*')},
    {'wm_class': 'maya.bin', 'title': re.compile('.*Options.*')}
]
font = 'ubuntu'
font_size = 13
wallpaper = '~/wallpaper.png'
bar_size = 25
