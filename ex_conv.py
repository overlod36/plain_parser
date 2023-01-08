import xlsxwriter

def set_titles(wb, sheet):
    titles = ['Название', 'Оценка в Steam', 'Оценка на Metacritic', 'Жанры', 'Системные требования', 'Схожие игры', 'Описание']
    content_format = wb.add_format({'bold':True})
    column = 0
    for title in titles:
        sheet.write(0, column, title, content_format)
        column += 1


def fill_table(data, name):
    wb = xlsxwriter.Workbook(name)
    sheet = wb.add_worksheet()
    sheet.set_column(0, 0, 50)
    sheet.set_column(1, 1, 20)
    sheet.set_column(2, 2, 20)
    sheet.set_column(3, 3, 150)
    sheet.set_column(4, 4, 180)
    sheet.set_column(5, 5, 175)
    row = 1
    set_titles(wb, sheet)
    for element in data:
        sheet.write(row, 0, element['title'])
        sheet.write(row, 1, element['steam_rank']) if len(element['steam_rank']) != 0 else sheet.write(row, 1, '-')
        sheet.write(row, 2, element['metacritic_rank']) if len(element['metacritic_rank']) != 0 else sheet.write(row, 2, '-')
        sheet.write(row, 3, ', '.join(element['genres'])) if len(element['genres']) != 0 else sheet.write(row, 3, '-')
        sheet.write(row, 4, ', '.join(element['sys_req'])) if len(element['sys_req']) != 0 else sheet.write(row, 4, '-')
        sheet.write(row, 5, ', '.join(element['same_games'])) if len(element['same_games']) != 0 else sheet.write(row, 5, '-')
        sheet.write(row, 6, element['description']) if len(element['description']) != 0 else sheet.write(row, 6, '-')
        row += 1
    wb.close()