import requests

url='https://mineru.net/api/v4/file-urls/batch'
header = {
    'Content-Type':'application/json',
    'Authorization':'Bearer eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJqdGkiOiIwMzA2OTgiLCJyb2wiOiJST0xFX1JFR0lTVEVSLFJPTEVfREFUQVNFVCIsImlzcyI6Ik9wZW5YTGFiIiwiaWF0IjoxNzUxOTc4MTYwLCJjbGllbnRJZCI6ImxremR4NTdudnkyMmprcHE5eDJ3IiwicGhvbmUiOiIiLCJvcGVuSWQiOm51bGwsInV1aWQiOiIzN2M2ZmFjMS03M2Y3LTRkYzAtYWM0Ny01ODFlMWRmOGY5MGYiLCJlbWFpbCI6Ik9wZW5EYXRhTGFiQHBqbGFiLm9yZy5jbiIsImV4cCI6MTc1MzE4Nzc2MH0.5wOJsYIBW1DyUYH-QxtDlOoMD2_OQFsnP7qSexuiVouCbZatl4sf6C91Td4xd43IhS4mxL46hNfftC22Q7ViMQ'
}
data = {
    "enable_formula": True,
    "language": "en",
    "enable_table": True,
    "files": [
        {"name":"1966-423.pdf", "is_ocr": True, "data_id": "abcd"}
    ]
}
file_path = ["/Users/weiliqun/Documents/parse_sample_data/1966-423.pdf"]
try:
    response = requests.post(url,headers=header,json=data)
    if response.status_code == 200:
        result = response.json()
        print('response success. result:{}'.format(result))
        if result["code"] == 0:
            batch_id = result["data"]["batch_id"]
            urls = result["data"]["file_urls"]
            print('batch_id:{},urls:{}'.format(batch_id, urls))
            for i in range(0, len(urls)):
                with open(file_path[i], 'rb') as f:
                    res_upload = requests.put(urls[i], data=f)
                    if res_upload.status_code == 200:
                        print(f"{urls[i]} upload success")
                    else:
                        print(f"{urls[i]} upload failed")
        else:
            print('apply upload url failed,reason:{}'.format(result.msg))
    else:
        print('response not success. status:{} ,result:{}'.format(response.status_code, response))
except Exception as err:
    print(err)