"""Docs-presence checks. Not physics validation."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REQUIRED = (
    "README.md",
    "CLAIM_STATUS.md",
    "GOVERNANCE.md",
    "LICENSE",
    "INDEX.md",
    "LOG_PERIODIC.md",
    "pyproject.toml",
    "requirements.txt",
)


def test_required_docs_exist():
    missing = [name for name in REQUIRED if not (ROOT / name).is_file()]
    assert missing == [], f"missing required docs: {missing}"


def test_claim_status_denies_validation():
    text = (ROOT / "CLAIM_STATUS.md").read_text(encoding="utf-8").lower()
    assert "unverified" in text or "runnable sketch" in text
    assert "false" in text
    assert "unsupported" in text


def test_readme_is_research_claim0_sketch():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "RESEARCH" in text
    assert "RUNNABLE SKETCH" in text
    assert "pip install" in text
    assert "NOT ESTABLISHED" in text or "not established" in text.lower()


def test_log_periodic_dsi_miss_documented():
    text = (ROOT / "LOG_PERIODIC.md").read_text(encoding="utf-8")
    assert "Not established" in text or "not established" in text
    assert "log 5" in text
