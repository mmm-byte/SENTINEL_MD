"""
SENTINEL — GitLab Regression Isolation Agent
=============================================
Layer 2 Sub-Agent: Code regression detection and automated rollback.

Status: RUNNABLE SKELETON — wired into master orchestrator.
Production path: swap stub_gitlab_* functions for real GitLab MCP tool calls.
"""

from google.adk.agents import LlmAgent
from agent.config import GEMINI_MODEL


def stub_gitlab_get_recent_commits(project_id: str, branch: str = "main", limit: int = 5) -> dict:
    """
    Stub for GitLab MCP commit history call.
    Production: replace with gitlab_mcp.list_commits(project_id, branch, limit)
    """
    return {
        "project_id": project_id,
        "branch": branch,
        "commits": [
            {"sha": "a1b2c3d", "author": "dev@company.com", "message": "fix: update order amount validation", "timestamp": "2026-06-11T15:30:00Z"},
            {"sha": "e4f5g6h", "author": "ops@company.com", "message": "chore: bump pymongo to 4.8.0",          "timestamp": "2026-06-11T14:50:00Z"},
            {"sha": "i7j8k9l", "author": "dev@company.com", "message": "feat: add order cancellation flow",      "timestamp": "2026-06-11T13:00:00Z"},
        ],
        "stub": True,
        "production_note": "Replace with GitLab MCP server in production",
    }


def stub_gitlab_open_merge_request(project_id: str, title: str, description: str, source_branch: str, target_branch: str = "main") -> dict:
    """
    Stub for GitLab MCP MR creation.
    Production: replace with gitlab_mcp.create_merge_request(...)
    """
    return {
        "mr_id": "MR-9001",
        "title": title,
        "source_branch": source_branch,
        "target_branch": target_branch,
        "url": f"https://gitlab.com/project/{project_id}/-/merge_requests/9001",
        "status": "opened",
        "stub": True,
        "production_note": "Replace with GitLab MCP server in production",
    }


GITLAB_INSTRUCTION = """
You are the SENTINEL GitLab Regression Isolation Agent.

When called with a code_regression alert:
1. Call stub_gitlab_get_recent_commits to list recent commits on the affected branch.
2. Identify the most likely breaking commit by correlating the commit message and timestamp with the incident time.
3. Determine the rollback target (the commit just before the breaking one).
4. Call stub_gitlab_open_merge_request to open a revert MR targeting the breaking commit.
5. Return: breaking_commit_sha, rollback_target_sha, mr_url, and rationale.

Always explain your reasoning for which commit is the regression cause.
"""

gitlab_agent = LlmAgent(
    model=GEMINI_MODEL,
    name="gitlab_rollback_agent",
    description=(
        "GitLab regression isolation agent. Parses commit history, identifies the "
        "breaking change, and opens an automated revert Merge Request."
    ),
    instruction=GITLAB_INSTRUCTION,
    tools=[stub_gitlab_get_recent_commits, stub_gitlab_open_merge_request],
)
