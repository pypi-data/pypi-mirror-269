# mypy: disable-error-code="override"
from typing import List, Optional

import aiohttp

from klu.common.client import KluClientBase
from klu.evals.constants import EVALS_ENDPOINT
from klu.evals.models import Eval, EvalRun, EvalType
from klu.utils.dict_helpers import dict_no_empty


class EvalClient(KluClientBase):
    def __init__(self, api_key: str):
        super().__init__(api_key, EVALS_ENDPOINT, Eval)

    async def create(
        self,
        name: str,
        action: str,
        eval_types: List[dict],
        dataset: Optional[str],
        version: Optional[str],
        sampling_rate: Optional[float],
        alert_on_fail: Optional[bool],
    ) -> Eval:
        """
        Creates a new Eval.

        Args:
            name (str): Name of the data set.
            action (str): Action parameter.
            eval_types (List[dict]): List of eval types. Each eval type should be a dictionary with the following keys:
                - guid (str): The GUID of the eval type.
                - name (str): The name of the eval type.
                - metadata (dict): Additional metadata for the eval type, such as variables.

            dataset (str, optional): Dataset parameter.
            version (str, optional): Version parameter.
            sampling_rate (float, optional): Sampling rate parameter.
            alert_on_fail (bool, optional): Alert on fail parameter.

        Returns:
            Eval: A new Eval object.
        """
        return await super().create(
            name=name,
            action=action,
            eval_types=eval_types,
            dataset=dataset,
            version=version,
            sampling_rate=sampling_rate,
            alert_on_fail=alert_on_fail,
            url=EVALS_ENDPOINT,
        )

    async def get(self, guid: str) -> Eval:
        """
        Retrieves Eval from a GUID.

        Args:
            guid (str): GUID of an Eval  to fetch.

        Returns:
            An Eval object.
        """
        return await super().get(guid)

    async def get_all(self) -> List[Eval]:
        """
        Retrieves all Evals in the workspace.

        Returns:
            A List of Eval objects.
        """
        async with aiohttp.ClientSession() as session:
            client = self._get_api_client(session)

            response = await client.get(EVALS_ENDPOINT)
            return [Eval._from_engine_format(eval_item) for eval_item in response]

    async def run(self, guid: str) -> str:
        """
        Run an Eval.

        Returns:
            'ok' if the Eval was run successfully.
        """
        async with aiohttp.ClientSession() as session:
            client = self._get_api_client(session)

            response = await client.post(EVALS_ENDPOINT + f"{guid}/run")
            return response

    async def get_eval_types(self) -> List[EvalType]:
        """
        Retrieves all Eval Types in the workspace.

        Returns:
            A List of Eval Types objects.
        """
        async with aiohttp.ClientSession() as session:
            client = self._get_api_client(session)

            response = await client.get(EVALS_ENDPOINT + "types")
            return [EvalType._from_engine_format(eval_type) for eval_type in response]

    async def get_eval_runs(self, guid: str) -> List[EvalRun]:
        """
        Retrieves all Eval Runs for a given Eval.

        Args:
            guid (str): GUID of an Eval to fetch.

        Returns:
            A List of Eval Run objects.
        """
        async with aiohttp.ClientSession() as session:
            client = self._get_api_client(session)

            response = await client.get(EVALS_ENDPOINT + f"{guid}/runs")
            return [EvalRun._from_engine_format(eval_run) for eval_run in response]

    async def get_eval_run(self, eval: str, guid: str) -> EvalRun:
        """
        Retrieves all Eval Runs for a given Eval.

        Args:
            guid (str): GUID of an Eval to fetch.

        Returns:
            A List of Eval Run objects.
        """
        async with aiohttp.ClientSession() as session:
            client = self._get_api_client(session)

            response = await client.get(EVALS_ENDPOINT + f"{eval}/runs/{guid}")
            return EvalRun._from_engine_format(response)

    async def update(
        self,
        guid: str,
        name: Optional[str],
        action: Optional[str],
        eval_types: Optional[List[dict]],
        dataset: Optional[str],
        version: Optional[str],
        sampling_rate: Optional[float],
        alert_on_fail: Optional[bool],
    ) -> Eval:
        """Update an Eval"""

        update_payload = {
            "name": name,
            "action": action,
            "eval_types": eval_types,
            "dataset": dataset,
            "version": version,
            "sampling_rate": sampling_rate,
            "alert_on_fail": alert_on_fail,
        }

        return await super().update(**{"guid": guid, **dict_no_empty(update_payload)})

    async def delete(self, guid: str) -> Eval:
        return await super().delete(guid)
