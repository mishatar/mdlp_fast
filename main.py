from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from settings import app_config


class Server:
    """
    Server class to initialise FastAPI server.
    """

    __app: FastAPI
    __title = 'MDLP Fast'
    __description = \
        '''
        FastAPI version of backend server for LPU.
        '''
    __version = '0.3.2'

    def __init__(self):
        self.__app = FastAPI(
            title=self.__title,
            description=self.__description,
            version=self.__version,
            debug=not app_config.DEVELOPMENT,
        )
        self.__app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=False,
            allow_methods=["*"],
            allow_headers=["*"]
        )
        self.routers = []
        self.__register_routes(self.__app)
        self.__register_events(self.__app)
        self.__register_middlewares(self.__app)
        self.__register_exception_handlers(self.__app)

    def get_app(self) -> FastAPI:
        """
        Get method to return app.
        :return: FastAPI app.
        """
        return self.__app

    @staticmethod
    def __register_routes(self, app):
        for router in self.routers:
            app.include_router(router)



