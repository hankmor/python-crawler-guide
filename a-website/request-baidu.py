import urllib.request
import lxml.etree

# 请求baidu，获得按钮中的百度一下

# 定制request，带上请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

url = "http://www.baidu.com"
request = urllib.request.Request(url=url, headers=headers)
response = urllib.request.urlopen(request)
# 获取html内容
html = response.read().decode("utf-8")

# 使用 xpath 解析 html
tree = lxml.etree.HTML(html)
# 获取到的是一个列表，可以使用下标取值
result = tree.xpath("//input[@id='su']/@value")
print(result[0])  # 百度一下
