"""
Unit тесты для модуля расчёта налогов

Тестируемый модуль:
- app/utils/tax.py — расчёт НПД, комиссии ЮKassa
"""

import pytest
from decimal import Decimal

from app.utils.tax import (
    calculate_npd_tax,
    calculate_yukassa_commission,
    calculate_total_deductions,
    calculate_net_amount,
    calculate_gross_amount,
    format_tax_breakdown,
)


class TestCalculateNPDTax:
    """Тесты расчёта НПД (4%)"""

    def test_npd_tax_integer_amount(self):
        """Расчёт НПД для целой суммы"""
        result = calculate_npd_tax(1000)

        assert result == Decimal("40.00")

    def test_npd_tax_decimal_amount(self):
        """Расчёт НПД для суммы с копейками"""
        result = calculate_npd_tax(Decimal("1234.56"))

        # 1234.56 * 0.04 = 49.38
        assert result == Decimal("49.38")

    def test_npd_tax_small_amount(self):
        """Расчёт НПД для малой суммы"""
        result = calculate_npd_tax(Decimal("10.00"))

        assert result == Decimal("0.40")

    def test_npd_tax_zero(self):
        """Расчёт НПД для нулевой суммы"""
        result = calculate_npd_tax(0)

        assert result == Decimal("0.00")


class TestCalculateYuKassaCommission:
    """Тесты расчёта комиссии ЮKassa (2.8%)"""

    def test_yukassa_commission_integer_amount(self):
        """Расчёт комиссии для целой суммы"""
        result = calculate_yukassa_commission(1000)

        assert result == Decimal("28.00")

    def test_yukassa_commission_decimal_amount(self):
        """Расчёт комиссии для суммы с копейками"""
        result = calculate_yukassa_commission(Decimal("5000.00"))

        # 5000 * 0.028 = 140.00
        assert result == Decimal("140.00")

    @pytest.mark.skip(reason="Функция не поддерживает кастомную ставку")
    def test_yukassa_commission_custom_rate(self):
        """Расчёт комиссии с кастомной ставкой"""
        # SKIP: calculate_yukassa_commission() не поддерживает параметр rate
        pass

    def test_yukassa_commission_zero(self):
        """Расчёт комиссии для нулевой суммы"""
        result = calculate_yukassa_commission(0)

        assert result == Decimal("0.00")


class TestCalculateTotalDeductions:
    """Тесты расчёта общих вычетов (НПД + комиссия)"""

    def test_total_deductions_standard(self):
        """Расчёт общих вычетов для стандартной суммы"""
        result = calculate_total_deductions(1000)

        # НПД: 40, ЮKassa: 28, Итого: 68
        assert result == Decimal("68.00")

    def test_total_deductions_subscription_package(self):
        """Расчёт общих вычетов для подписки 299₽"""
        result = calculate_total_deductions(299)

        # НПД: 11.96, ЮKassa: 8.37, Итого: 20.33
        expected = Decimal("11.96") + Decimal("8.37")
        assert result == expected

    def test_total_deductions_credits_package(self):
        """Расчёт общих вычетов для пакета кредитов 199₽"""
        result = calculate_total_deductions(199)

        # НПД: 7.96, ЮKassa: 5.57, Итого: 13.53
        expected = Decimal("7.96") + Decimal("5.57")
        assert result == expected


class TestCalculateNetAmount:
    """Тесты расчёта чистой суммы (после вычетов)"""

    def test_net_amount_standard(self):
        """Расчёт чистой суммы для стандартной суммы"""
        result = calculate_net_amount(1000)

        # 1000 - (40 + 28) = 932
        assert result == Decimal("932.00")

    def test_net_amount_subscription_299(self):
        """Расчёт чистой суммы для подписки 299₽"""
        result = calculate_net_amount(299)

        # 299 - (11.96 + 8.37) = 278.67
        npd = Decimal("11.96")
        commission = Decimal("8.37")
        expected = Decimal("299") - npd - commission
        assert result == expected

    def test_net_amount_zero(self):
        """Расчёт чистой суммы для нулевой суммы"""
        result = calculate_net_amount(0)

        assert result == Decimal("0.00")


