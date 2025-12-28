import textwrap

from {{ cookiecutter.project_slug }}.config.config_loader import ConfigLoader


def test_mcp_config_loader_filters_inactive(tmp_path, monkeypatch):
    config_file = tmp_path / "mcp.yaml"
    config_file.write_text(
        textwrap.dedent(
            """
            gateways:
              - name: local
                host: localhost
                port: 9000
                active: true
                credentials:
                  api_key: "${LOCAL_KEY}"
                tools:
                  - name: search_docs
                    resource: docs.search
                    description: Search docs
                    active: true
                  - name: disabled_tool
                    resource: docs.disabled
                    description: Disabled
                    active: false
              - name: disabled_gateway
                host: example.com
                port: 1234
                active: false
                tools:
                  - name: not_listed
                    resource: ignore.me
                    active: true
            """
        )
    )

    monkeypatch.setenv("MCP_CONFIG_PATH", str(config_file))
    monkeypatch.setenv("LOCAL_KEY", "resolved-key")

    config = ConfigLoader().load_config()

    # Active connectors are loaded with resolved credentials.
    assert config["mcp_connectors"][0]["credentials"]["api_key"] == "resolved-key"

    # Only active tools and gateways become tool specs.
    active_tool_names = [tool["function"]["name"] for tool in config["mcp_tools"]]
    assert active_tool_names == ["mcp__local__search_docs"]
