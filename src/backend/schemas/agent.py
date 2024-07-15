import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AgentBase(BaseModel):
    user_id: str
    organization_id: Optional[str] = None


# Agent Tool Metadata
class AgentToolMetadata(AgentBase):
    id: str
    tool_name: str
    artifacts: list[dict]


class AgentToolMetadataPublic(AgentToolMetadata):
    user_id: Optional[str] = Field(exclude=True)

    class Config:
        from_attributes = True


class CreateAgentToolMetadata(BaseModel):
    id: Optional[str] = None
    tool_name: str
    artifacts: list[dict]


class UpdateAgentToolMetadata(BaseModel):
    id: Optional[str] = None
    tool_name: Optional[str] = None
    artifacts: Optional[list[dict]] = None


class DeleteAgentToolMetadata(BaseModel):
    pass


# Agent
class Agent(AgentBase):
    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    version: int
    name: str
    description: Optional[str]
    preamble: Optional[str]
    temperature: float
    tools: list[str]
    tools_metadata: list[AgentToolMetadata]

    model: str
    deployment: str

    class Config:
        from_attributes = True
        use_enum_values = True


class AgentPublic(Agent):
    user_id: Optional[str] = Field(exclude=True)
    organization_id: Optional[str] = Field(exclude=True)
    tools_metadata: Optional[list[AgentToolMetadataPublic]] = None


class CreateAgent(BaseModel):
    name: str
    version: Optional[int] = None
    description: Optional[str] = None
    preamble: Optional[str] = None
    temperature: Optional[float] = None
    model: str
    deployment: str
    tools: Optional[list[str]] = None
    tools_metadata: Optional[list[CreateAgentToolMetadata]] = None

    class Config:
        from_attributes = True
        use_enum_values = True


class ListAgentsResponse(BaseModel):
    agents: list[Agent]


class UpdateAgent(BaseModel):
    name: Optional[str] = None
    version: Optional[int] = None
    description: Optional[str] = None
    preamble: Optional[str] = None
    temperature: Optional[float] = None
    model: Optional[str] = None
    deployment: Optional[str] = None
    tools: Optional[list[str]] = None
    tools_metadata: Optional[list[CreateAgentToolMetadata]] = None

    class Config:
        from_attributes = True
        use_enum_values = True


class DeleteAgent(BaseModel):
    pass
