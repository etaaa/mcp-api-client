# mcp-api-client

[![CI](https://github.com/etaaa/mcp-api-client/actions/workflows/python-package.yml/badge.svg)](https://github.com/etaaa/mcp-api-client/actions/workflows/python-package.yml)

**Postman for LLMs.** A specialized MCP server designed for rapid REST API testing and exploration. Instead of writing boilerplate test code, your LLM assistant can now directly interact with, debug, and validate your endpoints in real-time.

Built with [FastMCP](https://github.com/jlowin/fastmcp) and [httpx](https://www.python-httpx.org/).

## Why `mcp-api-client`?

Traditional API testing requires writing scripts or switching to GUI tools like Postman. This server brings that power directly into your AI-assisted development workflow:

- **LLM-Native Testing**: Quickly pre-test endpoints using natural language without writing a single line of test code.
- **Zero-Boilerplate Prototyping**: Interact with new APIs instantly to understand their behavior.
- **Local Dev Companion**: Perfect for testing your local development server (`localhost`) during the build phase.
- **Deep Inspection**: Get full visibility into status codes, headers, and structured JSON responses.

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

## Tool Reference: `http_request`

The primary tool for making arbitrary HTTP requests.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `method` | string | Yes | HTTP method (GET, POST, PUT, etc.) |
| `url` | string | Yes | The target endpoint URL |
| `body` | any | No | Request body (auto-serialized as JSON if dict/list) |
| `headers` | dict | No | Custom headers |
| `params` | dict | No | Query parameters |
| `timeout` | float | No | Request timeout (default: 30s) |

## Agent Automation (Skills)

To make testing even more convenient, we've included a **Skill** definition. You can copy the contents of [`skills/mcp-api-client.md`](./skills/mcp-api-client.md) into your own AI agent's codebase (as a "Skill" or "Instruction") to automatically teach it how to use this server for systematic API verification.

## Examples

**Check a local health endpoint:**
```text
method: GET
url: http://localhost:8000/health
```

**Validate a POST request with JSON:**
```text
method: POST
url: http://localhost:3000/api/users
body: {"name": "Test User", "role": "admin"}
headers: {"Content-Type": "application/json"}
```

## Testing & Contributing

```bash
pip install pytest pytest-asyncio
pytest
```

Contributions are welcome! If you find a bug or have a feature request, please open an issue or submit a PR.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

