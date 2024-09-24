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
        self.auth = "https://api-3d4a13e1.duosecurity.com/frame/v4/auth/prompt?sid=frameless-21be7b6b-588d-4e25-a190-d6885aa67e6f"
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

    # def parse_info(self):
    #     pass

    def get_info(self):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, """//*[@id="content-view"]/div[3]/div/div/career-fair-content/div[1]/div[2]/div/div/div/div[1]/h1"""))
        )

        dropdown = Select(self.driver.find_element(By.CLASS_NAME, "ng-star-inserted"))
        dropdown.select_by_value('250')

        time.sleep(15)

        company_elements = self.driver.find_elements(By.CLASS_NAME, "list-item list_rows list-item-responsive-actions cursor-pointer")

        for company in company_elements:
            tabindex = company.get_attribute("tabindex")
            print(f"Tabindex: {tabindex}")
            
            company.click()
            time.sleep(1)

            parse_info()

            self.driver.back()

    

    def run_parser(self):
        self.get_to_page()
        self.get_info()

        for i in range(7):
            print(i + 1)
            time.sleep(1)
        self.driver.quit()


def get_data():
    response = requests.get(listings).text
    soup = BeautifulSoup(response, 'html.parser')

    print(soup)

def get_data_selenium():
    service = Service(executable_path="C:/Program Files/chromedriver-win64/chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get(listings)

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "ritUsername"))
    )

    # input_element = driver.find_element(By.ID, "ritUsername")
    # input_element.clear()
    # input_element.send_keys(os.getenv("RIT_USERNAME"))

    # input_element = driver.find_element(By.ID, "ritPassword")
    # input_element.clear()
    # input_element.send_keys(os.getenv("RIT_PASSWORD"))

    # login_button = driver.find_element(By.XPATH, "/html/body/div/div[1]/form/div/span/button")
    # login_button.click()

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "University-Wide Career Fair Fall 2024- September 25, 2024"))
    )

    for i in range(7):
        print(i + 1)
        time.sleep(1)
    driver.quit()
    # thread.join()


def main():
    Parser().run_parser()
    
if __name__ == "__main__":
    main()