from browser import Browser 
from definition import Spreadsheet
import time 


class SpareBinBot:
    def __init__(self):
        self.bot = Browser()
        self.spreadsheet = Spreadsheet()
    
    def run(self):

        self.bot.open_browser('https://robotsparebinindustries.com/')
        self.bot.download_file("https://robotsparebinindustries.com/SalesData.xlsx")

        self.bot.fill_by_id('username', 'maria')
        self.bot.fill_by_id('password', 'thoushallnotpass')
        self.bot.click_general_element('class', 'btn btn-primary')
        time.sleep(5)

        sales_target_dict = {
            '5000': '1',
            '10000': '2',
            '15000': '3',
            '20000': '4',
            '25000': '5',
            '30000': '6',
            '35000': '7',
            '40000': '8',
            '45000': '9',
            '50000': '10',
            '55000': '11',
            '60000': '12',
            '65000': '13',
            '70000': '14',
            '75000': '15',
            '80000': '16',
            '85000': '17',
            '90000': '18',
            '95000': '19',
            '100000': '20'
        }

        def get_sales_target_index(key: str):
            return sales_target_dict[key]

        worksheet = self.spreadsheet.get_excel_data('SalesData.xlsx', 'data')
        for row in worksheet:
            self.bot.fill_by_id('firstname', row['First Name'])

            sales_target_index = get_sales_target_index(str(row['Sales Target']))
            self.bot.click_select_option_index('//*[@id="salestarget"]', sales_target_index)
            self.bot.fill_by_id('lastname', row['Last Name'])
            self.bot.fill_by_id('salesresult', str(row['Sales']))
            self.bot.click_general_element('class', 'btn btn-primary')