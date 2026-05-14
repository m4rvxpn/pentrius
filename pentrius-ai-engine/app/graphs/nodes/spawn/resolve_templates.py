"""Template resolution for SpawnGraph — scope-aware placeholder substitution.

pentrius-ai-engine/app/graphs/nodes/spawn/resolve_templates.py:65-113
"""
import re
from typing import Any, Dict


def _build_resolution_context(parent_finding: Dict[str, Any]) -> Dict[str, str]:
    context = {
        "target":   parent_finding.get("target", "unknown"),
        "port":     str(parent_finding.get("port", "")),
        "service":  parent_finding.get("service", ""),
        "protocol": parent_finding.get("protocol", "tcp"),
    }
    target, port = context["target"], context["port"]
    if target and target != "unknown":
        if port and port not in ["80", "443", ""]:
            context["url"] = f"{context['protocol']}://{target}:{port}"
        elif port == "443":
            context["url"] = f"https://{target}"
        else:
            context["url"] = f"http://{target}"
    context["credential"] = "{credential}"  # never auto-resolved
    return context


def _resolve_template(template: str, context: Dict[str, str]) -> str:
    result = template
    for key, value in context.items():
        result = result.replace("{" + key + "}", value)
    result = re.sub(r'\{[a-zA-Z_]+\}', '', result)  # remove unresolved
    return re.sub(r'\s+', ' ', result).strip()
