import sys
import pytest
from agents.deepagent.router import route_request, main


class TestRouteRequest:
    def test_prints_destination_in_output(self, capsys):
        route_request("mindmax")
        captured = capsys.readouterr()
        assert "mindmax" in captured.out

    def test_prints_routing_message(self, capsys):
        route_request("wealthbridge")
        captured = capsys.readouterr()
        assert "Routing request to wealthbridge" in captured.out

    def test_accepts_arbitrary_destination(self, capsys):
        route_request("some-custom-agent")
        captured = capsys.readouterr()
        assert "some-custom-agent" in captured.out

    def test_returns_none(self):
        result = route_request("mindmax")
        assert result is None


class TestMainCLI:
    def test_route_command_calls_route_request(self, monkeypatch, capsys):
        monkeypatch.setattr(sys, "argv", ["router", "route", "mindmax"])
        main()
        captured = capsys.readouterr()
        assert "mindmax" in captured.out

    def test_route_command_with_different_destination(self, monkeypatch, capsys):
        monkeypatch.setattr(sys, "argv", ["router", "route", "wealthbridge"])
        main()
        captured = capsys.readouterr()
        assert "wealthbridge" in captured.out

    def test_no_command_prints_help(self, monkeypatch, capsys):
        monkeypatch.setattr(sys, "argv", ["router"])
        main()
        captured = capsys.readouterr()
        # argparse prints usage/help to stdout or stderr when no subcommand given
        assert len(captured.out) > 0 or len(captured.err) > 0

    def test_invalid_command_exits_with_error(self, monkeypatch):
        monkeypatch.setattr(sys, "argv", ["router", "unknowncmd"])
        with pytest.raises(SystemExit):
            main()
