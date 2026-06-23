from __future__ import annotations

import re
from datetime import date


CPF_PATTERN = re.compile(r"^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$")
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_PATTERN = re.compile(r"^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$")


def only_digits(value: str) -> str:
    return re.sub(r"\D", "", value or "")


def validate_cpf(cpf: str) -> bool:
    digits = only_digits(cpf)
    if len(digits) != 11 or digits == digits[0] * 11:
        return False

    def check_digit(numbers: str, factor: int) -> str:
        total = sum(int(number) * weight for number, weight in zip(numbers, range(factor, 1, -1)))
        remainder = (total * 10) % 11
        return "0" if remainder == 10 else str(remainder)

    return digits[-2] == check_digit(digits[:9], 10) and digits[-1] == check_digit(digits[:10], 11)


def validate_email(email: str) -> bool:
    return bool(EMAIL_PATTERN.match((email or "").strip()))


def validate_phone(phone: str) -> bool:
    digits = only_digits(phone)
    return 10 <= len(digits) <= 13


def validate_birth_date(birth_date: date) -> bool:
    today = date.today()
    return birth_date < today and (today.year - birth_date.year) <= 110


def required(value: str) -> bool:
    return bool((value or "").strip())
