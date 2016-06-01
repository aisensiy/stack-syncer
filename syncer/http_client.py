import requests


class HttpClient:
    def __init__(self):
        self.session = requests.Session()

    def get(self, url):
        response = self.session.get(url)
        return response.status_code, response.json()

    def post(self, url, json):
        response = self.session.post(url, json=json)
        return response.status_code

    def put(self, url, json):
        response = self.session.put(url, json=json)
        return response.status_code
