import os
from datetime import datetime
import xlsxwriter
from xlsxwriter.utility import xl_range
from func import convert_from_sec, get_date_my_format, get_percent, sum_time
from model import EmployeeActivity, EmployeeActivityXLSX


class ReportActivity():
    def __init__(self, employees_activity: list[EmployeeActivityXLSX]) -> None:
        self._employees_activity = employees_activity
        self.file_name = F"report_activity_{datetime.now().strftime('%d.%m.%Y')}.xlsx"
        self.path = os.path.join(os.path.dirname(
            __file__), 'tmp', self.file_name)

        self._workbook = xlsxwriter.Workbook(self.path)
        self._worksheet = self._workbook.add_worksheet()

        self._cook_xlsx()

    def _cook_xlsx(self):
        column = 0
        for employee in self._employees_activity:
            self._create_first_header(
                employee.date_start, employee.date_end, employee.fio, column)
            self._create_sub_header(column)
            row = self._set_data(employee.activity, column)
            self._create_total_row(employee.activity, column, row)
            column += 6

        self._workbook.close()

    def _create_first_header(self, date_start: str, date_end: str, fio: str, column: int) -> None:
        style = self._workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'})
        style.set_text_wrap()

        text = F"{fio} \n посещаемость с {get_date_my_format(date_start)} по {get_date_my_format(date_end)}"
        self._worksheet.merge_range(
            xl_range(0, column, 0, column+4),
            text,
            style
        )

    def _create_sub_header(self, column: int) -> None:
        style = self._workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'})
        style.set_text_wrap()

        self._worksheet.write(1, column, 'Д/н', style)
        self._worksheet.write(1, column+1, 'Дата', style)
        self._worksheet.write(1, column+2, 'Всего время',  style)
        self._worksheet.write(1, column+3, 'Активное время',  style)
        self._worksheet.write(1, column+4, '%',  style)

    def _set_data(self, items: list[EmployeeActivity], column: int) -> int:
        style_body = self._workbook.add_format({
            'border': 1,
            'align': 'center',
        })

        style_body_with_bold = self._workbook.add_format({
            'border': 1,
            'align': 'center',
            'bold': True
        })

        row = 2
        for item in items:
            self._worksheet.write(
                row, column, item.day_week, style_body_with_bold)
            self._worksheet.write(row, column+1, item.date, style_body)
            self._worksheet.write(
                row, column+2, item.total_time,  style_body)
            self._worksheet.write(
                row, column+3, item.active_time,  style_body)
            self._worksheet.write(row, column+4, item.procent,  style_body)
            row += 1

        return row

    def _create_total_row(self, items: list[EmployeeActivity], column: int, row: int):
        style = self._workbook.add_format({
            'border': 1,
            'align': 'center',
            'bold': True
        })

        self._worksheet.merge_range(
            xl_range(row, column, row, column+1), 'Всего', style
        )
        total_time = sum_time([item.total_time for item in items])
        total_active_time = sum_time([item.total_time for item in items])
        self._worksheet.write(
            row, column+2, convert_from_sec(total_time), style)
        self._worksheet.write(
            row, column+3, convert_from_sec(total_active_time), style)

        self._worksheet.write(
            row, column+4, F"{get_percent(total_active_time, total_time)} %", style)
