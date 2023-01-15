import gs_parse
import ex_conv, parser_module, data_module
import xlsxwriter
import time


def menu():
    pages_count = parser_module.GS_Parse.get_pages_count()
    while True:
        print(f'Количество страниц -> {pages_count}')
        cnt = int(input('Введите количество страниц -> '))
        pg = int(input('Номер страницы -> '))
        if not str(pg).isnumeric() or not str(cnt).isnumeric():
            print('Введено не число!')
        elif pg < 0 or cnt < 0:
            print('Количество страниц отрицательно!')
        elif pg > pages_count or cnt > pages_count:
            print(f'Максимальное количество страниц {pages_count}!')
        elif (pg + cnt) > pages_count:
            print('Выход за пределы!')
        else:
            return [pg, cnt]
    


if __name__ == "__main__":
    choice = menu()
    start_time = time.time()
    gs_parse.run_parse(choice[0], choice[1])
    print("|- %s секунд -|" % (time.time() - start_time))
    data = gs_parse.get_result_list()
    data_module.write_journal(data, f'/game_site/[first_page={choice[0]}][pages_cnt={choice[1]}]')
    # try:
    #     ex_conv.fill_table(data, 'result1.xlsx')
    # except xlsxwriter.exceptions.FileCreateError:
    #     print("Открыт excel файл!")

    