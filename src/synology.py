import requests
import os
import json


class Synology:
    def __init__(self, scheme, host, port, verifySsl):
        self.scheme = scheme
        self.host = host
        self.port = port
        self.verifySsl = verifySsl

        self.baseUrl = "{}://{}:{}/webapi/".format(scheme, host, port)
        self.defaultCookies = {}

    def login(self, username: str, password: str) -> None:
        res = requests.get(
            self.baseUrl + "auth.cgi",
            {
                "api": "SYNO.API.Auth",
                "version": "3",
                "method": "login",
                "account": username,
                "passwd": password,
                "session": "",
                "format": "sid",
            },
            verify=self.verifySsl,
        )
        json = res.json()

        if not json["success"]:
            raise Exception("Login failed!")

        self.sid = json["data"]["sid"]
        self.defaultCookies["id"] = self.sid

    def logout(self) -> None:
        res = requests.get(
            self.baseUrl + "auth.cgi",
            {
                "api": "SYNO.API.Auth",
                "version": "3",
                "method": "logout",
            },
            verify=self.verifySsl,
        )
        json = res.json()

        if not json["success"]:
            raise Exception("Logout failed!")

        self.sid = None
        self.defaultCookies["id"] = None

    def getDefaultCert(self) -> dict:
        res = requests.get(
            self.baseUrl + "entry.cgi",
            params={"api": "SYNO.Core.Certificate.CRT",
                    "version": 1, "method": "list"},
            cookies=self.defaultCookies,
            verify=self.verifySsl,
        )
        json = res.json()

        if not json["success"]:
            raise Exception("Could not get default certificate")

        for certificate in json["data"]["certificates"]:
            if certificate["is_default"]:
                return certificate

    def importDefaultCert(self, desc: str, cert: str, chain: str, key: str) -> str:
        res = requests.post(
            self.baseUrl + "entry.cgi",
            params={
                "api": "SYNO.Core.Certificate",
                "version": "1",
                "method": "import",
            },
            files=[
                (
                    "key",
                    (
                        os.path.basename(key),
                        open(key, "rb"),
                        "application/octet-stream",
                    ),
                ),
                (
                    "cert",
                    (
                        os.path.basename(cert),
                        open(cert, "rb"),
                        "application/octet-stream",
                    ),
                ),
                (
                    "inter_cert",
                    (
                        os.path.basename(chain),
                        open(chain, "rb"),
                        "application/octet-stream",
                    ),
                ),
                ("desc", (None, desc)),
                ("id", (None, "")),
                ("as_default", (None, "True")),
            ],
            cookies=self.defaultCookies,
            verify=self.verifySsl,
        )
        body = res.json()

        if not body["success"]:
            raise Exception(
                f"Could not import certificate. API-Error: {body['error']['code']}")

        return body["data"]["id"]

    def deleteCert(self, id: str) -> dict:
        res = requests.post(
            self.baseUrl + "entry.cgi",
            data={
                "api": "SYNO.Core.Certificate.CRT",
                "version": 1,
                "method": "delete",
                "ids": json.dumps([id]),
            },
            cookies=self.defaultCookies,
            verify=self.verifySsl,
        )
        body = res.json()

        if not body["success"]:
            raise Exception("Could not delete certificate")

        return body["data"]
