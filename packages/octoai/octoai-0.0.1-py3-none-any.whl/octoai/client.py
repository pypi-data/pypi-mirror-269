from octoai.uploading_asset_lake import AsyncUploadingAssetLakeClient, UploadingAssetLakeClient
from .base_client import BaseOctoAI, AsyncBaseOctoAI

import os
import typing
import httpx

from .asset_lake.client import AssetLakeClient, AsyncAssetLakeClient
from .core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from .environment import OctoAIEnvironment
from .fine_tuning.client import AsyncFineTuningClient, FineTuningClient
from .image_gen.client import AsyncImageGenClient, ImageGenClient
from .text_gen.client import AsyncTextGenClient, TextGenClient


class OctoAI(BaseOctoAI):
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propogate to these functions.

    Parameters:
        - environment: OctoAIEnvironment. The environment to use for requests from the client. from .environment import OctoAIEnvironment

                                          Defaults to OctoAIEnvironment.PRODUCTION

        - api_key: typing.Optional[typing.Union[str, typing.Callable[[], str]]].

        - timeout: typing.Optional[float]. The timeout to be used, in seconds, for requests by default the timeout is 60 seconds.

        - httpx_client: typing.Optional[httpx.Client]. The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.
    ---
    from octoai.client import OctoAI

    client = OctoAI(
        api_key="YOUR_API_KEY",
    )
    """

    def __init__(
        self,
        *,
        environment: OctoAIEnvironment = OctoAIEnvironment.PRODUCTION,
        api_key: typing.Optional[typing.Union[str, typing.Callable[[], str]]] = os.getenv("OCTOAI_TOKEN"),
        timeout: typing.Optional[float] = 60,
        httpx_client: typing.Optional[httpx.Client] = None
    ):
        super().__init__(
            environment=environment,
            api_key=api_key,
            timeout=timeout,
            httpx_client=httpx_client
        )

        self.asset_lake = UploadingAssetLakeClient(client_wrapper=self._client_wrapper)


class AsyncOctoAI(AsyncBaseOctoAI):
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propogate to these functions.

    Parameters:
        - environment: OctoAIEnvironment. The environment to use for requests from the client. from .environment import OctoAIEnvironment

                                          Defaults to OctoAIEnvironment.PRODUCTION

        - api_key: typing.Optional[typing.Union[str, typing.Callable[[], str]]].

        - timeout: typing.Optional[float]. The timeout to be used, in seconds, for requests by default the timeout is 60 seconds.

        - httpx_client: typing.Optional[httpx.AsyncClient]. The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.
    ---
    from octoai.client import AsyncOctoAI

    client = AsyncOctoAI(
        api_key="YOUR_API_KEY",
    )
    """

    def __init__(
        self,
        *,
        environment: OctoAIEnvironment = OctoAIEnvironment.PRODUCTION,
        api_key: typing.Optional[typing.Union[str, typing.Callable[[], str]]] = os.getenv("OCTOAI_TOKEN"),
        timeout: typing.Optional[float] = 60,
        httpx_client: typing.Optional[httpx.AsyncClient] = None
    ):
        super().__init__(
            environment=environment,
            api_key=api_key,
            timeout=timeout,
            httpx_client=httpx_client
        )

        self.asset_lake = AsyncUploadingAssetLakeClient(client_wrapper=self._client_wrapper)