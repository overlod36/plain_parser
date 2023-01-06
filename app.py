import parser_module
import async_parse, single_thread_parse
import ex_conv
import xlsxwriter
import time

def menu():
    pages_count = parser_module.get_pages_count()
    while True:
        print(f'Количество страниц -> {pages_count}')
        ch = input('Выберите парсер, (1 - однопоточный, 2 - асинхронный) -> ')
        if not ch.isnumeric():
            print('Неправильный ввод, введено не число!')
        if int(ch) not in [1, 2]:
            print('Неправильный ввод, введите либо 1, либо 2!') 
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
            return [int(ch), pg, cnt]
    


if __name__ == "__main__":
    choice = menu()
    if choice[0] == 1:
        start_time = time.time()
        single_thread_parse.run_parse(choice[1], choice[2])
        print("|- %s секунд -|" % (time.time() - start_time))
        data = single_thread_parse.get_result_list()
        try:
            ex_conv.fill_table(data, 'result1.xlsx')
        except xlsxwriter.exceptions.FileCreateError:
            print("Открыт excel файл!")
    else:
        start_time = time.time()
        async_parse.run_parse(choice[1], choice[2])
        print("|- %s секунд -|" % (time.time() - start_time))
        data = async_parse.get_result_list()
        try:
            ex_conv.fill_table(data, 'result2.xlsx')
        except xlsxwriter.exceptions.FileCreateError:
            print("Открыт excel файл!")

    