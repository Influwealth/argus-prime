import pytest
from mcp.loader import load_mcp_config, get_client


class TestLoadMcpConfig:
    def test_returns_dict(self):
        config = load_mcp_config()
        assert isinstance(config, dict)

    def test_has_version(self):
        config = load_mcp_config()
        assert "version" in config

    def test_has_registry(self):
        config = load_mcp_config()
        assert "registry" in config
        assert isinstance(config["registry"], list)

    def test_registry_has_ten_entries(self):
        config = load_mcp_config()
        assert len(config["registry"]) == 10

    def test_each_entry_has_name_and_enabled(self):
        config = load_mcp_config()
        for entry in config["registry"]:
            assert "name" in entry
            assert "enabled" in entry

    def test_endpoint_field_is_resolved(self):
        config = load_mcp_config()
        for entry in config["registry"]:
            assert "endpoint" in entry
            assert isinstance(entry["endpoint"], str)


class TestGetClient:
    @pytest.mark.parametrize("name", [
        "robinhood", "coinbase", "telegram", "shopify", "web_llm",
        "turbo_quantum", "cbi_insights", "x402", "whisper", "openjarvis",
    ])
    def test_get_client_returns_instance(self, name):
        client = get_client(name)
        assert client is not None

    def test_get_client_unknown_raises_value_error(self):
        with pytest.raises(ValueError, match="Unknown MCP client"):
            get_client("nonexistent_mcp")

    def test_robinhood_has_get_portfolio(self):
        client = get_client("robinhood")
        assert hasattr(client, "get_portfolio")

    def test_web_llm_has_infer(self):
        client = get_client("web_llm")
        assert hasattr(client, "infer")

    def test_whisper_has_transcribe(self):
        client = get_client("whisper")
        assert hasattr(client, "transcribe")
