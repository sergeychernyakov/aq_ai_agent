import inspect

# Importing agent will use the FakeFastAgent stub from conftest
import agent

def test_fast_agent_instance():
    # The stubbed FastAgent should be assigned to `fast`
    assert hasattr(agent, "fast"), "Module should have `fast` attribute"
    assert agent.fast.name == "aquarium-agent"

def test_main_is_coroutine_function():
    # The main function should be an async coroutine function
    assert inspect.iscoroutinefunction(agent.main), "main should be an async function"