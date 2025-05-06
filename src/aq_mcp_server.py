# src/aq_mcp_server.py

from typing import Any, Optional, List, Dict
import inspect
from fastapi import APIRouter, Query
from mcp.server.fastmcp import FastMCP
from aquarium.helpers.logger import get_logger
from aquarium.clients.aquarium_client import AquariumClient

# Initialize FastMCP server
mcp = FastMCP("aquarium")

router = APIRouter(prefix="/aquarium", tags=["Aquarium"])
aquarium_client = AquariumClient()


logger = get_logger(__name__)

# Helper to convert arbitrary Aquarium model instances to plain dictionaries
def _to_dict(obj: Any) -> dict[str, Any]:
    """Convert any Aquarium SDK / Pydantic object to a plain `dict`.

    Falls back gracefully for dataclasses and bare objects.
    """
    if hasattr(obj, "model_dump"):  # Pydantic v2
        return obj.model_dump()  # type: ignore[attr-defined]
    if hasattr(obj, "dict"):  # Pydantic v1
        return obj.dict()  # type: ignore[attr-defined]
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    return {"value": obj}

# --- Inserted get_customers_by_email tool ---
@mcp.tool()
async def get_customers_by_email(email: str) -> list[dict[str, Any]] | str:
    """Retrieve Aquarium customers by their email address.

    Args:
        email (str): Email address to search for.

    Returns:
        list[dict[str, Any]] | str: A list of customer dictionaries if found, otherwise a message string.
    """
    customers = aquarium_client.get_customers_by_email(email)

    if not customers:
        return f"No customers found for email: {email}"
    logger.debug(f"Retrieved customers for {email}: {customers}")
    return [_to_dict(cust) for cust in customers]


# --------------------------------------------------------------------------- #
# Cases by Lead ID
# --------------------------------------------------------------------------- #
@mcp.tool()
async def get_cases_by_lead_id(lead_id: int) -> list[dict[str, Any]] | str:
    """Return all cases for the given LeadID."""
    cases = aquarium_client.get_cases_by_lead_id(lead_id)
    if not cases:
        return f"No cases found for lead_id: {lead_id}"
    logger.debug("Retrieved %s cases for lead_id=%s", len(cases), lead_id)
    return [_to_dict(case) for case in cases]

@mcp.tool()
async def get_first_case_by_lead_id(lead_id: int) -> dict[str, Any] | str:
    """Return the first case (if any) for the given LeadID."""
    case_obj = aquarium_client.get_first_case_by_lead_id(lead_id)
    if not case_obj:
        return f"No cases found for lead_id: {lead_id}"
    logger.debug("Retrieved first case for lead_id=%s: %s", lead_id, case_obj)
    return _to_dict(case_obj)

@mcp.tool()
async def get_first_case_id_by_lead_id(lead_id: str) -> str:
    """Return the first CaseID for the given LeadID."""
    case_id = aquarium_client.get_first_case_id_by_lead_id(lead_id)
    return case_id or f"No CaseID found for lead_id: {lead_id}"

# --------------------------------------------------------------------------- #
# Leads / Cases / Matters by Customer ID
# --------------------------------------------------------------------------- #
@mcp.tool()
async def get_leads_cases_matters_ids_by_customer_id(
        customer_id: str) -> list[dict[str, int]] | str:
    """Return a list of lead/case/matter ID mappings for the customer."""
    ids = aquarium_client.get_leads_cases_matters_ids_by_customer_id(customer_id)
    if not ids:
        return f"No leads/cases/matters found for customer_id: {customer_id}"
    logger.debug("Retrieved %s id rows for customer_id=%s", len(ids), customer_id)
    return ids

# --------------------------------------------------------------------------- #
# Cases by Customer ID
# --------------------------------------------------------------------------- #
@mcp.tool()
async def get_cases_by_customer_id(customer_id: str) -> list[dict[str, Any]] | str:
    """Return all cases for the specified CustomerID."""
    cases = aquarium_client.get_cases_by_customer_id(customer_id)
    if not cases:
        return f"No cases found for customer_id: {customer_id}"
    logger.debug("Retrieved %s cases for customer_id=%s", len(cases), customer_id)
    return [_to_dict(case) for case in cases]

@mcp.tool()
async def get_first_case_by_customer_id(customer_id: str) -> dict[str, Any] | str:
    """Return the first case (if any) for the specified CustomerID."""
    case_obj = aquarium_client.get_first_case_by_customer_id(customer_id)
    if not case_obj:
        return f"No cases found for customer_id: {customer_id}"
    logger.debug("Retrieved first case for customer_id=%s: %s",
                 customer_id, case_obj)
    return _to_dict(case_obj)

