import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time


class Parser:
    def __init__(self) -> None:
        self.service = Service(executable_path="C:/Program Files/chromedriver-win64/chromedriver.exe")
        self.driver = webdriver.Chrome(service=self.service)
        self.listings = "https://rit-csm.symplicity.com/students/app/career-fairs/c44d4e872414c27ed31d34e6d3767018/employers"
        self.driver.get(self.listings)

    def get_to_page(self):
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "ritUsername"))
        )

        input_element = self.driver.find_element(By.ID, "ritUsername")
        input_element.clear()
        input_element.send_keys(os.getenv("RIT_USERNAME"))

        input_element = self.driver.find_element(By.ID, "ritPassword")
        input_element.clear()
        input_element.send_keys(os.getenv("RIT_PASSWORD"))

        login_button = self.driver.find_element(By.XPATH, "/html/body/div/div[1]/form/div/span/button")
        login_button.click()

        print("Please complete 2FA manually.")
        time.sleep(10)

        # Wait for the browser to return to the original site after 2FA
        WebDriverWait(self.driver, 120).until(
            lambda driver: driver.current_url == self.listings
        )
        print("2FA completed and redirected back. Continuing automation...")

    def get_info(self):
        dropdown_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@aria-label="Select the number of items to show per page"]'))
        )
        dropdown = Select(dropdown_element)

        dropdown.select_by_value('250')

        # time.sleep(15)

        # company_elements = self.driver.find_elements(By.CLASS_NAME, "list-item list_rows list-item-responsive-actions cursor-pointer")

        # for company in company_elements:
        #     tabindex = company.get_attribute("tabindex")
        #     print(f"Tabindex: {tabindex}")
            
        #     company.click()
        #     time.sleep(1)

        #     self.parse_info()

        #     self.driver.back()

    def parse_info(self):
        pass

    def run_parser(self):
        self.get_to_page()
        self.get_info()

        for i in range(40):
            print(i + 1)
            time.sleep(1)
        self.driver.quit()


# def get_data():
#     response = requests.get(listings).text
#     soup = BeautifulSoup(response, 'html.parser')

#     print(soup)

def main():
    Parser().run_parser()
    
if __name__ == "__main__":
    main()