from mitmproxy import ctx


def request(flow):
    """
    mitmdump -s script.py启动mitmrpoxy, 请求会交给该方法处理.
    修改 User-Agent 然后打印请求头信息
    访问 http://httpbin.org/get 可以看到输出中 User-Agent 变为 “Mitmproxy/1.0”:

    ```
    {
      "args": {},
      "headers": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Host": "httpbin.org",
        "Proxy-Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mitmproxy/1.0",
        "X-Amzn-Trace-Id": "Root=1-672c5f62-655849f06dbfd7a341715cf2"
      },
      "origin": "182.138.85.134",
      "url": "http://httpbin.org/get"
    }
    ```
    后台打印:
    ```
    Headers[(b'Host', b'httpbin.org'), (b'Proxy-Connection', b'keep-alive'), (b'Cache-Control', b'max-age=0'), (b'Upgrade-Insecure-Requests', b'1'), (b'User-Agent', b'Mitmproxy/1.0'), (b'Accept', b'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'), (b'Accept-Encoding', b'gzip, deflate'), (b'Accept-Language', b'zh-CN,zh;q=0.9')]
    [06:34:10.204][127.0.0.1:50455] server connect httpbin.org:80 (54.237.204.19:80)
    127.0.0.1:50455: GET http://httpbin.org/get
    ```
    """

    flow.request.headers["User-Agent"] = "Mitmproxy/1.0"
    # log
    ctx.log.info(flow.request.headers)
    # ctx.log.warn("this is a warning message")
    # ctx.log.error("this is an error message")
    request = flow.request
    info = ctx.log.info
    info(request.url)
    info(str(request.headers))
    info(str(request.cookies))
    info(request.host)
    info(request.method)
    info(str(request.port))
    info(request.scheme)
