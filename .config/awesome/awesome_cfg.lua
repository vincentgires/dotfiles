config = {
  tags = {'main', 'net', 'dev', 'chat', 'media', 'work'},
  rules = {
    {rule_any = {class = {'firefox', 'brave-browser'}},
     properties = {tag = 'net'}},
    {rule = {class = 'kdevelop'},
     properties = {tag = 'dev'}},
    {rule_any = {class = {'Element', 'discord'}},
     properties = {tag = 'chat'}},
    {rule_any = {class = {'mpv', 'vlc', 'Audacious', 'QjackCtl'}},
     properties = {floating = true, ontop = true}},
    {rule = {class = 'Blender'},
     properties = {maximized = false}}
  },
  master_classes = {'Blender', 'firefox', 'code-oss'}
}

return config
