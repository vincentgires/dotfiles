groups_config = {
    'main': {
        'key': 'quotedbl',
        'layout': 'tile'},
    'net': {
        'key': 'guillemotleft',
        'layout': 'tile',
        'matches': [{'wm_class': ['Firefox']}]},
    'dev': {
        'key': 'guillemotright',
        'layout': 'tile',
        'matches': [{'wm_class': ['kdevelop']}]},
    'chat': {
        'key': 'parenleft',
        'layout': 'tile',
        'matches': [{'wm_class': ['element', 'discord']}]},
    'music': {
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

master_match = {'wm_class': ['kdevelop', 'Nuke', 'maya.bin', 'Blender']}
