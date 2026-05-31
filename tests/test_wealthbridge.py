import pytest
from agents.argus.wealthbridge import WealthBridgeCapsule


@pytest.fixture
def wb():
    return WealthBridgeCapsule()


@pytest.fixture
def sample_client():
    return {"name": "Alice", "income": 45000, "zip": "90210"}


class TestCreditAnalysis:
    def test_returns_dict(self, wb, sample_client):
        result = wb.credit_analysis(sample_client)
        assert isinstance(result, dict)

    def test_trigger_field(self, wb, sample_client):
        result = wb.credit_analysis(sample_client)
        assert result["trigger"] == "credit_analysis"

    def test_capsule_field(self, wb, sample_client):
        result = wb.credit_analysis(sample_client)
        assert result["capsule"] == "wealthbridge"

    def test_client_echoed(self, wb, sample_client):
        result = wb.credit_analysis(sample_client)
        assert result["client"] == sample_client


class TestGrantMatch:
    def test_returns_dict(self, wb, sample_client):
        result = wb.grant_match(sample_client)
        assert isinstance(result, dict)

    def test_trigger_field(self, wb, sample_client):
        result = wb.grant_match(sample_client)
        assert result["trigger"] == "grant_match"

    def test_matches_is_list(self, wb, sample_client):
        result = wb.grant_match(sample_client)
        assert isinstance(result["matches"], list)


class TestHousingAid:
    def test_returns_dict(self, wb, sample_client):
        result = wb.housing_aid(sample_client)
        assert isinstance(result, dict)

    def test_trigger_field(self, wb, sample_client):
        result = wb.housing_aid(sample_client)
        assert result["trigger"] == "housing_aid"

    def test_programs_is_list(self, wb, sample_client):
        result = wb.housing_aid(sample_client)
        assert isinstance(result["programs"], list)


class TestGenerateInvoice:
    def test_returns_dict(self, wb, sample_client):
        items = [{"description": "Consulting", "amount": 500.0}]
        result = wb.generate_invoice(sample_client, items)
        assert isinstance(result, dict)

    def test_subtotal_is_sum_of_items(self, wb, sample_client):
        items = [{"amount": 100.0}, {"amount": 250.0}]
        result = wb.generate_invoice(sample_client, items)
        assert result["subtotal"] == 350.0

    def test_total_equals_subtotal_at_zero_tax(self, wb, sample_client):
        items = [{"amount": 200.0}]
        result = wb.generate_invoice(sample_client, items)
        assert result["total"] == result["subtotal"]

    def test_empty_line_items(self, wb, sample_client):
        result = wb.generate_invoice(sample_client, [])
        assert result["subtotal"] == 0.0
        assert result["total"] == 0.0


class TestCashflowProjection:
    def test_returns_dict(self, wb, sample_client):
        result = wb.cashflow_projection(sample_client)
        assert isinstance(result, dict)

    def test_default_months_is_12(self, wb, sample_client):
        result = wb.cashflow_projection(sample_client)
        assert result["months"] == 12

    def test_projected_monthly_length_matches_months(self, wb, sample_client):
        result = wb.cashflow_projection(sample_client, months=6)
        assert len(result["projected_monthly"]) == 6

    def test_capsule_field(self, wb, sample_client):
        result = wb.cashflow_projection(sample_client)
        assert result["capsule"] == "wealthbridge"
