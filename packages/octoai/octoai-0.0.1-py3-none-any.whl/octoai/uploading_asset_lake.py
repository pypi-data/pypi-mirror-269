import asyncio
import contextlib
import functools
from time import sleep
import time
import typing

from octoai.asset_lake.types.status import Status
from .asset_lake.client import AsyncAssetLakeClient
from .asset_lake.types.create_asset_response import CreateAssetResponse
from .asset_lake.types.create_asset_response_transfer_api import CreateAssetResponseTransferApi, CreateAssetResponseTransferApi_PresignedUrl, CreateAssetResponseTransferApi_Sts
import boto3
from .core.client_wrapper import AsyncClientWrapper
import httpx
from octoai.asset_lake.types.asset import Asset

from .asset_lake.client import OMIT
from .asset_lake.types.data import Data
from .asset_lake.types.transfer_api_type import TransferApiType
from .core.request_options import RequestOptions
from .core.client_wrapper import SyncClientWrapper
from .asset_lake.client import AssetLakeClient
from .core.api_error import ApiError


_TERMINAL_STATUSES: typing.Set[Status] = {"ready", "deleted", "rejected", "error"}


class AssetReadyTimeout(Exception):
    pass


class AssetNotReady(Exception):
    pass


def _sts_upload(x_api: CreateAssetResponseTransferApi_Sts, file: typing.Union[str, typing.BinaryIO]):
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=x_api.aws_access_key_id,
        aws_secret_access_key=x_api.aws_secret_access_key,
        aws_session_token=x_api.aws_session_token,
    )
    try:
        s3_client.upload_file(file, x_api.s3bucket, x_api.s3key)
    except Exception as e:
        raise Exception(f"Error uploading file to server: {e}")


class UploadingAssetLakeClient(AssetLakeClient):
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)

    def create_from_file(
        self,
        file: typing.Union[str, typing.BinaryIO],
        data: Data,
        name: str,
        description: typing.Optional[str] = OMIT,
        is_public: typing.Optional[bool] = OMIT,
        transfer_api_type: typing.Optional[TransferApiType] = OMIT
    ) -> Asset:
        """
        Parameters:
            - file: typing.Union[str, typing.BinaryIO]. File to upload.

            - data: Data. Asset data.

            - name: str. Asset name.

            - description: typing.Optional[str].

            - is_public: typing.Optional[bool]. True if asset is public.

            - transfer_api_type: typing.Optional[TransferApiType]. Transfer API type.
        """
        response: CreateAssetResponse = self.create(
            data=data,
            name=name,
            asset_type=data.asset_type,
            description=description,
            is_public=is_public,
            transfer_api_type=transfer_api_type
        )
        self._transfer_file(response.transfer_api, file=file)

        self.complete_upload(response.asset.id)

        return self.wait_for_ready(response.asset)


    def wait_for_ready(self, asset: Asset, poll_interval=10, timeout_seconds=900):
        """
        Wait for asset to be ready to use.

        This waits until the asset's status is READY or an error status.

        Parameters:
            - asset: Asset. Asset to wait on.
        """
        start_time = time.monotonic()

        while asset.status not in _TERMINAL_STATUSES:
            now = time.monotonic()
            if now - start_time > timeout_seconds:
                raise AssetReadyTimeout("Asset creation timed out")

            time.sleep(poll_interval)
            asset = self.get(asset.id).asset

        if asset.status != "ready":
            raise AssetNotReady(f"Asset creation failed with status: {asset.status}")

        return asset


    def _transfer_file(self, transfer_api_used: CreateAssetResponseTransferApi, file: typing.Union[str, typing.BinaryIO]):
        if isinstance(transfer_api_used, CreateAssetResponseTransferApi_PresignedUrl):
            with contextlib.ExitStack() as exit_stack:
                file_data = exit_stack.enter_context(open(file, "rb")) if isinstance(file, str) else file
                upload_resp = httpx.put(
                    url=transfer_api_used.put_url, content=file_data, timeout=60000
                )
                upload_resp.raise_for_status()
        elif isinstance(transfer_api_used, CreateAssetResponseTransferApi_Sts):
            _sts_upload(transfer_api_used, file)


class AsyncUploadingAssetLakeClient(AsyncAssetLakeClient):
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)
        self._signed_url_client = httpx.AsyncClient()

    async def create_from_file(
        self,
        file: typing.Union[str, typing.BinaryIO],
        data: Data,
        name: str,
        description: typing.Optional[str] = OMIT,
        is_public: typing.Optional[bool] = OMIT,
        transfer_api_type: typing.Optional[TransferApiType] = OMIT
    ) -> Asset:
        """
        Parameters:
            - file: typing.Union[str, typing.BinaryIO]. File to upload.

            - data: Data. Asset data.

            - name: str. Asset name.

            - description: typing.Optional[str].

            - is_public: typing.Optional[bool]. True if asset is public.

            - transfer_api_type: typing.Optional[TransferApiType]. Transfer API type.
        """

        response: CreateAssetResponse = await self.create(
            data=data,
            name=name,
            asset_type=data.asset_type,
            description=description,
            is_public=is_public,
            transfer_api_type=transfer_api_type
        )

        await self._transfer_file(response.transfer_api, file=file)

        await self.complete_upload(response.asset.id)

        return await self.wait_for_ready(response.asset)

    async def wait_for_ready(self, asset: Asset, poll_interval=10, timeout_seconds=900):
        """
        Wait for asset to be ready to use.

        This waits until the asset's status is READY or an error status.

        Parameters:
            - asset: Asset. Asset to wait on.
        """
        start_time = time.monotonic()

        while asset.status not in _TERMINAL_STATUSES:
            now = time.monotonic()
            if now - start_time > timeout_seconds:
                raise AssetReadyTimeout("Asset creation timed out")

            await asyncio.sleep(poll_interval)
            asset = (await self.get(asset.id)).asset

        if asset.status != "ready":
            raise AssetNotReady(f"Asset creation failed with status: {asset.status}")

        return asset

    async def _transfer_file(self, transfer_api_used: CreateAssetResponseTransferApi, file: typing.Union[str, typing.BinaryIO]):
        if isinstance(transfer_api_used, CreateAssetResponseTransferApi_PresignedUrl):
            # TODO: Use aiofiles to make this fully async?
            file_data_bytes = await asyncio.get_running_loop().run_in_executor(
                None,
                functools.partial(
                    _read_entire_file,
                    file
                )
            )

            upload_resp = await self._signed_url_client.put(
                url=transfer_api_used.put_url, content=file_data_bytes, timeout=60000
            )
            upload_resp.raise_for_status()
        elif isinstance(transfer_api_used, CreateAssetResponseTransferApi_Sts):
            _sts_upload(transfer_api_used, file)


def _read_entire_file(file: typing.Union[str, typing.BinaryIO]) -> bytes:
    if isinstance(file, str):
        with open(file, "rb") as f:
            return f.read()
    else:
        return file.read()