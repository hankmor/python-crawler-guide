def request(flow):
    """
    有时候 URL 虽然是正确的，但是内容并非是正确的。我们需要进一步提高自己的安全防范意识
    """
    flow.request.url = "http://www.baidu.com"
