import sys
import types

# Stub out external dependencies for testing
# ----- mcp.server.fastmcp -----
mcp = types.ModuleType("mcp")
mcp.server = types.ModuleType("mcp.server")
fastmcp_mod = types.ModuleType("mcp.server.fastmcp")
class FakeFastMCP:
    def __init__(self, name): self.name = name
    def tool(self):
        def decorator(func): return func
        return decorator
fastmcp_mod.FastMCP = FakeFastMCP
sys.modules["mcp"] = mcp
sys.modules["mcp.server"] = mcp.server
sys.modules["mcp.server.fastmcp"] = fastmcp_mod

# ----- mcp.server.sse -----
sse_mod = types.ModuleType("mcp.server.sse")
class FakeSseServerTransport:
    def __init__(self, path): self.path = path
    def handle_post_message(self, request=None): return None
    def connect_sse(self, scope, receive, send):
        class ContextManager:
            async def __aenter__(self): return (None, None)
            async def __aexit__(self, exc_type, exc, tb): pass
        return ContextManager()
sse_mod.SseServerTransport = FakeSseServerTransport
sys.modules["mcp.server.sse"] = sse_mod

# ----- mcp_agent.core.fastagent -----
fastagent_parent = types.ModuleType("mcp_agent")
fastagent_core = types.ModuleType("mcp_agent.core")
fastagent_mod = types.ModuleType("mcp_agent.core.fastagent")
class FakeFastAgent:
    def __init__(self, name): self.name = name
    def agent(self, instruction, servers):
        def decorator(func): return func
        return decorator
    def run(self): return self
    async def __aenter__(self): return self
    async def __aexit__(self, exc_type, exc, tb): pass
    async def interactive(self): pass
fastagent_mod.FastAgent = FakeFastAgent
sys.modules["mcp_agent"] = fastagent_parent
sys.modules["mcp_agent.core"] = fastagent_core
sys.modules["mcp_agent.core.fastagent"] = fastagent_mod

# ----- aquarium.helpers.logger -----
helpers_parent = types.ModuleType("aquarium")
helpers_clients = types.ModuleType("aquarium.helpers")
logger_mod = types.ModuleType("aquarium.helpers.logger")
def get_logger(name):
    class FakeLogger:
        def debug(self, *args, **kwargs): pass
        def info(self, *args, **kwargs): pass
    return FakeLogger()
logger_mod.get_logger = get_logger
sys.modules["aquarium.helpers.logger"] = logger_mod

# ----- aquarium.clients.aquarium_client -----
clients_parent = types.ModuleType("aquarium.clients")
client_mod = types.ModuleType("aquarium.clients.aquarium_client")
class AquariumClient:
    pass
client_mod.AquariumClient = AquariumClient
sys.modules["aquarium.clients"] = clients_parent
sys.modules["aquarium.clients.aquarium_client"] = client_mod

# Ensure parent modules exist
sys.modules.setdefault("aquarium", types.ModuleType("aquarium"))
sys.modules.setdefault("aquarium.helpers", types.ModuleType("aquarium.helpers"))
sys.modules.setdefault("aquarium.clients", clients_parent)
# Stub dotenv to avoid dependency in tests
dotenv_mod = types.ModuleType("dotenv")
def load_dotenv(path=None):
    return None
dotenv_mod.load_dotenv = load_dotenv
sys.modules["dotenv"] = dotenv_mod
# Stub faker to avoid external dependency in tests
faker_mod = types.ModuleType("faker")
class Faker:
    def __init__(self): pass
    def email(self): return "test@example.com"
    def random_int(self, min=0, max=1000):
        import random
        return random.randint(min, max)
    def word(self): return "word"
faker_mod.Faker = Faker
sys.modules["faker"] = faker_mod