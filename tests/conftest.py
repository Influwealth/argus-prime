import pytest


@pytest.fixture
def capsule_dir(tmp_path):
    """A temporary directory pre-populated with sample capsule YAML files."""
    (tmp_path / "wealthbridge.yaml").write_text("name: wealthbridge")
    (tmp_path / "mindmax.yaml").write_text("name: mindmax")
    (tmp_path / "deepagent.yaml").write_text("name: deepagent")
    return tmp_path
