import requests
import os
import time
import json
from dotenv import load_dotenv

load_dotenv()  
api_key = os.getenv("MinerU_KEY")

# 第一部分：提交提取任务
batch_id = None
token = api_key
url = "https://mineru.net/api/v4/extract/task/batch"
header = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}
data = {
    "enable_formula": True,
    "language": "ch",
    "enable_table": True,
    "files": [
        {"url":"https://cdn-mineru.openxlab.org.cn/demo/example.pdf", "is_ocr": True, "data_id": "abcd"}
    ]
}
try:
    response = requests.post(url, headers=header, json=data)
    response.raise_for_status()
    result = response.json()
    print('response success. result:{}'.format(result))
    if result.get("code") == 0:
        batch_id = result["data"]["batch_id"]
        print('batch_id:{}'.format(batch_id))
    else:
        print('submit task failed,reason:{}'.format(result.msg))
except Exception as err:
    print(err)

# 第二部分：轮询查询任务结果，直到完成或失败

46208bcd-9e29-47da-9015-27359fdb1b76

if batch_id:
    print("\n--- 正在轮询任务结果 ---")
query_results_url = f"https://mineru.net/api/v4/extract-results/batch/{batch_id}"
res = requests.get(query_results_url, headers=header)
print(res.status_code)
print(res.json())
print(res.json()["data"])