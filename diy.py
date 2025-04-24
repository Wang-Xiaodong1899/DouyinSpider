import json
import asyncio
import requests

from parser import parse_video_share_url, parse_video_id, VideoSource

# 根据分享链接解析
video_info = asyncio.run(parse_video_share_url("https://www.douyin.com/video/7484646023793478924"))
print(
    "解析分享链接：\n",
    json.dumps(video_info, ensure_ascii=False, indent=4, default=lambda x: x.__dict__),
    "\n",
)

info = json.dumps(video_info, ensure_ascii=False, indent=4, default=lambda x: x.__dict__)

info = json.loads(info)

print(info)

url = info['video_url']



filename = "videos/7484646023793478924.mp4"

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
