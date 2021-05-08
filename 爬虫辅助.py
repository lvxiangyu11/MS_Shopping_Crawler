import requests
from bs4 import BeautifulSoup
import json

url = 'https://www.microsoftstore.com.cn/certified-refurbished-surface-book-2-configurate'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

script_all = soup.find_all('script')
# 找到类别

categories = ''
for i in script_all:
    try:
        if "IsobarCommerce_BundleSwatches/js/swatch-renderer" in i.contents[0]:
            categories = i.contents[0]
            break
    except:
        pass


categories = json.loads(categories)
categories = categories["[data-role=swatch-options]"]
categories = categories["IsobarCommerce_BundleSwatches/js/swatch-renderer"]
categories = categories["jsonConfig"]

mainProducts = categories['mainProducts']
index = categories['index']
# 这里获取到编号即可，具体解析放入模拟操纵中
for i in index:
    # 遍历大类
    print(i, categories[i])
    categories_small = categories[i]
    print(categories_small)

print(categories)
print(soup)
