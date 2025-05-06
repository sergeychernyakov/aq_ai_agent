import asyncio
import pytest
from faker import Faker

import src.aq_mcp_server as server

# Dummy objects for testing _to_dict
class ModelV2:
    def __init__(self, data): self._data = data
    def model_dump(self): return self._data

class ModelV1:
    def __init__(self, data): self._data = data
    def dict(self): return self._data

class BareObj:
    def __init__(self, x, y): self.x = x; self.y = y

class NoDictObj:
    __slots__ = ()

def test_to_dict_with_model_v2():
    data = {"a": 1, "b": 2}
    obj = ModelV2(data)
    result = server._to_dict(obj)
    assert result == data

def test_to_dict_with_model_v1():
    data = {"c": 3}
    obj = ModelV1(data)
    result = server._to_dict(obj)
    assert result == data

def test_to_dict_with_dunder_dict():
    obj = BareObj(5, 6)
    result = server._to_dict(obj)
    assert result == {"x": 5, "y": 6}

def test_to_dict_fallback():
    obj = NoDictObj()
    result = server._to_dict(obj)
    assert result == {"value": obj}

@pytest.fixture
def fake():
    return Faker()

def make_client_method(name, value):
    # Factory for stub methods that ignore args
    return lambda self, *args, **kwargs: value

def test_get_customers_by_email_with_results(monkeypatch, fake):
    # Prepare fake data and objects
    data1 = {"email": fake.email(), "id": fake.random_int()}
    data2 = {"email": fake.email(), "id": fake.random_int()}
    obj1 = ModelV1(data1)
    obj2 = ModelV1(data2)
    client = type("C", (), {"get_customers_by_email": make_client_method("get_customers_by_email", [obj1, obj2])})()
    monkeypatch.setattr(server, "aquarium_client", client)
    result = asyncio.run(server.get_customers_by_email("foo@bar.com"))
    assert isinstance(result, list)
    assert result == [data1, data2]

def test_get_customers_by_email_no_results(monkeypatch):
    client = type("C", (), {"get_customers_by_email": make_client_method("get_customers_by_email", [])})()
    monkeypatch.setattr(server, "aquarium_client", client)
    result = asyncio.run(server.get_customers_by_email("foo@bar.com"))
    assert isinstance(result, str)
    assert "No customers found for email: foo@bar.com" == result

def test_get_cases_by_lead_id(monkeypatch, fake):
    data = {"case_id": fake.random_int()}
    obj = ModelV1(data)
    client = type("C", (), {"get_cases_by_lead_id": make_client_method("get_cases_by_lead_id", [obj])})()
    monkeypatch.setattr(server, "aquarium_client", client)
    result = asyncio.run(server.get_cases_by_lead_id(123))
    assert result == [data]

def test_get_cases_by_lead_id_no(monkeypatch):
    client = type("C", (), {"get_cases_by_lead_id": make_client_method("get_cases_by_lead_id", [])})()
    monkeypatch.setattr(server, "aquarium_client", client)
    result = asyncio.run(server.get_cases_by_lead_id(123))
    assert result == "No cases found for lead_id: 123"

def test_get_first_case_id_by_lead_id(monkeypatch, fake):
    expected = str(fake.random_int())
    client = type("C", (), {"get_first_case_id_by_lead_id": make_client_method("get_first_case_id_by_lead_id", expected)})()
    monkeypatch.setattr(server, "aquarium_client", client)
    result = asyncio.run(server.get_first_case_id_by_lead_id("lead123"))
    assert result == expected

def test_get_first_case_id_by_lead_id_none(monkeypatch):
    client = type("C", (), {"get_first_case_id_by_lead_id": make_client_method("get_first_case_id_by_lead_id", None)})()
    monkeypatch.setattr(server, "aquarium_client", client)
    result = asyncio.run(server.get_first_case_id_by_lead_id("lead123"))
    assert result == "No CaseID found for lead_id: lead123"

def test_get_case_status_by_matter_id(monkeypatch, fake):
    expected = fake.word()
    client = type("C", (), {"get_case_status_by_matter_id": make_client_method("get_case_status_by_matter_id", expected)})()
    monkeypatch.setattr(server, "aquarium_client", client)
    result = asyncio.run(server.get_case_status_by_matter_id(456))
    assert result == expected

def test_get_case_status_by_matter_id_none(monkeypatch):
    client = type("C", (), {"get_case_status_by_matter_id": make_client_method("get_case_status_by_matter_id", None)})()
    monkeypatch.setattr(server, "aquarium_client", client)
    result = asyncio.run(server.get_case_status_by_matter_id(456))
    assert result == "No status found for matter_id: 456"

def test_get_leads_cases_matters_ids_by_customer_id(monkeypatch):
    expected = [{"lead": 1, "case": 2, "matter": 3}]
    client = type("C", (), {"get_leads_cases_matters_ids_by_customer_id": make_client_method("get_leads_cases_matters_ids_by_customer_id", expected)})()
    monkeypatch.setattr(server, "aquarium_client", client)
    result = asyncio.run(server.get_leads_cases_matters_ids_by_customer_id("cust1"))
    assert result == expected

def test_get_leads_cases_matters_ids_by_customer_id_none(monkeypatch):
    client = type("C", (), {"get_leads_cases_matters_ids_by_customer_id": make_client_method("get_leads_cases_matters_ids_by_customer_id", [])})()
    monkeypatch.setattr(server, "aquarium_client", client)
    result = asyncio.run(server.get_leads_cases_matters_ids_by_customer_id("cust1"))
    assert result == "No leads/cases/matters found for customer_id: cust1"

def test_get_detail_values_by_field_ids(monkeypatch, fake):
    data = {"field": fake.random_int()}
    obj = ModelV1(data)
    client = type("C", (), {"get_detail_values_by_field_ids": make_client_method("get_detail_values_by_field_ids", [obj])})()
    monkeypatch.setattr(server, "aquarium_client", client)
    result = asyncio.run(server.get_detail_values_by_field_ids([1, 2], case_id=1, lead_id=2, matter_id=3))
    assert result == [data]

def test_get_detail_values_by_field_ids_none(monkeypatch):
    client = type("C", (), {"get_detail_values_by_field_ids": make_client_method("get_detail_values_by_field_ids", [])})()
    monkeypatch.setattr(server, "aquarium_client", client)
    result = asyncio.run(server.get_detail_values_by_field_ids([1, 2], case_id=None, lead_id=None, matter_id=None))
    assert result == "No detail field values found for the provided parameters."

def test_customers_by_email_route(monkeypatch, fake):
    # Stub the tool function
    async def fake_tool(email): return [{"email": email}]
    monkeypatch.setattr(server, "get_customers_by_email", fake_tool)
    result = asyncio.run(server.customers_by_email_route("a@b.com"))
    assert result == [{"email": "a@b.com"}]