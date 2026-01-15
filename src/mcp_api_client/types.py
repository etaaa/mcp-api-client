from typing import Any, Literal
from pydantic import BaseModel, HttpUrl, Field


class Request(BaseModel):
    """Model representing an HTTP request."""
    url: HttpUrl = Field(..., description="Target URL")
    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD"] = Field(
        "GET", description="HTTP method"
    )
    body: dict | list | str | None = Field(None, description="Request body")
    headers: dict[str, str] | None = Field(None, description="HTTP headers")
    params: dict[str, str] | None = Field(None, description="Query parameters")


class Response(BaseModel):
    """Model representing an HTTP response."""
    status: int = Field(..., description="HTTP status code")
    body: Any = Field(None, description="Response body")
    headers: dict[str, str] | None = Field(None, description="Response headers")
