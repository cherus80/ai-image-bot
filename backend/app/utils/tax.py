"""
Утилиты для расчёта налогов и комиссий.

Включает расчёт:
- Налога для самозанятых (НПД): 4%
- Комиссии ЮKassa: 2.8%
- Чистой суммы после вычета налогов и комиссий
"""

from decimal import Decimal, ROUND_HALF_UP


# Константы налогов и комиссий
NPD_TAX_RATE = Decimal("0.04")  # 4% НПД (налог для самозанятых)
YUKASSA_COMMISSION_RATE = Decimal("0.028")  # 2.8% комиссия ЮKassa


def calculate_npd_tax(amount: Decimal) -> Decimal:
    """
    Расчёт налога для самозанятых (НПД) - 4%.

    Args:
        amount: Сумма платежа в рублях

    Returns:
        Decimal: Сумма налога (округлено до 2 знаков после запятой)

    Example:
        >>> calculate_npd_tax(Decimal("1000"))
        Decimal('40.00')
    """
    if amount <= 0:
        return Decimal("0.00")

    tax = amount * NPD_TAX_RATE
    return tax.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_yukassa_commission(amount: Decimal) -> Decimal:
    """
    Расчёт комиссии ЮKassa - 2.8%.

    Args:
        amount: Сумма платежа в рублях

    Returns:
        Decimal: Сумма комиссии (округлено до 2 знаков после запятой)

    Example:
        >>> calculate_yukassa_commission(Decimal("1000"))
        Decimal('28.00')
    """
    if amount <= 0:
        return Decimal("0.00")

    commission = amount * YUKASSA_COMMISSION_RATE
    return commission.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_total_deductions(amount: Decimal) -> Decimal:
    """
    Расчёт общей суммы вычетов (НПД + комиссия ЮKassa).

    Args:
        amount: Сумма платежа в рублях

    Returns:
        Decimal: Общая сумма вычетов (округлено до 2 знаков после запятой)

    Example:
        >>> calculate_total_deductions(Decimal("1000"))
        Decimal('68.00')  # 40 (НПД) + 28 (комиссия)
    """
    if amount <= 0:
        return Decimal("0.00")

    npd = calculate_npd_tax(amount)
    commission = calculate_yukassa_commission(amount)
    total = npd + commission

    return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_net_amount(amount: Decimal) -> Decimal:
    """
    Расчёт чистой суммы после вычета НПД и комиссии ЮKassa.

    Args:
        amount: Сумма платежа в рублях

    Returns:
        Decimal: Чистая сумма (округлено до 2 знаков после запятой)

    Example:
        >>> calculate_net_amount(Decimal("1000"))
        Decimal('932.00')  # 1000 - 40 (НПД) - 28 (комиссия)
    """
    if amount <= 0:
        return Decimal("0.00")

    deductions = calculate_total_deductions(amount)
    net = amount - deductions

    return net.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_gross_amount(net_amount: Decimal) -> Decimal:
    """
    Обратный расчёт: из чистой суммы рассчитать сумму платежа (с учётом налогов и комиссий).

    Формула: gross = net / (1 - npd_rate - commission_rate)

    Args:
        net_amount: Желаемая чистая сумма в рублях

    Returns:
        Decimal: Требуемая сумма платежа (округлено до 2 знаков после запятой)

    Example:
        >>> calculate_gross_amount(Decimal("932"))
        Decimal('1000.00')
    """
    if net_amount <= 0:
        return Decimal("0.00")

    # Коэффициент вычетов (1 - 0.04 - 0.028 = 0.932)
    deduction_coefficient = Decimal("1") - NPD_TAX_RATE - YUKASSA_COMMISSION_RATE
    gross = net_amount / deduction_coefficient

    return gross.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def format_tax_breakdown(amount: Decimal) -> dict:
    """
    Полная разбивка суммы на составляющие.

    Args:
        amount: Сумма платежа в рублях

    Returns:
        dict: Словарь с разбивкой:
            - gross_amount: Общая сумма платежа
            - npd_tax: Налог НПД (4%)
            - yukassa_commission: Комиссия ЮKassa (2.8%)
            - total_deductions: Общая сумма вычетов
            - net_amount: Чистая сумма
            - deduction_percentage: Процент вычетов

    Example:
        >>> format_tax_breakdown(Decimal("1000"))
        {
            'gross_amount': Decimal('1000.00'),
            'npd_tax': Decimal('40.00'),
            'yukassa_commission': Decimal('28.00'),
            'total_deductions': Decimal('68.00'),
            'net_amount': Decimal('932.00'),
            'deduction_percentage': Decimal('6.80')
        }
    """
    if amount <= 0:
        return {
            "gross_amount": Decimal("0.00"),
            "npd_tax": Decimal("0.00"),
            "yukassa_commission": Decimal("0.00"),
            "total_deductions": Decimal("0.00"),
            "net_amount": Decimal("0.00"),
            "deduction_percentage": Decimal("0.00"),
        }

    npd = calculate_npd_tax(amount)
    commission = calculate_yukassa_commission(amount)
    deductions = calculate_total_deductions(amount)
    net = calculate_net_amount(amount)
    deduction_pct = (deductions / amount * 100).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )

    return {
        "gross_amount": amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        "npd_tax": npd,
        "yukassa_commission": commission,
        "total_deductions": deductions,
        "net_amount": net,
        "deduction_percentage": deduction_pct,
    }
