"""TC-05: Composite formula correctness (Equation 4).

tests/unit/test_coverage.py
"""


def compute_composite(scores: dict) -> float:
    weights = {"owasp": 0.25, "mitre": 0.30, "ptes": 0.25, "nist": 0.20}
    return sum(scores[fw] * w for fw, w in weights.items())


def test_composite_formula_matches_equation_4():
    scores = {"owasp": 0.912, "mitre": 0.851, "ptes": 0.923, "nist": 0.887}
    expected = (0.25 * 0.912) + (0.30 * 0.851) + (0.25 * 0.923) + (0.20 * 0.887)

    result = compute_composite(scores)
    assert abs(result - expected) < 0.0001
