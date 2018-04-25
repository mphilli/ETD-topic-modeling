# A script for exporting data from ETD_metadata to an Excel spreadsheet (.xlsx)
from os import listdir
import xlsxwriter


def get_etd_data():
    text_files = "../resources/ETD_metadata"
    content = [1, 4, 7, 10]
    data = []
    for file in listdir(text_files):
        with open(text_files + '/' + file, 'r', encoding='utf-8') as text_file:
            this_row = [file.split('.')[0]]
            for i, line in enumerate(text_file.readlines()):
                if i in content:
                    this_row.append(line.replace('\n', ''))
            data.append(this_row)
    return data


def write_to_excel(rows):
    workbook = xlsxwriter.Workbook("../resources/ETD_metadata.xlsx")
    worksheet = workbook.add_worksheet()
    rows.insert(0, ['etd_code', 'title', 'department', 'keywords', 'abstract'])  # prepend title column
    for row, row_value in enumerate(rows):
        worksheet.write_row(row, 0, row_value)
    workbook.close()
    print("Finished creating Excel file.")


if __name__ == "__main__":
    etd_data = get_etd_data()
    write_to_excel(etd_data)



