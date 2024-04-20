# This file was auto-generated by Fern from our API Definition.

import typing
import urllib.parse
from json.decoder import JSONDecodeError

from ..core.api_error import ApiError
from ..core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ..core.jsonable_encoder import jsonable_encoder
from ..core.pydantic_utilities import pydantic_v1
from ..core.remove_none_from_dict import remove_none_from_dict
from ..core.request_options import RequestOptions
from .errors.unprocessable_entity_error import UnprocessableEntityError
from .types.http_validation_error import HttpValidationError
from .types.image_generation_request import ImageGenerationRequest
from .types.image_generation_response import ImageGenerationResponse

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class ImageGenClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def generate_ssd(
        self, *, request: ImageGenerationRequest, request_options: typing.Optional[RequestOptions] = None
    ) -> ImageGenerationResponse:
        """
        Generate images in response to the given request.

        Parameters:
            - request: ImageGenerationRequest.

            - request_options: typing.Optional[RequestOptions]. Request-specific configuration.
        ---
        from octoai.client import OctoAI
        from octoai.image_gen import ImageGenerationRequest

        client = OctoAI(
            api_key="YOUR_API_KEY",
        )
        client.image_gen.generate_ssd(
            request=ImageGenerationRequest(
                prompt="An octopus playing chess, masterpiece, photorealistic",
            ),
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(f"{self._client_wrapper.get_environment().image_gen}/", "generate/ssd"),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            json=jsonable_encoder(request)
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(request),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(ImageGenerationResponse, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(
                pydantic_v1.parse_obj_as(HttpValidationError, _response.json())  # type: ignore
            )
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def generate_controlnet_sdxl(
        self, *, request: ImageGenerationRequest, request_options: typing.Optional[RequestOptions] = None
    ) -> ImageGenerationResponse:
        """
        Generate images in response to the given request.

        Parameters:
            - request: ImageGenerationRequest.

            - request_options: typing.Optional[RequestOptions]. Request-specific configuration.
        ---
        from octoai.client import OctoAI
        from octoai.image_gen import ImageGenerationRequest

        client = OctoAI(
            api_key="YOUR_API_KEY",
        )
        client.image_gen.generate_controlnet_sdxl(
            request=ImageGenerationRequest(
                prompt="An octopus playing chess, masterpiece, photorealistic",
            ),
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(f"{self._client_wrapper.get_environment().image_gen}/", "generate/controlnet-sdxl"),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            json=jsonable_encoder(request)
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(request),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(ImageGenerationResponse, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(
                pydantic_v1.parse_obj_as(HttpValidationError, _response.json())  # type: ignore
            )
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def generate_controlnet_sd15(
        self, *, request: ImageGenerationRequest, request_options: typing.Optional[RequestOptions] = None
    ) -> ImageGenerationResponse:
        """
        Generate images in response to the given request.

        Parameters:
            - request: ImageGenerationRequest.

            - request_options: typing.Optional[RequestOptions]. Request-specific configuration.
        ---
        from octoai.client import OctoAI
        from octoai.image_gen import ImageGenerationRequest

        client = OctoAI(
            api_key="YOUR_API_KEY",
        )
        client.image_gen.generate_controlnet_sd15(
            request=ImageGenerationRequest(
                prompt="An octopus playing chess, masterpiece, photorealistic",
            ),
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(f"{self._client_wrapper.get_environment().image_gen}/", "generate/controlnet-sd15"),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            json=jsonable_encoder(request)
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(request),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(ImageGenerationResponse, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(
                pydantic_v1.parse_obj_as(HttpValidationError, _response.json())  # type: ignore
            )
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def generate_sdxl(
        self, *, request: ImageGenerationRequest, request_options: typing.Optional[RequestOptions] = None
    ) -> ImageGenerationResponse:
        """
        Generate images in response to the given request.

        Parameters:
            - request: ImageGenerationRequest.

            - request_options: typing.Optional[RequestOptions]. Request-specific configuration.
        ---
        from octoai.client import OctoAI
        from octoai.image_gen import ImageGenerationRequest

        client = OctoAI(
            api_key="YOUR_API_KEY",
        )
        client.image_gen.generate_sdxl(
            request=ImageGenerationRequest(
                prompt="An octopus playing chess, masterpiece, photorealistic",
            ),
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(f"{self._client_wrapper.get_environment().image_gen}/", "generate/sdxl"),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            json=jsonable_encoder(request)
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(request),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(ImageGenerationResponse, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(
                pydantic_v1.parse_obj_as(HttpValidationError, _response.json())  # type: ignore
            )
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def generate_sd(
        self, *, request: ImageGenerationRequest, request_options: typing.Optional[RequestOptions] = None
    ) -> ImageGenerationResponse:
        """
        Generate images in response to the given request.

        Parameters:
            - request: ImageGenerationRequest.

            - request_options: typing.Optional[RequestOptions]. Request-specific configuration.
        ---
        from octoai.client import OctoAI
        from octoai.image_gen import ImageGenerationRequest

        client = OctoAI(
            api_key="YOUR_API_KEY",
        )
        client.image_gen.generate_sd(
            request=ImageGenerationRequest(
                prompt="An octopus playing chess, masterpiece, photorealistic",
            ),
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(f"{self._client_wrapper.get_environment().image_gen}/", "generate/sd"),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            json=jsonable_encoder(request)
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(request),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(ImageGenerationResponse, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(
                pydantic_v1.parse_obj_as(HttpValidationError, _response.json())  # type: ignore
            )
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncImageGenClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def generate_ssd(
        self, *, request: ImageGenerationRequest, request_options: typing.Optional[RequestOptions] = None
    ) -> ImageGenerationResponse:
        """
        Generate images in response to the given request.

        Parameters:
            - request: ImageGenerationRequest.

            - request_options: typing.Optional[RequestOptions]. Request-specific configuration.
        ---
        from octoai.client import AsyncOctoAI
        from octoai.image_gen import ImageGenerationRequest

        client = AsyncOctoAI(
            api_key="YOUR_API_KEY",
        )
        await client.image_gen.generate_ssd(
            request=ImageGenerationRequest(
                prompt="An octopus playing chess, masterpiece, photorealistic",
            ),
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(f"{self._client_wrapper.get_environment().image_gen}/", "generate/ssd"),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            json=jsonable_encoder(request)
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(request),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(ImageGenerationResponse, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(
                pydantic_v1.parse_obj_as(HttpValidationError, _response.json())  # type: ignore
            )
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def generate_controlnet_sdxl(
        self, *, request: ImageGenerationRequest, request_options: typing.Optional[RequestOptions] = None
    ) -> ImageGenerationResponse:
        """
        Generate images in response to the given request.

        Parameters:
            - request: ImageGenerationRequest.

            - request_options: typing.Optional[RequestOptions]. Request-specific configuration.
        ---
        from octoai.client import AsyncOctoAI
        from octoai.image_gen import ImageGenerationRequest

        client = AsyncOctoAI(
            api_key="YOUR_API_KEY",
        )
        await client.image_gen.generate_controlnet_sdxl(
            request=ImageGenerationRequest(
                prompt="An octopus playing chess, masterpiece, photorealistic",
            ),
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(f"{self._client_wrapper.get_environment().image_gen}/", "generate/controlnet-sdxl"),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            json=jsonable_encoder(request)
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(request),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(ImageGenerationResponse, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(
                pydantic_v1.parse_obj_as(HttpValidationError, _response.json())  # type: ignore
            )
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def generate_controlnet_sd15(
        self, *, request: ImageGenerationRequest, request_options: typing.Optional[RequestOptions] = None
    ) -> ImageGenerationResponse:
        """
        Generate images in response to the given request.

        Parameters:
            - request: ImageGenerationRequest.

            - request_options: typing.Optional[RequestOptions]. Request-specific configuration.
        ---
        from octoai.client import AsyncOctoAI
        from octoai.image_gen import ImageGenerationRequest

        client = AsyncOctoAI(
            api_key="YOUR_API_KEY",
        )
        await client.image_gen.generate_controlnet_sd15(
            request=ImageGenerationRequest(
                prompt="An octopus playing chess, masterpiece, photorealistic",
            ),
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(f"{self._client_wrapper.get_environment().image_gen}/", "generate/controlnet-sd15"),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            json=jsonable_encoder(request)
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(request),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(ImageGenerationResponse, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(
                pydantic_v1.parse_obj_as(HttpValidationError, _response.json())  # type: ignore
            )
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def generate_sdxl(
        self, *, request: ImageGenerationRequest, request_options: typing.Optional[RequestOptions] = None
    ) -> ImageGenerationResponse:
        """
        Generate images in response to the given request.

        Parameters:
            - request: ImageGenerationRequest.

            - request_options: typing.Optional[RequestOptions]. Request-specific configuration.
        ---
        from octoai.client import AsyncOctoAI
        from octoai.image_gen import ImageGenerationRequest

        client = AsyncOctoAI(
            api_key="YOUR_API_KEY",
        )
        await client.image_gen.generate_sdxl(
            request=ImageGenerationRequest(
                prompt="An octopus playing chess, masterpiece, photorealistic",
            ),
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(f"{self._client_wrapper.get_environment().image_gen}/", "generate/sdxl"),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            json=jsonable_encoder(request)
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(request),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(ImageGenerationResponse, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(
                pydantic_v1.parse_obj_as(HttpValidationError, _response.json())  # type: ignore
            )
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def generate_sd(
        self, *, request: ImageGenerationRequest, request_options: typing.Optional[RequestOptions] = None
    ) -> ImageGenerationResponse:
        """
        Generate images in response to the given request.

        Parameters:
            - request: ImageGenerationRequest.

            - request_options: typing.Optional[RequestOptions]. Request-specific configuration.
        ---
        from octoai.client import AsyncOctoAI
        from octoai.image_gen import ImageGenerationRequest

        client = AsyncOctoAI(
            api_key="YOUR_API_KEY",
        )
        await client.image_gen.generate_sd(
            request=ImageGenerationRequest(
                prompt="An octopus playing chess, masterpiece, photorealistic",
            ),
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(f"{self._client_wrapper.get_environment().image_gen}/", "generate/sd"),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            json=jsonable_encoder(request)
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(request),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(ImageGenerationResponse, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(
                pydantic_v1.parse_obj_as(HttpValidationError, _response.json())  # type: ignore
            )
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
