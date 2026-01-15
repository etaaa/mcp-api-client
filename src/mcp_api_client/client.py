from typing import Any
import asyncio
import httpx
import logging

logger = logging.getLogger(__name__)

async def make_request(
    method: str,
    url: str,
    body: dict | list | str | None = None,
    headers: dict[str, str] | None = None,
    params: dict[str, str] | None = None,
    timeout: float = 30.0,
    include_headers: bool = False,
) -> dict[str, Any]:
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

        result = {
            "status": response.status_code,
            "body": body_content,
        }

        # Add headers if requested
        if include_headers:
            result["headers"] = dict(response.headers)

        logger.debug(f"Request completed: {method} {url} - Status: {response.status_code}")
        return result

    except httpx.TimeoutException:
        logger.warning(f"Request timeout: {method} {url}")
        return {"error": "timeout", "message": f"Timed out after {timeout}s"}
    except httpx.ConnectError as e:
        logger.warning(f"Connection error: {method} {url} - {e}")
        return {"error": "connection", "message": str(e)}
    except httpx.RequestError as e:
        logger.warning(f"Request error: {method} {url} - {e}")
        return {"error": "request", "message": str(e)}
    except Exception as e:
        logger.exception(f"Unexpected error: {method} {url}")
        return {"error": "unknown", "message": str(e)}


async def batch_request(
    requests: list[dict[str, Any]],
    timeout: float = 30.0,
    include_headers: bool = False,
) -> list[dict[str, Any]]:
    logger.info(f"Starting batch request with {len(requests)} requests")
    
    tasks = []
    for req in requests:
        url = req.get("url")
        if not url:
            # Return error for missing url
            async def invalid_req():
                 return {"error": "invalid_request", "message": "Missing 'url' field"}
            tasks.append(invalid_req())
            continue

        method = req.get("method", "GET")
        body = req.get("body")
        headers = req.get("headers")
        params = req.get("params")

        tasks.append(
            make_request(
                method=method,
                url=url,
                body=body,
                headers=headers,
                params=params,
                timeout=timeout,
                include_headers=include_headers,
            )
        )
    
    results = await asyncio.gather(*tasks)
    logger.info("Batch request completed")
    return list(results)
