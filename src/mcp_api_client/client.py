from typing import Any
import asyncio
import httpx
import logging
from mcp_api_client.types import Request, Response

logger = logging.getLogger(__name__)


async def make_request(
    method: str,
    url: str,
    body: dict | list | str | None = None,
    headers: dict[str, str] | None = None,
    params: dict[str, str] | None = None,
    timeout: float = 30.0,
    include_headers: bool = False,
) -> Response:
    logger.debug(f"Making request: {method} {url}")
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.request(
                method=method.upper(),
                url=url,
                headers=headers,
                params=params,
                json=body if isinstance(body, (dict, list)) else None,
                content=body if isinstance(body, str) else None,
            )

        # Parse response body
        content_type = response.headers.get("content-type", "")
        if response.content and "application/json" in content_type:
            try:
                body_content = response.json()
            except ValueError:
                body_content = response.text
        else:
            body_content = response.text or None

        response_headers = dict(response.headers) if include_headers else None

        result = Response(
            status=response.status_code, body=body_content, headers=response_headers
        )

        logger.debug(
            f"Request completed: {method} {url} - Status: {response.status_code}"
        )
        return result

    except httpx.TimeoutException:
        logger.warning(f"Request timeout: {method} {url}")
        return Response(
            status=408,
            body={"error": "timeout", "message": f"Timed out after {timeout}s"},
        )
    except httpx.ConnectError as e:
        logger.warning(f"Connection error: {method} {url} - {e}")
        return Response(status=503, body={"error": "connection", "message": str(e)})
    except httpx.RequestError as e:
        logger.warning(f"Request error: {method} {url} - {e}")
        return Response(status=500, body={"error": "request", "message": str(e)})
    except Exception as e:
        logger.exception(f"Unexpected error: {method} {url}")
        return Response(status=500, body={"error": "unknown", "message": str(e)})


async def batch_request(
    requests: list[Request],
    timeout: float = 30.0,
    include_headers: bool = False,
) -> list[Response]:
    logger.info(f"Starting batch request with {len(requests)} requests")

    tasks = []
    for req in requests:
        # Pydantic URL is strictly typed, convert to string
        url_str = str(req.url)

        tasks.append(
            make_request(
                method=req.method,
                url=url_str,
                body=req.body,
                headers=req.headers,
                params=req.params,
                timeout=timeout,
                include_headers=include_headers,
            )
        )

    results = await asyncio.gather(*tasks)
    logger.info("Batch request completed")
    return list(results)
