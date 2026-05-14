"""Pydantic models for the backend API."""
from pydantic import BaseModel


class CommandBlock(BaseModel):
    raw: str
    tool: str | None = None
    pid: int | None = None
    ppid: int | None = None
    cwd: str | None = None
    user: str | None = None


class OutputBlock(BaseModel):
    stdout: str | None = None
    stderr: str | None = None


class PulseAgentEvent(BaseModel):
    event_id: str
    timestamp: str
    command: CommandBlock | None = None
    output: OutputBlock | None = None
    agent_id: str
    scope_id: str
    chain_hash: str | None = None
    previous_hash: str | None = None
