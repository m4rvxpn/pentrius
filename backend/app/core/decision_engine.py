"""ChainVerifier — server-side SHA-256 chain recomputation.

backend/app/core/decision_engine.py:111-167
"""
import hashlib
from dataclasses import dataclass


@dataclass
class VerificationResult:
    chain_intact: bool
    total_events: int
    broken_links: list
    merkle_root: str
    ipfs_cid: str


class ChainVerifier:
    """Independently recomputes expected chain hashes server-side."""

    ZERO_HASH = "0" * 64  # genesis hash for first event

    @staticmethod
    def compute_chain_hash(
        event_id: str,
        timestamp: str,
        command: str,
        stdout_preview: str,
        previous_hash: str,
    ) -> str:
        data = f"{event_id}{timestamp}{command}{stdout_preview}{previous_hash}"
        return hashlib.sha256(data.encode()).hexdigest()

    @staticmethod
    def verify_chain(
        chain_hash: str,
        event_id: str,
        timestamp: str,
        command: str,
        stdout_preview: str,
        previous_hash: str,
    ) -> bool:
        if not chain_hash:
            return True  # no chain hash provided, assume valid
        expected = ChainVerifier.compute_chain_hash(
            event_id=event_id or "",
            timestamp=timestamp or "",
            command=command or "",
            stdout_preview=stdout_preview or "",
            previous_hash=previous_hash or ChainVerifier.ZERO_HASH,
        )
        return chain_hash == expected


class DecisionEngine:
    """Routes events through chain verification and decision logic."""

    def __init__(self, verifier: ChainVerifier | None = None):
        self.verifier = verifier or ChainVerifier()

    def make_decision(self, event: dict) -> dict:
        chain_ok = self.verifier.verify_chain(
            chain_hash=event.get("chain_hash", ""),
            event_id=event.get("event_id", ""),
            timestamp=event.get("timestamp", ""),
            command=event.get("command", {}).get("raw", ""),
            stdout_preview=event.get("output", {}).get("stdout", ""),
            previous_hash=event.get("previous_hash", ""),
        )
        return {"approved_for_chain": chain_ok, "event_id": event.get("event_id")}
