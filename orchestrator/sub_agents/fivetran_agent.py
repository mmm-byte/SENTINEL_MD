"""
SENTINEL — Fivetran Pipeline Schema-Drift Agent
================================================
Layer 2 Sub-Agent: Data pipeline schema mutation detection and remediation.

Status: RUNNABLE SKELETON — wired into master orchestrator.
Production path: swap stub_fivetran_* for real Fivetran MCP tool calls.
"""

from google.adk.agents import LlmAgent
from agent.config import GEMINI_MODEL


def stub_fivetran_get_connector_status(connector_id: str) -> dict:
    """
    Stub for Fivetran MCP connector status call.
    Production: replace with fivetran_mcp.get_connector(connector_id)
    """
    return {
        "connector_id": connector_id,
        "status": "broken",
        "last_sync": "2026-06-11T15:29:00Z",
        "error": "SchemaChange: column 'amount' type changed from FLOAT to VARCHAR in source",
        "affected_table": "orders",
        "source_system": "PostgreSQL (prod)",
        "destination": "BigQuery (analytics)",
        "stub": True,
        "production_note": "Replace with Fivetran MCP server in production",
    }


def stub_fivetran_patch_schema(connector_id: str, table: str, column: str, new_type: str) -> dict:
    """
    Stub for Fivetran MCP schema patch call.
    Production: replace with fivetran_mcp.update_schema(connector_id, table, column, new_type)
    """
    return {
        "connector_id": connector_id,
        "table": table,
        "column": column,
        "old_type": "VARCHAR",
        "new_type": new_type,
        "patch_applied": True,
        "next_sync_scheduled": "2026-06-11T15:50:00Z",
        "stub": True,
        "production_note": "Replace with Fivetran MCP server in production",
    }


FIVETRAN_INSTRUCTION = """
You are the SENTINEL Fivetran Pipeline Schema-Drift Agent.

When called with a pipeline_drift alert:
1. Call stub_fivetran_get_connector_status to identify which connector is broken and what schema changed.
2. Map the source-to-destination type mutation (e.g., FLOAT -> VARCHAR).
3. Call stub_fivetran_patch_schema to update the destination schema definition.
4. Return: connector_id, affected_table, affected_column, old_type, new_type, next_sync_scheduled.

Always check whether data already synced during the broken window needs backfilling.
"""

fivetran_agent = LlmAgent(
    model=GEMINI_MODEL,
    name="fivetran_pipeline_agent",
    description=(
        "Fivetran pipeline schema-drift agent. Detects sync errors, maps type mutations, "
        "patches warehouse schema definitions, and re-schedules catch-up syncs."
    ),
    instruction=FIVETRAN_INSTRUCTION,
    tools=[stub_fivetran_get_connector_status, stub_fivetran_patch_schema],
)
