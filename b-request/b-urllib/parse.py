import urllib.parse
import urllib.request

data = bytes(urllib.parse.urlencode({"hello": "world"}).encode("utf-8"))
resp = urllib.request.urlopen("http://httpbin.org/post", data=data)
print(resp.read())