# --------------------------------------------------------------------------- #
# Cases by Email
# --------------------------------------------------------------------------- #
@mcp.tool()
async def get_cases_by_email(email: str) -> list[dict[str, Any]] | str:
    """Return all cases associated with the given email."""
    cases = aquarium_client.get_cases_by_email(email)
    if not cases:
        return f"No cases found for email: {email}"
    logger.debug("Retrieved %s cases for email=%s", len(cases), email)
    return [_to_dict(case) for case in cases]

@mcp.tool()
async def get_first_case_by_email(email: str) -> dict[str, Any] | str:
    """Return the first case (if any) associated with the given email."""
    case_obj = aquarium_client.get_first_case_by_email(email)
    if not case_obj:
        return f"No cases found for email: {email}"
    logger.debug("Retrieved first case for email=%s: %s", email, case_obj)
    return _to_dict(case_obj)

# --------------------------------------------------------------------------- #
# Case Status by Matter ID
# --------------------------------------------------------------------------- #
@mcp.tool()
async def get_case_status_by_matter_id(matter_id: int) -> str:
    """Return the StatusName for the specified MatterID."""
    status = aquarium_client.get_case_status_by_matter_id(matter_id)
    return status or f"No status found for matter_id: {matter_id}"

# --------------------------------------------------------------------------- #
# First Matter ID by Lead ID
# --------------------------------------------------------------------------- #
@mcp.tool()
async def get_first_matter_id_by_lead_id(lead_id: str) -> str:
    """Return the first MatterID (if any) for the given LeadID."""
    matter_id = aquarium_client.get_first_matter_id_by_lead_id(lead_id)
    return matter_id or f"No matter_id found for lead_id: {lead_id}"

# --------------------------------------------------------------------------- #
# Customer by Customer ID
# --------------------------------------------------------------------------- #
@mcp.tool()
async def get_customer_by_customer_id(customer_id: int) -> dict[str, Any] | str:
    """Return the customer corresponding to the given CustomerID."""
    customer_obj = aquarium_client.get_customer_by_customer_id(customer_id)
    if not customer_obj:
        return f"No customer found for customer_id: {customer_id}"
    logger.debug("Retrieved customer for customer_id=%s: %s",
                 customer_id, customer_obj)
    return _to_dict(customer_obj)

# --------------------------------------------------------------------------- #
# Event History by Case ID
# --------------------------------------------------------------------------- #
@mcp.tool()
async def get_event_history(case_id: int) -> list[dict[str, Any]] | str:
    """Return the event history for the specified CaseID."""
    events = aquarium_client.get_event_history(case_id)
    if not events:
        return f"No event history found for case_id: {case_id}"
    logger.debug("Retrieved %s events for case_id=%s", len(events), case_id)
    return [_to_dict(event) for event in events]

# --------------------------------------------------------------------------- #
# Detail Field Values
# --------------------------------------------------------------------------- #
@mcp.tool()
async def get_detail_values_by_field_ids(
    field_ids: list[int],
    case_id: int | None = None,
    lead_id: int | None = None,
    matter_id: int | None = None,
) -> list[dict[str, Any]] | str:
    """Return DetailField values for the provided field IDs and context."""
    details = aquarium_client.get_detail_values_by_field_ids(
        field_ids=field_ids,
        case_id=case_id,
        lead_id=lead_id,
        matter_id=matter_id,
    )
    if not details:
        return "No detail field values found for the provided parameters."
    logger.debug(
        "Retrieved %s detail fields for field_ids=%s (case_id=%s, lead_id=%s, matter_id=%s)",
        len(details), field_ids, case_id, lead_id, matter_id,
    )
    return [_to_dict(detail) for detail in details]

# --------------------------------------------------------------------------- #
# HTTP wrappers for Aquarium MCP tools
# --------------------------------------------------------------------------- #

async def _maybe_await(result):
    """Await the result if it's awaitable, otherwise return it directly."""
    if inspect.isawaitable(result):
        return await result
    return result

@router.get(
    "/customers",
    operation_id="get_customers_by_email",
    summary="Get all Aquarium customers that match the given email address",
)
async def customers_by_email_route(email: str):
    """HTTP wrapper that exposes get_customers_by_email as a REST endpoint."""
    return await _maybe_await(get_customers_by_email(email))

