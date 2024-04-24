import base64
import hashlib

import requests

from .models import *

SEATALK_ACESS_TOKEN_URL = "https://openapi.seatalk.io/auth/app_access_token"


class send_to_group_though_app(object):
    def __init__(self, app_name: str, group_id: str):
        self.json = dict
        self.app = App.objects.get(name=app_name)
        self.end_point = "https://openapi.seatalk.io/messaging/v2/group_chat"
        self.access_token = requests.post(
            "https://openapi.seatalk.io/auth/app_access_token",
            json={
                "app_id": self.app.id,
                "app_secret": self.app.secret,
            },
        ).json()["app_access_token"]
        self.json = {
            "group_id": group_id,
        }

    def text(self, content: str):
        self.json = {
            **self.json,
            "message": {"tag": "text", "text": {"format": 1, "content": content}},
        }

        requests.post(
            url=self.end_point,
            json=self.json,
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            },
        )

    def interactive(self, content: [], title: str = "", description: str = "",):
        self.json = {
            **self.json,
            "message": {"tag": "interactive_message", "interactive_message": {
                "elements": [
                    {
                        "element_type": "title",
                        "title": {
                            "text": title
                        }
                    } if title else None,
                    {
                        "element_type": "description",
                        "description": {
                            "text": description
                        }
                    }if description else None,
                ] + content
            }},
        }

        requests.post(
            url=self.end_point,
            json=self.json,
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            },
        )


def image_to_base64(image: str):
    with open(image, "rb") as f:
        image_byte: bytes = f.read()

        return base64.b64encode(image_byte).decode("utf-8")


def is_valid_signature(signing_secret: bytes, body: bytes, signature: str) -> bool:
    verifiy_sig = hashlib.sha256(body + signing_secret).hexdigest()
    return verifiy_sig == signature
