# SENTINEL — Demo Recording Script

> **Deadline: June 11, 2026 @ 4:00 PM CDT**  
> Target runtime: **3–5 minutes**. Follow the beats below in order.

---

## Before You Hit Record

```bash
# 1. Terminal setup — use a clean, dark terminal (iTerm2 / Windows Terminal)
# 2. Set font size to 16–18pt so text is legible in recording
# 3. Open two terminal tabs: Tab A = agent, Tab B = demo commands
# 4. Open browser at http://localhost:8000 — ADK Web UI
# 5. Open a second browser tab at ui/index.html (file:// or live-server)
# 6. Screen resolution: 1920x1080 or 1440x900
```

---

## BEAT 1 — Setup (off-camera or sped up, ~30s)

```bash
# Clone and install — do this BEFORE recording
git clone https://github.com/mmm-byte/SENTINEL_MD
cd SENTINEL_MD
pip install -r requirements.txt
npm install -g @mongodb-js/mongodb-mcp-server

# Copy your .env
cp .env.example .env
# Fill in: GOOGLE_API_KEY and MONGODB_URI
```

---

## BEAT 2 — Seed clean data (on-camera, 20s)

**Say:** *"First, I seed a clean MongoDB Atlas collection with 3 valid orders."*

```bash
python -m demo.setup_demo_collection
```

**Expected output:**
```
✔ Connected to Atlas cluster: sentinel_demo
✔ Dropped existing orders collection
✔ Inserted 3 clean orders: ORD-00001, ORD-00002, ORD-00003
✔ $jsonSchema validator applied — 5 required fields, amount: double
```

---

## BEAT 3 — Inject schema drift (on-camera, 20s)

**Say:** *"Now I inject two corrupt documents — exactly what happens in real production when a bad deploy goes out."*

```bash
python -m demo.inject_schema_drift
```

**Expected output:**
```
⚡ Injected ORD-99999 — TYPE_MISMATCH: order_id is int, amount missing
⚡ Injected ORD-88888 — TYPE_MISMATCH: amount is string 'free'
⚠  Collection now has 2 schema-violating documents in live orders
```

---

## BEAT 4 — Launch SENTINEL agent (on-camera, 30s)

**Switch to Tab A. Say:** *"I launch SENTINEL — a fully autonomous agent powered by Gemini 2.0 Flash and the MongoDB MCP Server."*

```bash
adk web
```

- Browser auto-opens at **http://localhost:8000**
- Show the ADK Web UI loading
- **Say:** *"This is Google ADK's built-in UI. SENTINEL runs as an autonomous agent — no human in the loop."*

---

## BEAT 5 — Fire the agent prompt (on-camera, THE KEY MOMENT ~60s)

**In the ADK Web UI chat box, type exactly:**

```
Run the full SENTINEL pipeline on the orders collection. Detect schema violations, patch the schema, quarantine bad documents, and generate an incident report.
```

**Press Enter. Switch camera focus to the terminal streaming output.**

**Narrate each step as it appears:**

| When you see... | Say... |
|---|---|
| `[schema_inspector]` firing | *"Step 1 — SENTINEL reads the live $jsonSchema validator from Atlas"* |
| `[payload_validator]` firing | *"Step 2 — It scans every document. Three violations found: two type mismatches, one missing field"* |
| `[schema_patcher]` firing | *"Step 3 — Surgical collMod. Only the violating fields are relaxed. The rest stays strict."* |
| `[quarantine_manager]` firing | *"Step 4 — Bad documents are moved to orders_quarantine with full metadata. Source deleted ONLY after safe copy."* |
| `[incident_reporter]` firing | *"Step 5 — Structured incident report generated. Status: CONTAINED."* |

---

## BEAT 6 — Show the incident report (on-camera, 20s)

**Scroll the ADK response to show the final JSON:**

```json
{
  "status": "CONTAINED",
  "violations_found": 3,
  "docs_quarantined": 2,
  "pipeline_seconds": 7,
  "data_loss": false
}
```

**Say:** *"Seven seconds. Zero data loss. Zero human intervention. Live traffic never interrupted."*

---

## BEAT 7 — Show the dashboard (on-camera, 30s)

**Switch to the `ui/index.html` browser tab.**

- Point at the **KPI cards**: 3 violations, 7s, 2/2 quarantined, 0% traffic impact
- Point at the **violations table**: real ORD-99999 and ORD-88888 data
- Point at the **quarantine JSON**: `_sentinel_metadata` with remediation hints
- Point at the **pipeline timing bar chart**

**Say:** *"This dashboard shows the full picture — every number here came from a real run against a live Atlas M0 cluster."*

---

## BEAT 8 — Close strong (on-camera, 20s)

**Say:**

> *"SENTINEL is a production-ready autonomous agent built on Google ADK, Gemini 2.0 Flash, and the MongoDB MCP Server. It turns hours of manual schema debugging into a 7-second fully automated pipeline — with zero data loss and zero traffic impact. Thank you."*

---

## Recording Tips

- **Use OBS or Loom** — record at 1080p, 30fps
- **Mute notifications** before recording (Do Not Disturb mode)
- **Terminal**: dark background, white/green text, font size 16+
- **Keep cursor visible** — move it slowly to guide the viewer's eye
- **Don't skip the quarantine terminal output** — it's the most impressive visual moment
- If the agent is slow, narrate while it runs: *"Gemini is reasoning through the pipeline steps…"*
- Trim the dead air in post — keep it under 5 minutes total
