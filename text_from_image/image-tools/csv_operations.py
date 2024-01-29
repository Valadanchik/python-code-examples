import pandas as pd
from config import csv_delimiter



def read_csv(file_path, csv_delim="^"):
    df = pd.read_csv(file_path, sep=csv_delim)
    data = df.to_dict(orient='records')
    return data


def csv_to_html_table(data):
    table_html = "<a href='/' style='  background-color: #007BFF;color: #fff;padding: 10px 20px;margin-right:5px;border: none;border-radius: 5px;cursor: pointer;text-decoration: none;padding-top: 5px;padding-bottom: 5px;'>Back</a>" \
                 "<a href='/download-data/' style='  background-color: #007BFF;color: #fff;padding: 10px 20px;border: none;border-radius: 5px;cursor: pointer;text-decoration: none;padding-top: 5px;padding-bottom: 5px;'>Download Data</a>" \
                 "<table style='border-collapse: collapse; margin-top:30px'>"
    table_html += "<tr>"
    if len(data) == 0:
        return table_html
    for key in data[0].keys():
        table_html += f"<th style='border: 1px solid black; padding: 8px;'>{key}</th>"
    table_html += f"<th style='border: 1px solid black; padding: 8px;'>Remove</th>"
    table_html += "</tr>"
    i = 1
    for row in data:
        table_html += "<tr>"
        for value in row.values():
            table_html += f"<td style='border: 1px solid black; padding: 8px;'>{value}</td>"
        table_html += f"<td style='border: 1px solid black; padding: 8px; b'><a class='background-color: red;' onclick=\"return confirm(\'Are you sure\')\" href='/remove_row/{i}' style='background-color: red;color: white; #fff;padding: 10px 20px;border: none;border-radius: 5px;cursor: pointer;text-decoration: none;padding-top: 5px;padding-bottom: 5px;'>Remove</a></td>"
        table_html += '</tr>'
        i += 1
    table_html += "</table>"
    return table_html


def append_to_csv(file_path, barcode="_", ingredient="_", energy="_"):
    df = pd.read_csv(file_path, sep=csv_delimiter, encoding='utf-8')

    new_row = {'Barcode': barcode,
               'Ingredient': ingredient,
               'Energy': energy,
               }
    new_row_df = pd.DataFrame([new_row])

    df = pd.concat([df, new_row_df], ignore_index=True, )
    df.to_csv(file_path, sep=csv_delimiter, index=False, lineterminator='\n', encoding='utf-8', )

    return df
