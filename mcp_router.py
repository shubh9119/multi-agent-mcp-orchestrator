"""Core MCP routing and tool deduplication utilities (importable without Streamlit runtime)."""
from typing import Dict, List, Any

def classify_intent(query: str) -> str:
    """Weighted multi-keyword intent classifier for routing queries to specialized MCP agents."""
    query_lower = (query or "").lower()
    keyword_map = {
        "security_auditor": [
            "security", "vulnerability", "owasp", "injection", "xss",
            "csrf", "secret", "credential", "auth", "penetration", "cve"
        ],
        "code_reviewer": [
            "review", "bug", "refactor", "code quality", "anti-pattern",
            "lint", "test", "coverage", "pull request", "pr ", "exception"
        ],
        "bim_engineer": [
            "revit", "bim", "wall", "floor plan", "sheet", "construction",
            "building", "architecture", "detail", "annotation"
        ],
    }
    scores = {
        agent_id: sum(1 for kw in kws if kw in query_lower)
        for agent_id, kws in keyword_map.items()
    }
    best_agent, best_score = max(scores.items(), key=lambda item: item[1])
    return best_agent if best_score > 0 else "researcher"

def deduplicate_mcp_tools(server_tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Ensure tool definitions across multiple MCP servers have unique names for Anthropic tool-use API."""
    seen = set()
    unique_tools = []
    for tool in server_tools:
        name = tool.get("name")
        if name and name not in seen:
            seen.add(name)
            unique_tools.append(tool)
    return unique_tools
