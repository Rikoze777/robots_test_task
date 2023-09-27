import openpyxl
from robots.services import fetch_robots


def create_excel():
    week_robots = fetch_robots()
    wb = openpyxl.Workbook()
    ws = wb.active
    wb.remove_sheet(ws)
    page = 1

    for model, _ in week_robots.items():
        ws = wb.create_sheet(model, page)
        ws.cell(row=1, column=1, value='Модель')
        ws.cell(row=1, column=2, value='Версия')
        ws.cell(row=1, column=3, value='Количество за неделю')
        page += 1
        row_num = 2

        for version, count in week_robots[model].items():
            ws.cell(row=row_num, column=1, value=model)
            ws.cell(row=row_num, column=2, value=version)
            ws.cell(row=row_num, column=3, value=count)
            row_num += 1

    return wb
