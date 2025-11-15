import requests

url = f'https://mineru.net/api/v4/extract-results/batch/d71852d4-32a3-43fb-9282-645f4f26f358'
header = {
    'Content-Type':'application/json',
    'Authorization':'Bearer eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJqdGkiOiIwMzA2OTgiLCJyb2wiOiJST0xFX1JFR0lTVEVSLFJPTEVfREFUQVNFVCIsImlzcyI6Ik9wZW5YTGFiIiwiaWF0IjoxNzUxOTc4MTYwLCJjbGllbnRJZCI6ImxremR4NTdudnkyMmprcHE5eDJ3IiwicGhvbmUiOiIiLCJvcGVuSWQiOm51bGwsInV1aWQiOiIzN2M2ZmFjMS03M2Y3LTRkYzAtYWM0Ny01ODFlMWRmOGY5MGYiLCJlbWFpbCI6Ik9wZW5EYXRhTGFiQHBqbGFiLm9yZy5jbiIsImV4cCI6MTc1MzE4Nzc2MH0.5wOJsYIBW1DyUYH-QxtDlOoMD2_OQFsnP7qSexuiVouCbZatl4sf6C91Td4xd43IhS4mxL46hNfftC22Q7ViMQ'
}

res = requests.get(url, headers=header)
print(res.status_code)
print(res.json())
print(res.json()["data"])