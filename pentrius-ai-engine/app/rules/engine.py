"""CDE Phase 1 rule engine — DROP > KEEP > BORDERLINE precedence.

pentrius-ai-engine/app/rules/engine.py:141-167
"""
import re
from dataclasses import dataclass
from typing import Optional, Tuple

from pentrius_ai_engine.app.models.enums import OutputRouting


@dataclass
class CommandEnvelope:
    tool: str
    command_raw: str
    stdout_preview: str


HIGH_VALUE_TOOLS = frozenset({
    "nmap", "sqlmap", "metasploit", "msfconsole", "nuclei",
    "burpsuite", "masscan", "gobuster", "hashcat", "hydra",
    "john", "ffuf", "nikto", "wpscan", "dirb",
})

CRITICAL_PATTERNS = [
    re.compile(r"CVE-\d{4}-\d+"),
    re.compile(r"password\s*:"),
    re.compile(r"token\s*:"),
    re.compile(r"RSA PRIVATE"),
    re.compile(r"BEGIN CERTIFICATE"),
    re.compile(r"root shell"),
]

DROP_COMMANDS = frozenset({"cd", "ls", "pwd", "clear", "echo", "cat", "whoami"})


class RuleEngine:
    """Evaluates command envelopes against deterministic rules."""

    @staticmethod
    def check_drop_rules(envelope: CommandEnvelope) -> Tuple[bool, Optional[str]]:
        if envelope.tool in DROP_COMMANDS:
            return True, f"builtin shell command: {envelope.tool}"
        if len(envelope.stdout_preview) < 10:
            return True, "output too short"
        return False, None

    @staticmethod
    def check_keep_rules(envelope: CommandEnvelope) -> Tuple[bool, Optional[str]]:
        if envelope.tool in HIGH_VALUE_TOOLS:
            return True, f"high-value tool: {envelope.tool}"
        for pattern in CRITICAL_PATTERNS:
            if pattern.search(envelope.stdout_preview):
                return True, f"critical pattern match: {pattern.pattern}"
        return False, None

    @staticmethod
    def evaluate(envelope: CommandEnvelope) -> Tuple[OutputRouting, Optional[str]]:
        # 1. DROP rules first (filter out noise)
        should_drop, drop_reason = RuleEngine.check_drop_rules(envelope)
        if should_drop:
            return OutputRouting.DROP, drop_reason

        # 2. KEEP rules (identify high value)
        should_keep, keep_reason = RuleEngine.check_keep_rules(envelope)
        if should_keep:
            return OutputRouting.KEEP, keep_reason

        # 3. Default to BORDERLINE for LLM review
        return OutputRouting.BORDERLINE, "No strong signals, needs LLM review"
