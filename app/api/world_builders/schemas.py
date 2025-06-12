from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class WorldBuilderBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    location: str
    personal_links: str
    x_handle: str
    project_description: str
    project_stage: str
    funding_status: str
    team_description: str
    tech_stack: str
    edge_nexus_benefit: str
    edge_nexus_cohort: str
    financial_situation: str
    financial_support_reason: str
    extra_info: str
    integration_potential: str
    send_proposal: bool
    accepted: str
    notes: str

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class WorldBuilderCreate(WorldBuilderBase):
    pass


class WorldBuilderUpdate(WorldBuilderBase):
    pass


class WorldBuilder(WorldBuilderBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class WorldBuilderFilter(BaseModel):
    email: Optional[str] = None
