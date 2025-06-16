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
        'layout': 'tile'}}
master_match = [
    {'wm_class': [
        'kdevelop',
        'Nuke',
        'Blender',
        'code']}]
floating_rules = [
    {'wm_instance_class': ['vlc', 'TeamViewer']}]
font = 'ubuntu'
font_size = 13
wallpaper = '/data/wallpaper.png'
bar_size = 25
