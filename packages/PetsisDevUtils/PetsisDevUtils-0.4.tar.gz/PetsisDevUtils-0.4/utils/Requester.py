import requests
from .funcs import *
from .Logga import *


def request(*args, **kwargs):
    res = Requester().make_request(*args, **kwargs)
    return res

class Requester:
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(Requester)
            log(f"Requester.__init__:{ln()}")
        return cls.__instance
        ''
    def make_request(self,
                     url,
                     headers=None,
                     typ='GET',
                     data=None,
                     json=None,
                     params=None,
                     timeout=None):

        lib = {
            'GET': requests.get,
            'POST': requests.post,
            'PUT': requests.put,
            'DELETE': requests.delete,
            'PATCH': requests.patch}
        log(f"Requester.make_request:{ln()}: {typ} request to {url}")
        try:
            res = lib[typ](url=url, headers=headers, json=json, data=data, params=params, timeout=timeout)
            return self.handle_response(res)
        except Exception as e:
            log(f"Requester.make_request:{ln()}: error: {e}", level='ERROR')

    def handle_response(self, res):
        if res.status_code == 200 or 201 or 202 or 203 or 204:
            try:
                response = res.json()
                return response
            except Exception as e:
                log(f"Requester.make_request:{ln()}: error: {e}", level='ERROR')
        else:
            log(f"Requester.make_request:{ln()}: uunknown error: status_code:{res.status_code}", level='ERROR')
