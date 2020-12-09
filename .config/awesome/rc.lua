-- Standard awesome library
local gears = require('gears')
local awful = require('awful')
require('awful.autofocus')
-- Widget and layout library
local wibox = require('wibox')
-- Theme handling library
local beautiful = require('beautiful')
-- Notification library
local naughty = require('naughty')
local menubar = require('menubar')
local hotkeys_popup = require('awful.hotkeys_popup')
-- Enable hotkeys help widget for VIM and other apps
-- when client with a matching name is opened:
require('awful.hotkeys_popup.keys')

-- {{{ Error handling
-- Check if awesome encountered an error during startup and fell back to
-- another config (This code will only ever execute for the fallback config)
if awesome.startup_errors then
  naughty.notify({
    preset = naughty.config.presets.critical,
    title = 'There were errors during startup!',
    text = awesome.startup_errors})
end

-- Handle runtime errors after startup
do
  local in_error = false
  awesome.connect_signal('debug::error', function(err)
    -- Make sure we don't go into an endless error loop
    if in_error then return end
    in_error = true

    naughty.notify({
      preset = naughty.config.presets.critical,
      title = 'An error happened!',
      text = tostring(err)})
    in_error = false
  end)
end
-- }}}

-- {{{ Variable definitions
-- Themes define colours, icons, font and wallpapers.
beautiful.init('~/.config/awesome/theme.lua')

-- Applications
local terminal = 'alacritty'
local editor = os.getenv('EDITOR') or 'nano'
local editor_cmd = terminal .. ' -e ' .. editor

-- Define modkeys
local modkey = 'Mod4'
local altkey = 'Mod1'

-- Table of layouts to cover with awful.layout.inc, order matters.
awful.layout.layouts = {
  awful.layout.suit.tile,
  awful.layout.suit.tile.left,
  awful.layout.suit.tile.bottom,
  awful.layout.suit.tile.top,
  awful.layout.suit.spiral,
  -- awful.layout.suit.spiral.dwindle,
  awful.layout.suit.max,
  awful.layout.suit.floating
}
-- }}}

-- {{{ Menu
-- Create a launcher widget and a main menu
local awesome_menu = {
  {'hotkeys', function() hotkeys_popup.show_help(nil, awful.screen.focused()) end},
  {'manual', terminal .. ' -e man awesome'},
  {'edit config', editor_cmd .. ' ' .. awesome.conffile},
  {'restart', awesome.restart},
  {'quit', function() awesome.quit() end},
}

local main_menu = awful.menu({
  items = {
    {'awesome', awesome_menu, beautiful.awesome_icon},
    {'open terminal', terminal}}
})

local launcher = awful.widget.launcher({
  image = beautiful.awesome_icon,
  menu = main_menu})

-- Menubar configuration
menubar.utils.terminal = terminal -- Set the terminal for applications that require it
-- }}}

-- Keyboard map indicator and switcher
local keyboard_layout = awful.widget.keyboardlayout()

