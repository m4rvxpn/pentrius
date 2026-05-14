"""TC-04: Rule engine classification tests.

tests/unit/test_rule_engine.py
"""
from pentrius_ai_engine.app.rules.engine import RuleEngine, CommandEnvelope
from pentrius_ai_engine.app.models.enums import OutputRouting


def test_nmap_classified_as_keep():
    env = CommandEnvelope(
        tool="nmap", command_raw="nmap -sV -p 1-65535 10.0.0.1",
        stdout_preview="PORT  STATE  SERVICE\n22/tcp open ssh\n80/tcp open http"
    )
    routing, reason = RuleEngine.evaluate(env)
    assert routing == OutputRouting.KEEP


def test_echo_classified_as_drop():
    env = CommandEnvelope(
        tool="echo", command_raw="echo hello world",
        stdout_preview="hello world"
    )
    routing, _ = RuleEngine.evaluate(env)
    assert routing == OutputRouting.DROP


def test_cve_pattern_triggers_keep():
    env = CommandEnvelope(
        tool="curl", command_raw="curl -s http://target/check",
        stdout_preview="CVE-2023-44487 confirmed on target, CVSS 7.5"
    )
    routing, _ = RuleEngine.evaluate(env)
    assert routing == OutputRouting.KEEP
