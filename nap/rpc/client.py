import json

import requests


class RPCProxy:
    def __init__(self, client, name):
        self.client = client
        self.name = name

    def __call__(self, **kwargs):
        resp = self.client.session.post(
            self.client.endpoint,
            data=json.dumps(kwargs),
            headers={
                'X-Rpc-Action': self.name,
                'Content-Type': 'application/json',
            },
        )
        return resp.json()


class RPCClient:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.session = requests.Session()

    def __getattr__(self, key):
        return RPCProxy(self, key)
