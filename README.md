# genshin_calendar

~~公主连结~~原神图形化活动日历插件，Fork的公主连接版本，适用于 `HoshinoBot v2`.

项目地址 <https://github.com/NepPure/genshin_calendar>

![calendar](preview.gif)

## 日程信息源

原神没找到合适的可以扒的数据源，我们先整个静态文件将就一下

数据大概就从这里来，https://bbs.mihoyo.com/ys/home/28?type=1

做个爬虫也不是不行，但是总觉得不会很准确，先能用(╯‵□′)╯︵┻━┻

https://genshin-calendar.neptunia.vip/event.json


## 安装方法

1. 在HoshinoBot的插件目录modules下clone本项目 `git clone https://github.com/NepPure/genshin_calendar.git`
1. 在 `config/__bot__.py`的模块列表里加入 `genshin_calendar`
1. 重启HoshinoBot

## 指令列表

- `原神日历` : 查看本群订阅服务器日历
- `原神日历 on/off` : 订阅/取消订阅指定服务器的日历推送
- `原神日历 time 时:分` : 设置日历推送时间
- `原神日历 status` : 查看本群日历推送设置
- `原神日历 cardimage` : (go-cqhttp限定)切换是否使用cardimage模式发送日历图片
