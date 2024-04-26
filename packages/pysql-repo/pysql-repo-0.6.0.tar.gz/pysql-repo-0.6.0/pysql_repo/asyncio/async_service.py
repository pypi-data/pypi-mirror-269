# MODULES
from typing import TypeVar, Generic
from logging import Logger

# CONTEXTLIB
from contextlib import AbstractAsyncContextManager

# SQLALCHEMY
from sqlalchemy.ext.asyncio import AsyncSession

# MODELS
from pysql_repo.asyncio.async_repository import AsyncRepository


_T = TypeVar("_T", bound=AsyncRepository)


class AsyncService(Generic[_T]):
    """
    Represents a generic asynchronous service.

    Attributes:
        _repository: The repository object.

    Methods:
        session_manager: Returns the session factory.
    """

    def __init__(
        self,
        repository: _T,
    ) -> None:
        """
        Initializes the AsyncService.

        Args:
            repository: The repository object.
        """
        self._repository = repository

    def session_manager(self) -> AbstractAsyncContextManager[AsyncSession]:
        """
        Returns the session manager from the repository.

        Returns:
            A session manager.
        """
        return self._repository.session_manager()
