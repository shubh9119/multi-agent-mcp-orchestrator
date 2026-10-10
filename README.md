# Multi-Agent LLM Orchestration Platform with Model Context Protocol (MCP)

[![CI Pipeline](https://img.shields.io/badge/CI-Passing-brightgreen)](#)
[![MCP](https://img.shields.io/badge/Protocol-Model%20Context%20Protocol-purple)](#)
[![Anthropic](https://img.shields.io/badge/LLM-Claude%20Sonnet%204-blue)](#)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-informational)](#)

Production **Multi-Agent LLM Orchestration Platform** implementing **Model Context Protocol (MCP)** stdio server lifecycle management, weighted intent routing, cross-server tool schema deduplication, and bounded agentic tool-execution loops.

---

## Multi-Agent MCP Architecture

```mermaid
flowchart LR
    USER(["User Prompt"]) --> ROUTER["Weighted Intent Router"]

    subgraph Agents["Domain-Specialized Agent Pool"]
        SEC["Security Auditor Agent"]
        CODE["Code Reviewer Agent"]
        RES["Deep Researcher Agent"]
        ARCH["Systems / BIM Agent"]
    end

    subgraph MCP["Model Context Protocol (MCP) Server Bus"]
        GH[("GitHub MCP Server")]
        FS[("Filesystem MCP Server")]
        FETCH[("Web Fetch MCP Server")]
    end

    ROUTER -->|"OWASP / Auth / CVE"| SEC
    ROUTER -->|"PR / Refactor / Lint"| CODE
    ROUTER -->|"Synthesis / Citations"| RES
    ROUTER -->|"Specs / CAD / Models"| ARCH

    SEC --> GH & FETCH
    CODE --> GH & FS
    RES --> FETCH & FS
    ARCH --> FS
```

---

## MCP Tool-Call Execution Workflow

```mermaid
sequenceDiagram
    autonumber
    participant U as User
    participant R as Intent Router
    participant A as Specialized Agent
    participant S as AsyncExitStack (MCP Client)
    participant M as MCP Stdio Servers

    U->>R: Submit multi-step engineering query
    R->>A: Select highest-scoring specialist agent
    A->>S: Spawn isolated stdio MCP servers
    S->>M: Initialize JSON-RPC 2.0 sessions & list tools
    M-->>S: Return deduplicated tool schemas
    loop Bounded Tool-Use Loop (max_iterations = 10)
        A->>M: Dispatch tool_use call via session_map[tool_name]
        M-->>A: Return structured tool_result payload
    end
    A->>S: Guarantee AsyncExitStack.aclose() teardown
    A-->>U: Stream final synthesized response
```

---

## Key Bug Fixes & Production Hardening

1. **Zero-Leak MCP Subprocess Teardown (`connect_mcp_servers`):** Wrapped multi-server `stdio_client` initialization inside `try / except BaseException: await stack.aclose(); raise` so a failing second MCP server never leaves zombie `npx` child processes running.
2. **Cross-Server Tool Schema Deduplication:** Prevented Anthropic API `400 Bad Request (duplicate tool name)` errors when two MCP servers expose identically named tools.
3. **Bounded Agentic Tool Loop (`run_agent_async`):** Added `max_iterations = 10` guard to the `while response.stop_reason == "tool_use":` loop to prevent infinite tool-calling cycles.
4. **Weighted Intent Classification (`classify_query`):** Upgraded greedy first-match keyword checks to weighted multi-keyword scoring so queries mentioning both `"test"` and `"SQL injection vulnerability"` route accurately to `security_auditor`.

---

## Quickstart

```bash
git clone https://github.com/shubh9119/multi-agent-mcp-orchestrator.git
cd multi-agent-mcp-orchestrator
pip install -r requirements.txt
streamlit run app.py
```

### Run Unit Tests
```bash
pytest -v
```
