import openpyxl

def excel_to_list(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    data = []
    for row in sheet.iter_rows(values_only=True):
        data.append(list(row))
    print( data)
    return data

def excel_to_list2(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    data = []

    rows = sheet.iter_rows(min_row=2, values_only=True)
    for row in rows:
        filtered_row = [cell for cell in row if cell is not None]
        data.append(filtered_row)
    print(data)
    return data

if __name__ == '__main__':
    excel_to_list2(r"C:\Users\admini\Desktop\ERE性能测试用例_模板.xlsx")