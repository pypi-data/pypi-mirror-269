import requests


class SpiderKid:
    def __init__(
            self,
            host,
            auth=None,
    ):
        self.host = host
        self.auth = auth

        if 'localhost' not in host and not auth:
            raise ValueError('auth is required for non-localhost hosts')

        if self.host.endswith('/'):
            self.host = self.host[:-1]

    def post(self, path, data):
        url = self.host + path
        print(url)
        return requests.post(url, json=data, headers={
            'Authorization': self.auth,
        })

    def get(self, path):
        url = self.host + path
        return requests.get(url, headers={
            'Authorization': self.auth,
        }).json()

    def melon(self, email, password, hash_key):
        return self.post('/melon/encrypt', {
            'email': email,
            'password': password,
            'hashKey': hash_key,
        }).json()
