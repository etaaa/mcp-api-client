# mcp-api-client

An MCP server that enables LLMs to make HTTP requests to external APIs. Built with [FastMCP](https://github.com/jlowin/fastmcp) and [httpx](https://www.python-httpx.org/).

## What is MCP?

Model Context Protocol (MCP) is a standard for connecting LLMs to external tools and data sources. This server exposes an `http_request` tool that allows LLMs to fetch data from APIs, submit forms, and interact with web services.

## Installation

Clone the repository and install:

```bash
git clone https://github.com/your-username/mcp-api-client.git
cd mcp-api-client
pip install .
```

## Usage

Add the server to your MCP client configuration:

```json
{
  "mcpServers": {
    "api-client": {
      "command": "mcp-api-client"
    }
  }
}
```

Or run directly from the command line:

```bash
mcp-api-client
```

## Tool Reference

### http_request

Makes an HTTP request and returns the response.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| method | string | yes | HTTP method (GET, POST, PUT, PATCH, DELETE, HEAD) |
| url | string | yes | target URL |
| body | dict, list, or string | no | request body (automatically serialized as JSON for dict/list) |
| headers | dict | no | custom HTTP headers |
| params | dict | no | query parameters |
| timeout | float | no | request timeout in seconds (default: 30) |

**Response:**

```json
{
  "status_code": 200,
  "headers": { "content-type": "application/json", ... },
  "body": { ... },
  "elapsed_ms": 123.45,
  "url": "https://api.example.com/data"
}
```

On error, returns:

```json
{
  "error": "timeout",
  "message": "Timed out after 30s"
}
```

Error types: `timeout`, `connection`, `request`

## Examples

Fetch JSON from an API:

```
method: GET
url: https://api.github.com/users/octocat
```

Post data with custom headers:

```
method: POST
url: https://httpbin.org/post
body: {"name": "test", "value": 123}
headers: {"Authorization": "Bearer token123"}
```

## Testing

Install test dependencies and run the test suite:

```bash
pip install pytest pytest-asyncio
pytest
```

Tests run against [httpbin.org](https://httpbin.org) to verify request handling.

## License

MIT