-- {{{ Wibar
-- Create a textclock widget
local textclock_widget = wibox.widget.textclock('%Y-%m-%d %H:%M')

-- Create separator widget
local separator_widget = wibox.widget{
  markup = ' | ',
  widget = wibox.widget.textbox}

-- Create volume widget
local volume_widget = wibox.widget{
  markup = 'volume',
  align = 'center',
  valign = 'center',
  widget = wibox.widget.textbox}

function volume_widget:update()
  local get_volume_cmd = "amixer sget Master | grep 'Left:' | awk -F'[][]' '{print $2}'"
  awful.spawn.easy_async_with_shell(get_volume_cmd, function(out)
      self.markup = 'volume ' .. out
  end)
end

-- Create memory widget
local memory_widget = wibox.widget{
  markup = 'memory',
  align = 'center',
  valign = 'center',
  widget = wibox.widget.textbox}

function memory_widget:update()
  local get_memory_cmd = 'free -h | awk \'/Mem:/ {print $3 " / " $2}\''
  awful.spawn.easy_async_with_shell(get_memory_cmd, function(out)
      self.markup = 'memory ' .. out
  end)
end

-- Create a wibox for each screen and add it
local taglist_buttons = gears.table.join(
  awful.button({}, 1, function(t) t:view_only() end),
  awful.button({modkey}, 1,
    function(t)
      if client.focus then
        client.focus:move_to_tag(t)
      end
    end),
  awful.button({}, 3, awful.tag.viewtoggle),
  awful.button({modkey}, 3,
    function(t)
      if client.focus then
        client.focus:toggle_tag(t)
      end
    end),
  awful.button({}, 4, function(t) awful.tag.viewnext(t.screen) end),
  awful.button({}, 5, function(t) awful.tag.viewprev(t.screen) end)
)

local tasklist_buttons = gears.table.join(
  awful.button({}, 1,
    function(c)
      if c == client.focus then
        c.minimized = true
      else
        c:emit_signal(
          'request::activate',
          'tasklist',
          {raise = true})
      end
    end),
  awful.button({}, 3,
    function()
      awful.menu.client_list({theme = {width = 250}})
    end),
  awful.button({}, 4,
    function()
      awful.client.focus.byidx(1)
    end),
  awful.button({}, 5,
    function()
      awful.client.focus.byidx(-1)
    end))

local function set_wallpaper(s)
  -- Wallpaper
  if beautiful.wallpaper then
    local wallpaper = beautiful.wallpaper
    -- If wallpaper is a function, call it with the screen
    if type(wallpaper) == 'function' then
      wallpaper = wallpaper(s)
    end
    gears.wallpaper.maximized(wallpaper, s, true)
  end
end

-- Re-set wallpaper when a screen's geometry changes (e.g. different resolution)
screen.connect_signal('property::geometry', set_wallpaper)

awful.screen.connect_for_each_screen(function(s)
  -- Wallpaper
  set_wallpaper(s)

  -- Each screen has its own tag table
  awful.tag({'main', 'net', 'dev', 'chat', 'music', 'work'}, s, awful.layout.layouts[1])

  -- Create a promptbox for each screen
  s.prompt_box = awful.widget.prompt()

  -- Create an imagebox widget which will contain an icon indicating which layout we're using
  -- We need one layoutbox per screen
  s.layoutbox_widget = awful.widget.layoutbox(s)
  s.layoutbox_widget:buttons(
    gears.table.join(
      awful.button({}, 1, function() awful.layout.inc(1) end),
      awful.button({}, 3, function() awful.layout.inc(-1) end),
      awful.button({}, 4, function() awful.layout.inc(1) end),
      awful.button({}, 5, function() awful.layout.inc(-1) end)))

  -- Create a taglist widget
  s.tag_list = awful.widget.taglist{
    screen = s,
    filter = awful.widget.taglist.filter.all,
    buttons = taglist_buttons}

  -- Create a tasklist widget
  s.tasklist_widget = awful.widget.tasklist{
    screen = s,
    filter = awful.widget.tasklist.filter.currenttags,
    buttons = tasklist_buttons}

  -- Create the wibox
  s.main_wibar = awful.wibar({position = 'top', screen = s})

  -- Add widgets to the wibox
  s.main_wibar:setup{
    layout = wibox.layout.align.horizontal,
    { -- Left widgets
      layout = wibox.layout.fixed.horizontal,
      launcher,
      s.tag_list,
      s.prompt_box,
    },
    s.tasklist_widget, -- Middle widget
    { -- Right widgets
      layout = wibox.layout.fixed.horizontal,
      keyboard_layout,
      wibox.widget.systray(),
      separator_widget,
      textclock_widget,
      separator_widget,
      memory_widget,
      separator_widget,
      volume_widget,
      separator_widget,
      s.layoutbox_widget
    },
  }
end)
-- }}}

-- {{{ Mouse bindings
root.buttons(gears.table.join(
  awful.button({}, 3, function() main_menu:toggle() end),
  awful.button({}, 4, awful.tag.viewnext),
  awful.button({}, 5, awful.tag.viewprev)))
-- }}}

