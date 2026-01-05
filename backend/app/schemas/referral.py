"""
Pydantic схемы для реферальной программы
"""

from datetime import datetime
from pydantic import BaseModel, Field


class ReferralLinkResponse(BaseModel):
    """Ответ с реферальной ссылкой"""

    referral_link: str = Field(..., description="Реферальная ссылка для приглашения друзей")
    referral_code: str = Field(..., description="Реферальный код пользователя")
    total_referrals: int = Field(..., description="Общее количество приглашённых друзей")
    total_earned: int = Field(..., description="Всего заработано ⭐️звезд за рефералов")


class ReferralRegisterRequest(BaseModel):
    """Запрос на регистрацию по реферальной ссылке"""

    referral_code: str = Field(
        ...,
        description="Реферальный код пригласившего пользователя",
        min_length=1,
        max_length=100,
    )


class ReferralRegisterResponse(BaseModel):
    """Ответ после регистрации по реферальной ссылке"""

    success: bool = Field(..., description="Успешно ли зарегистрирован реферал")
    message: str = Field(..., description="Сообщение о результате")
    bonus_credits: int = Field(
        default=0, description="Количество бонусных ⭐️звезд (если есть)"
    )


class ReferralItem(BaseModel):
    """Информация об одном реферале"""

    id: int = Field(..., description="ID реферала")
    telegram_id: int | None = Field(
        None, description="Telegram ID приглашённого пользователя"
    )
    username: str | None = Field(None, description="Username приглашённого пользователя")
    credits_awarded: int = Field(..., description="Количество начисленных ⭐️звезд")
    is_awarded: bool = Field(
        ..., description="Были ли начислены ⭐️звезды (после первого действия)"
    )
    created_at: datetime = Field(..., description="Дата приглашения")

    class Config:
        from_attributes = True


class ReferralStatsResponse(BaseModel):
    """Статистика по рефералам"""

    total_referrals: int = Field(..., description="Общее количество приглашённых друзей")
    active_referrals: int = Field(
        ..., description="Активные рефералы (совершили хотя бы одно действие)"
    )
    pending_referrals: int = Field(
        ..., description="Ожидающие рефералы (ещё не совершили действие)"
    )
    total_earned: int = Field(..., description="Всего заработано ⭐️звезд")
    referrals: list[ReferralItem] = Field(
        default_factory=list, description="Список рефералов"
    )
    referral_link: str = Field(..., description="Реферальная ссылка")
    referral_code: str = Field(..., description="Реферальный код")


class ReferralReward(BaseModel):
    """Информация о награде за реферала"""

    referral_id: int = Field(..., description="ID реферальной записи")
    credits_awarded: int = Field(..., description="Количество начисленных ⭐️звезд")
    referrer_id: int = Field(..., description="ID пользователя, получившего награду")
    referred_id: int = Field(..., description="ID пользователя, который был приглашён")
