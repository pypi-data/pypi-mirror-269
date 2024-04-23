import httpx

from stsdk.utils.log import log

timeout = httpx.Timeout(5.0, connect=60.0)
client = httpx.Client(timeout=timeout)


class Request:
    def get(self, url, headers=None, params=None):
        log.info("get info: ", url, params)
        resp = client.get(url, headers=headers, params=params, timeout=timeout)
        return resp.json()

    def post(self, url, data, headers=None):
        log.info("post info: ", url, data)
        resp = client.post(url, headers=headers, data=data, timeout=timeout).json()
        if resp.get("code", 200) != 200:
            raise Exception(resp)
        return resp

    def patch(self, url, data, headers=None):
        log.info("patch info: ", url, data)
        resp = client.patch(url, headers=headers, data=data, timeout=timeout)
        return resp.json()

    def delete(self, url, data, headers=None):
        log.info("delete info: ", url, data)
        resp = client.delete(url, headers=headers, data=data, timeout=timeout)
        return resp.json()

    def close(self):
        self.session.close()


request = Request()
