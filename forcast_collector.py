import json
import requests

from bs4 import BeautifulSoup


def replace_keys_name(dic):
    # Replacing The Existing Strings From Web Site With The Strings That Was Required
    correct_keys_names = {'DESCRIPTION': 'DESC', 'TEMP': 'TEMP', 'FEELS': 'FEEL', 'PRECIP': 'PRECIP',
                          'HUMIDITY': 'HUMIDITY', 'WIND': 'WIND'}

    return {correct_keys_names[k]: v for k, v in dic.items()}


def create_new_item(values, rows_counter):
    hours_map[times_list[rows_counter]] = replace_keys_name(dict(zip(headers_list[1::], values[1::])))
    return hours_map, rows_counter + 1


def fill_data(main_table, values, hours):
    rows_counter = 0
    for item in main_table.find_all('td')[1::]:

        value = item.get_text()
        if value != '':
            values.append(value)
        else:
            map, rows_counter = create_new_item(values, rows_counter)

    create_new_item(values, rows_counter)

    return hours


# Initialize Lists and Dictionary
headers_list, times_list, values_list = [], [], []
table_values = {}

# Scrap The Web Page
page = requests.get('https://weather.com/weather/hourbyhour/l/ISXX0026:1:IS')
soup = BeautifulSoup(page.text, 'lxml')

extract_main_table = soup.find(class_='twc-table')

# Extract Columns Headers Titles Into A List
for item in extract_main_table.find_all('th'):
    headers_list.append(item.get_text().upper())

# Extract Times Values Into A List
for item in extract_main_table.find_all('span', {'class': 'dsx-date'}):
    times_list.append(item.get_text().upper())

# Create Main Dictionary
hours_map = dict.fromkeys(times_list, )

hours_map = fill_data(extract_main_table, values_list, hours_map)

with open('forcast_data.json', 'w') as fd:
    fd.write(json.dumps(hours_map, ensure_ascii=False, indent=4))



