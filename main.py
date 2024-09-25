import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
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

        time.sleep(5)

        total_elements = int(str(self.driver.find_element(By.CLASS_NAME, "lst-cnt").text).split(" ")[0])
        print(f"total_elements: {total_elements}")
        successes = 0
        fails = 0

        for i in range(total_elements):
            retries = 2
            for attempt in range(retries):
                try:
                    company = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.ID, f"list-item-{i}"))
                    )

                    self.driver.execute_script("arguments[0].scrollIntoView(true);", company)

                    company = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.ID, f"list-item-{i}"))
                    )
                    
                    actions = ActionChains(self.driver)
                    actions.move_to_element(company).click().perform()

                    icn_link = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'icn-link')]/parent::a"))
                    )
                    
                    description = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "field-widget-tinymce"))
                    )

                    self.post_to_xlsx(icn_link.text, description.text)

                    self.driver.back()
                    successes += 1
                    break

                except StaleElementReferenceException:
                    fails += 1
                    continue

                except Exception as e:
                    fails += 1
                    continue

    def post_to_xlsx(self, icn_link, description):
        print(f"icn_link: {icn_link}")
        print(f"Description: {description}")

    def run_parser(self):
        self.get_to_page()
        self.get_info()

        self.driver.quit()

def main():
    Parser().run_parser()
    
if __name__ == "__main__":
    main()