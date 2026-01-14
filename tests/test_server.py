# tests for MCP API client server

import pytest

from mcp_api_client.server import make_request


@pytest.mark.asyncio
async def test_get_request():
    result = await make_request("GET", "https://httpbin.org/get")
    assert result["status_code"] == 200
    assert "headers" in result
    assert "body" in result
    assert "elapsed_ms" in result


@pytest.mark.asyncio
async def test_post_with_json_body():
    result = await make_request(
        "POST",
        "https://httpbin.org/post",
        body={"key": "value", "number": 42},
    )
    assert result["status_code"] == 200
    assert result["body"]["json"] == {"key": "value", "number": 42}


@pytest.mark.asyncio
async def test_custom_headers():
    result = await make_request(
        "GET",
        "https://httpbin.org/headers",
        headers={"X-Custom": "test-value"},
    )
    assert result["status_code"] == 200
    assert result["body"]["headers"]["X-Custom"] == "test-value"


@pytest.mark.asyncio
async def test_query_params():
    result = await make_request(
        "GET",
        "https://httpbin.org/get",
        params={"foo": "bar"},
    )
    assert result["status_code"] == 200
    assert result["body"]["args"] == {"foo": "bar"}


@pytest.mark.asyncio
async def test_timeout_error():
    # uses httpbin delay endpoint to force a timeout
    result = await make_request("GET", "https://httpbin.org/delay/5", timeout=1.0)
    assert result["error"] == "timeout"


@pytest.mark.asyncio
async def test_connection_error():
    # connect to non-existent local port to trigger connection error
    result = await make_request("GET", "http://localhost:59999", timeout=2.0)
    assert result["error"] == "connection"


@pytest.mark.asyncio
async def test_put_request():
    result = await make_request("PUT", "https://httpbin.org/put", body={"a": 1})
    assert result["status_code"] == 200
    assert result["body"]["json"] == {"a": 1}


@pytest.mark.asyncio
async def test_delete_request():
    result = await make_request("DELETE", "https://httpbin.org/delete")
    assert result["status_code"] == 200
