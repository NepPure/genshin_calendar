import os
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import aiohttp
import asyncio
import math

# type 0普通 1双倍 2 公会战 3 活动

event_data = {
    'cn': [],
}

event_updated = {
    'cn': '',
}

lock = {
    'cn': asyncio.Lock(),
}


async def query_data(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.json()
    except:
        pass
    return None


async def load_event_cn():
    data = await query_data('https://genshin-calendar.neptunia.vip/event.json')
    if data and 'cn' in data:
        event_data['cn'] = []
        for item in data['cn']:
            start_time = datetime.strptime(
                item['start'], r"%Y/%m/%d %H:%M")
            end_time = datetime.strptime(
                item['end'], r"%Y/%m/%d %H:%M")
            event = {'title': item['title'],
                     'start': start_time,
                     'end': end_time,
                     'forever': item['forever'],
                     'type': 1}
            if 'H5' in event['title'] or '倍' in event['title']:
                event['type'] = 2
            elif item['category'] == 'clanbattle':
                event['type'] = 3
            event_data['cn'].append(event)
        # 深渊提醒
        i = 0
        while i < 2:
            curmon = datetime.today() + relativedelta(months=i)
            nextmon = curmon + relativedelta(months=1)
            event_data['cn'].append({
                'title': '「深镜螺旋」',
                'start': datetime.strptime(
                    curmon.strftime("%Y/%m/01 04:00"), r"%Y/%m/%d %H:%M"),
                'end': datetime.strptime(
                    curmon.strftime("%Y/%m/16 03:59"), r"%Y/%m/%d %H:%M"),
                'forever': False,
                'type': 3
            })
            event_data['cn'].append({
                'title': '「深镜螺旋」',
                'start': datetime.strptime(
                    curmon.strftime("%Y/%m/16 04:00"), r"%Y/%m/%d %H:%M"),
                'end': datetime.strptime(
                    nextmon.strftime("%Y/%m/01 03:59"), r"%Y/%m/%d %H:%M"),
                'forever': False,
                'type': 3
            })
            i = i+1

        return 0
    return 1


async def load_event(server):
    if server == 'cn':
        return await load_event_cn()
    return 1


def get_pcr_now(offset):
    pcr_now = datetime.now()
    if pcr_now.hour < 4:
        pcr_now -= timedelta(days=1)
    pcr_now = pcr_now.replace(
        hour=18, minute=0, second=0, microsecond=0)  # 用晚6点做基准
    pcr_now = pcr_now + timedelta(days=offset)
    return pcr_now


async def get_events(server, offset, days):
    events = []
    pcr_now = datetime.now()
    if pcr_now.hour < 4:
        pcr_now -= timedelta(days=1)
    pcr_now = pcr_now.replace(
        hour=18, minute=0, second=0, microsecond=0)  # 用晚6点做基准

    await lock[server].acquire()
    try:
        t = pcr_now.strftime('%y%m%d')
        if event_updated[server] != t:
            if await load_event(server) == 0:
                event_updated[server] = t
    finally:
        lock[server].release()

    start = pcr_now + timedelta(days=offset)
    end = start + timedelta(days=days)
    end -= timedelta(hours=18)  # 晚上12点结束

    for event in event_data[server]:
        if end > event['start'] and start < event['end']:  # 在指定时间段内 已开始 且 未结束
            event['start_days'] = math.ceil(
                (event['start'] - start) / timedelta(days=1))  # 还有几天开始
            event['left_days'] = math.floor(
                (event['end'] - start) / timedelta(days=1))  # 还有几天结束
            events.append(event)
    # 按type从大到小 按剩余天数从小到大
    events.sort(key=lambda item: item["type"]
                * 100 - item['left_days'], reverse=True)
    return events


if __name__ == '__main__':
    async def main():
        await load_event_cn()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
