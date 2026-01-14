# mcp-api-client

[![CI](https://github.com/etaaa/mcp-api-client/actions/workflows/python-package.yml/badge.svg)](https://github.com/etaaa/mcp-api-client/actions/workflows/python-package.yml)

A lightweight MCP server that gives LLMs the ability to make HTTP requests. Perfect for local development, testing API endpoints, and integrating with web services. Built with [FastMCP](https://github.com/jlowin/fastmcp) and [httpx](https://www.python-httpx.org/).

## Use Cases

- **Local development**: Test your API endpoints directly through your LLM assistant
- **API debugging**: Inspect responses, headers, and status codes from any endpoint
- **Rapid prototyping**: Quickly interact with REST APIs without leaving your editor
- **Integration testing**: Verify API behavior during development

## What is MCP?

Model Context Protocol (MCP) is a standard for connecting LLMs to external tools and data sources. This server exposes an `http_request` tool that allows LLMs to call APIs, test endpoints, and interact with web services, including your local dev server.

## Installation

**Requirements:** Python 3.10 or higher

Clone the repository and install:

```bash
git clone https://github.com/etaaa/mcp-api-client.git
cd mcp-api-client
pip install .
```

## Usage

First, find where `mcp-api-client` was installed:

```bash
which mcp-api-client
```

Add the server to your MCP client configuration using the **full path**:

```json
{
  "mcpServers": {
    "api-client": {
      "command": "/full/path/to/mcp-api-client"
    }
  }
}
```

To run directly from the command line:

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

Test a local endpoint:

```
method: GET
url: http://localhost:3000/api/users
```

Check your local server's health endpoint:

```
method: GET
url: http://localhost:8080/health
```

Post data to a local API:

```
method: POST
url: http://localhost:3000/api/users
body: {"name": "test", "email": "test@example.com"}
headers: {"Content-Type": "application/json"}
```

Call an external API:

```
method: GET
url: https://api.github.com/users/octocat
```

## Testing

Install test dependencies and run the test suite:

```bash
pip install pytest pytest-asyncio
pytest
```

Tests run against [httpbin.org](https://httpbin.org) to verify request handling.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/new-feature`)
3. Run tests (`pytest`)
4. Commit your changes (`git commit -m 'feat: add new feature'`)
5. Push to the branch (`git push origin feature/new-feature`)
6. Open a Pull Request

## License

MIT
