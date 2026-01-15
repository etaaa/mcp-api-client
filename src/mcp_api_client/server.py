import logging
from typing import Annotated, Any

from fastmcp import FastMCP
from mcp_api_client.client import batch_request, make_request

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("mcp_api_client")

mcp = FastMCP("API Client")


@mcp.tool
async def http_request(
    method: Annotated[str, "HTTP method (GET, POST, PUT, PATCH, DELETE, HEAD)"],
    url: Annotated[str, "Target URL"],
    body: Annotated[dict | list | str | None, "Request body"] = None,
    headers: Annotated[dict[str, str] | None, "HTTP headers"] = None,
    params: Annotated[dict[str, str] | None, "Query parameters"] = None,
    timeout: Annotated[float, "Timeout in seconds"] = 30.0,
    include_headers: Annotated[bool, "Include response headers in output"] = False,
) -> dict[str, Any]:
    """Make a single HTTP request. Returns status and body only by default."""
    logger.info(f"Tool 'http_request' called: {method} {url}")
    return await make_request(
        method, url, body, headers, params, timeout, include_headers
    )


@mcp.tool
async def http_batch_request(
    requests: Annotated[
        list[dict[str, Any]],
        "List of requests. Each dict must have 'method' and 'url', optionally 'body', 'headers', 'params'",
    ],
    timeout: Annotated[float, "Timeout in seconds for each request"] = 30.0,
    include_headers: Annotated[bool, "Include response headers in output"] = False,
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
    logger.info(f"Tool 'http_batch_request' called with {len(requests)} requests")
    return await batch_request(requests, timeout, include_headers)


def main() -> None:
    logger.info("Starting MCP API Client...")
    mcp.run()


if __name__ == "__main__":
    main()
