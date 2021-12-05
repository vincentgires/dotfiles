local config = require('awesome_cfg')
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
local terminal = os.getenv('TERMINAL')
local editor = os.getenv('EDITOR') or 'vim'
local editor_cmd = terminal .. ' -e ' .. editor

-- Define modkeys
local modkey = 'Mod4'
local altkey = 'Mod1'

-- Table of layouts to cover with awful.layout.inc, order matters.
awful.layout.layouts = {
  awful.layout.suit.tile,
  awful.layout.suit.spiral,
  awful.layout.suit.max,
  awful.layout.suit.floating
}
-- }}}

function delete_tag()
  local tag = awful.screen.focused().selected_tag
  if not tag then
    return
  end
  tag:delete()
end

function add_tag(name)
  local name = name or #awful.screen.focused().tags + 1
  awful.tag.add(name, {
    screen = awful.screen.focused(),
    layout = awful.layout.suit.tile}):view_only()
end

function rename_tag()
  awful.prompt.run {
    prompt = 'New tag name: ',
    textbox = awful.screen.focused().prompt_box.widget,
    exe_callback = function(new_name)
      if not new_name or #new_name == 0 then
        return
      end
      local tag = awful.screen.focused().selected_tag
      if tag then
        tag.name = new_name
      end
    end
  }
end

