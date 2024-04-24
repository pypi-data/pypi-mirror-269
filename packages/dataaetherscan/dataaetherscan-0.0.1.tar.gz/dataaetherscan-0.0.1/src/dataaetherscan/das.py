import json, requests


class DataAetherScan(object):
    base_url = "https://api.dataaetherscan.com/api/{}"

    def __init__(self, email, password):
        self._email = email
        self._password = password
        self.authenticate()

    def authenticate(self):
        data = self.send_request("POST", "/User/login", data={"email": self._email, "password": self._password}, with_token=False)
        if data:
            self._refresh_token = data["refresh"]
            self._access_token = data["access"]
            print("Authenticated")
        else:
            raise ValueError("Authentication failed")

    def send_request(self, method, url, data={}, with_token=True) -> dict:
        url = self.base_url.format(url)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if with_token:
            headers["Authorization"] = "Bearer {}".format(self._access_token)
        cookies = {}

        if method == "GET":
            response = requests.get(url, headers=headers, cookies=cookies)
            if response.status_code in (200, 201):
                return json.loads(response.content)
            raise ValueError(method, response.status_code, response.content)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, cookies=cookies)
            if response.status_code in (200, 201):
                return json.loads(response.content)
            print(method, response.status_code, response.content)
            raise ValueError(method, response.status_code, response.content)
        elif method == "PATCH":
            response = requests.patch(
                url, headers=headers, data=data, cookies=cookies
            )
            if response.status_code in (200, 201):
                return json.loads(response.content)
            print(method, response.status_code, response.content)
            raise ValueError(method, response.status_code, response.content)
        else:
            response = requests.post(
                url, headers=headers, data=json.dumps(data), cookies=cookies
            )
            if response.status_code in (200, 201):
                return json.loads(response.content)
            print(method, response.status_code, response.content)
            raise ValueError(method, response.status_code, response.content)

    def get_user(self) -> dict:
        return self.send_request("GET", "User")

    def get_channels(self) -> dict:
        return self.send_request("GET", "Channel")

    def get_credit(self) -> dict:
        return self.send_request("GET", "Credit")

    def get_jobs(self) -> dict:
        return self.send_request("GET", "Job")
    
    def get_job(self, id:int) -> dict:
        return self.send_request("GET", "Job/{}".format(id))
    
    def delete_job(self, id:int) -> dict:
        return self.send_request("DELETE", "Job/{}".format(id))
    
    def create_job(self, data:dict) -> dict:
        return self.send_request("POST", "Job", data)
    