@router.get(
    "/cases/by-lead/{lead_id}",
    operation_id="get_cases_by_lead_id",
    summary="Retrieve all cases associated with a given LeadID, including matter details",
)
async def cases_by_lead_route(lead_id: int):
    """Return all cases for the specified LeadID."""
    return await get_cases_by_lead_id(lead_id)

@router.get(
    "/cases/by-lead/{lead_id}/first",
    operation_id="get_first_case_by_lead_id",
    summary="Retrieve the first case found for a given LeadID",
)
async def first_case_by_lead_route(lead_id: int):
    """Return the first case (if any) for the specified LeadID."""
    return await get_first_case_by_lead_id(lead_id)

@router.get(
    "/cases/by-lead/{lead_id}/first-id",
    operation_id="get_first_case_id_by_lead_id",
    summary="Get the first CaseID associated with a given LeadID",
)
async def first_case_id_by_lead_route(lead_id: str):
    """Return the first CaseID for the specified LeadID."""
    return await get_first_case_id_by_lead_id(lead_id)

@router.get(
    "/leads-cases-matters/by-customer/{customer_id}",
    operation_id="get_leads_cases_matters_ids_by_customer_id",
    summary="Get all Lead, Case, and Matter ID mappings for a given CustomerID",
)
async def leads_cases_matters_route(customer_id: str):
    """Return lead/case/matter ID mappings for the specified CustomerID."""
    return await get_leads_cases_matters_ids_by_customer_id(customer_id)

@router.get(
    "/cases/by-customer/{customer_id}",
    operation_id="get_cases_by_customer_id",
    summary="Retrieve all cases for the specified CustomerID, including matter details",
)
async def cases_by_customer_route(customer_id: str):
    """Return all cases for the specified CustomerID."""
    return await get_cases_by_customer_id(customer_id)

@router.get(
    "/cases/by-customer/{customer_id}/first",
    operation_id="get_first_case_by_customer_id",
    summary="Retrieve the first case found for the specified CustomerID",
)
async def first_case_by_customer_route(customer_id: str):
    """Return the first case (if any) for the specified CustomerID."""
    return await get_first_case_by_customer_id(customer_id)

@router.get(
    "/cases/by-email",
    operation_id="get_cases_by_email",
    summary="Get all cases linked to the given email address across all matching customers",
)
async def cases_by_email_route(email: str):
    """Return all cases linked to the specified email address."""
    return await get_cases_by_email(email)

@router.get(
    "/cases/by-email/first",
    operation_id="get_first_case_by_email",
    summary="Retrieve the first case associated with the given email address",
)
async def first_case_by_email_route(email: str):
    """Return the first case (if any) linked to the specified email address."""
    return await get_first_case_by_email(email)

@router.get(
    "/case-status/by-matter/{matter_id}",
    operation_id="get_case_status_by_matter_id",
    summary="Get the current status name of a case by its MatterID",
)
async def case_status_by_matter_route(matter_id: int):
    """Return the StatusName for the specified MatterID."""
    return await get_case_status_by_matter_id(matter_id)

@router.get(
    "/matters/first-by-lead/{lead_id}",
    operation_id="get_first_matter_id_by_lead_id",
    summary="Retrieve the first MatterID associated with a given LeadID",
)
async def first_matter_by_lead_route(lead_id: str):
    """Return the first MatterID (if any) for the specified LeadID."""
    return await get_first_matter_id_by_lead_id(lead_id)

@router.get(
    "/customer/{customer_id}",
    operation_id="get_customer_by_customer_id",
    summary="Retrieve Aquarium customer details for a specific CustomerID",
)
async def customer_by_customer_id_route(customer_id: int):
    """Return the customer corresponding to the specified CustomerID."""
    return await get_customer_by_customer_id(customer_id)

@router.get(
    "/event-history/{case_id}",
    operation_id="get_event_history",
    summary="Get the full event history for a given CaseID",
)
async def event_history_route(case_id: int):
    """Return event history for the specified CaseID."""
    return await get_event_history(case_id)

@router.get(
    "/detail-values",
    operation_id="get_detail_values_by_field_ids",
    summary="Get values for specified detail fields by field IDs and context (case, lead, or matter)",
)
async def detail_values_route(
    field_ids: list[int] = Query(..., description="List of DetailFieldIDs"),
    case_id: int | None = Query(None, description="CaseID context"),
    lead_id: int | None = Query(None, description="LeadID context"),
    matter_id: int | None = Query(None, description="MatterID context"),
):
    """Return detail field values for the provided IDs and context."""
    return await get_detail_values_by_field_ids(
        field_ids=field_ids,
        case_id=case_id,
        lead_id=lead_id,
        matter_id=matter_id,
    )


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="sse")
