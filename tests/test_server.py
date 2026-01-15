import pytest

from mcp_api_client.server import batch_request, make_request


@pytest.mark.asyncio
async def test_get_request():
    result = await make_request("GET", "https://httpbin.org/get")
    assert result["status"] == 200
    assert "body" in result
    assert "elapsed_ms" not in result
    assert "headers" not in result


@pytest.mark.asyncio
async def test_get_request_with_headers():
    result = await make_request("GET", "https://httpbin.org/get", include_headers=True)
    assert result["status"] == 200
    assert "headers" in result
    assert "body" in result


@pytest.mark.asyncio
async def test_post_with_json_body():
    result = await make_request(
        "POST",
        "https://httpbin.org/post",
        body={"key": "value", "number": 42},
    )
    assert result["status"] == 200
    assert result["body"]["json"] == {"key": "value", "number": 42}


@pytest.mark.asyncio
async def test_custom_headers():
    result = await make_request(
        "GET",
        "https://httpbin.org/headers",
        headers={"X-Custom": "test-value"},
    )
    assert result["status"] == 200
    assert result["body"]["headers"]["X-Custom"] == "test-value"


@pytest.mark.asyncio
async def test_query_params():
    result = await make_request(
        "GET",
        "https://httpbin.org/get",
        params={"foo": "bar"},
    )
    assert result["status"] == 200
    assert result["body"]["args"] == {"foo": "bar"}


@pytest.mark.asyncio
async def test_timeout_error():
    # Force timeout
    result = await make_request("GET", "https://httpbin.org/delay/5", timeout=1.0)
    assert result["error"] == "timeout"


@pytest.mark.asyncio
async def test_connection_error():
    # Trigger connection error
    result = await make_request("GET", "http://localhost:59999", timeout=2.0)
    assert result["error"] == "connection"


@pytest.mark.asyncio
async def test_put_request():
    result = await make_request("PUT", "https://httpbin.org/put", body={"a": 1})
    assert result["status"] == 200
    assert result["body"]["json"] == {"a": 1}


@pytest.mark.asyncio
async def test_delete_request():
    result = await make_request("DELETE", "https://httpbin.org/delete")
    assert result["status"] == 200


@pytest.mark.asyncio
async def test_batch_request_multiple_endpoints():
    requests = [
        {"method": "GET", "url": "https://httpbin.org/get"},
        {"method": "POST", "url": "https://httpbin.org/post", "body": {"test": "data"}},
        {"method": "GET", "url": "https://httpbin.org/status/201"},
    ]
    results = await batch_request(requests)

    assert len(results) == 3
    assert results[0]["status"] == 200
    assert results[1]["status"] == 200
    assert results[1]["body"]["json"] == {"test": "data"}
    assert results[2]["status"] == 201


@pytest.mark.asyncio
async def test_batch_request_with_params():
    requests = [
        {"method": "GET", "url": "https://httpbin.org/get", "params": {"key1": "val1"}},
        {"method": "GET", "url": "https://httpbin.org/get", "params": {"key2": "val2"}},
    ]
    results = await batch_request(requests)

    assert len(results) == 2
    assert results[0]["body"]["args"] == {"key1": "val1"}
    assert results[1]["body"]["args"] == {"key2": "val2"}


@pytest.mark.asyncio
async def test_batch_request_with_errors():
    requests = [
        {"method": "GET", "url": "https://httpbin.org/get"},
        {"method": "GET", "url": "http://localhost:59999"},
        {"method": "GET", "url": "https://httpbin.org/status/200"},
    ]
    results = await batch_request(requests, timeout=2.0)

    assert len(results) == 3
    assert results[0]["status"] == 200
    assert "error" in results[1]
    assert results[2]["status"] == 200


@pytest.mark.asyncio
async def test_batch_request_missing_url():
    requests = [
        {"method": "GET"},
    ]
    results = await batch_request(requests)

    assert len(results) == 1
    assert results[0]["error"] == "invalid_request"


@pytest.mark.asyncio
async def test_batch_request_with_headers():
    requests = [
        {"method": "GET", "url": "https://httpbin.org/get"},
        {"method": "POST", "url": "https://httpbin.org/post", "body": {"x": 1}},
    ]
    results = await batch_request(requests, include_headers=True)

    assert len(results) == 2
    assert "headers" in results[0]
    assert "headers" in results[1]


@pytest.mark.asyncio
async def test_batch_request_empty_list():
    results = await batch_request([])
    assert len(results) == 0
