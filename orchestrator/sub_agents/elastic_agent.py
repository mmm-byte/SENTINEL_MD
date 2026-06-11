"""
SENTINEL — Elastic Log Anomaly Agent
=====================================
Layer 2 Sub-Agent: Log triage and root-cause synthesis.

Status: RUNNABLE SKELETON — wired into master orchestrator.
Production path: swap stub_elastic_search() for real Elastic MCP tool calls.
"""

from google.adk.agents import LlmAgent
from agent.config import GEMINI_MODEL


def stub_elastic_search(index: str, query: str, time_range_minutes: int = 30) -> dict:
    """
    Stub for Elastic MCP server call.
    Production: replace with elastic_mcp.search(index, query, time_range)

    Returns a simulated log anomaly result.
    """
    return {
        "index": index,
        "query": query,
        "time_range_minutes": time_range_minutes,
        "hits": [
            {
                "@timestamp": "2026-06-11T15:44:01Z",
                "level": "ERROR",
                "service": "orders-api",
                "message": "MongoServerError: Document failed validation",
                "trace_id": "abc-123-def",
                "count_last_30m": 47,
            }
        ],
        "anomaly_detected": True,
        "root_cause_hint": "Spike in MongoDB validation errors correlates with deploy at 15:30Z",
        "stub": True,
        "production_note": "Replace with Elastic MCP server in production",
    }


ELASTIC_INSTRUCTION = """
You are the SENTINEL Elastic Log Anomaly Agent.

When called with a log_anomaly alert:
1. Call stub_elastic_search to retrieve recent error logs from the affected service.
2. Identify the anomaly pattern (error type, spike time, affected services).
3. Extract a root-cause hypothesis from the log messages.
4. Return a structured summary: anomaly_type, first_seen, affected_services, root_cause_hypothesis.

Always include the trace_id if present so the operator can correlate with APM.
"""

elastic_agent = LlmAgent(
    model=GEMINI_MODEL,
    name="elastic_log_agent",
    description=(
        "Elastic log anomaly agent. Queries error indices, identifies anomaly spikes, "
        "and extracts root-cause signatures from distributed logs."
    ),
    instruction=ELASTIC_INSTRUCTION,
    tools=[stub_elastic_search],
)