-- {{{ Key bindings
local globalkeys = gears.table.join(
  awful.key(
    {modkey}, 'F1', hotkeys_popup.show_help,
    {description = 'show help', group = 'awesome'}),
  awful.key(
    {modkey}, 'Left', awful.tag.viewprev,
    {description = 'view previous', group = 'tag'}),
  awful.key(
    {modkey}, 'Right', awful.tag.viewnext,
    {description = 'view next', group = 'tag'}),
  awful.key(
    {modkey}, 'Escape', awful.tag.history.restore,
    {description = 'go back', group = 'tag'}),

  awful.key({modkey}, 's',
    function()
      awful.client.focus.byidx( 1)
    end,
    {description = 'focus next by index', group = 'client'}),
  awful.key({modkey}, 'r',
    function()
      awful.client.focus.byidx(-1)
    end,
    {description = 'focus previous by index', group = 'client'}),
  awful.key(
    {modkey}, 'w', function() main_menu:show() end,
    {description = 'show main menu', group = 'awesome'}),

  -- Layout manipulation
  awful.key(
    {modkey, 'Shift'}, 's', function() awful.client.swap.byidx(1) end,
    {description = 'swap with next client by index', group = 'client'}),
  awful.key(
    {modkey, 'Shift'}, 'r', function() awful.client.swap.byidx(-1) end,
    {description = 'swap with previous client by index', group = 'client'}),
  awful.key(
    {modkey, 'Control'}, 's', function() awful.screen.focus_relative(1) end,
    {description = 'focus the next screen', group = 'screen'}),
  awful.key(
    {modkey, 'Control'}, 'r', function() awful.screen.focus_relative(-1) end,
    {description = 'focus the previous screen', group = 'screen'}),
  awful.key(
    {modkey}, 'Tab',
    function()
      awful.client.focus.history.previous()
      if client.focus then
        client.focus:raise()
      end
    end,
    {description = 'go back', group = 'client'}),

  -- Standard program
  -- awful.key(
  --   {modkey}, 'Return', function() awful.spawn(terminal) end,
  --   {description = 'open a terminal', group = 'launcher'}),
  awful.key(
    {modkey, 'Control'}, 'o', awesome.restart,
    {description = 'reload awesome', group = 'awesome'}),
  awful.key(
    {modkey, 'Control'}, 'q', awesome.quit,
    {description = 'quit awesome', group = 'awesome'}),

  awful.key(
    {modkey}, 'n', function() awful.tag.incmwfact(0.05) end,
    {description = 'increase master width factor', group = 'layout'}),
  awful.key(
    {modkey}, 't', function() awful.tag.incmwfact(-0.05) end,
    {description = 'decrease master width factor', group = 'layout'}),
  awful.key(
    {modkey}, 'l', function() awful.client.incwfact(0.05) end,
    {description = 'increase master width factor', group = 'layout'}),
  awful.key(
    {modkey}, 'd', function() awful.client.incwfact(-0.05) end,
    {description = 'decrease master width factor', group = 'layout'}),
  awful.key(
    {modkey, 'Shift'}, 't', function() awful.tag.incnmaster(1, nil, true) end,
    {description = 'increase the number of master clients', group = 'layout'}),
  awful.key(
    {modkey, 'Shift'}, 'n', function() awful.tag.incnmaster(-1, nil, true) end,
    {description = 'decrease the number of master clients', group = 'layout'}),
  awful.key(
    {modkey, 'Control'}, 't', function() awful.tag.incncol(1, nil, true) end,
    {description = 'increase the number of columns', group = 'layout'}),
  awful.key(
    {modkey, 'Control'}, 'n', function() awful.tag.incncol(-1, nil, true) end,
    {description = 'decrease the number of columns', group = 'layout'}),
  awful.key(
    {modkey}, 'space', function() awful.layout.inc(1) end,
    {description = 'select next', group = 'layout'}),
  awful.key(
    {modkey, 'Shift'}, 'space', function() awful.layout.inc(-1) end,
    {description = 'select previous', group = 'layout'}),

  -- Prompt
  -- awful.key(
    -- {altkey}, 'r', function() awful.screen.focused().prompt_box:run() end,
    -- {altkey}, 'space', function() awful.spawn('dmenu_run -p Run: -l 5 -sb dimgrey') end,
    -- {description = 'run prompt', group = 'launcher'}),
  awful.key(
    {modkey}, 'x',
    function()
      awful.prompt.run{
        prompt = 'Run Lua code: ',
        textbox = awful.screen.focused().prompt_box.widget,
        exe_callback = awful.util.eval,
        history_path = awful.util.get_cache_dir() .. '/history_eval'}
    end,
    {description = 'lua execute prompt', group = 'awesome'}),

  -- Menubar
  awful.key(
    {modkey}, 'p', function() menubar.show() end,
    {description = 'show the menubar', group = 'launcher'})

  -- Sound volume
  -- awful.key(
  --   {}, 'XF86AudioMute',
  --   function()
  --     awful.spawn.with_shell('amixer -q set Master toggle')
  --     volume_widget:update()
  --   end,
  --   {description = 'mute sound', group = 'sound'}),
  -- awful.key(
  --   {}, 'XF86AudioLowerVolume',
  --   function()
  --     awful.spawn.with_shell('amixer -c 0 sset Master 1- unmute')
  --     volume_widget:update()
  --   end,
  --   {description = 'lower volume', group = 'sound'}),
  -- awful.key(
  --   {}, 'XF86AudioRaiseVolume',
  --   function()
  --     awful.spawn.with_shell('amixer -c 0 sset Master 1+ unmute')
  --     volume_widget:update()
  --   end,
  --   {description = 'raise volume', group = 'sound'}),
  --
  -- -- Screen brightness
  -- awful.key(
  --   {}, 'XF86MonBrightnessDown', function() awful.spawn.with_shell('xbacklight -dec 15') end,
  --   {description = 'lower brightness', group = 'sound'}),
  -- awful.key(
  --   {}, 'XF86MonBrightnessUp', function() awful.spawn.with_shell('xbacklight -inc 15') end,
  --   {description = 'raise brightness', group = 'sound'})
)

local clientkeys = gears.table.join(
  awful.key({modkey}, 'f',
    function(c)
      c.fullscreen = not c.fullscreen
      c:raise()
    end,
    {description = 'toggle fullscreen', group = 'client'}),
  awful.key(
    {modkey}, 'c', function(c) c:kill() end,
    {description = 'close', group = 'client'}),
  awful.key(  -- same function but useful to use with a mouse
    {modkey}, 'eacute', function(c) c:kill() end,
    {description = 'close', group = 'client'}),
  awful.key(
    {modkey, 'Control'}, 'f',
    function(c)
      awful.client.floating.toggle()
      c.ontop = not c.ontop
    end,
    {description = 'toggle floating', group = 'client'}),
  awful.key(
    {modkey, 'Control'}, 'Return', function(c) c:swap(awful.client.getmaster()) end,
    {description = 'move to master', group = 'client'}),
  awful.key(
    {modkey}, 'o', function(c) c:move_to_screen() end,
    {description = 'move to screen', group = 'client'}),
  awful.key(
    {modkey, 'Control'}, 'm',
    function(c)
      -- The client currently has the input focus, so it cannot be
      -- minimized, since minimized clients can't have the focus.
      c.minimized = true
    end ,
    {description = 'minimize', group = 'client'}),
  awful.key(
    {modkey}, 'm',
    function(c)
      c.maximized = not c.maximized
      c:raise()
    end,
    {description = '(un)maximize', group = 'client'}),
  awful.key(
    {modkey, 'Control'}, 'm',
    function(c)
      c.maximized_vertical = not c.maximized_vertical
      c:raise()
    end,
    {description = '(un)maximize vertically', group = 'client'}),
  awful.key(
    {modkey, 'Shift'}, 'm',
    function(c)
      c.maximized_horizontal = not c.maximized_horizontal
      c:raise()
    end,
    {description = '(un)maximize horizontally', group = 'client'})
)

-- Bind all key numbers to tags
-- Be careful: we use keycodes to make it work on any keyboard layout
-- This should map on the top row of your keyboard, usually 1 to 9
for i = 1, 9 do
  globalkeys = gears.table.join(globalkeys,
    -- View tag only.
    awful.key(
      {modkey}, '#' .. i + 9,
      function()
        local screen = awful.screen.focused()
        local tag = screen.tags[i]
        if tag then
          tag:view_only()
        end
      end,
      {description = 'view tag #'..i, group = 'tag'}),
    -- Toggle tag display.
    awful.key(
      {modkey, 'Control'}, '#' .. i + 9,
      function()
        local screen = awful.screen.focused()
        local tag = screen.tags[i]
        if tag then
          awful.tag.viewtoggle(tag)
        end
      end,
      {description = 'toggle tag #' .. i, group = 'tag'}),
    -- Move client to tag.
    awful.key(
      {modkey, 'Shift'}, '#' .. i + 9,
      function()
        if client.focus then
          local tag = client.focus.screen.tags[i]
          if tag then
            client.focus:move_to_tag(tag)
          end
        end
      end,
      {description = 'move focused client to tag #' .. i, group = 'tag'}),
    -- Toggle tag on focused client.
    awful.key(
      {modkey, 'Control', 'Shift'}, '#' .. i + 9,
      function()
        if client.focus then
          local tag = client.focus.screen.tags[i]
          if tag then
            client.focus:toggle_tag(tag)
          end
        end
      end,
      {description = 'toggle focused client on tag #' .. i, group = 'tag'})
  )
end

clientbuttons = gears.table.join(
  awful.button({}, 1,
    function(c)
      c:emit_signal('request::activate', 'mouse_click', {raise = true})
    end),
  awful.button({modkey}, 1,
    function(c)
      c:emit_signal('request::activate', 'mouse_click', {raise = true})
      awful.mouse.client.move(c)
    end),
  awful.button({modkey}, 3,
    function(c)
      c:emit_signal('request::activate', 'mouse_click', {raise = true})
      awful.mouse.client.resize(c)
    end)
)

-- Set keys
root.keys(globalkeys)
-- }}}

