import random
import calendar

# Mapa dni w miesiącach
days_month_count = {
    1: 31,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31,
}

# Wagi dla cyfr PESEL
multipliers = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]


def pesel_checksum(pesel):
    """Oblicza cyfrę kontrolną PESEL."""
    sum = 0
    pesel_list = map(int, list(pesel))
    for a, b in zip(pesel_list, multipliers):
        sum += a * b
    checksum = (10 - sum % 10) % 10
    return checksum


def generate_random_pesel(start_year=1900, end_year=2023):
    """Generuje losowy numer PESEL."""
    # Losowanie roku, miesiąca i dnia
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)

    # Losowanie liczby dni w miesiącu
    if month == 2:
        days_count = 29 if calendar.isleap(year) else 28
    else:
        days_count = days_month_count.get(month, 31)

    day = random.randint(1, days_count)

    # Generowanie losowego numeru identyfikacyjnego (4 cyfry)
    random_digits = random.randint(0, 9999)

    # Formatowanie daty i numeru
    pesel_without_control = f"{year % 100:02d}{month:02d}{day:02d}{random_digits:04d}"

    # Obliczanie cyfry kontrolnej
    checksum = pesel_checksum(pesel_without_control)

    # Zwracamy pełny numer PESEL
    return pesel_without_control + str(checksum)
