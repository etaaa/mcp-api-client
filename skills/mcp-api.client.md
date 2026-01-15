---
name: mcp-api-client
description: MANDATORY skill for any task involving API routes, endpoints, or server logic. Use this whenever you create, modify, or debug backend endpoints to ensure they work as expected.
---

# MCP API Client Skill

## When to use this skill
- **MANDATORY**: Whenever you change a route definition (e.g., `@app.get`, `@app.post`).
- Whenever you modify the logic inside an endpoint function.
- Whenever you change data models (Pydantic, etc.) that the API uses.
- If you are debugging a "Method Not Allowed" or "404 Not Found" error.

## How to execute
1. **Locate the endpoint**: Identify the URL and the required HTTP method.
2. **Start/Restart Server**: Ensure the server is running on the correct port.
3. **Test with `api-client`**: Use the `mcp-api-client` to make a real HTTP request to the local server.
4. **Validate**: Check that the status code and body match the expected outcome.
5. **Negative Testing**: If you changed a method (e.g., POST to GET), test the old method to ensure it now correctly returns a 405.