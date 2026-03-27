import pytest
from introspect import CapsuleIntrospector


class TestListCapsules:
    def test_returns_only_yaml_files(self, capsule_dir):
        (capsule_dir / "README.md").write_text("docs")
        (capsule_dir / "notes.txt").write_text("notes")
        introspector = CapsuleIntrospector(base_path=str(capsule_dir))
        result = introspector.list_capsules()
        assert all(f.endswith(".yaml") for f in result)

    def test_returns_all_yaml_files(self, capsule_dir):
        introspector = CapsuleIntrospector(base_path=str(capsule_dir))
        result = introspector.list_capsules()
        assert set(result) == {"wealthbridge.yaml", "mindmax.yaml", "deepagent.yaml"}

    def test_returns_empty_list_for_empty_directory(self, tmp_path):
        introspector = CapsuleIntrospector(base_path=str(tmp_path))
        assert introspector.list_capsules() == []

    def test_excludes_yaml_look_alike_extensions(self, tmp_path):
        (tmp_path / "capsule.yaml.bak").write_text("")
        (tmp_path / "real.yaml").write_text("")
        introspector = CapsuleIntrospector(base_path=str(tmp_path))
        assert introspector.list_capsules() == ["real.yaml"]

    def test_missing_base_path_raises(self):
        introspector = CapsuleIntrospector(base_path="/nonexistent/path/xyz")
        with pytest.raises(FileNotFoundError):
            introspector.list_capsules()


class TestCheckHealth:
    def test_returns_true_for_existing_capsule(self, capsule_dir):
        introspector = CapsuleIntrospector(base_path=str(capsule_dir))
        assert introspector.check_health("wealthbridge") is True

    def test_returns_false_for_missing_capsule(self, capsule_dir):
        introspector = CapsuleIntrospector(base_path=str(capsule_dir))
        assert introspector.check_health("nonexistent") is False

    def test_returns_false_for_misspelled_capsule(self, capsule_dir):
        introspector = CapsuleIntrospector(base_path=str(capsule_dir))
        assert introspector.check_health("wealthbridg") is False

    def test_check_health_is_case_sensitive(self, capsule_dir):
        introspector = CapsuleIntrospector(base_path=str(capsule_dir))
        assert introspector.check_health("Wealthbridge") is False
        assert introspector.check_health("wealthbridge") is True

    def test_returns_false_when_base_path_missing(self):
        introspector = CapsuleIntrospector(base_path="/nonexistent/path/xyz")
        assert introspector.check_health("wealthbridge") is False

    def test_all_fixture_capsules_are_healthy(self, capsule_dir):
        introspector = CapsuleIntrospector(base_path=str(capsule_dir))
        for name in ("wealthbridge", "mindmax", "deepagent"):
            assert introspector.check_health(name) is True
