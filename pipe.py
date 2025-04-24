import pandas as pd

import json
import asyncio
import os
import requests
from tqdm import tqdm

from parser import parse_video_share_url, parse_video_id, VideoSource


def process(share_url, id):
    url = share_url
    # TODO extract 7486941659146538277
    url = url.split('/?mid')[0].replace('share/', '')

    print(url)

    # video_info = asyncio.run(parse_video_share_url(share_url))
    video_info = asyncio.run(parse_video_share_url(url))
    # print(f"share_url: {share_url}")
    # print(
    #     "解析分享链接：\n",
    #     json.dumps(video_info, ensure_ascii=False, indent=4, default=lambda x: x.__dict__),
    #     "\n",
    # )

    info = json.dumps(video_info, ensure_ascii=False, indent=4, default=lambda x: x.__dict__)

    info = json.loads(info)

    # print(info)

    url = info['video_url']

    os.makedirs('videos', exist_ok=True)

    filename = f"videos/{id}.mp4"

    print("下载中......", filename)

    # 发起请求并下载
    headers = {
        "User-Agent": "Mozilla/5.0",  # 模拟浏览器，避免部分服务器拒绝请求
    }
    with requests.get(url, headers=headers, stream=True) as r:
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    print("下载完成:", filename)

# 读取CSV文件
df = pd.read_csv('game_1k.csv')

# 遍历每一行，获取“视频id”和“视频连接”
for index, row in tqdm(df[63:].iterrows()):
    video_id = row['视频id']
    video_url = row['视频链接']
    
    # 在这里处理每个视频，比如打印、下载、分析等
    print(f'正在处理视频 ID: {video_id}，连接: {video_url}')

    # mp4 file
    filename = f"videos/{video_id}.mp4"

    # add try except
    # if failed, try 3 times
    try:
        process(video_url, video_id)
    except Exception as e:
        print(f"下载失败: {filename}, 错误信息: {e}")
        # try 3 times
        for i in range(3):
            try:
                process(video_url, video_id)
                break
            except Exception as e:
                print(f"下载失败: {filename}, 错误信息: {e}")
                if i == 2:
                    print(f"下载失败: {filename}, 错误信息: {e}")
                else:
                    print(f"重试中... {i+1}/3")
    # print(f'正在处理视频 ID: {video_id}，连接: {video_url}')

