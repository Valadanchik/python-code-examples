import pandas as pd

def append_to_csv(file_path, barcode="", ingredient="", energy=""):

    existing_data = pd.read_csv(file_path)
    new_data = pd.DataFrame({'Barcode': [barcode],
                             'Ingredient': [ingredient],
                             'Energy':  [energy],
                            })

    combined_data = pd.concat([existing_data, new_data], ignore_index=True)

    combined_data.to_csv('Output.csv', index=True)

append_to_csv('Output.csv', '123456789', 'test', 'test')
