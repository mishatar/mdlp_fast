from aiohttp import ClientSession

from settings import app_config


class RequestMixin:
    def __init__(self):
        self.api_url = 'api.mdlp.crpt.ru/api/v1' if app_config.DEVELOPMENT else 'api.sb.mdlp.crpt.ru/api/v1'
        self.base_url = 'http://api.mdlp.crpt.ru/' if app_config.DEVELOPMENT else 'http://api.sb.mdlp.crpt.ru/'
        self.request_session: ClientSession = ClientSession(
            base_url=self.api_url,
            headers={
                "Content-Type": "application/json",
            }
        )
