# AI PM Copilot Frontend

This frontend is a Streamlit demo shell for the AI Product Manager Copilot.

## Run

From the project root:

```powershell
cd C:\Users\VICTUS\OneDrive\Desktop\ai-pm-copilot\ai-product-management-copilot
.\.venv\Scripts\python.exe -m streamlit run frontend\app.py
```

## What’s inside

- `app.py` — page registry, sidebar branding, navigation.
- `requirements.txt` — frontend dependencies.
- `.streamlit/config.toml` — theme settings.
- `pages/` — app pages with dashboard, exploration, prioritization, PRD, roadmap, chat.
- `utils/` — styling, mock data, backend bridge.

## Backend wiring

`utils/backend_bridge.py` exposes `run_chat_turn(message)` for chat support. Replace this demo function with an orchestrator/agent API call.
