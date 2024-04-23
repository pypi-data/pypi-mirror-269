from urllib.parse import urljoin
from ..decorators import decorators

import requests


class RequestsSessionWrapper(requests.Session):
    baseurl: str

    def __init__(self, baseurl: str):
        super().__init__()

        self.baseurl = baseurl

    @decorators.unwrap
    def request(self, method, url, *args, **kwargs):
        return super().request(method, urljoin(self.baseurl, url), *args, **kwargs)
