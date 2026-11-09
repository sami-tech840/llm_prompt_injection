# src/tools.py
from typing import Dict, Any

# Tool 1: Read-only document lookup (Benign expected tool)
def search_knowledge_base(query: str) -> Dict[str, Any]:
    """Searches company knowledge base for answers."""
    return {"status": "success", "result": f"KB snippet for: {query}"}

# Tool 2: Database query (High-risk target for parameter injection)
def execute_sql_query(query: str) -> Dict[str, Any]:
    """Executes a customer support SQL query."""
    return {"status": "success", "executed_query": query}

# Tool 3: Outbound communication (High-risk target for data exfiltration)
def send_email(recipient: str, subject: str, body: str) -> Dict[str, Any]:
    """Sends an automated email notification."""
    return {"status": "success", "recipient": recipient, "subject": subject}

AVAILABLE_TOOLS = {
    "search_knowledge_base": search_knowledge_base,
    "execute_sql_query": execute_sql_query,
    "send_email": send_email,
}