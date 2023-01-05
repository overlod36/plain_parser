import xlsxwriter

def set_titles(wb, sheet):
    titles = ['Название', 'Жанры', 'Системные требования', 'Схожие игры', 'Описание']
    content_format = wb.add_format({'bold':True})
    column = 0
    for title in titles:
        sheet.write(0, column, title, content_format)
        column += 1


def fill_table(data):
    wb = xlsxwriter.Workbook('result.xlsx')
    sheet = wb.add_worksheet()
    sheet.set_column(0, 0, 50)
    sheet.set_column(1, 1, 150)
    sheet.set_column(2, 2, 180)
    sheet.set_column(3, 3, 175)
    row = 1
    set_titles(wb, sheet)
    for element in data:
        sheet.write(row, 0, element['title'])
        sheet.write(row, 1, ', '.join(element['genres'])) if len(element['genres']) != 0 else sheet.write(row, 1, '-')
        sheet.write(row, 2, ', '.join(element['sys_req'])) if len(element['sys_req']) != 0 else sheet.write(row, 2, '-')
        sheet.write(row, 3, ', '.join(element['same_games'])) if len(element['same_games']) != 0 else sheet.write(row, 3, '-')
        sheet.write(row, 4, element['description'])
        row += 1
    wb.close()