class TestCalculateGrossAmount:
    """Тесты обратного расчёта (от чистой к валовой сумме)"""

    def test_gross_amount_standard(self):
        """Обратный расчёт для стандартной чистой суммы"""
        net = 932
        result = calculate_gross_amount(net)

        # net = gross - (gross * 0.04) - (gross * 0.028)
        # net = gross * (1 - 0.04 - 0.028)
        # net = gross * 0.932
        # gross = net / 0.932 ≈ 1000
        assert abs(result - Decimal("1000")) < Decimal("0.01")

    def test_gross_amount_round_trip(self):
        """Проверка обратного преобразования (round trip)"""
        original_gross = Decimal("500.00")
        net = calculate_net_amount(original_gross)
        recovered_gross = calculate_gross_amount(net)

        # Должны быть примерно равны (с точностью до копеек)
        assert abs(recovered_gross - original_gross) < Decimal("0.01")


class TestFormatTaxBreakdown:
    """Тесты форматирования разбивки налогов"""

    def test_format_tax_breakdown_standard(self):
        """Форматирование разбивки для стандартной суммы"""
        result = format_tax_breakdown(Decimal("1000"))

        assert "gross_amount" in result
        assert result["gross_amount"] == Decimal("1000.00")
        assert "npd_tax" in result
        assert result["npd_tax"] == Decimal("40.00")
        assert "yukassa_commission" in result
        assert result["yukassa_commission"] == Decimal("28.00")
        assert "total_deductions" in result
        assert result["total_deductions"] == Decimal("68.00")
        assert "net_amount" in result
        assert result["net_amount"] == Decimal("932.00")

    def test_format_tax_breakdown_keys(self):
        """Проверка всех ключей в разбивке"""
        result = format_tax_breakdown(Decimal("500"))

        expected_keys = [
            "gross_amount",
            "npd_tax",
            "yukassa_commission",
            "total_deductions",
            "net_amount",
            "deduction_percentage",
        ]

        for key in expected_keys:
            assert key in result

    def test_format_tax_breakdown_deduction_percentage(self):
        """Проверка процента вычетов"""
        result = format_tax_breakdown(Decimal("1000"))

        # (68 / 1000) * 100 = 6.8%
        assert result["deduction_percentage"] == Decimal("6.80")


class TestRealWorldScenarios:
    """Тесты реальных сценариев с тарифами проекта"""

    def test_subscription_basic_299(self):
        """Тариф: Базовая подписка 299₽"""
        gross = Decimal("299.00")

        npd = calculate_npd_tax(gross)
        commission = calculate_yukassa_commission(gross)
        net = calculate_net_amount(gross)

        assert npd == Decimal("11.96")
        assert commission == Decimal("8.37")
        assert net == Decimal("278.67")

    def test_subscription_standard_499(self):
        """Тариф: Стандартная подписка 499₽"""
        gross = Decimal("499.00")

        npd = calculate_npd_tax(gross)
        commission = calculate_yukassa_commission(gross)
        net = calculate_net_amount(gross)

        assert npd == Decimal("19.96")
        assert commission == Decimal("13.97")
        assert net == Decimal("465.07")

    def test_subscription_premium_899(self):
        """Тариф: Премиум подписка 899₽"""
        gross = Decimal("899.00")

        npd = calculate_npd_tax(gross)
        commission = calculate_yukassa_commission(gross)
        net = calculate_net_amount(gross)

        assert npd == Decimal("35.96")
        assert commission == Decimal("25.17")
        assert net == Decimal("837.87")

    def test_credits_package_199(self):
        """Пакет кредитов: 100 кредитов за 199₽"""
        gross = Decimal("199.00")

        breakdown = format_tax_breakdown(gross)

        assert breakdown["gross_amount"] == Decimal("199.00")
        assert breakdown["npd_tax"] == Decimal("7.96")
        assert breakdown["yukassa_commission"] == Decimal("5.57")
        assert breakdown["net_amount"] == Decimal("185.47")

    def test_profit_margin_basic_subscription(self):
        """Проверка чистой прибыли для базовой подписки"""
        gross = Decimal("299.00")
        net = calculate_net_amount(gross)

        # Чистая прибыль: 278.67₽
        # Процент чистой прибыли: (278.67 / 299) * 100 = 93.2%
        profit_percentage = (net / gross) * 100

        assert profit_percentage > Decimal("93")
        assert profit_percentage < Decimal("94")
