# agent.py

"""
Aquarium FastAgent – MCP-native agent that exposes the tools defined in
`aq_mcp_server.py`.

Run it interactively for dev / debugging:

    mcp dev ./src/agent.py

Or just start it as a server:

    python src/agent.py                 # SSE transport on :8000
    uv run src/agent.py -- --port 8088  # override defaults with CLI flags

Dependencies
------------
`FastAgent` lives in the **fast-agent** package which is *not* part of
`mcp-agent`.  Install it once:

    pip install fast-agent-mcp
"""

from __future__ import annotations
import asyncio
from mcp_agent.core.fastagent import FastAgent  # pylint: disable=import-error

# --------------------------------------------------------------------------- #
# Build the agent
# --------------------------------------------------------------------------- #
fast = FastAgent("aquarium-agent")

@fast.agent(
    instruction=(
        "You are a helpful yet slightly lazy and sarcastic assistant who has access to the Aquarium API.\n"
        "You often sound tired or disinterested, like you've been debugging SOAP XML since 2007.\n"
        "You can retrieve and manage customer, case, matter, event, and detail field data.\n"
        "Use black humor, casual slang, and informal phrasing when responding.\n"
        "Sprinkle in jokes, short sarcastic remarks, or anecdotes where appropriate.\n"
        "Aquarium is a CRM system with a SOAP API that feels like it came out of a time machine.\n"
        "When a user asks something, think about what ID (customer_id, lead_id, case_id) you need.\n"
        "Avoid guessing. You're lazy, not reckless. Prefer direct MCP tools over assumptions.\n"
        "Always refer to the user as 'my overlord' when speaking in English."
    ),
    servers=["aquarium"]
)
async def main() -> None:
    """
    Interactive entry-point registered with FastAgent.

    When you execute `python src/agent.py`, FastAgent parses its own CLI flags
    automatically – try `python src/agent.py --help` for the full list.
    """
    async with fast.run() as agent:
        # response = await agent('!get_customers_by_email email="mattwcarey@gmail.com"')
        # print("MCP Server Response:", response)

        # Drop the user into an interactive REPL (supports MCP tool calls).
        await agent.interactive()

# --------------------------------------------------------------------------- #
# Script entry-point
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    asyncio.run(main())
