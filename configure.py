import os


def _create_symlink(src, dst, create_folder=None):
    if create_folder is not None:
        os.makedirs(os.path.expandvars(create_folder), exist_ok=True)
    current_path = os.path.dirname(__file__)
    os.symlink(
        os.path.join(current_path, os.path.expandvars(src)),
        os.path.expandvars(dst))


_create_symlink('.config/awesome', '$HOME/.config/awesome')
_create_symlink('.config/mpv', '$HOME/.config/mpv')
_create_symlink('.config/qtile', '$HOME/.config/qtile')
_create_symlink('.config/git', '$HOME/.config/git')
_create_symlink('.vimrc', '$HOME/.vimrc')
_create_symlink('.xbindkeysrc', '$HOME/.xbindkeysrc')
_create_symlink('.xprofile', '$HOME/.xprofile')
_create_symlink('.config/fish/config.fish', '$HOME/.config/fish/config.fish', create_folder='$HOME/.config/fish')
_create_symlink('.config/ranger/rc.conf', '$HOME/.config/ranger/rc.conf', create_folder='$HOME/.config/ranger')

os.system('sudo pacman -S alacritty awesome dmenu fish git lxappearance mpv qt5ct qtile ranger tk ttf-hack ttf-ubuntu-font-family vim xbindkeys')
os.system('chsh -s $(which fish)')
