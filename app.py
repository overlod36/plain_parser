import first_parser
import ex_conv
import xlsxwriter

data = first_parser.get_all()

try:
    ex_conv.fill_table(data)
except xlsxwriter.exceptions.FileCreateError:
    print("Открыт excel файл!")