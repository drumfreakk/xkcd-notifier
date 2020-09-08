# xkcd-notifier

Displays the current xkcd comic and whether there are any new ones in polybar.
For options see `notifier --help`.


## Module

```
[module/xkcd]
type = custom/script
exec = ~/.config/polybar/xkcd-notifier/notifier.py -f ~/.config/polybar/xkcd-notifier/latest
click-left = xdg-open https://xkcd.com/ && ~/.config/polybar/xkcd-notifier/notifier.py -f ~/.config/polybar/xkcd-notifier/latest --read
interval = 300
```

