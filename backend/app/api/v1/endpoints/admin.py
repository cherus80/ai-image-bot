"""
API endpoints для админки.

Endpoints:
- GET /api/v1/admin/stats — общая статистика (защищено ADMIN_SECRET_KEY)
- GET /api/v1/admin/charts — данные для графиков (защищено ADMIN_SECRET_KEY)
- GET /api/v1/admin/users — список пользователей (защищено ADMIN_SECRET_KEY)
- GET /api/v1/admin/payments/export — экспорт платежей CSV/JSON (защищено ADMIN_SECRET_KEY)
"""

import csv
import io
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Response
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db
from app.models import ChatHistory, Generation, Payment, Referral, User
from app.schemas.admin import (
    AdminChartsData,
    AdminStats,
    AdminUsersRequest,
    AdminUsersResponse,
    AdminUserItem,
    ChartDataPoint,
    PaymentExportItem,
    PaymentExportRequest,
    PaymentExportResponse,
)
from app.utils.tax import (
    calculate_npd_tax,
    calculate_yukassa_commission,
    calculate_net_amount,
)

router = APIRouter()
settings = settings


# ============================================================================
# Dependency для проверки ADMIN_SECRET_KEY
# ============================================================================

async def verify_admin_secret(
    x_admin_secret: Annotated[str | None, Header()] = None
) -> None:
    """
    Проверяет ADMIN_SECRET_KEY из заголовка X-Admin-Secret.

    Raises:
        HTTPException: 401 если ключ не предоставлен или неверный.
    """
    if not x_admin_secret:
        raise HTTPException(
            status_code=401,
            detail="Admin authentication required. Provide X-Admin-Secret header."
        )

    if x_admin_secret != settings.ADMIN_SECRET_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid admin secret key."
        )


# ============================================================================
# GET /api/v1/admin/stats — Общая статистика
# ============================================================================

