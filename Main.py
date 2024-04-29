import pandas as pd
from bs4 import BeautifulSoup
import requests
import html
import sys
import csv

csv_file = 'company data.csv'
url = 'https://www.seia.org/directory?field_business_type_value=All&field_physical_state_value=All&page='
company_data = [[],[],[]]
num_list = list(range(1, 214))

for number in num_list:

    html_data = requests.get(url + str(number))

    if html_data.status_code == 200:

        soup = BeautifulSoup(html_data.text, 'html.parser')
        all_div_blocks = soup.find_all('div', class_='list-resources__block padded grid__row grid__block--start grid__block--wrap views-row')
        
        for div_block in all_div_blocks:

            h3_heading = div_block.find('h3')
            link_p = div_block.find('p', class_ = 'copy--20 color--primary--purple')
            link_a = link_p.find('a')
            company_type = div_block.find('span', class_ = 'color--gray copy--roboto copy--roboto--18')

            company_data[0].append(h3_heading.text.strip())
            company_data[1].append(link_a.text.strip())
            company_data[2].append(company_type.text.strip())

    else:
        print("Failed to retrieve the webpage. Status code:", html_data.status_code)
        sys.exit(1)
    
    print('Appended Item ' + str(number))

company_data_formatted = list(zip(*company_data))

with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(company_data_formatted)