-- {{{ Menu
-- Create a launcher widget and a main menu
local awesome_menu = {
  {'hotkeys', function() hotkeys_popup.show_help(nil, awful.screen.focused()) end},
  {'manual', terminal .. ' -e man awesome'},
  {'edit config', editor_cmd .. ' ' .. awesome.conffile},
  {'toggle titlebar', function()
      for _, c in ipairs(client.get()) do
        awful.titlebar.toggle(c)
      end
    end},
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

-- {{{ Wibar
-- Create a textclock widget
local textclock_widget = wibox.widget.textclock('%Y-%m-%d %H:%M')

-- Create separator widget
local separator_widget = wibox.widget{
  markup = ' | ',
  widget = wibox.widget.textbox}

-- Create volume widget
volume_buttons = awful.util.table.join(
    awful.button({}, 1, function() awful.spawn(terminal .. ' -e alsamixer') end),
    awful.button({}, 2, function() awful.spawn('amixer -q set Master toggle') end), -- mute
    awful.button({}, 4, function() awful.spawn('amixer -c 0 sset Master 1+ unmute') end), -- raise
    awful.button({}, 5, function() awful.spawn('amixer -c 0 sset Master 1- unmute') end) -- lower
)

local volume_widget = wibox.widget{
  markup = 'volume',
  align = 'center',
  valign = 'center',
  widget = wibox.widget.textbox,
  buttons = volume_buttons}

function volume_widget:update()
  local get_volume_cmd = "amixer sget Master | grep 'Left:' | awk -F'[][]' '{print $2}'"
  awful.spawn.easy_async_with_shell(get_volume_cmd, function(out)
      self.markup = '🔊 ' .. out
  end)
end

-- Create battery widget
local battery_widget = wibox.widget{
  markup = 'battery',
  align = 'center',
  valign = 'center',
  widget = wibox.widget.textbox}

function battery_widget:update()
  local capacity_file = '/sys/class/power_supply/BAT1/capacity'
  local f = io.open(capacity_file, 'r')
  if f then
    self.markup = 'battery ' .. f:read() .. '%'
    f:close()
  else
    self.markup = 'no battery'
  end
end

-- Create cpu widget
local cpu_widget = wibox.widget{
  markup = 'cpu',
  align = 'center',
  valign = 'center',
  widget = wibox.widget.textbox}

function cpu_widget:update()
  local get_cpu_cmd = "top -b -n1 | grep 'Cpu(s)' | awk '{print int(($2 + $4)) \"%\"}'"
  awful.spawn.easy_async_with_shell(get_cpu_cmd, function(out)
      self.markup = 'cpu ' .. out
  end)
end

-- Create memory widget
local memory_widget = wibox.widget{
  markup = 'memory',
  align = 'center',
  valign = 'center',
  widget = wibox.widget.textbox}

function memory_widget:update()
  local get_memory_cmd = 'free | awk \'/^Mem/ {print int(($3 / $2) * 100) "%"}\''
  awful.spawn.easy_async_with_shell(get_memory_cmd, function(out)
      self.markup = 'mem ' .. out
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
  awful.tag(config.tags, s, awful.layout.layouts[1])

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
    buttons = tasklist_buttons,
    style = {disable_task_name = true}}

  -- Create a title focused window
  s.tasktitle_widget = awful.widget.tasklist{
    screen = s,
    filter = awful.widget.tasklist.filter.focused,
    style = {tasklist_disable_icon = true}}

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
    { -- Middle widget
      layout = wibox.layout.fixed.horizontal,
      s.tasklist_widget,
      s.tasktitle_widget,
    },
    { -- Right widgets
      layout = wibox.layout.fixed.horizontal,
      cpu_widget,
      separator_widget,
      memory_widget,
      separator_widget,
      battery_widget,
      separator_widget,
      wibox.widget.systray(),
      volume_widget,
      separator_widget,
      textclock_widget,
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
    {modkey}, 't', awful.tag.viewprev,
    {description = 'view previous', group = 'tag'}),
  awful.key(
    {modkey}, 'n', awful.tag.viewnext,
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

  -- Awesome session
  awful.key(
    {modkey, 'Control'}, 'o', awesome.restart,
    {description = 'reload awesome', group = 'awesome'}),
  awful.key(
    {modkey, 'Control'}, 'q', awesome.quit,
    {description = 'quit awesome', group = 'awesome'}),

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

  awful.key(
    {modkey}, 'j', function() awful.tag.incmwfact(0.05) end,
    {description = 'increase master width factor', group = 'layout'}),
  awful.key(
    {modkey}, 'v', function() awful.tag.incmwfact(-0.05) end,
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
  awful.key(
    {modkey}, 'x', function() awful.screen.focused().prompt_box:run() end,
    {description = 'run prompt', group = 'launcher'}),
  awful.key(
    {modkey, 'Control'}, 'x',
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
    {description = 'show the menubar', group = 'launcher'}),

  -- Add tag
  awful.key(
    {modkey, 'Control', 'Shift'}, 'n', add_tag,
    {description = 'add tag ', group = 'tag'}),

  -- Delete tag
  awful.key(
    {modkey, 'Control', 'Shift'}, 'd', delete_tag,
    {description = 'delete tag ', group = 'tag'}),

  -- Rename tag
  awful.key(
    {modkey}, 'F2', rename_tag,
    {description = 'rename tag ', group = 'tag'})
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

  -- Titlebars to normal clients and dialogs
  {
    rule_any = {type = {'normal', 'dialog'}},
    properties = {titlebars_enabled = false}
  },

  -- Make dialogs ontop to avoid losing them behind tiled windows
  {
    rule_any = {type = {'dialog'}},
    properties = {ontop = true}
  }
}

-- Add rules from awesome_cfg file
for _, v in ipairs(config.rules) do
  table.insert(awful.rules.rules, v)
end

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

  local titlebar = awful.titlebar(c, {size = 20})

  titlebar:setup{
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
      awful.titlebar.widget.minimizebutton(c),
      awful.titlebar.widget.maximizedbutton(c),
      awful.titlebar.widget.stickybutton(c),
      awful.titlebar.widget.ontopbutton(c),
      awful.titlebar.widget.floatingbutton(c),
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
  timeout = 0.2,
  autostart = true,
  callback = function()
    volume_widget:update()
  end
}

gears.timer{
  timeout = 5,
  autostart = true,
  callback = function()
    battery_widget:update()
    cpu_widget:update()
    memory_widget:update()
  end
}

-- Startup
volume_widget:update()
battery_widget:update()
memory_widget:update()