-- {{{ Rules
-- Rules to apply to new clients (through the 'manage' signal)
awful.rules.rules = {
  -- All clients will match this rule
  {
    rule = {},
    properties = {
      border_width = beautiful.border_width,
      border_color = beautiful.border_normal,
      focus = awful.client.focus.filter,
      raise = true,
      keys = clientkeys,
      buttons = clientbuttons,
      screen = awful.screen.preferred,
      placement = awful.placement.no_overlap + awful.placement.no_offscreen
    }
  },

  -- Floating clients
  {
    rule_any = {
      instance = {
        'DTA',  -- Firefox addon DownThemAll
        'copyq',  -- Includes session name in class
        'pinentry',
      },
      class = {
        'Arandr',
        'Blueman-manager',
        'Gpick',
        'Kruler',
        'MessageWin',  -- kalarm
        'Sxiv',
        'Tor Browser', -- Needs a fixed window size to avoid fingerprinting by screen size
        'Wpa_gui',
        'veromix',
        'xtightvncviewer'},

      -- Note that the name property shown in xprop might be set slightly after creation of the client
      -- and the name shown there might not match defined rules here
      name = {
        'Event Tester',  -- xev
      },
      role = {
        'AlarmWindow',  -- Thunderbird's calendar
        'ConfigManager',  -- Thunderbird's about:config
        'pop-up',  -- e.g. Google Chrome's (detached) Developer Tools
      }
    },
    properties = {floating = true}
  },

  -- Add titlebars to normal clients and dialogs
  {
    rule_any = {type = {'normal', 'dialog'}},
    properties = {titlebars_enabled = true}
  },

  -- Set Firefox to always map on the tag named '2' on screen 1
  -- {rule = { class = 'Firefox'},
  --  properties = {screen = 1, tag = '2'}},

  -- Set Blender to not start as maximize which is the default on this application
  {
    rule_any = {
      class = {'Blender'},
    },
    properties = {maximized = false, minimized = true}
  },
}
-- }}}

