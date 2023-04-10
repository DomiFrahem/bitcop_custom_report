import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.security.api_key import APIKey
from starlette.status import HTTP_200_OK, HTTP_502_BAD_GATEWAY
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


import auth
import getter_data
from excel import ReportActivity
from func import *
from model import *

# Load variable from .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)




app = FastAPI()
app.version = '0.2'
app.mount('/static', StaticFiles(directory='static'), name='static')
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )
templates = Jinja2Templates(directory='templates')

@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



@app.get("/employees")
async def read_employees(api_key_header: APIKey = Depends(auth.get_api_key)) -> list[Employee]:
    '''Список активированых пользовательй'''
    if api_key_header != HTTP_200_OK:
        return api_key_header
    
    return getter_data.get_employees()

@app.get('/activity/{date_start}/{date_end}/{id_employee}')
async def read_activity(date_start: str, date_end: str, id_employee: int, api_key_header: APIKey = Depends(auth.get_api_key)) -> list[EmployeeActivity]:
    ''' Список активностей по датам '''
    if api_key_header != HTTP_200_OK:
        return api_key_header

    employee_activities = getter_data.get_employee_activity(
        date_start, date_end, id_employee)

    if len(employee_activities) != 0:
        return employee_activities
    else:
        return HTTPException(status_code=HTTP_502_BAD_GATEWAY, detail='Не смогли полуить данные')

@app.get('/activity/file/{date_start}/{date_end}/{ids_employee}') 
def read_employees_activity(date_start: str, date_end: str, ids_employee: str, api_key_header: APIKey = Depends(auth.get_api_key)) -> FileResponse:
    ''' Возвращает активность xlsx файлом '''
    if api_key_header != HTTP_200_OK:
        return api_key_header

    ra = ReportActivity(getter_data.get_employee_activity_to_xlsx(
        date_start, date_end, ids_employee))
    headers = {'Content-Disposition': 'attachment; filename="Book.xlsx"'}
    return FileResponse(ra.path, headers=headers)


@app.get('/activity/smartboard/{date}/')
def read_smartboard_report(date: str, api_key_header: APIKey = Depends(auth.get_api_key)):
    ''' Возвращает активность Smartboard '''
    if api_key_header != HTTP_200_OK:
        return api_key_header

    smartboards = get_only_smart_board(getter_data.get_employees())
    return getter_data.get_productivity_smartboard(date, smartboards)
