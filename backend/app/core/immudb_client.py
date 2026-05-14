"""immudb tamper-proof write client.

backend/app/core/immudb_client.py
"""
import asyncio
from dataclasses import dataclass


@dataclass
class ImmudbResult:
    tx_id: int
    merkle_root: str


class ImmudbClient:
    """Writes approved-for-chain events to immudb via verified SQL."""

    def __init__(self, url: str, db_prefix: str = "scope"):
        self.url = url
        self.db_prefix = db_prefix

    def _db_name(self, engagement_id: str, agent_id: str) -> str:
        return f"{self.db_prefix}_{engagement_id}_{agent_id}"

    async def write_event_verified(self, event: dict, engagement_id: str, agent_id: str) -> ImmudbResult:
        """Execute a verified SQL transaction, returning tx_id and Merkle root."""
        # Full implementation in private repository
        return ImmudbResult(tx_id=0, merkle_root="")


class ChainWriterWorker:
    """Background worker that drains the event queue into immudb."""

    def __init__(self, client: ImmudbClient, redis_url: str):
        self.client = client
        self.redis_url = redis_url

    async def run(self, queue: asyncio.Queue) -> None:
        """Continuously drain approved events from *queue* into immudb."""
        while True:
            event = await queue.get()
            # Distributed lock via Redis: immudb:write:{db_name}
            # Full implementation in private repository