-- {{{ Signals
-- Signal function to execute when a new client appears
client.connect_signal('manage', function(c)
  -- Set the windows at the slave
  -- i.e. put it at the end of others instead of setting it master
  -- if not awesome.startup then awful.client.setslave(c) end

  if awesome.startup
    and not c.size_hints.user_position
    and not c.size_hints.program_position then
      -- Prevent clients from being unreachable after screen count changes
      awful.placement.no_offscreen(c)
  end
end)

-- Add a titlebar if titlebars_enabled is set to true in the rules
client.connect_signal('request::titlebars', function(c)
  -- buttons for the titlebar
  local buttons = gears.table.join(
    awful.button({}, 1,
      function()
        c:emit_signal('request::activate', 'titlebar', {raise = true})
        awful.mouse.client.move(c)
      end),
    awful.button({}, 3,
      function()
        c:emit_signal('request::activate', 'titlebar', {raise = true})
        awful.mouse.client.resize(c)
      end)
  )

  awful.titlebar(c):setup{
    { -- Left
      awful.titlebar.widget.iconwidget(c),
      buttons = buttons,
      layout = wibox.layout.fixed.horizontal
    },
    { -- Middle
      { -- Title
        align = 'center',
        widget = awful.titlebar.widget.titlewidget(c)
      },
      buttons = buttons,
      layout = wibox.layout.flex.horizontal
    },
    { -- Right
      awful.titlebar.widget.floatingbutton(c),
      awful.titlebar.widget.maximizedbutton(c),
      awful.titlebar.widget.stickybutton(c),
      awful.titlebar.widget.ontopbutton(c),
      awful.titlebar.widget.closebutton(c),
      layout = wibox.layout.fixed.horizontal()
    },
    layout = wibox.layout.align.horizontal
  }
end)

-- Enable sloppy focus, so that focus follows mouse
client.connect_signal('mouse::enter', function(c)
  c:emit_signal('request::activate', 'mouse_enter', {raise = false})
end)

client.connect_signal('focus', function(c) c.border_color = beautiful.border_focus end)
client.connect_signal('unfocus', function(c) c.border_color = beautiful.border_normal end)
-- }}}

-- Timer update
gears.timer{
  timeout = 5,
  autostart = true,
  callback = function()
    volume_widget:update()
    memory_widget:update()
  end
}

-- Startup
volume_widget:update()
memory_widget:update()
