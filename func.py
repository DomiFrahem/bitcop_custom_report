from datetime import timedelta, datetime
from time import strftime, gmtime, strptime
import re
from model import *


short_name_day_week = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']


def get_range_date(start_date: str, end_date: str) -> list[datetime]:
    start_date = datetime.strptime(start_date, '%Y%m%d')
    end_date = datetime.strptime(end_date, '%Y%m%d')
    delta = end_date - start_date

    range_date = [start_date + timedelta(days=i)
                  for i in range(delta.days + 1)]

    return range_date


def get_next_day(date: datetime) -> datetime:
    """get_next_day
    Args:
        date (datetime): Дата

    Returns:
        datetime: Возвращается следующий день
    """
    return date + timedelta(days=1)


def convert_from_sec(timestemp: int, format: str = '%H:%M:%S') -> str:
    return strftime(format, gmtime(timestemp))


def get_percent(part: int, total: int) -> float:
    try:
        return round((part / total) * 100, 2)
    except ZeroDivisionError:
        return 0


def filter_employee_by_id(id: int, employees: list[Employee]) -> str:
    return [employee.fio for employee in employees if int(employee.id) == int(id)][0]


def get_date_my_format(date: str) -> str:
    return get_datetime(date).strftime('%d.%m.%Y')


def get_datetime(date: str) -> datetime:
    return datetime.strptime(date, '%Y%m%d')


def get_name_week_day(date: datetime) -> str:
    return short_name_day_week[date.weekday()]


def sum_time(times: list) -> float:
    return sum([get_seconds(strptime(time, '%H:%M:%S')) for time in times])


def get_seconds(time) -> int:
    return timedelta(hours=time.tm_hour, minutes=time.tm_min, seconds=time.tm_sec).total_seconds()


def get_only_smart_board(employees: list[Employee]) -> list[Employee]:
    return [employee for employee in employees if 'Smart Board' in employee.fio]


def parse_name_smartboard(name: str, type: int = 1) -> str:
    """parse_name_smartboard

    Args:
        name (str): fullName SmartBoard from bitcop
        type (int, optional): type selected information. \n\t 1 - corpus \n\t 2 - cabinet \n Defaults to 1.

    Returns:
        str: value by type
    """
    if type == 2:
        cabinet = re.findall(r'Каб\.\s(.+)\s\(Smart', name)[0]
        if cabinet[-1] == '.':
            return cabinet[0:-1]
        else:
            return cabinet
    else:
        return re.findall(r'(.+)\ К', name)[0]


def parse_time_smartboard(time: int) -> str:
    _time = gmtime(time)
    return F"{_time.tm_hour} ч. {_time.tm_min} м." if _time.tm_hour != 0 else F"{_time.tm_min} м."


def get_seconds_from_str_time(time: str) -> int:
    return get_seconds(strptime(time, '%H:%M:%S'))
