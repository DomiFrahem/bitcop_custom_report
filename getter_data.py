import func
import requests
import os
from datetime import datetime, timedelta
from model import *


def get_employee_activity(start_date: str, end_date: str, id_employee: str) -> list[EmployeeActivity]:
    employee_activities = []

    for date in func.get_range_date(start_date, end_date):
        request = requests.get(F"{os.environ.get('API')}/activity", params={
            'apikey': os.environ.get("APIKEY"),
            'begin': date.strftime('%Y%m%d'),
            'end': func.get_next_day(date).strftime('%Y%m%d'),
            'employees': id_employee
        })

        json = request.json()

        if 'status' in json:
            employee_activities.append(EmployeeActivity(
                day_week=func.get_name_week_day(date),
                date=date.strftime('%d.%m.%Y'),
                total_time=func.convert_from_sec(
                    json['items'][0]['totalTime']),
                active_time=func.convert_from_sec(
                    json['items'][0]['activeTime']),
                procent=F"{func.get_percent(json['items'][0]['activeTime'], json['items'][0]['totalTime'])} %"
            ))

    return employee_activities


def get_employees() -> list[Employee] | None:
    request = requests.get(F"{os.environ.get('API')}/employees", params={
        'apikey': os.environ.get("APIKEY"),
        'active': 'true'
    })

    json = request.json()
    if 'status' in json:
        return [Employee(id=item['id'], fio=F"{item['lastName']} {item['firstName']}") for item in json['items']]


def get_employee_activity_to_xlsx(date_start: str, date_end: str, ids_employee: str) -> list[EmployeeActivityXLSX]:
    employees = get_employees()
    employeeActivityXLSX = []
    
    for id in ids_employee.split(','):
        employeeActivityXLSX.append(EmployeeActivityXLSX(
            date_start=date_start,
            date_end=date_end,
            fio=func.filter_employee_by_id(id, employees),
            activity=get_employee_activity(date_start, date_end, id)
        ))
        
    return employeeActivityXLSX


def get_productivity_smartboard(date: str, smartboards: list[Employee]) -> list:
    smardboard_ids = ','.join([str(smartboard.id)
                              for smartboard in smartboards])

    request = requests.get(F"{os.environ.get('API')}productivity", params={
        'apikey': os.environ.get('APIKEY'),
        'begin': date,
        'end': func.get_next_day(datetime.strptime(date, '%Y%m%d')).strftime('%Y%m%d'),
        'employees': smardboard_ids
    })

    json = request.json()

    if json['status'] == 'success':
        data = []
        for item in json['items']:
            smartboard_active = get_employee_activity(date, date, item['id'])[0]
            active_time = func.get_seconds_from_str_time(
                smartboard_active.active_time)
            total_time = func.get_seconds_from_str_time(
                smartboard_active.total_time)

            data.append({
                'corpus': func.parse_name_smartboard(item['name'], 1),
                'cabinet': func.parse_name_smartboard(item['name'], 2),
                'name': 'Smart Board',
                'date': datetime.strptime(date, '%Y%m%d').strftime('%d.%m.%d'),
                'totalTime':  func.parse_time_smartboard(total_time),
                'productiveTime': func.parse_time_smartboard(item['productiveTime']),
                'unproductiveTime': func.parse_time_smartboard(item['unproductiveTime']),
                'neutralTime': func.parse_time_smartboard(item['totalTime'] - item['productiveTime']),
                'percent_productive': F"{func.get_percent(item['productiveTime'], active_time)} %",
                'time_workday': F"{func.get_percent(total_time, timedelta(minutes=480).total_seconds())} %"
            })

        return data
    else:
        return json
