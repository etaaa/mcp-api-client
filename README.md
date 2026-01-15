# mcp-api-client

[![CI](https://github.com/etaaa/mcp-api-client/actions/workflows/python-package.yml/badge.svg)](https://github.com/etaaa/mcp-api-client/actions/workflows/python-package.yml)

**Postman for LLMs.** A specialized, resource-efficient MCP server designed for rapid REST API testing and exploration. Instead of writing boilerplate test code, your LLM assistant can now directly interact with, debug, and validate your endpoints in real-time.

Built with [FastMCP](https://github.com/jlowin/fastmcp) and [httpx](https://www.python-httpx.org/).

## Why `mcp-api-client`?

Traditional API testing requires writing scripts or switching to GUI tools like Postman. This server brings that power directly into your AI-assisted development workflow:

- **LLM-Native Testing**: Quickly test endpoints using natural language without writing test code.
- **Resource Efficient**: Minimal response format reduces token consumption, only returns status and body by default.
- **Zero-Boilerplate Prototyping**: Interact with new APIs instantly to understand their behavior.
- **Local Dev Companion**: Perfect for testing your local development server (`localhost`) during the build phase.

## Installation

**Requirements:** Python 3.10+

```bash
git clone https://github.com/etaaa/mcp-api-client.git
cd mcp-api-client
pip install .
```

## Setup

1. Find the installed path:
   ```bash
   which mcp-api-client
   ```

2. Add the server to your MCP client configuration (e.g., Claude Desktop):
   ```json
   {
     "mcpServers": {
       "api-client": {
         "command": "/full/path/to/mcp-api-client"
       }
     }
   }
   ```

## Tools

### `http_request`

Make a single HTTP request with minimal response data.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `method` | string | Yes | HTTP method (GET, POST, PUT, etc.) |
| `url` | string | Yes | The target endpoint URL |
| `body` | any | No | Request body (auto-serialized as JSON if dict/list) |
| `headers` | dict | No | Custom headers |
| `params` | dict | No | Query parameters |
| `timeout` | float | No | Request timeout (default: 30s) |
| `include_headers` | bool | No | Include response headers (default: false) |

**Response format:**
```json
{
  "status": 200,
  "body": {"key": "value"}
}
```

### `http_batch_request`

Execute multiple HTTP requests efficiently in a single call. **Highly recommended** for testing multiple endpoints to minimize token usage.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `requests` | list | Yes | List of request objects (each with method, url, body, headers, params) |
| `timeout` | float | No | Request timeout for each request (default: 30s) |
| `include_headers` | bool | No | Include response headers (default: false) |

**Example:**
```json
{
  "requests": [
    {"method": "GET", "url": "http://localhost:8000/health"},
    {"method": "POST", "url": "http://localhost:8000/users", "body": {"name": "Test"}},
    {"method": "GET", "url": "http://localhost:8000/users/1"}
  ]
}
```

**Returns:** Array of responses in the same order as requests.

## Examples

**Single request:**
```text
method: GET
url: http://localhost:8000/health
```

**Batch testing (recommended for multiple endpoints):**
```text
requests:
  - method: GET
    url: http://localhost:3000/api/health
  - method: POST
    url: http://localhost:3000/api/users
    body: {"name": "Test User", "role": "admin"}
  - method: GET
    url: http://localhost:3000/api/users
```

## Resource Efficiency Features

1. **Minimal Response Format**: Returns only `status` and `body` by default
2. **Optional Headers**: Headers excluded unless explicitly requested with `include_headers=true`
3. **No Timing Data**: Removed `elapsed_ms` to reduce token usage
4. **Batch Operations**: Test multiple endpoints in one call instead of multiple tool invocations
5. **Smart Body Parsing**: Automatically detects and parses JSON responses

## Testing & Contributing

```bash
pip install pytest pytest-asyncio
pytest
```

Contributions are welcome! If you find a bug or have a feature request, please open an issue or submit a PR.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