@router.get("/stats", response_model=AdminStats)
async def get_admin_stats(
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_admin_secret)
) -> AdminStats:
    """
    Получить общую статистику приложения.

    Требует заголовок: `X-Admin-Secret: <ADMIN_SECRET_KEY>`
    """
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=7)
    month_start = today_start - timedelta(days=30)

    # Пользователи
    total_users = await db.scalar(select(func.count(User.id)))

    active_users_today = await db.scalar(
        select(func.count(User.id)).where(User.last_active_at >= today_start)
    )
    active_users_week = await db.scalar(
        select(func.count(User.id)).where(User.last_active_at >= week_start)
    )
    active_users_month = await db.scalar(
        select(func.count(User.id)).where(User.last_active_at >= month_start)
    )

    new_users_today = await db.scalar(
        select(func.count(User.id)).where(User.created_at >= today_start)
    )
    new_users_week = await db.scalar(
        select(func.count(User.id)).where(User.created_at >= week_start)
    )
    new_users_month = await db.scalar(
        select(func.count(User.id)).where(User.created_at >= month_start)
    )

    # Генерации
    total_generations = await db.scalar(select(func.count(Generation.id)))
    generations_today = await db.scalar(
        select(func.count(Generation.id)).where(Generation.created_at >= today_start)
    )
    generations_week = await db.scalar(
        select(func.count(Generation.id)).where(Generation.created_at >= week_start)
    )
    generations_month = await db.scalar(
        select(func.count(Generation.id)).where(Generation.created_at >= month_start)
    )

    fitting_generations = await db.scalar(
        select(func.count(Generation.id)).where(Generation.generation_type == "fitting")
    )
    editing_generations = await db.scalar(
        select(func.count(Generation.id)).where(Generation.generation_type == "editing")
    )

    # Платежи
    total_payments = await db.scalar(select(func.count(Payment.id)))
    successful_payments = await db.scalar(
        select(func.count(Payment.id)).where(Payment.status == "succeeded")
    )

    total_revenue_result = await db.scalar(
        select(func.sum(Payment.amount)).where(Payment.status == "succeeded")
    )
    total_revenue = total_revenue_result or Decimal("0")

    revenue_today_result = await db.scalar(
        select(func.sum(Payment.amount)).where(
            and_(Payment.status == "succeeded", Payment.created_at >= today_start)
        )
    )
    revenue_today = revenue_today_result or Decimal("0")

    revenue_week_result = await db.scalar(
        select(func.sum(Payment.amount)).where(
            and_(Payment.status == "succeeded", Payment.created_at >= week_start)
        )
    )
    revenue_week = revenue_week_result or Decimal("0")

    revenue_month_result = await db.scalar(
        select(func.sum(Payment.amount)).where(
            and_(Payment.status == "succeeded", Payment.created_at >= month_start)
        )
    )
    revenue_month = revenue_month_result or Decimal("0")

    average_payment = (
        total_revenue / successful_payments if successful_payments > 0 else Decimal("0")
    )

    # Подписки
    active_subscriptions_basic = await db.scalar(
        select(func.count(User.id)).where(
            and_(
                User.subscription_type == "basic",
                User.subscription_expires_at > now
            )
        )
    )
    active_subscriptions_pro = await db.scalar(
        select(func.count(User.id)).where(
            and_(
                User.subscription_type == "pro",
                User.subscription_expires_at > now
            )
        )
    )
    active_subscriptions_premium = await db.scalar(
        select(func.count(User.id)).where(
            and_(
                User.subscription_type == "premium",
                User.subscription_expires_at > now
            )
        )
    )

    # Рефералы
    total_referrals = await db.scalar(select(func.count(Referral.id)))
    active_referrals = await db.scalar(
        select(func.count(Referral.id)).where(Referral.is_active == True)
    )

    # Freemium
    freemium_users = await db.scalar(
        select(func.count(User.id)).where(User.freemium_actions_remaining > 0)
    )
    freemium_generations_today = await db.scalar(
        select(func.count(Generation.id)).where(
            and_(
                Generation.used_freemium == True,
                Generation.created_at >= today_start
            )
        )
    )

    return AdminStats(
        total_users=total_users or 0,
        active_users_today=active_users_today or 0,
        active_users_week=active_users_week or 0,
        active_users_month=active_users_month or 0,
        new_users_today=new_users_today or 0,
        new_users_week=new_users_week or 0,
        new_users_month=new_users_month or 0,
        total_generations=total_generations or 0,
        generations_today=generations_today or 0,
        generations_week=generations_week or 0,
        generations_month=generations_month or 0,
        fitting_generations=fitting_generations or 0,
        editing_generations=editing_generations or 0,
        total_payments=total_payments or 0,
        successful_payments=successful_payments or 0,
        total_revenue=total_revenue,
        revenue_today=revenue_today,
        revenue_week=revenue_week,
        revenue_month=revenue_month,
        average_payment=average_payment,
        active_subscriptions_basic=active_subscriptions_basic or 0,
        active_subscriptions_pro=active_subscriptions_pro or 0,
        active_subscriptions_premium=active_subscriptions_premium or 0,
        total_referrals=total_referrals or 0,
        active_referrals=active_referrals or 0,
        freemium_users=freemium_users or 0,
        freemium_generations_today=freemium_generations_today or 0,
    )


# ============================================================================
# GET /api/v1/admin/charts — Данные для графиков
# ============================================================================

@router.get("/charts", response_model=AdminChartsData)
async def get_admin_charts(
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_admin_secret)
) -> AdminChartsData:
    """
    Получить данные для графиков (последние 30 дней).

    Требует заголовок: `X-Admin-Secret: <ADMIN_SECRET_KEY>`
    """
    now = datetime.utcnow()
    days_ago_30 = now - timedelta(days=30)

    # График выручки
    revenue_data = await db.execute(
        select(
            func.date(Payment.created_at).label("date"),
            func.sum(Payment.amount).label("value")
        )
        .where(
            and_(
                Payment.status == "succeeded",
                Payment.created_at >= days_ago_30
            )
        )
        .group_by(func.date(Payment.created_at))
        .order_by(func.date(Payment.created_at))
    )
    revenue_chart = [
        ChartDataPoint(date=str(row.date), value=float(row.value or 0))
        for row in revenue_data.all()
    ]

    # График новых пользователей
    users_data = await db.execute(
        select(
            func.date(User.created_at).label("date"),
            func.count(User.id).label("value")
        )
        .where(User.created_at >= days_ago_30)
        .group_by(func.date(User.created_at))
        .order_by(func.date(User.created_at))
    )
    users_chart = [
        ChartDataPoint(date=str(row.date), value=float(row.value or 0))
        for row in users_data.all()
    ]

    # График генераций
    generations_data = await db.execute(
        select(
            func.date(Generation.created_at).label("date"),
            func.count(Generation.id).label("value")
        )
        .where(Generation.created_at >= days_ago_30)
        .group_by(func.date(Generation.created_at))
        .order_by(func.date(Generation.created_at))
    )
    generations_chart = [
        ChartDataPoint(date=str(row.date), value=float(row.value or 0))
        for row in generations_data.all()
    ]

    return AdminChartsData(
        revenue_chart=revenue_chart,
        users_chart=users_chart,
        generations_chart=generations_chart,
    )


