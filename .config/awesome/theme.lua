local theme_assets = require('beautiful.theme_assets')
local xresources = require('beautiful.xresources')
local gfs = require('gears.filesystem')

local dpi = xresources.apply_dpi
local themes_path = gfs.get_themes_dir()
local image_path = '~/.config/awesome/images'

local theme = {}
-- Add any variables and access them by using beautiful.variable in your rc.lua

theme.wallpaper = '/data/wallpaper.png'
theme.font = 'ubuntu 11'

theme.bg_normal = '#222222'
theme.bg_focus = '#131313'
theme.bg_urgent = '#ff0000'
theme.bg_minimize = '#444444'
theme.bg_systray = theme.bg_normal

theme.fg_normal = '#aaaaaa'
theme.fg_focus = '#ffffff'
theme.fg_urgent = '#ffffff'
theme.fg_minimize = '#ffffff'

theme.useless_gap = dpi(3)
theme.border_width = dpi(1)
theme.border_normal = '#222222'
theme.border_focus = '#555555'
theme.border_marked = '#91231c'

theme.taglist_fg_focus = '#d5d5d5'
theme.taglist_fg_occupied = '#d5d5d5'
theme.taglist_fg_urgent = '#db716b'
theme.taglist_fg_empty = '#666666'
theme.taglist_spacing = 2

theme.menu_submenu_icon = themes_path .. 'default/submenu.png'
theme.menu_height = dpi(18)
theme.menu_width  = dpi(125)

-- Titlebar images
titlebar_img = {
  titlebar_close_button_normal = '/titlebar/close.svg',
  titlebar_close_button_normal_hover  = '/titlebar/close_hover.svg',
  titlebar_minimize_button_normal = '/titlebar/minimize.svg',
  titlebar_ontop_button_normal_inactive = '/titlebar/ontop.svg',
  titlebar_ontop_button_normal_active = '/titlebar/ontop_active.svg',
  titlebar_ontop_button_focus_inactive = '/titlebar/ontop.svg',
  titlebar_ontop_button_focus_active = '/titlebar/ontop_active.svg',
  titlebar_sticky_button_normal_inactive = '/titlebar/sticky.svg',
  titlebar_sticky_button_normal_active = '/titlebar/sticky_active.svg',
  titlebar_sticky_button_focus_inactive = '/titlebar/sticky.svg',
  titlebar_sticky_button_focus_active = '/titlebar/sticky_active.svg',
  titlebar_floating_button_normal_inactive = '/titlebar/tiling.svg',
  titlebar_floating_button_normal_active = '/titlebar/floating.svg',
  titlebar_floating_button_focus_inactive = '/titlebar/tiling.svg',
  titlebar_floating_button_focus_active = '/titlebar/floating.svg',
  titlebar_maximized_button_normal_inactive = '/titlebar/maximize.svg',
  titlebar_maximized_button_normal_active = '/titlebar/maximize_active.svg',
  titlebar_maximized_button_focus_inactive = '/titlebar/maximize.svg',
  titlebar_maximized_button_focus_active = '/titlebar/maximize_active.svg'
}
for k, v in pairs(titlebar_img) do
  theme[k] = image_path .. v
end

-- Layout images
theme.layout_fairh = themes_path .. 'default/layouts/fairhw.png'
theme.layout_fairv = themes_path .. 'default/layouts/fairvw.png'
theme.layout_floating  = themes_path .. 'default/layouts/floatingw.png'
theme.layout_magnifier = themes_path .. 'default/layouts/magnifierw.png'
theme.layout_max = themes_path .. 'default/layouts/maxw.png'
theme.layout_fullscreen = themes_path .. 'default/layouts/fullscreenw.png'
theme.layout_tilebottom = themes_path .. 'default/layouts/tilebottomw.png'
theme.layout_tileleft   = themes_path .. 'default/layouts/tileleftw.png'
theme.layout_tile = themes_path .. 'default/layouts/tilew.png'
theme.layout_tiletop = themes_path .. 'default/layouts/tiletopw.png'
theme.layout_spiral  = themes_path .. 'default/layouts/spiralw.png'
theme.layout_dwindle = themes_path .. 'default/layouts/dwindlew.png'
theme.layout_cornernw = themes_path .. 'default/layouts/cornernww.png'
theme.layout_cornerne = themes_path .. 'default/layouts/cornernew.png'
theme.layout_cornersw = themes_path .. 'default/layouts/cornersww.png'
theme.layout_cornerse = themes_path .. 'default/layouts/cornersew.png'

-- Generate Awesome icon:
theme.awesome_icon = theme_assets.awesome_icon(
  theme.menu_height, theme.bg_focus, theme.fg_focus
)

-- Define the icon theme for application icons. If not set then the icons
-- from /usr/share/icons and /usr/share/icons/hicolor will be used.
theme.icon_theme = nil

return theme
