# AQ AI Agent (FastAPI + MCP SSE + Aquarium API)

This project demonstrates how to integrate an Aquarium CRM SOAP API (via the `crm-aq` package) into a Model Context Protocol (MCP) server using FastAPI and Server-Sent Events (SSE), and provides a FastAgent client for interactive usage. Aquarium is a CRM system with a SOAP API, and this example exposes its operations as MCP tools that can be called programmatically.

## Project Structure

```bash
.
├── README.md                     # Project documentation
├── agent.py                      # FastAgent client entrypoint
├── fastagent.config.yaml         # FastAgent configuration (agent name, servers)
├── fastagent.secrets.yaml        # Secret keys (e.g., OpenAI API key)
├── pyproject.toml                # Poetry project configuration
├── requirements.txt              # Pip dependencies (alternative to Poetry)
├── src/
│   ├── main.py                   # FastAPI application setup, SSE transport mount
│   ├── routes.py                 # General HTTP endpoints: `/`, `/about`, `/status`
│   ├── aq_mcp_server.py          # FastMCP server, Aquarium tool definitions, HTTP wrappers
│   └── config/
│       └── settings.py           # Environment-based application settings
├── tests/                        # Unit tests for Aquarium client and MCP tools
└── uv.lock                       # Lockfile for the `uv` tool (optional)
```

## Prerequisites

- Python 3.12 or higher
- Git
- [Poetry](https://python-poetry.org/) (recommended) or pip

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/aq_ai_agent.git
   cd aq_ai_agent
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate    # Linux/macOS
   # .venv\Scripts\activate   # Windows
   ```

3. Install dependencies:

   - Using Poetry:

     ```bash
     poetry install
     ```

   - Or using pip:

     ```bash
     pip install -r requirements.txt
     ```

## Configuration

Copy the provided example and set your environment variables:

```bash
cp fastagent.secrets.yaml.example fastagent.secrets.yaml
# Edit fastagent.secrets.yaml to include your OpenAI API key and other secrets

# Create a .env file in the root (if needed) for server-side settings:
# GROK_URL=https://<your_server_url>
# Additional variables required by crm-aq (AquariumClient):
# AQUARIUM_USERNAME, AQUARIUM_PASSWORD, AQUARIUM_WSDL_URL, etc.
```

## Running the Server

Start the FastAPI MCP server with SSE transport:

```bash
uvicorn src.main:app --reload
```

The server will be available at `http://127.0.0.1:8000`. Key endpoints:

- `GET /` — HTML welcome page
- `GET /about` — Plain text application info
- `GET /status` — JSON server status
- `GET /sse` — SSE endpoint for MCP clients
- `POST /messages` — Internal MCP communication endpoint
- `/openapi.json` — OpenAPI schema for tool integration
- Aquarium-specific endpoints under `/aquarium/*`

## Running the FastAgent Client

With the server running, start the FastAgent interactive client:

```bash
uv run agent.py       # uses `fastagent.config.yaml`
# or
python agent.py
```

You will enter an interactive REPL:

```
default >
```

Invoke Aquarium tools with the `!` prefix, for example:

```bash
!get_customers_by_email email="user@example.com"
!get_cases_by_lead_id lead_id=12345
!get_event_history case_id=67890
```

Responses will stream back via SSE.

## Integrating with ChatGPT

1. Expose your local server (e.g., via ngrok):

   ```bash
   ngrok http 8000
   ```

2. Import the OpenAPI schema in the ChatGPT Custom GPT builder:

   ```
   https://<your_public_url>/openapi.json
   ```

ChatGPT will detect available Aquarium tool endpoints for function calling.

## Testing

Run unit tests with pytest:

```bash
pytest
```

## Author

**Sergey Chernyakov**  
📬 Telegram: [@AIBotsTech](https://t.me/AIBotsTech)

