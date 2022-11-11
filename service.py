"""Performing actions"""

import itertools
import uuid
from typing import List

import xlsxwriter

from database import UserData


def write_xls(users: List[UserData]):
    """Fills new file with users, include headers"""
    file_inner_id = f'{uuid.uuid4()}.xlsx'
    workbook = xlsxwriter.Workbook(file_inner_id)
    worksheet = workbook.add_worksheet()
    for i, value in enumerate(['Name', "Birth", "Role"]):
        worksheet.write(0, i, value)
    columns = itertools.cycle((0, 1, 2))
    for i, value in enumerate(users):
        print(value)
        worksheet.write(1 + i, next(columns), value.nsp)
        date_str = value.birth_date.strftime('%d.%m.%Y')
        worksheet.write(1 + i, next(columns), date_str)
        worksheet.write(1 + i, next(columns), value.role)
    workbook.close()
    return file_inner_id
