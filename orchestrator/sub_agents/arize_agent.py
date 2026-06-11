"""
SENTINEL — Arize Cognitive Supervisor Agent
============================================
Layer 2 Sub-Agent: AI watchdog that monitors all SENTINEL sub-agents for
hallucinations, infinite tool-call loops, and token drift.

Status: RUNNABLE SKELETON — wired into master orchestrator as supervisor.
Production path: swap stub_arize_* for real Arize Phoenix MCP tool calls.
"""

from google.adk.agents import LlmAgent
from agent.config import GEMINI_MODEL


def stub_arize_get_agent_traces(session_id: str, agent_name: str) -> dict:
    """
    Stub for Arize Phoenix MCP trace query.
    Production: replace with arize_mcp.get_traces(session_id, agent_name)
    """
    return {
        "session_id": session_id,
        "agent_name": agent_name,
        "total_tool_calls": 7,
        "hallucination_score": 0.04,   # 0.0 = clean, 1.0 = severe hallucination
        "loop_detected": False,
        "token_drift_score": 0.11,     # 0.0 = stable, 1.0 = severe drift
        "evaluation": "HEALTHY",
        "stub": True,
        "production_note": "Replace with Arize Phoenix MCP server in production",
    }


def stub_arize_flag_session(session_id: str, reason: str, severity: str) -> dict:
    """
    Stub for Arize Phoenix MCP session flag call.
    Production: replace with arize_mcp.flag_session(session_id, reason, severity)
    """
    return {
        "session_id": session_id,
        "flagged": True,
        "reason": reason,
        "severity": severity,
        "action": "Operator notified. Session marked for human review.",
        "stub": True,
        "production_note": "Replace with Arize Phoenix MCP server in production",
    }


ARIZE_INSTRUCTION = """
You are the SENTINEL Arize Cognitive Supervisor — the AI watchdog layer.

You are called AFTER every other sub-agent completes to audit their session quality.

For each sub-agent session:
1. Call stub_arize_get_agent_traces(session_id, agent_name) to retrieve the cognitive trace.
2. If hallucination_score > 0.30 OR loop_detected is True OR token_drift_score > 0.50:
   a. Call stub_arize_flag_session(session_id, reason, severity="HIGH").
   b. Recommend the operator discard the sub-agent's output and retry.
3. If scores are within safe bounds, confirm the session as HEALTHY.
4. Return a cognitive audit report: agent_name, evaluation, scores, and any flags raised.

You are the last line of defence. Your role is to catch AI errors before they become
operational errors.
"""

arize_agent = LlmAgent(
    model=GEMINI_MODEL,
    name="arize_supervisor_agent",
    description=(
        "Arize cognitive supervisor. Monitors all SENTINEL sub-agents for hallucinations, "
        "tool-call loops, and token drift. Flags sessions that exceed safe thresholds."
    ),
    instruction=ARIZE_INSTRUCTION,
    tools=[stub_arize_get_agent_traces, stub_arize_flag_session],
)
