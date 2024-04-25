# mypy: disable-error-code="override"
from typing import NoReturn, Optional

from klu.common.client import KluClientBase
from klu.common.errors import NotSupportedError
from klu.session.constants import SESSION_ENDPOINT
from klu.session.models import Session


class SessionClient(KluClientBase):
    def __init__(self, api_key: str):
        super().__init__(api_key, SESSION_ENDPOINT, Session)

    async def create(
        self, action: str, name: Optional[str] = None, extUserId: Optional[str] = None
    ) -> Session:
        """
        Creates a session based on the data provided.

        Args:
            action (str): guid of the action to which the session belongs.
            name (Optional[str]): Name of the session. If not provided will be left blank.

        Returns:
            A newly created Session object.
        """
        return await super().create(action=action, name=name, extUserId=extUserId)

    async def get(self, guid: str) -> Session:
        """
        Retrieves session information based on the unique Session guid

        Args:
            guid (str): guid of a session to fetch.

        Returns:
            Session object
        """
        return await super().get(guid)

    async def update(self) -> NoReturn:
        raise NotSupportedError()

    async def delete(self, guid: str) -> Session:
        """
        Delete a session.

        Args:
            guid (str): Unique guid of a session to delete.

        Returns:
            Deleted Session object
        """
        return await super().delete(guid)
