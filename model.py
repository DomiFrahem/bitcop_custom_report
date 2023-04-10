from pydantic import BaseModel


class Employee(BaseModel):
    id: int = 31
    fio: str = "ИПЭиФ. Каб. 409. (Smart Board)."


class EmployeeActivity(BaseModel):
    day_week: str = "Пн"
    date: str = "10.04.2023"
    total_time: str = "00:00:00"
    active_time: str = "00:00:00"
    procent: str = "0 %"


class EmployeeActivityXLSX(BaseModel):
    date_start: str
    date_end: str
    fio: str
    activity: list[EmployeeActivity]


class SmartboardActivity(BaseModel):
    corpus: str
    cabinet: str
    name: str = 'Smart Board'
    date: str
    totalTime: str
    productiveTime: str
    unproductiveTime: str
    neutralTime: str
    percent_productive: str
    time_workday: str