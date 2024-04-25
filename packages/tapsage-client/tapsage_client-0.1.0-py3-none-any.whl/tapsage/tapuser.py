import requests
from taptypes import Bot, BotRequest


class TapSageUser:
    API_V1 = "https://api.tapsage.com/api/v1"

    def __init__(self, api_key):
        self.API_KEY = api_key
        self.endpoints = {
            "bots": f"{self.API_V1}/bots",
            "get_bot": f"{self.API_V1}/bots/{{bot_id}}",
            "sessions": f"{self.API_V1}/chat/sessions?userId={{user_id}}",
            "session": f"{self.API_V1}/chat/session",
            "get_session": f"{self.API_V1}/chat/session/{{session_id}}",
            "message": f"{self.API_V1}/chat/session/{{session_id}}/message",
        }
        self.headers = {
            "Content-Type": "application/json",
            "X-Api-Key": self.API_KEY,
        }

    def create_bot(self, bot_data: BotRequest):
        assert isinstance(bot_data, BotRequest)
        response = requests.post(
            url=self.endpoints.get("bots"),
            headers=self.headers,
            json=bot_data.model_dump(),
        )
        return Bot(**response.json())

    def retrieve_bot(self):
        response = requests.get(
            url=self.endpoints.get("get_bot").format(bot_id=self.bot_id),
            headers=self.headers,
        )
        return response.json()
