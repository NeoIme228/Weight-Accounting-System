import xlsxwriter

def export_to_excel(path: str, data: dict):
    """Экспорт данных ввиде таблицы-excel"""

    headers = ["Название", "Дата", "Вес", "Погода"]

    workbook = xlsxwriter.Workbook(path)
    worksheet =  workbook.add_worksheet()

    row = 0
    col = 0
    for header in headers:
        worksheet.write(row, col, header)
        col += 1

    row += 1
    
    for account in data.values():
        for date, info in account["dates"].items():
            worksheet.write(row, 0, account["name"])
            worksheet.write(row, 1, date)
            worksheet.write(row, 2, info["weight"])
            worksheet.write(row, 3, info["weather"])
            row += 1

    workbook.close()
