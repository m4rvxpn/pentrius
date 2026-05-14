"""TC-01 / TC-02: Hash-chain unit tests.

tests/unit/test_chain_verifier.py
"""
import hashlib
from backend.app.core.decision_engine import ChainVerifier


def test_first_event_uses_zero_hash():
    raw = "e1" + "2025-01-01T00:00:00Z" + "nmap -sV 192.168.1.1" + \
          "PORT STATE SERVICE" + "0" * 64
    expected_hash = hashlib.sha256(raw.encode()).hexdigest()

    result = ChainVerifier.verify_chain(
        chain_hash=expected_hash,
        event_id="e1",
        timestamp="2025-01-01T00:00:00Z",
        command="nmap -sV 192.168.1.1",
        stdout_preview="PORT STATE SERVICE",
        previous_hash=ChainVerifier.ZERO_HASH,
    )
    assert result == True


def test_tampered_stdout_breaks_chain():
    h1 = ChainVerifier.compute_chain_hash(
        "e1", "2025-01-01T00:00:00Z", "nmap", "22/tcp open ssh", "0" * 64
    )
    valid_h2 = ChainVerifier.compute_chain_hash(
        "e2", "2025-01-01T00:01:00Z", "sqlmap", "[*] Found SQLi", h1
    )

    tampered = ChainVerifier.verify_chain(
        chain_hash=valid_h2,
        event_id="e2",
        timestamp="2025-01-01T00:01:00Z",
        command="sqlmap",
        stdout_preview="MODIFIED OUTPUT",  # tampered
        previous_hash=h1,
    )
    assert tampered == False  # chain must break
