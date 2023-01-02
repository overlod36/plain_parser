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
    for title, genres, sys_req, same_games, descr in data:
        sheet.write(row, 0, title)
        sheet.write(row, 1, ', '.join(genres)) if len(genres) != 0 else sheet.write(row, 1, '-')
        sheet.write(row, 2, ', '.join(sys_req)) if len(sys_req) != 0 else sheet.write(row, 2, '-')
        sheet.write(row, 3, ', '.join(same_games)) if len(same_games) != 0 else sheet.write(row, 3, '-')
        sheet.write(row, 4, descr)
        row += 1
    wb.close()