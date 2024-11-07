from mitmproxy import ctx


def response(flow):
    resp = flow.response
    info = ctx.log.info
    info("code: " + str(resp.status_code))
    info("headers: " + str(resp.headers))
    info("cookies: " + str(resp.cookies))
    info("text: " + str(resp.text))
