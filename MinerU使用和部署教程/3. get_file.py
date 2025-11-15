import requests
import os

zip_url = "https://cdn-mineru.openxlab.org.cn/pdf/2025-07-08/7bc373a0-4ee5-48f6-b615-6a9a08cf5dc0.zip"
filename = zip_url.split("/")[-1]
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
save_path = os.path.join(desktop_path, filename)

print(f"开始下载文件到：{save_path}")
res = requests.get(zip_url)
if res.status_code == 200:
    with open(save_path, 'wb') as f:
        f.write(res.content)
    print("下载完成 ✅")
else:
    print(f"下载失败 ❌，状态码：{res.status_code}")