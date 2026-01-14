# MCP server for HTTP requests

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
) -> dict[str, Any]:
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            # use json param for structured data, content for raw strings
            response = await client.request(
                method=method.upper(),
                url=url,
                headers=headers,
                params=params,
                json=body if isinstance(body, (dict, list)) else None,
                content=body if isinstance(body, str) else None,
            )

        # attempt JSON parsing if content-type indicates JSON
        content_type = response.headers.get("content-type", "")
        if response.content and "application/json" in content_type:
            try:
                body_content = response.json()
            except ValueError:
                body_content = response.text
        else:
            body_content = response.text or None

        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": body_content,
            "elapsed_ms": round(response.elapsed.total_seconds() * 1000, 2),
            "url": str(response.url),
        }

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
) -> dict[str, Any]:
    # exposed as MCP tool for external clients
    return await make_request(method, url, body, headers, params, timeout)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
