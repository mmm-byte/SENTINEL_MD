#!/usr/bin/env bash
# =============================================================================
# SENTINEL — One-shot local demo runner
# Usage: bash demo/run_demo.sh
# Requires: Python 3.11+, Node.js, MongoDB MCP Server, .env configured
# =============================================================================

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"
cd "$PROJECT_ROOT"

echo ""
echo -e "${BOLD}${GREEN}╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}${GREEN}║   SENTINEL — MongoDB Schema Continuity Agent         ║${NC}"
echo -e "${BOLD}${GREEN}║   Google Cloud Rapid Agent Hackathon 2026             ║${NC}"
echo -e "${BOLD}${GREEN}╚══════════════════════════════════════════════════════╝${NC}"
echo ""

# ── Check prerequisites ──────────────────────────────────────────────────────
echo -e "${CYAN}[1/6] Checking prerequisites...${NC}"

if ! command -v python3 &>/dev/null; then
  echo -e "${RED}✗ python3 not found. Install Python 3.11+${NC}"; exit 1
fi
echo -e "${GREEN}✔ Python: $(python3 --version)${NC}"

if ! command -v node &>/dev/null; then
  echo -e "${RED}✗ node not found. Install Node.js 18+${NC}"; exit 1
fi
echo -e "${GREEN}✔ Node: $(node --version)${NC}"

if ! command -v adk &>/dev/null; then
  echo -e "${YELLOW}⚠  adk not found. Installing google-adk...${NC}"
  pip install google-adk --quiet
fi
echo -e "${GREEN}✔ ADK: $(adk --version 2>/dev/null || echo 'installed')${NC}"

if [ ! -f ".env" ]; then
  echo -e "${RED}✗ .env file not found. Copy .env.example and fill in your keys:${NC}"
  echo -e "  cp .env.example .env"
  exit 1
fi
echo -e "${GREEN}✔ .env found${NC}"

# ── Load env ─────────────────────────────────────────────────────────────────
export $(grep -v '^#' .env | xargs 2>/dev/null) || true

if [ -z "$GOOGLE_API_KEY" ]; then
  echo -e "${RED}✗ GOOGLE_API_KEY not set in .env${NC}"; exit 1
fi
if [ -z "$MONGODB_URI" ]; then
  echo -e "${RED}✗ MONGODB_URI not set in .env${NC}"; exit 1
fi
echo -e "${GREEN}✔ Environment variables loaded${NC}"

# ── Install Python dependencies ───────────────────────────────────────────────
echo ""
echo -e "${CYAN}[2/6] Installing Python dependencies...${NC}"
pip install -r requirements.txt --quiet
echo -e "${GREEN}✔ Dependencies installed${NC}"

# ── Seed clean data ───────────────────────────────────────────────────────────
echo ""
echo -e "${CYAN}[3/6] Seeding clean Atlas collection...${NC}"
python3 -m demo.setup_demo_collection
echo -e "${GREEN}✔ Clean collection ready${NC}"

# ── Inject schema drift ───────────────────────────────────────────────────────
echo ""
echo -e "${CYAN}[4/6] Injecting schema drift (corrupt documents)...${NC}"
python3 -m demo.inject_schema_drift
echo -e "${YELLOW}⚡ Schema drift injected — SENTINEL is needed!${NC}"

# ── Open dashboard in browser ─────────────────────────────────────────────────
echo ""
echo -e "${CYAN}[5/6] Opening SENTINEL dashboard...${NC}"
DASHBOARD_PATH="$PROJECT_ROOT/ui/index.html"
if command -v open &>/dev/null; then
  open "$DASHBOARD_PATH"
elif command -v xdg-open &>/dev/null; then
  xdg-open "$DASHBOARD_PATH"
elif command -v start &>/dev/null; then
  start "$DASHBOARD_PATH"
fi
echo -e "${GREEN}✔ Dashboard opened${NC}"

# ── Launch ADK Web ────────────────────────────────────────────────────────────
echo ""
echo -e "${CYAN}[6/6] Launching SENTINEL agent via ADK Web...${NC}"
echo ""
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}  ADK Web UI → http://localhost:8000${NC}"
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}  Paste this prompt into the ADK chat:${NC}"
echo ""
echo -e "${BOLD}  Run the full SENTINEL pipeline on the orders collection.${NC}"
echo -e "${BOLD}  Detect schema violations, patch the schema, quarantine${NC}"
echo -e "${BOLD}  bad documents, and generate an incident report.${NC}"
echo ""
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}  Press Ctrl+C to stop the agent when done recording.${NC}"
echo ""

adk web
