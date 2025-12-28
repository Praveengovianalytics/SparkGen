from {{ cookiecutter.project_slug }}.connectors.mcp_client import MCPClient, _safe_eval_math


def test_demo_calculator_eval():
    client = MCPClient()
    result = client.invoke("demo.calculator", {"expression": "1 + 2 * 3"})
    assert result["status"] == "ok"
    assert result["result"] == 7


def test_demo_datetime_returns_iso():
    client = MCPClient()
    result = client.invoke("demo.datetime")
    assert result["status"] == "ok"
    assert result["utc_iso"].endswith("+00:00")


def test_demo_terminal_allowlist():
    client = MCPClient()
    result = client.invoke("demo.local_terminal", {"command": "echo hello"})
    assert result["status"] == "ok"
    assert "hello" in result["stdout"]

    blocked = client.invoke("demo.local_terminal", {"command": "rm -rf /"})
    assert blocked["status"] == "error"
    assert "allowed" in blocked["error"]


def test_safe_eval_rejects_unsupported_ops():
    try:
        _safe_eval_math("__import__('os').system('echo hi')")
    except ValueError:
        assert True
    else:
        raise AssertionError("Unsafe expression should be rejected")