# ============================================================================
# GET /api/v1/admin/users — Список пользователей
# ============================================================================

@router.get("/users", response_model=AdminUsersResponse)
async def get_admin_users(
    page: int = Query(default=1, ge=1, description="Номер страницы"),
    page_size: int = Query(default=50, ge=1, le=200, description="Размер страницы"),
    sort_by: str = Query(default="created_at", description="Поле для сортировки"),
    order: str = Query(default="desc", description="Порядок сортировки (asc/desc)"),
    search: str | None = Query(default=None, description="Поиск по username/telegram_id"),
    filter_subscription: str | None = Query(default=None, description="Фильтр по подписке"),
    filter_active: bool | None = Query(default=None, description="Фильтр по активности"),
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_admin_secret)
) -> AdminUsersResponse:
    """
    Получить список пользователей с фильтрацией и пагинацией.

    Требует заголовок: `X-Admin-Secret: <ADMIN_SECRET_KEY>`
    """
    now = datetime.utcnow()
    month_ago = now - timedelta(days=30)

    # Базовый запрос
    query = select(User)

    # Фильтрация по поиску
    if search:
        query = query.where(
            (User.username.ilike(f"%{search}%")) |
            (User.telegram_id.cast(db.bind.dialect.BIGINT).op("::text").ilike(f"%{search}%"))
        )

    # Фильтрация по подписке
    if filter_subscription:
        query = query.where(User.subscription_type == filter_subscription)

    # Фильтрация по активности
    if filter_active is not None:
        if filter_active:
            query = query.where(User.last_active_at >= month_ago)
        else:
            query = query.where(
                (User.last_active_at < month_ago) | (User.last_active_at.is_(None))
            )

    # Сортировка
    if order == "desc":
        query = query.order_by(getattr(User, sort_by).desc())
    else:
        query = query.order_by(getattr(User, sort_by).asc())

    # Подсчёт общего количества
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query) or 0

    # Пагинация
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    result = await db.execute(query)
    users = result.scalars().all()

    # Формирование ответа с дополнительными данными
    user_items = []
    for user in users:
        # Подсчёт генераций пользователя
        total_generations = await db.scalar(
            select(func.count(Generation.id)).where(Generation.user_id == user.id)
        ) or 0

        # Подсчёт потраченных денег
        total_spent_result = await db.scalar(
            select(func.sum(Payment.amount)).where(
                and_(Payment.user_id == user.id, Payment.status == "succeeded")
            )
        )
        total_spent = total_spent_result or Decimal("0")

        # Подсчёт рефералов
        referrals_count = await db.scalar(
            select(func.count(Referral.id)).where(Referral.referrer_user_id == user.id)
        ) or 0

        # Проверка активности
        is_active = user.last_active_at is not None and user.last_active_at >= month_ago

        user_items.append(
            AdminUserItem(
                id=user.id,
                telegram_id=user.telegram_id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                balance_credits=user.balance_credits,
                subscription_type=user.subscription_type,
                subscription_expires_at=user.subscription_expires_at,
                freemium_actions_remaining=user.freemium_actions_remaining,
                freemium_reset_at=user.freemium_reset_at,
                created_at=user.created_at,
                last_active_at=user.last_active_at,
                total_generations=total_generations,
                total_spent=total_spent,
                referrals_count=referrals_count,
                is_active=is_active,
            )
        )

    total_pages = (total + page_size - 1) // page_size

    return AdminUsersResponse(
        users=user_items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


# ============================================================================
# GET /api/v1/admin/payments/export — Экспорт платежей
# ============================================================================

@router.get("/payments/export")
async def export_payments(
    date_from: datetime | None = Query(default=None, description="Начальная дата"),
    date_to: datetime | None = Query(default=None, description="Конечная дата"),
    status: str = Query(default="succeeded", description="Статус платежа"),
    format: str = Query(default="csv", description="Формат экспорта (csv/json)"),
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_admin_secret)
):
    """
    Экспортировать платежи в CSV или JSON.

    Требует заголовок: `X-Admin-Secret: <ADMIN_SECRET_KEY>`
    """
    # Базовый запрос
    query = (
        select(Payment, User)
        .join(User, Payment.user_id == User.id)
        .where(Payment.status == status)
    )

    if date_from:
        query = query.where(Payment.created_at >= date_from)
    if date_to:
        query = query.where(Payment.created_at <= date_to)

    query = query.order_by(Payment.created_at.desc())

    result = await db.execute(query)
    rows = result.all()

    # Формирование данных
    export_items = []
    total_amount = Decimal("0")
    total_npd_tax = Decimal("0")
    total_yukassa_commission = Decimal("0")
    total_net_amount = Decimal("0")

    for payment, user in rows:
        npd_tax = calculate_npd_tax(payment.amount)
        yukassa_commission = calculate_yukassa_commission(payment.amount)
        net_amount = calculate_net_amount(payment.amount)

        export_items.append(
            PaymentExportItem(
                payment_id=str(payment.id),
                user_id=user.id,
                telegram_id=user.telegram_id,
                username=user.username,
                payment_type=payment.payment_type,
                amount=payment.amount,
                status=payment.status,
                created_at=payment.created_at,
                paid_at=payment.paid_at,
                subscription_type=payment.subscription_type,
                credits_amount=payment.credits_amount,
                yukassa_payment_id=payment.yukassa_payment_id,
                npd_tax=npd_tax,
                yukassa_commission=yukassa_commission,
                net_amount=net_amount,
            )
        )

        total_amount += payment.amount
        total_npd_tax += npd_tax
        total_yukassa_commission += yukassa_commission
        total_net_amount += net_amount

    # JSON формат
    if format == "json":
        export_response = PaymentExportResponse(
            payments=export_items,
            total_count=len(export_items),
            total_amount=total_amount,
            total_npd_tax=total_npd_tax,
            total_yukassa_commission=total_yukassa_commission,
            total_net_amount=total_net_amount,
            date_from=date_from,
            date_to=date_to,
        )
        return export_response

    # CSV формат
    output = io.StringIO()
    writer = csv.writer(output)

    # Заголовки
    writer.writerow([
        "Payment ID",
        "User ID",
        "Telegram ID",
        "Username",
        "Payment Type",
        "Amount (₽)",
        "Status",
        "Created At",
        "Paid At",
        "Subscription Type",
        "Credits Amount",
        "YuKassa Payment ID",
        "НПД 4% (₽)",
        "ЮKassa 2.8% (₽)",
        "Net Amount (₽)",
    ])

    # Данные
    for item in export_items:
        writer.writerow([
            item.payment_id,
            item.user_id,
            item.telegram_id,
            item.username or "",
            item.payment_type,
            float(item.amount),
            item.status,
            item.created_at.isoformat(),
            item.paid_at.isoformat() if item.paid_at else "",
            item.subscription_type or "",
            item.credits_amount or "",
            item.yukassa_payment_id or "",
            float(item.npd_tax),
            float(item.yukassa_commission),
            float(item.net_amount),
        ])

    # Итоговая строка
    writer.writerow([])
    writer.writerow([
        "ИТОГО:",
        "",
        "",
        "",
        "",
        float(total_amount),
        "",
        "",
        "",
        "",
        "",
        "",
        float(total_npd_tax),
        float(total_yukassa_commission),
        float(total_net_amount),
    ])

    csv_content = output.getvalue()
    output.close()

    # Возвращаем CSV файл
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=payments_export_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
        }
    )
