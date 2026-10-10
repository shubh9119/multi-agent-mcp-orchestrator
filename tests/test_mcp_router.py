from mcp_router import classify_intent, deduplicate_mcp_tools

def test_classify_intent_routes_to_highest_scoring_agent():
    q1 = "Check this PR for SQL injection, XSS, and OWASP credential leaks"
    assert classify_intent(q1) == "security_auditor"

    q2 = "Please review this pull request for refactor opportunities and test coverage"
    assert classify_intent(q2) == "code_reviewer"

    q3 = "Summarize the latest benchmarks on speculative decoding"
    assert classify_intent(q3) == "researcher"

def test_deduplicate_mcp_tools_preserves_first_registration():
    tools = [
        {"name": "read_file", "server": "filesystem"},
        {"name": "search_code", "server": "github"},
        {"name": "read_file", "server": "github"},
    ]
    deduped = deduplicate_mcp_tools(tools)
    assert len(deduped) == 2
    assert deduped[0]["server"] == "filesystem"
