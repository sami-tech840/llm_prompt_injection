# src/gateway.py
import re
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, Dict, Any

class SafeEmailArgs(BaseModel):
    recipient: EmailStr
    subject: str = Field(max_length=100)
    body: str = Field(max_length=500)

    @field_validator("recipient")
    def only_internal_domains(cls, v: str) -> str:
        allowed_domains = ("@company.com", "@support.org")
        if not any(v.endswith(domain) for domain in allowed_domains):
            raise ValueError(f"Unauthorized recipient domain: {v}")
        return v

class SafeSQLArgs(BaseModel):
    query: str = Field(max_length=200)

    @field_validator("query")
    def block_destructive_sql(cls, v: str) -> str:
        forbidden = r"\b(DROP|DELETE|TRUNCATE|ALTER|UPDATE|INSERT|UNION|--|;)\b"
        if re.search(forbidden, v, re.IGNORECASE):
            raise ValueError("SQL injection / destructive keyword detected")
        return v

class ToolGateway:
    """Interception layer validating tool selection and argument bounds."""

    def __init__(self, allowed_tools: list[str]):
        self.allowed_tools = allowed_tools

    def validate_call(self, tool_name: str, tool_args: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        # 1. Enforce Tool Permissions
        if tool_name not in self.allowed_tools:
            return False, f"Permission Denied: Tool '{tool_name}' not permitted in this context."

        # 2. Enforce Parameter Hygiene with Pydantic
        try:
            if tool_name == "send_email":
                SafeEmailArgs(**tool_args)
            elif tool_name == "execute_sql_query":
                SafeSQLArgs(**tool_args)
            return True, None
        except Exception as e:
            return False, f"Validation Error: {str(e)}"