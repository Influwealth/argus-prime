import pytest
from deepflex.interface import ArgusDeepFlexInterface, DeepFlexCommand, ArgusReport


@pytest.fixture
def iface():
    return ArgusDeepFlexInterface()


@pytest.fixture
def basic_command():
    return DeepFlexCommand(command_id="cmd-001", capsule="deepagent", payload={"query": "test"})


class TestDeepFlexCommand:
    def test_default_command_type(self):
        cmd = DeepFlexCommand(command_id="x", capsule="deepagent")
        assert cmd.command_type == "execute_capsule"

    def test_default_issued_by(self):
        cmd = DeepFlexCommand(command_id="x", capsule="deepagent")
        assert cmd.issued_by == "deepflex"

    def test_default_priority(self):
        cmd = DeepFlexCommand(command_id="x", capsule="deepagent")
        assert cmd.priority == 0


class TestReceiveCommand:
    def test_returns_argus_report(self, iface, basic_command):
        report = iface.receive_command(basic_command)
        assert isinstance(report, ArgusReport)

    def test_command_id_is_preserved(self, iface, basic_command):
        report = iface.receive_command(basic_command)
        assert report.command_id == "cmd-001"

    def test_capsule_is_preserved(self, iface, basic_command):
        report = iface.receive_command(basic_command)
        assert report.capsule == "deepagent"

    def test_status_is_accepted(self, iface, basic_command):
        report = iface.receive_command(basic_command)
        assert report.status == "accepted"

    def test_result_is_dict(self, iface, basic_command):
        report = iface.receive_command(basic_command)
        assert isinstance(report.result, dict)

    def test_node_id_defaults_to_argus_prime(self, iface, basic_command):
        report = iface.receive_command(basic_command)
        assert report.node_id == "argus-prime"

    def test_timestamp_is_float(self, iface, basic_command):
        report = iface.receive_command(basic_command)
        assert isinstance(report.timestamp, float)

    def test_to_dict_has_required_keys(self, iface, basic_command):
        d = iface.receive_command(basic_command).to_dict()
        assert set(d.keys()) == {"command_id", "capsule", "status", "result", "node_id", "timestamp"}

    def test_multiple_commands_are_logged(self, iface):
        for i in range(3):
            iface.receive_command(DeepFlexCommand(command_id=f"c{i}", capsule="deepagent", payload={}))
        assert iface.report_status()["commands_processed"] == 3


class TestReportStatus:
    def test_returns_dict(self, iface):
        assert isinstance(iface.report_status(), dict)

    def test_role_is_offline_executor(self, iface):
        assert iface.report_status()["role"] == "offline-it-executor"

    def test_supervisor_is_deepflex(self, iface):
        assert iface.report_status()["supervisor"] == "deepflex"

    def test_node_id_is_present(self, iface):
        assert "node_id" in iface.report_status()

    def test_commands_processed_starts_at_zero(self, iface):
        assert iface.report_status()["commands_processed"] == 0

    def test_commands_processed_increments_on_receive(self, iface):
        iface.receive_command(DeepFlexCommand(command_id="c1", capsule="deepagent", payload={}))
        assert iface.report_status()["commands_processed"] == 1
