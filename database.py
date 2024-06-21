from typing import AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool

from settings import BaseSQLConfig, app_config

Base = declarative_base()

metadata = MetaData()


class Connection:
    def __init__(self):
        self._engine = create_async_engine(
            self.__prepare_connection_data(config=app_config.db_config),
            hide_parameters=False,
            poolclass=NullPool,
            future=True,
            echo=app_config.DEVELOPMENT
        )
        self._session = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            class_=AsyncSession
        )

    @asynccontextmanager
    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._session() as session:
            try:
                yield session
                await session.commit()
            except Exception as err:
                await session.rollback()
                raise err
            finally:
                await session.close()

    @staticmethod
    def __prepare_connection_data(config: BaseSQLConfig) -> str:
        """
        Base hidden prepare connection type.
        """

        return f"{config.connector}://{config.user}:{config.password}@{config.host}:{config.port}/{config.schema}"
