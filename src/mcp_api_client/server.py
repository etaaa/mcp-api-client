from typing import Annotated, Any

import httpx
from fastmcp import FastMCP

mcp = FastMCP("API Client")


async def make_request(
    method: str,
    url: str,
    body: dict | list | str | None = None,
    headers: dict[str, str] | None = None,
    params: dict[str, str] | None = None,
    timeout: float = 30.0,
    include_headers: bool = False,
) -> dict[str, Any]:
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

        # parse json or text based on content-type
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

        # include headers only if requested to save tokens
        if include_headers:
            result["headers"] = dict(response.headers)

        return result

    except httpx.TimeoutException:
        return {"error": "timeout", "message": f"Timed out after {timeout}s"}
    except httpx.ConnectError as e:
        return {"error": "connection", "message": str(e)}
    except httpx.RequestError as e:
        return {"error": "request", "message": str(e)}


@mcp.tool
async def http_request(
    method: Annotated[str, "HTTP method (GET, POST, PUT, PATCH, DELETE, HEAD)"],
    url: Annotated[str, "Target URL"],
    body: Annotated[dict | list | str | None, "Request body"] = None,
    headers: Annotated[dict[str, str] | None, "HTTP headers"] = None,
    params: Annotated[dict[str, str] | None, "Query parameters"] = None,
    timeout: Annotated[float, "Timeout in seconds"] = 30.0,
    include_headers: Annotated[bool,
                               "Include response headers in output"] = False,
) -> dict[str, Any]:
    """Make a single HTTP request. Returns status and body only by default."""
    return await make_request(method, url, body, headers, params, timeout, include_headers)


async def batch_request(
    requests: list[dict[str, Any]],
    timeout: float = 30.0,
    include_headers: bool = False,
) -> list[dict[str, Any]]:
    results = []
    async with httpx.AsyncClient(timeout=timeout) as client:
        for req in requests:
            try:
                method = req.get("method", "GET")
                url = req.get("url")
                if not url:
                    results.append({"error": "invalid_request",
                                   "message": "Missing 'url' field"})
                    continue

                body = req.get("body")
                headers = req.get("headers")
                params = req.get("params")

                response = await client.request(
                    method=method.upper(),
                    url=url,
                    headers=headers,
                    params=params,
                    json=body if isinstance(body, (dict, list)) else None,
                    content=body if isinstance(body, str) else None,
                )

                # parse json or text response
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

                if include_headers:
                    result["headers"] = dict(response.headers)

                results.append(result)

            except httpx.TimeoutException:
                results.append(
                    {"error": "timeout", "message": f"Timed out after {timeout}s"})
            except httpx.ConnectError as e:
                results.append({"error": "connection", "message": str(e)})
            except httpx.RequestError as e:
                results.append({"error": "request", "message": str(e)})
            except Exception as e:
                results.append({"error": "unknown", "message": str(e)})

    return results


@mcp.tool
async def http_batch_request(
    requests: Annotated[
        list[dict[str, Any]],
        "List of requests. Each dict must have 'method' and 'url', optionally 'body', 'headers', 'params'"
    ],
    timeout: Annotated[float, "Timeout in seconds for each request"] = 30.0,
    include_headers: Annotated[bool,
                               "Include response headers in output"] = False,
) -> list[dict[str, Any]]:
    """Execute multiple HTTP requests efficiently in a single call.

    Reduces token usage by batching requests and minimizing response overhead.
    Each request in the list can have: method, url, body, headers, params.

    Example:
        requests = [
            {"method": "GET", "url": "https://api.example.com/users"},
            {"method": "POST", "url": "https://api.example.com/users", "body": {"name": "Test"}},
            {"method": "GET", "url": "https://api.example.com/health"}
        ]
    """
    return await batch_request(requests, timeout, include_headers)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
